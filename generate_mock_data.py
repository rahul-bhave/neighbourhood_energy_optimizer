import sqlite3, random, time

conn = sqlite3.connect("mock_data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    house_id TEXT,
    timestamp INTEGER,
    gen_kw REAL,
    load_kw REAL,
    soc_pct REAL
)
""")

houses = [f"house_{i}" for i in range(1, 6)]
now = int(time.time())
hour_sec = 3600

records = []
for h in houses:
    soc = random.uniform(40, 80)
    for i in range(0, 24):
        ts = now - (23 - i) * hour_sec
        gen = max(0, round(random.uniform(0.5, 5.0) * (1 - abs(12 - i) / 12), 2))
        load = round(random.uniform(1.0, 3.5), 2)
        soc = min(100, max(0, soc + (gen - load) * 2))
        records.append((h, ts, gen, load, soc))

cur.executemany("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?)", records)
conn.commit()
conn.close()
print(f"Inserted {len(records)} rows of mock data into mock_data.db")
