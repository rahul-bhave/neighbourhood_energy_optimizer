# MCP server: simple stdio JSON-lines server
import sys, json, sqlite3, os, traceback
DB = os.path.join(os.path.dirname(__file__), "../data/mock_data.db")
def handle_request(req):
    cmd = req.get('cmd')
    if cmd == 'get_consumer_summary':
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("""
        SELECT consumer_id, AVG(daily_kwh) as avg_kwh, MAX(uses_efficient_equipment) as efficient, MAX(produces_solar) as solar
        FROM consumption
        GROUP BY consumer_id
        """)
        rows = cur.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append({
                'consumer_id': r[0],
                'avg_kwh': round(r[1],2),
                'uses_efficient_equipment': bool(r[2]),
                'produces_solar': bool(r[3])
            })
        return {'ok': True, 'data': result}
    elif cmd == 'get_recent_records':
        n = req.get('n', 100)
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("""SELECT consumer_id, date, daily_kwh, uses_efficient_equipment, produces_solar
                       FROM consumption ORDER BY date DESC LIMIT ?""", (n,))
        rows = cur.fetchall()
        conn.close()
        data = [{'consumer_id':r[0], 'date':r[1], 'daily_kwh':r[2], 'uses_efficient_equipment':bool(r[3]), 'produces_solar':bool(r[4])} for r in rows]
        return {'ok': True, 'data': data}
    else:
        return {'ok': False, 'error': 'unknown_cmd'}

def main():
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line: continue
            try:
                req = json.loads(line)
                resp = handle_request(req)
            except Exception as e:
                resp = {'ok': False, 'error': str(e), 'trace': traceback.format_exc()}
            sys.stdout.write(json.dumps(resp) + '\n')
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
