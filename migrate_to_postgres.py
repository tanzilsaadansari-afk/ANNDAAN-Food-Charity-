import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).parent / "anndaan.db"
SCHEMA_PATH = Path(__file__).parent / "schema_postgres.sql"

def get_postgres_url():
    if len(sys.argv) > 1:
        return sys.argv[1]
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("ERROR: DATABASE_URL is not provided.")
        print("Usage: python migrate_to_postgres.py [POSTGRES_DATABASE_URL]")
        print("Or set DATABASE_URL in your .env file.")
        sys.exit(1)
    return url

def migrate():
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        print("ERROR: psycopg2 is not installed. Run 'pip install psycopg2-binary'")
        sys.exit(1)

    if not DB_PATH.exists():
        print(f"ERROR: SQLite database file not found at {DB_PATH}")
        sys.exit(1)

    pg_url = get_postgres_url()
    print(f"Connecting to SQLite database: {DB_PATH}")
    sqlite_conn = sqlite3.connect(DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()

    print(f"Connecting to PostgreSQL database...")
    try:
        pg_conn = psycopg2.connect(pg_url)
        pg_conn.autocommit = False
        pg_cur = pg_conn.cursor()
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        sys.exit(1)

    print("Creating tables in PostgreSQL if they do not exist...")
    with open(SCHEMA_PATH, "r", encoding="utf-8-sig") as f:
        schema_sql = f.read()
    pg_cur.execute(schema_sql)
    pg_conn.commit()

    # Migrate users
    sqlite_cur.execute("SELECT id, name, phone, email, password_hash, role, verified, created_at FROM users")
    users = sqlite_cur.fetchall()
    print(f"Found {len(users)} users in SQLite database.")

    for u in users:
        verified_bool = bool(u["verified"]) if u["verified"] is not None else False
        pg_cur.execute(
            """
            INSERT INTO users (id, name, phone, email, password_hash, role, verified, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                password_hash = EXCLUDED.password_hash,
                role = EXCLUDED.role,
                verified = EXCLUDED.verified,
                created_at = EXCLUDED.created_at
            """,
            (u["id"], u["name"], u["phone"], u["email"], u["password_hash"], u["role"], verified_bool, u["created_at"])
        )
    pg_conn.commit()
    print(f"Migrated {len(users)} users.")

    # Reset users_id_seq
    pg_cur.execute("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1))")
    pg_conn.commit()

    # Migrate donations
    sqlite_cur.execute("""
        SELECT id, donor_id, food_item, food_type, quantity, pickup_address,
               expiry_time, notes, status, claimed_by_id, created_at, claimed_at,
               expires_at, latitude, longitude
        FROM donations
    """)
    donations = sqlite_cur.fetchall()
    print(f"Found {len(donations)} donations in SQLite database.")

    for d in donations:
        pg_cur.execute(
            """
            INSERT INTO donations (
                id, donor_id, food_item, food_type, quantity, pickup_address,
                expiry_time, notes, status, claimed_by_id, created_at, claimed_at,
                expires_at, latitude, longitude
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                food_item = EXCLUDED.food_item,
                food_type = EXCLUDED.food_type,
                quantity = EXCLUDED.quantity,
                pickup_address = EXCLUDED.pickup_address,
                expiry_time = EXCLUDED.expiry_time,
                notes = EXCLUDED.notes,
                status = EXCLUDED.status,
                claimed_by_id = EXCLUDED.claimed_by_id,
                claimed_at = EXCLUDED.claimed_at,
                expires_at = EXCLUDED.expires_at,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude
            """,
            (
                d["id"], d["donor_id"], d["food_item"], d["food_type"], d["quantity"],
                d["pickup_address"], d["expiry_time"], d["notes"], d["status"],
                d["claimed_by_id"], d["created_at"], d["claimed_at"], d["expires_at"],
                d["latitude"], d["longitude"]
            )
        )
    pg_conn.commit()
    print(f"Migrated {len(donations)} donations.")

    # Reset donations_id_seq
    pg_cur.execute("SELECT setval('donations_id_seq', COALESCE((SELECT MAX(id) FROM donations), 1))")
    pg_conn.commit()

    sqlite_conn.close()
    pg_conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
