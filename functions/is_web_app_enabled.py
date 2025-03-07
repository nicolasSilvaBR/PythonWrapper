import pandas as pd

def IsWebAppEnabled(engine):     
    
    sql_query = f"""  
        Report.SSRS_IsSecurityEnabled      
    """
    try:
        # Read the SQL query into a DataFrame
        df = pd.read_sql_query(sql_query, engine)
        
        # Ensure the DataFrame is not empty
        if not df.empty:
            # Return only the value of ConfigSetting without DataFrame structure
            return df.iloc[0, 0]  # Access the first value directly
    except Exception:
        return '0'