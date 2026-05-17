"""One-time script to add missing columns to existing database tables."""
from sqlalchemy import create_engine, text, inspect

engine = create_engine("postgresql://postgres:root@localhost/HireSphere")

with engine.connect() as conn:
    inspector = inspect(engine)
    
    # Check existing tables and columns
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")
    
    if "users" in tables:
        columns = [c["name"] for c in inspector.get_columns("users")]
        print(f"Users columns: {columns}")
        if "role" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'candidate'"))
            conn.commit()
            print("SUCCESS: Added 'role' column to users table")
        else:
            print("'role' column already exists")
    
    # Also ensure jobs and applications tables exist
    if "jobs" not in tables:
        print("'jobs' table missing - will be created by create_all")
    if "applications" not in tables:
        print("'applications' table missing - will be created by create_all")

    # Check jobs table columns if it exists
    if "jobs" in tables:
        columns = [c["name"] for c in inspector.get_columns("jobs")]
        print(f"Jobs columns: {columns}")
        if "recruiter_id" not in columns:
            conn.execute(text("ALTER TABLE jobs ADD COLUMN recruiter_id INTEGER REFERENCES users(id)"))
            conn.commit()
            print("SUCCESS: Added 'recruiter_id' column to jobs table")

print("Database fix complete!")
