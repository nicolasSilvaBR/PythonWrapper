import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from functions.secrets_config import get_secrets_config

@st.cache_resource
def mydb() -> Engine:
    """
    Creates a connection to the SQL Server database using SQLAlchemy.

    Returns:
        engine: SQLAlchemy engine object for interactions with the database.
    """
         
    db_config = get_secrets_config()

    # Check if all required parameters are present
    required_keys = ["username", "password", "host", "port", "database"]
    missing_keys = [key for key in required_keys if key not in db_config]
    if missing_keys:
        st.error(f"Missing configuration parameters: {', '.join(missing_keys)}")
        return None

    # Use the default ODBC driver
    driver = "ODBC Driver 17 for SQL Server"

    # Build the connection string for SQL Server
    connection_string = (
        f"mssql+pyodbc://{db_config['username']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/{db_config['database']}?driver={driver}"
    )

    # Create the SQLAlchemy engine
    try:
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Error creating the connection engine: {e}")
        return None
