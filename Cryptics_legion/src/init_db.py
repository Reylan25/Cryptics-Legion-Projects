"""
Database initialization script
Creates all necessary tables and initializes admin configuration tables
"""

from core import db

def initialize_database():
    """Initialize all database tables"""
    print("Initializing database...")
    
    # Initialize main tables
    db.connect_db()
    print("✓ Main tables initialized")
    
    # Initialize admin configuration tables
    db.init_admin_config_tables()
    print("✓ Admin configuration tables initialized")
    
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    initialize_database()
