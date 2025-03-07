import streamlit as st
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from functions.secrets_config import get_secrets_config

# Initialize Sessions
if 'pin-number' not in st.session_state:
    st.session_state['pin-number'] = None
if 'pin-IsWebAppEnabled' not in st.session_state:
    st.session_state['pin-IsWebAppEnabled'] = None    
    
# Load database configurations from secrets
db_config = get_secrets_config()
infeed_database_name = db_config["database"]
enecoms_database_name = db_config["enecoms_database"]
database_infeed700DW = db_config["database_infeed700DW"]
pin_number = st.session_state['pin-number']

# Function to fetch and process the SQL query
def get_report_headers_and_reports_names(project, engine,pin_number):
    # Determine the database name based on the project    
    
    if project == 'Infeed700':
        database_name = infeed_database_name
    elif project == 'Enecoms':
        database_name = enecoms_database_name
    elif project == 'Python':
        database_name = database_infeed700DW
    else:
        st.error('Check report_header_name')
        

    # SQL query to retrieve data
    sql_query = f"""
        DECLARE @project varchar(15) = '{project}'
        
        IF @project = 'Infeed700'
        BEGIN
            Exec Report.SSRS_WebMenuItemsByUser '{pin_number}', ''
        END;
        
        IF @project = 'Enecoms'
        BEGIN
            SELECT	
                [MenuItems].[HeaderId]
                ,[HeaderName]
                ,[ReportDisplayName]
                ,[ReportName]
                ,ItemDisplayOrder      
            FROM {enecoms_database_name}.[Report].[MenuItems]
            JOIN {enecoms_database_name}.[Report].[MenuHeader] ON [MenuHeader].HeaderId = [MenuItems].HeaderId
            WHERE [MenuItems].IsActive = 1 AND [MenuHeader].IsActive = 1
            ORDER BY  
                [MenuHeader].WebHeaderDisplayOrder,
                [ItemDisplayOrder],
                [ReportDisplayName]
        END;
        
        IF @project = 'Python'
	    BEGIN
            SELECT	
                [MenuItems].[HeaderId]
                ,[HeaderName]
                ,[ReportDisplayName]
                ,[ReportName]
                ,ReportDisplayOrder      
            FROM {database_infeed700DW}.[Report].[MenuItems]
            JOIN {database_infeed700DW}.[Report].[MenuHeader] ON [MenuHeader].HeaderId = [MenuItems].HeaderId
            WHERE [MenuItems].IsActive = 1 AND [MenuHeader].IsActive = 1
            ORDER BY 			
                [HeaderId],
                ReportDisplayOrder
	    END;    
    """

    try:
        # Execute the SQL query and load the result into a DataFrame
        df = pd.read_sql_query(sql_query, engine)

        # Check if the DataFrame is empty
        if df.empty and st.session_state['pin-IsWebAppEnabled'] == True:
            # Display an error message if no data is found
            st.error(
                f"No data found for the project '{project}' in the database '{database_name}'. "
                "Please make sure the database name is correct and exists in the source."
            )
            return None, None

        # Process the data if the query returns results
        if project == 'Infeed700':
            # Extract and rename headers
            headers_name = df[['HeaderId', 'HeaderDisplayName']].drop_duplicates()
            headers_name = headers_name.rename(columns={
                'HeaderId': 'HeaderId',
                'HeaderDisplayName': 'HeaderName'  # Rename for consistency
            })
            
            # Extract and rename report details
            reports_names = df[['HeaderDisplayName', 'HeaderId', 'ReportDisplayName', 'ReportName']].drop_duplicates()
            reports_names = reports_names.rename(columns={
                'HeaderDisplayName': 'HeaderName',
                'HeaderId': 'HeaderId',
                'ReportDisplayName': 'ReportDisplayName',
                'ReportName': 'ReportName'
            })

        elif project == 'Enecoms':
            # Extract and rename headers
            headers_name = df[['HeaderId', 'HeaderName']].drop_duplicates()
            headers_name = headers_name.rename(columns={
                'HeaderId': 'HeaderId',
                'HeaderName': 'HeaderName'  # No renaming needed here, keeping for clarity
            })

            # Extract and rename report details
            reports_names = df[['HeaderName', 'HeaderId', 'ReportDisplayName', 'ReportName']].drop_duplicates()
            reports_names = reports_names.rename(columns={
                'HeaderName': 'HeaderName',
                'HeaderId': 'HeaderId',
                'ReportDisplayName': 'ReportDisplayName',
                'ReportName': 'ReportName'
            })
        elif project == 'Python':
            # Extract and rename headers
            headers_name = df[['HeaderId', 'HeaderName']].drop_duplicates()
            headers_name = headers_name.rename(columns={
                'HeaderId': 'HeaderId',
                'HeaderName': 'HeaderName'  # No renaming needed here, keeping for clarity
            })

            # Extract and rename report details
            reports_names = df[['HeaderName', 'HeaderId', 'ReportDisplayName', 'ReportName']].drop_duplicates()
            reports_names = reports_names.rename(columns={
                'HeaderName': 'HeaderName',
                'HeaderId': 'HeaderId',
                'ReportDisplayName': 'ReportDisplayName',
                'ReportName': 'ReportName'
            })
        else:
            st.error(f'The project name {project} does not exist!')
            
        return headers_name, reports_names

    except SQLAlchemyError as e:
        # Handle SQL execution errors
        st.error(
            f"An error occurred while querying the database '{database_name}': {str(e)}. "
            "Please make sure the database name is correct and exists in the source."
            "Check [Report].[SSRS_WebMenuItemsByUser]"
        )
        return None, None

    except Exception as e:
        # Handle any other unexpected errors
        st.error(
            f"An unexpected error occurred while processing the project '{project}': {str(e)}. "
            "Please make sure the database name is correct and exists in the source."
            "Check [Report].[SSRS_WebMenuItemsByUser]"
        )
        return None, None
