import streamlit as st
import requests
from requests_ntlm import HttpNtlmAuth
from functions.get_datetime_input import get_datetime_input
from functions.report_an_issue import report_an_issue_button
import toml
import os

def embed_ssrs_report(reportRDLname, minDate, maxDate):
    """
    Embeds an SSRS report into the Streamlit app.

    Args:
        reportRDLname (str): Name of the report to display.
        minDate (str): Start date.
        maxDate (str): End date.
    """
    # Section for selecting dates using a date picker
    with st.expander(label=f"📶 {st.session_state['select_report_options']} Report Parameters ", expanded=False):  
        # Capture date and time inputs
        minDate, maxDate, StartHour, EndHour, StartMinute, EndMinute = get_datetime_input()

    # Load configuration file name from Streamlit secrets
    secrets_config = st.secrets.get("secrets_config", {"secrets_name": "secrets.toml"})
    secrets_name = secrets_config.get("secrets_name", "secrets.toml")

    # Ensure the configuration file is in the correct directory and ends with `.toml`
    if not secrets_name.endswith(".toml"):
        secrets_name = f".streamlit/{secrets_name}.toml"
    else:
        secrets_name = f".streamlit/{secrets_name}"

    # Get the absolute path of the configuration file and check if it exists
    absolute_path = os.path.abspath(secrets_name)
    if not os.path.isfile(absolute_path):
        # Display an error message if the configuration file is missing
        st.error(f"The configuration file '{absolute_path}' was not found. Please check the path and file name.")
        return  # Stop execution

    # Attempt to load the SSRS configuration from the TOML file
    try:
        ssrs_config = toml.load(absolute_path)["ssrs_config"]
    except KeyError:
        # Handle missing SSRS configuration in the file
        st.error("The 'ssrs_config' section was not found in the configuration file.")
        return
    except Exception as e:
        # Handle any other errors while loading the configuration
        st.error(f"Error loading the configuration file: {e}")
        return

    # Set a default project if none is selected
    if 'selected-project' not in st.session_state:
        st.session_state['selected-project'] = 'Infeed700'
    
    # Select the database configuration based on the project name
    project = st.session_state['selected-project']
    if project == 'Infeed700':
        database_session = ssrs_config['database']
    elif project == 'Enecoms':
        database_session = ssrs_config.get('database-enecoms')
    else:
        # Display an error message for invalid project names
        st.error("Invalid project name. Use 'Infeed700' or 'Enecoms'. Ensure database names are specified in secrets.")
        return

    # Validate that all required SSRS keys are present
    required_keys = ["ipAddress", "port", "ReportServerName", "username", "password"]
    if not all(key in ssrs_config for key in required_keys):
        # Display an error if keys are missing
        st.error("Missing SSRS configuration keys. Please check your secrets.toml.")
        return

    # Retrieve SSRS connection details
    ipAddress = ssrs_config["ipAddress"]
    port = ssrs_config["port"]
    database = database_session
    ReportServerName = ssrs_config['ReportServerName']
    username = ssrs_config['username']
    password = ssrs_config['password']

    # Format time parameters as strings
    StartHour, EndHour = str(StartHour), str(EndHour)
    StartMinute, EndMinute = str(StartMinute), str(EndMinute)
    site_id = str(st.session_state.get('selected_site_id', ''))

    # Construct the SSRS report URL based on the project
    if project == 'Infeed700':        
        # Create URL for the 'Infeed700' project with optional SiteId
        ssrs_url = ( 
            f"http://{ipAddress}:{port}/{ReportServerName}/Pages/ReportViewer.aspx?%2f{database}%2f{reportRDLname}&rs:Command=Render"
            f"&MinDate={minDate}&MaxDate={maxDate}&StartHour={StartHour}&EndHour={EndHour}"
            f"&StartMinute={StartMinute}&EndMinute={EndMinute}"
        )
        
        # Add the SiteId parameter if multi-site is enabled
        if st.session_state.get('is_multi_site_enabled'):
            ssrs_url += f"&SiteId={site_id}"
            
    elif project == 'Enecoms':
        # Create URL for the 'Enecoms' project without time or SiteId parameters
        selected_report = st.session_state.get('selected_report')
        time_interval = st.session_state.get('selected_timeframe_index')
        
        if selected_report:
            ssrs_url = (
                f"http://{ipAddress}:{port}/{ReportServerName}/Pages/ReportViewer.aspx?%2f{database}%2f{reportRDLname}&rs:Command=Render"
                f"&MinDate={minDate}&MaxDate={maxDate}&Interval={time_interval}"                
            )
        else:
            # Prompt user to select a report if none is selected
            st.write("💬 Please select a Category and Report from the left menu.")
            return    

    # Display the date range
    st.markdown(
        f"""
        <p style="font-size:12px; color:gray;">
            Date From: {minDate.strftime('%d/%m/%Y')} To: {maxDate.strftime('%d/%m/%Y')}
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Function to render the iframe for the SSRS report
    def render_iframe(url):
        report_url = f"{url}&rs:Embed=true&rc:Parameters=Collapsed"            
        iframe_code = f"""
        <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
                src="{report_url}" frameborder="0" allowfullscreen></iframe>
        """
        # Display the report within the app
        st.components.v1.html(iframe_code, height=820, scrolling=False)
        st.markdown(
            f""" <a href="{ssrs_url}" target="_blank">Open SSRS Report</a> 
            """, unsafe_allow_html=True
        )        
        
        # Create a button to report an issue with additional details
        report_an_issue_button(minDate, StartHour, StartMinute, maxDate, EndHour, EndMinute)

    # Attempt to access the SSRS report
    try:
        # Send an HTTP GET request to the SSRS server
        response = requests.get(ssrs_url, auth=HttpNtlmAuth(username, password), timeout=100)

        # Render the iframe if the response is successful
        if response.status_code == 200:
            render_iframe(ssrs_url)
        else:
            # Handle non-200 status codes
            if st.session_state.get('selected_header'):
                error_msg = (
                    f"Error accessing the report: {response.status_code}. "
                    f"Check the report name or parameters for {reportRDLname}.rdl "
                    f"Check the Secrets File > Connection details for the SSRS server. "
                    f"Check the ReportServerName, username, password"
                )
                st.error(error_msg)
                st.session_state['error_msg'] = error_msg
                
                # Provide a button to report the issue
                report_an_issue_button(minDate, StartHour, StartMinute, maxDate, EndHour, EndMinute)
                url_for_debug = (f"http://{ipAddress}:{port}/{ReportServerName}/Pages/ReportViewer.aspx?%2f{database}%2f{reportRDLname}&rs:Command=Render"
                )
                st.markdown(f""" <a href="{url_for_debug}" target="_blank">Open SSRS Report</a> 
                    """, unsafe_allow_html=True
                )  
            else:
                # Prompt user to select a category or report
                st.write("💬 Please select a Category and Report from the left menu.")                    

    except requests.exceptions.ConnectTimeout:
        # Handle timeout errors
        st.error("Connection error: Timeout while trying to access the server.")
        st.error("Connection error: Check the Connection details on Secrets file.")
        
    except requests.exceptions.RequestException as e:
        # Handle other HTTP request errors
        st.error(f"Error accessing the report: {e}. Check your network connection and try again.")
