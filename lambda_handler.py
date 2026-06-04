from mangum import Mangum
from app.main import app
from app.database import create_tables

try:
    create_tables()
except Exception as e:
    print(f"[WARNING] Could not create tables: {e}")

handler = Mangum(app, lifespan="off")
