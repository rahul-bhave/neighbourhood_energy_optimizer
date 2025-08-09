import subprocess, sys, json, os, threading, queue, time
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
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._responses = queue.Queue()
        self._reader_thread.start()
    def _read_loop(self):
        for line in self.proc.stdout:
            line = line.strip()
            if not line: continue
            try:
                resp = json.loads(line)
            except:
                resp = {'ok': False, 'error': 'invalid_json', 'raw': line}
            self._responses.put(resp)
    def request(self, payload, timeout=5):
        with self._lock:
            self.proc.stdin.write(json.dumps(payload) + '\n')
            self.proc.stdin.flush()
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
