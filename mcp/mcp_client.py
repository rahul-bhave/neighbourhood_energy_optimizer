import subprocess, sys, json, threading, queue, os, time
import logging

class MCPClientError(Exception):
    pass

class MCPClient:
    def __init__(self, server_py=None):
        if server_py is None:
            server_py = os.path.join(os.path.dirname(__file__), 'mcp_server.py')
        self.proc = subprocess.Popen([sys.executable, server_py],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, bufsize=1)
        self._lock = threading.Lock()
        self._responses = queue.Queue()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()
        self._stderr_reader = threading.Thread(target=self._stderr_loop, daemon=True)
        self._stderr_reader.start()

    def _read_loop(self):
        for line in self.proc.stdout:
            line = line.strip()
            if not line: continue
            try:
                resp = json.loads(line)
            except:
                resp = {'ok': False, 'error': 'invalid_json', 'raw': line}
            self._responses.put(resp)

    def _stderr_loop(self):
        for line in self.proc.stderr:
            line = line.rstrip('\n')
            if line:
                logging.error("[MCP server stderr] %s", line)

    def request(self, payload, timeout=5):
        with self._lock:
            try:
                self.proc.stdin.write(json.dumps(payload) + '\n')
                self.proc.stdin.flush()
            except Exception as e:
                raise MCPClientError('failed write to server: ' + str(e))
            try:
                resp = self._responses.get(timeout=timeout)
            except queue.Empty:
                raise MCPClientError('timeout waiting for server response')
            return resp

    def close(self):
        try:
            self.proc.terminate()
        except:
            pass

if __name__ == '__main__':
    c = MCPClient()
    r = c.request({'cmd':'get_consumer_summary'})
    print('got', len(r.get('data',[])))
    c.close()
