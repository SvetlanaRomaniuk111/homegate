import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def save_listing(data):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    query = """INSERT INTO listings (listing_id, title, price, rooms, address, description)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (listing_id) DO NOTHING;"""
    
    cur.execute(query, (data["listing_id"], data["title"], data["price"], data["rooms"], data["address"], data["description"]))
    
    conn.commit()
    cur.close()
    conn.close()