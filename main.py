import functions.config as config
import streamlit as st
from left_menu.left_menu import LeftMenu
from functions.embedded_SSRS import embed_ssrs_report
from functions.embedded_Python import embed_python_report
import pandas as pd
import logging
from functions.database_connection import mydb
import streamlit.components.v1 as components
from pathlib import Path
from functions.utilities import load_local_css, get_base64_image
from functions.is_web_app_enabled import IsWebAppEnabled

# From function folder import config > set_page_config()
config.set_page_config()

# Load custom CSS
load_local_css("assets/css/style.css")

# Initialize Sessions
if 'pin-number' not in st.session_state:
    st.session_state['pin-number'] = None
if 'pin-IsWebAppEnabled' not in st.session_state:
    st.session_state['pin-IsWebAppEnabled'] = None  
if 'selected-project' not in st.session_state:        
    st.session_state["selected-project"] = None 
if 'is-logged' not in st.session_state:        
    st.session_state["is-logged"] = False       

def main():
    # Initial settings and database connection log
    engine = mydb()
    logging.info(f"Database engine: {engine}")
    
    # Check if PIn is Required    
    is_pin_required = IsWebAppEnabled(engine)
    project = st.session_state["selected-project"]
    is_logged = st.session_state['is-logged']
    
    # -- 1 // Pin Check....prompt for pin
    # -- 2 // Terminal black list...so not prompting for pin or terminal but security is enabled.
    # -- 0 // 0 = No Security, 1 = Pin Check and 2 = Terminal black list

    if is_pin_required == '1' and project == 'Infeed700':
        text_input_container = st.empty()       
        pin_number = text_input_container.text_input(label="🔑 Please enter the PIN to select a report from the left menu",key='text-input-pin-number')   
        st.session_state['pin-number'] = pin_number    
        st.session_state['IsWebAppEnabled'] = True
        st.session_state['is-logged'] = True
        
        if pin_number != "":
            text_input_container.empty()  
        LeftMenu(engine)    

    else:
        LeftMenu(engine)    
    
    # Initialize session variables
    if 'selected_report' not in st.session_state:
        st.session_state['selected_report'] = None
    if 'show_report' not in st.session_state:
        st.session_state['show_report'] = False  # Controls report display
    if 'show_content' not in st.session_state:
        st.session_state['show_content'] = False  # Controls specific content display (dashboard or report)

    # Default dates
    minDate = st.session_state.get('minDate')
    maxDate = st.session_state.get('maxDate')  
    
    # Function to display the SSRS report
    def display_ssrs_report():
        """Display the SSRS report."""
        try:
            #with st.spinner('Running Report...'):
                reportRDLname = st.session_state['selected_report']
                embed_ssrs_report(reportRDLname, minDate, maxDate)                
        except Exception as e:
            if st.session_state['selected_report']:
                logging.error(f"Error loading report: {e}")
                st.error("An error occurred while loading the report. Verify that the SSRS server is online.") 
            elif not st.session_state['selected_report']:
                st.write("💬 Please select a Category and Report from the left menu.")

    # Function to display the dashboard
    def display_python_reports():
        """Display dashboard content."""
        
        # st.session_state['selected-project']
        # st.write('Header:',st.session_state['selected_header'])
        # st.write('Report:',st.session_state['selected_report'])
        
        embed_python_report(st.session_state['selected_report'],minDate, maxDate)
        #intake_page(mindate=minDate, maxdate=maxDate)

    # Display main content based on session state
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # Update `show_content` and `show_report` based on the selected report
    if st.session_state['selected_report'] is not None:
        st.session_state['show_report'] = True
        st.session_state['show_content'] = True # Show SSRS Report

    # Display the home (index.html) only if `show_content` is False
    if not st.session_state['show_content']:
        # Load image in Base64
        image_path = Path("assets/images/home_silo.png")
        image_url = ""
        if image_path.exists():
            image_base64 = get_base64_image(image_path)
            image_url = f"data:image/png;base64,{image_base64}"
        else:
            st.error("Image not found.")

        # Load and display HTML for the home page
        with open("index.html", "r") as file:
            index_html = file.read()
        
        index_html = index_html.replace("assets/images/home_silo.png", image_url)
        components.html(index_html, height=900, scrolling=True) 
    
    # If  report header was selected, display specific content
    else:  
        # Show the SSRS report if a report header was selected
        if st.session_state['show_report']:
            #st.write('Show the SSRS report if a report header was selected')
            if st.session_state['selected-project'] == 'Infeed700' or st.session_state['selected-project'] == 'Enecoms':
                display_ssrs_report()
            elif st.session_state['selected-project'] == 'Python':
                display_python_reports()

    # Close main div
    st.markdown('</div>', unsafe_allow_html=True)    
    
# Entry point of the application
if __name__ == '__main__':
    main()

