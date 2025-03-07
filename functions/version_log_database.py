import streamlit as st
import pandas as pd
from secrets_config import get_secrets_config

db_config = get_secrets_config()
infeed_database_name = db_config["database"]

# Function to fetch and process the SQL query
def get_database_version_log_tfs_update(engine):
    sql_query = f"""  
        SELECT top 1 VersionId,VersionInfo,VersionDesc,AppliedBy,AppliedDT 
        FROM {infeed_database_name}.[dbo].[VersionLog] order by VersionId desc  
    """
    # Read the SQL query into a DataFrame
    df = pd.read_sql_query(sql_query, engine)
    # Ensure the DataFrame is not empty
    try:
        # Read the SQL query into a DataFrame
        df = pd.read_sql_query(sql_query, engine)
        
        # Ensure the DataFrame is not empty
        if not df.empty:
            # Return only the value of ConfigSetting without DataFrame structure
            st.subheader("Last TFS Update")
            st.write(df)  # Access the first value directly
            
    except Exception:
        return '0'