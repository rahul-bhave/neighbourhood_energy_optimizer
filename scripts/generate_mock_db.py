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

    # Create randomized consumer IDs to make data look more realistic
    # Generate 50 random 6-digit consumer IDs
    consumer_ids = []
    for i in range(50):
        # Generate random 6-digit number
        random_id = random.randint(100000, 999999)
        consumer_id = f"consumer_{random_id}"
        consumer_ids.append(consumer_id)
    
    base_date = datetime.utcnow().date() - timedelta(days=9)
    records = []
    
    # Scenario 1: 10% discount - usage < 4KW, efficient equipment, solar output (4-5 records)
    for i in range(5):
        consumer = consumer_ids[i]
        efficient = 1
        solar = 1
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            # Low usage: 2.0-3.8 kWh/day
            daily_kwh = round(random.uniform(2.0, 3.8), 2)
            records.append((consumer, date, daily_kwh, efficient, solar))
    
    # Scenario 2: 5% discount - usage < 4KW, efficient equipment, NO solar output (4-5 records)
    for i in range(5, 10):
        consumer = consumer_ids[i]
        efficient = 1
        solar = 0
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            # Low usage: 2.5-3.9 kWh/day
            daily_kwh = round(random.uniform(2.5, 3.9), 2)
            records.append((consumer, date, daily_kwh, efficient, solar))
    
    # Scenario 3: 5% discount - usage < 4KW, NO efficient equipment, solar output (4-5 records)
    for i in range(10, 15):
        consumer = consumer_ids[i]
        efficient = 0
        solar = 1
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            # Low usage: 2.0-3.8 kWh/day
            daily_kwh = round(random.uniform(2.0, 3.8), 2)
            records.append((consumer, date, daily_kwh, efficient, solar))
    
    # Scenario 4: No discount - usage < 4KW, NO efficient equipment, NO solar output (4-5 records)
    for i in range(15, 20):
        consumer = consumer_ids[i]
        efficient = 0
        solar = 0
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            # Low usage: 2.5-3.9 kWh/day
            daily_kwh = round(random.uniform(2.5, 3.9), 2)
            records.append((consumer, date, daily_kwh, efficient, solar))
    
    # Scenario 5: No discount - usage >= 4KW, various combinations (remaining 30 records)
    for i in range(20, 50):
        consumer = consumer_ids[i]
        efficient = random.choice([0, 1])
        solar = random.choice([0, 1])
        for d in range(10):
            date = (base_date + timedelta(days=d)).isoformat()
            # Higher usage: 4.0-12.0 kWh/day
            daily_kwh = round(random.uniform(4.0, 12.0), 2)
            records.append((consumer, date, daily_kwh, efficient, solar))

    cur.executemany("INSERT INTO consumption VALUES (?, ?, ?, ?, ?)", records)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
