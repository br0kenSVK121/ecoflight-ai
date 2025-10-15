"""
Quick test to verify your installation is working
Run this with: python test_setup.py
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing package imports...\n")
    
    packages = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'sqlalchemy': 'Database ORM',
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'geopy': 'Geographic calculations',
        'sklearn': 'Machine learning',
        'networkx': 'Graph algorithms',
        'pydantic': 'Data validation',
        'requests': 'HTTP requests'
    }
    
    failed = []
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - MISSING!")
            failed.append(package)
    
    print("\n" + "="*60)
    
    if failed:
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print("\nRun this to install them:")
        print("pip install -r requirements-lite.txt")
        return False
    else:
        print("\n🎉 All packages installed successfully!")
        return True

def test_database_config():
    """Test database configuration"""
    print("\n📁 Testing database configuration...\n")
    
    try:
        from config import settings
        print(f"✅ Database URL: {settings.DATABASE_URL}")
        print(f"✅ Using SQLite: {settings.USE_SQLITE}")
        
        if settings.USE_SQLITE:
            print(f"✅ Database will be created at: {settings.SQLITE_DB_PATH}")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_sqlalchemy():
    """Test SQLAlchemy database connection"""
    print("\n🗄️  Testing database connection...\n")
    
    try:
        from sqlalchemy import create_engine
        from config import settings
        
        engine = create_engine(settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            print("✅ Database connection successful!")
            print(f"✅ Using: {engine.url.drivername}")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    print("="*60)
    print("🚀 EcoFlight AI - Setup Verification")
    print("="*60 + "\n")
    
    print(f"Python version: {sys.version}\n")
    
    # Run all tests
    tests = [
        test_imports(),
        test_database_config(),
        test_sqlalchemy()
    ]
    
    print("\n" + "="*60)
    
    if all(tests):
        print("\n✨ SETUP COMPLETE! You're ready to proceed.")
        print("\n📊 Next step: Run the data collector")
        print("   python utils/data_collector.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    main()