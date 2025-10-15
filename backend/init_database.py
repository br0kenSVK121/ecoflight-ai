"""
Initialize the database and create all tables
Run this with: python init_database.py
"""

from sqlalchemy import create_engine
from models.database.schema import Base
from config import settings
import os

def init_db():
    """Create database and all tables"""
    print("="*60)
    print("🗄️  EcoFlight AI - Database Initialization")
    print("="*60)
    
    # Create database directory if using SQLite
    if settings.USE_SQLITE:
        db_dir = settings.SQLITE_DB_PATH.parent
        db_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 Database location: {settings.SQLITE_DB_PATH}")
    
    # Create engine
    print(f"\n🔧 Creating database engine...")
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Create all tables
    print(f"\n📊 Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print("\n" + "="*60)
    print("✅ Database initialized successfully!")
    print("="*60)
    
    # List created tables
    print("\n📋 Created tables:")
    for table in Base.metadata.sorted_tables:
        print(f"   ✓ {table.name}")
    
    print("\n🎯 Next step: Load airport and route data")
    print("   Run: python utils/data_collector.py")
    print("="*60)

if __name__ == "__main__":
    init_db()