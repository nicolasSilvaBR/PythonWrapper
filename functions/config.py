import streamlit as st


def set_page_config():
    """Set page configuration for Streamlit app."""
    
    if "selected-project" not in st.session_state:
        st.session_state["selected-project"] = 'Infeed700'
        
    project_name = st.session_state["selected-project"]
    site_name = st.secrets['site_info']['site_name']
   
    
    st.set_page_config(
        page_title=f"{project_name} Reports - {site_name}",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://icmcsl.com/',
            'Report a bug': "https://icmcsl.com/",
            'About': "Infeed700. Version 1.0 *BETA* ICM CSL"            
        }     

    )
