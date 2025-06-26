from app import get_db

with get_db() as db:
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tablas en la base de datos:")
    for table in tables:
        print(table['name'])