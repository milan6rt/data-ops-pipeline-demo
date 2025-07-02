import pyodbc
import sys

# Connection parameters
server = 'sqlserver-dataops-demo-milan.database.windows.net'
database = 'db-employees-demo'
username = 'sqladmin'
password = 'DataOps2025!'

# Connection string
connection_string = f"""
DRIVER={{ODBC Driver 18 for SQL Server}};
SERVER={server};
DATABASE={database};
UID={username};
PWD={password};
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
"""

try:
    print("🔗 Testing connection...")
    conn = pyodbc.connect(connection_string)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("✅ Connected successfully!")
    
    # Test simple query
    cursor.execute("SELECT GETDATE() as CurrentTime")
    result = cursor.fetchone()
    print(f"Current time: {result[0]}")
    
    # Check current database
    cursor.execute("SELECT DB_NAME() as CurrentDatabase")
    result = cursor.fetchone()
    print(f"Current database: {result[0]}")
    
    # List existing tables
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = cursor.fetchall()
    print(f"Existing tables: {[table[0] for table in tables]}")
    
    # Try to create a simple test table
    print("\n🧪 Testing table creation...")
    test_sql = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'test_table')
    BEGIN
        CREATE TABLE test_table (
            id INT IDENTITY(1,1) PRIMARY KEY,
            test_name NVARCHAR(50)
        );
        PRINT 'Test table created successfully!';
    END
    """
    
    cursor.execute(test_sql)
    print("✅ Test table creation attempted")
    
    # Check if test table was created
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'test_table'")
    exists = cursor.fetchone()[0]
    
    if exists > 0:
        print("✅ Test table creation successful!")
        # Clean up test table
        cursor.execute("DROP TABLE test_table")
        print("🧹 Test table cleaned up")
    else:
        print("❌ Test table creation failed")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()