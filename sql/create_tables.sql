-- Employee table creation script for data ops pipeline demo
-- This script will be executed automatically when changes are pushed to GitHub
#This is just a comment

USE [your-database-name];  -- We'll update this later with actual database name
GO

-- Create employees table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'employees' AND type = 'U')
BEGIN
    CREATE TABLE employees (
        id INT IDENTITY(1,1) PRIMARY KEY,
        first_name NVARCHAR(50) NOT NULL,
        last_name NVARCHAR(50) NOT NULL,
        email NVARCHAR(100) UNIQUE NOT NULL,
        department NVARCHAR(50),
        hire_date DATE DEFAULT GETDATE(),
        salary DECIMAL(10,2),
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
    
    PRINT 'SUCCESS: employees table created successfully!';
END
ELSE
BEGIN
    PRINT 'INFO: employees table already exists - no changes needed.';
END
GO

-- Insert sample data (only if table is empty)
IF NOT EXISTS (SELECT * FROM employees)
BEGIN
    INSERT INTO employees (first_name, last_name, email, department, salary)
    VALUES 
        ('John', 'Doe', 'john.doe@company.com', 'Data Engineering', 75000.00),
        ('Jane', 'Smith', 'jane.smith@company.com', 'Data Analytics', 68000.00),
        ('Mike', 'Johnson', 'mike.johnson@company.com', 'Data Science', 82000.00);
    
    PRINT 'SUCCESS: Sample employee data inserted!';
END
ELSE
BEGIN
    PRINT 'INFO: employees table already contains data - skipping insert.';
END
GO

-- Show final results
SELECT COUNT(*) as TotalEmployees FROM employees;
SELECT TOP 5 * FROM employees ORDER BY created_at DESC;
