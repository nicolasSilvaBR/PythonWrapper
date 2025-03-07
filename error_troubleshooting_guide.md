# Application Error Troubleshooting Guide

## Table of Contents
1. [Error 28000: SQL Server - Login Failed for User](#error-28000-sql-server---login-failed-for-user)
2. [Connection Error: Check the Connection Details on Secrets File](#connection-error-check-the-connection-details-on-secrets-file)

---

## Error 28000: SQL Server - Login Failed for User

### Cause
- Incorrect username or password.
- The user account is disabled or locked on the SQL Server.
- SQL Server is configured for Windows Authentication mode only.

### Solution
1. **Check Credentials**:
   - Verify the username (`UID`) and password (`PWD`) in the app configuration.
   - Test them in SQL Server Management Studio (SSMS).

2. **Enable SQL Authentication**:
   - In SSMS, go to **Server Properties > Security**.
   - Enable **SQL Server and Windows Authentication mode**.

3. **Check User Status**:
   - Run this query in SSMS:
     ```sql
     SELECT name, is_disabled FROM sys.sql_logins WHERE name = 'SW';
     ```
   - If disabled, enable the user:
     ```sql
     ALTER LOGIN SW ENABLE;
     ```

4. **Test Connection**:
   - Use a Python script to validate the connection:
     ```python
     import pyodbc
     conn_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_address;DATABASE=db_name;UID=SW;PWD=password"
     pyodbc.connect(conn_string)
     ```

---

## Connection Error: Check the Connection Details on Secrets File

### Cause
- This error occurs due to incorrect database or SSRS configuration in the `secrets.toml` file.

### Solution
1. **Locate the `secrets.toml` File**:
   - Go to the root directory of the application **Infeed700**.
   - Navigate to the `.streamlit` folder.

2. **Check the Configuration**:
   - Open the `secrets.toml` file and verify the details under `[mydb]`. Ensure the following fields are correct:
     ```toml
     [mydb]
     dialect = "mssql"
     driver = "ODBC Driver 17 for SQL Server"
     username = "sa"
     password = "1984Icm000"
     host = "127.0.0.0"
     port = "1433"
     database = "Infeed700"
     enecoms_database = "Enecoms"
     instance = "MSSQLSERVER"
     ```

3. **Check for SSRS Configuration**:
   - Verify the `[ssrs_config]` section:
     ```toml
     [ssrs_config]
     ipAddress = "127.0.0.0"
     port = "80"
     database = "Infeed700"
     database-enecoms = "Enecoms"
     ReportServerName = "Reportsmanager"
     username = "DDOMAIN\\Reports"
     password = "Reporting123"
     ```

4. **Ensure Sensitive Data Is Correct**:
   - Double-check credentials for the database and SSRS. Contact the project team if you don’t have the correct credentials.

---

## Notes
- If the error persists, verify network connectivity to the database server (`host` in `secrets.toml`) and ensure the server is accessible.
- For more details on configuration files, refer to the `README.md` or consult the project team.

---
