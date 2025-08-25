import os
import sys
import random
from sqlalchemy import create_engine, text, Table, Column, Integer, String, Date, Time, Boolean, MetaData
from dotenv import load_dotenv
from datetime import date, time, timedelta

# Add project root to sys.path to allow importing from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.config import JOB_ROLE_MAPPING

# --- Configuration ---
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set.")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the table structure to match db_Tech.sql
schedule_table = Table('Schedule', metadata,
    Column('ScheduleID', Integer, primary_key=True, autoincrement=True),
    Column('date', Date, nullable=False),
    Column('time', Time, nullable=False),
    Column('position', String(20), nullable=False),
    Column('available', Boolean, nullable=False)
)

# Get the SQL position names directly from our config file
POSITIONS = [role["sql_position_name"] for role in JOB_ROLE_MAPPING.values()]

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def seed_database():
    try:
        with engine.connect() as connection:
            with connection.begin() as transaction:
                print("Dropping old 'Schedule' table if it exists...")
                connection.execute(text("DROP TABLE IF EXISTS \"Schedule\" CASCADE;"))

                print("Creating new 'Schedule' table...")
                metadata.create_all(connection, tables=[schedule_table])

                print("Generating and inserting slots for all of 2025...")
                
                slots_to_add = []
                start_date = date(2025, 1, 1)
                end_date = date(2025, 12, 31)
                
                for single_date in daterange(start_date, end_date):
                    if single_date.weekday() in [0, 5]: continue
                    
                    for hour in range(9, 18):
                        for pos in POSITIONS:
                            is_available = random.random() >= 0.5
                            slots_to_add.append({
                                'date': single_date,
                                'time': time(hour, 0, 0),
                                'position': pos,
                                'available': is_available
                            })
                
                if slots_to_add:
                    connection.execute(schedule_table.insert(), slots_to_add)
                
                print(f"Successfully inserted {len(slots_to_add)} sample time slots for 2025.")
                transaction.commit()
    except Exception as e:
        print(f"An error occurred during database seeding: {e}")

if __name__ == "__main__":
    print("Starting PostgreSQL database seeding process...")
    seed_database()
    print("Seeding process finished.")
