import pandas as pd
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

def IsMultiSiteEnabled(engine):
    """
    Checks if multi-site functionality is enabled and updates the session state accordingly.
    """
    try:
        # Execute the stored procedure to check multi-site status
        storedProcedure = "EXEC [Report].[SSRS_IsMultiSiteEnabled]"
        is_multi_site_enabled_df = pd.read_sql(storedProcedure, engine)

        # Ensure the query returned a result
        if is_multi_site_enabled_df.empty:
            st.error("No data returned from the stored procedure [SSRS_IsMultiSiteEnabled].")
            st.session_state['is_multi_site_enabled'] = False
            st.session_state['selected_site_id'] = '0'
            return

        # Access the first returned value directly using 'iat' (first row, first column)
        is_multi_site_enabled = is_multi_site_enabled_df.iat[0, 0]

        # Update session state for multi-site status
        if 'is_multi_site_enabled' not in st.session_state:
            st.session_state['is_multi_site_enabled'] = is_multi_site_enabled
        if 'site_id_list' not in st.session_state:
            st.session_state['site_id_list'] = '0'

        # If multi-site is enabled, fetch and display site options
        if is_multi_site_enabled == '1':
            storedProcedure = "EXEC [Report].[SSRS_ListSites]"
            list_sites_df = pd.read_sql(storedProcedure, engine)

            # Ensure the query returned results
            if list_sites_df.empty:
                st.error("No sites returned from the stored procedure [SSRS_ListSites].")
                st.session_state['selected_site_id'] = '0'
                return

            # Display site options for selection
            site_desc = st.selectbox("Site", list_sites_df['SiteDesc'])

            # Find the SiteId corresponding to the selected site description
            selected_site_id = list_sites_df[list_sites_df['SiteDesc'] == site_desc]['SiteId'].values[0]

            # Update session state with the selected site ID
            st.session_state['selected_site_id'] = selected_site_id
        else:
            # If multi-site is not enabled, set defaults
            st.session_state['is_multi_site_enabled'] = False
            st.session_state['selected_site_id'] = '0'

    except SQLAlchemyError as e:
        # Handle database-related errors
        st.error(f"A database error occurred: {e}. Please check your database connection and stored procedures.")
        st.session_state['is_multi_site_enabled'] = False
        st.session_state['selected_site_id'] = '0'

    except Exception as e:
        # Handle any other unexpected errors
        st.error(f"An unexpected error occurred: {e}. Please contact support.")
        st.session_state['is_multi_site_enabled'] = False
        st.session_state['selected_site_id'] = '0'
