import sqlite3, random, os
from datetime import datetime, timedelta

DB = os.path.join(os.path.dirname(__file__), "../data/mock_data.db")

def create_db():
    # Ensure a fresh DB on each run by removing any existing file
    if os.path.exists(DB):
        os.remove(DB)
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS consumption (
        consumer_id TEXT,
        date TEXT,
        daily_kwh REAL,
        uses_efficient_equipment INTEGER,
        produces_solar INTEGER
    )
    """)
    conn.commit()

    consumers = [f"consumer_{i:03d}" for i in range(1,101)]
    base_date = datetime.utcnow().date() - timedelta(days=9)
    records = []
    for c in consumers:
        efficient = 1 if random.random() < 0.4 else 0
        solar = 1 if random.random() < 0.3 else 0
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            base = random.uniform(2.0, 12.0)
            if efficient:
                base *= random.uniform(0.6, 0.9)
            if solar:
                base -= random.uniform(0.0, 2.5)
            daily_kwh = max(0.2, round(base, 2))
            records.append((c, date, daily_kwh, efficient, solar))

    cur.executemany("INSERT INTO consumption VALUES (?, ?, ?, ?, ?)", records)
    conn.commit()
    conn.close()
    print(f"Inserted {len(records)} records into {DB}")

if __name__ == '__main__':
    create_db()
