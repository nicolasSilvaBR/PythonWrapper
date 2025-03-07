import os
import base64
import toml
import streamlit as st
from streamlit_option_menu import option_menu
from functions.footer import display_footer as footer
from functions.report_header_name import get_report_headers_and_reports_names
from functions.sites import IsMultiSiteEnabled
from functions.is_enecoms_enabled import IsEnecomsEnabled
from functions.python_enabled import IsPythonDemoEnabled

if 'pin-number' not in st.session_state:
    st.session_state['pin-number'] = None  
    
# Function to load secrets
def load_secrets():
    """Loads the primary secrets file to determine which additional secrets file to use."""
    try:
        primary_secrets = toml.load(".streamlit/secrets.toml")
        secrets_name = primary_secrets["secrets_config"]["secrets_name"]
        secrets_path = f".streamlit/{secrets_name}.toml"
        return toml.load(secrets_path)
    except Exception as e:
        st.warning(f"Could not load secrets file. Error: {e}")
        return None

# Function to convert image to Base64
def get_image_as_base64(image_path):
    """Converts an image to Base64 for use in HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# Function to generate the sidebar menu
def LeftMenu(engine):
    """Builds the sidebar menu for the Streamlit app."""
    
    secrets = load_secrets() 

    # Default: Disable the link
    server_url = None

    # Try to get server details from secrets
    if secrets:
        try:
            streamlit_server = secrets.get("streamlit_server", {})
            ip_address = streamlit_server.get("ip_address")
            port = streamlit_server.get("port")
            if ip_address and port:
                server_url = f"http://{ip_address}:{port}"
        except KeyError:
            st.warning("The 'streamlit_server' section is missing or incomplete in the secrets file. Logo link is disabled.")

    # Path to the logo image file
    sidebar_logo_image_name = "ICM_300X80_OPT15.png"
    png_file_path = os.path.join("assets/images", sidebar_logo_image_name)

    with st.sidebar:
        # Display the logo
        if os.path.exists(png_file_path):
            logo_base64 = get_image_as_base64(png_file_path)
            if server_url:
                # Clickable logo with link
                st.markdown(
                    f"""
                    <a href="{server_url}" target="_self">
                        <img src="data:image/png;base64,{logo_base64}" style="width:100%;">
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Non-clickable logo
                st.markdown(
                    f"""
                    <img src="data:image/png;base64,{logo_base64}" style="width:100%;">
                    """,
                    unsafe_allow_html=True
                )

        # Default project setup
        if "selected-project" not in st.session_state:
            st.session_state["selected-project"] = "Infeed700"

        def clean_report_session():
            """Clears the selected report session."""
            st.session_state['selected_report'] = False

        # Check if Enecoms is enabled
        EnecomsEnabled = IsEnecomsEnabled(engine)
        PythonEnabled = IsPythonDemoEnabled(engine)
        
        if EnecomsEnabled == '1':
            left, middle = st.columns(2)
            if left.button("📊 Infeed700", key='Infeed700', use_container_width=True, type='secondary', on_click=clean_report_session):
                st.session_state["selected-project"] = "Infeed700"
            if middle.button("⚡Enecoms", key='Enecoms', use_container_width=True, on_click=clean_report_session):
                st.session_state["selected-project"] = "Enecoms"
        if PythonEnabled == '1':
            if left.button("Python", key='IsPythonEnabled', use_container_width=True, type='secondary', on_click=clean_report_session):  
                st.session_state["selected-project"] = "Python"

                 
                   
        project = st.session_state["selected-project"]
        
        IsMultiSiteEnabled(engine)

        if st.session_state["selected-project"] != "":
            try:
                pin_number = st.session_state['pin-number']
                # Fetch headers and reports using the provided function                
                headers_name, reports_names = get_report_headers_and_reports_names(project, engine,pin_number)               
                
                if headers_name is not None and reports_names is not None:
                    selected_header = st.selectbox(
                        label='',
                        options=headers_name['HeaderName'],
                        index=None,
                        placeholder='Choose a category',
                        key='selected_header'
                    )
                    filtered_reports = reports_names[reports_names['HeaderName'] == selected_header]
                    menu_icon = "bar-chart" if st.session_state["selected-project"] == "Infeed700" else "bi-lightning"

                    if not filtered_reports.empty:
                        reports_option = option_menu(
                            menu_title=st.session_state["selected-project"],
                            menu_icon=menu_icon,            
                            icons=["dot"] * len(filtered_reports),
                            default_index=0,
                            options=filtered_reports['ReportDisplayName'].tolist(),
                            key="select_report_options",
                            styles={
                                "icon": {
                                    "font-size": "12px",  
                                    "margin-right": "2px",  
                                    "padding": "2px",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "display": "flex"
                                },
                                "nav-link": {
                                    "font-size": "14px",
                                    "text-align": "left",
                                    "margin-bottom": "1px",
                                    "padding-bottom": "10px",
                                    "--hover-color": "#eee",
                                    "line-height": "15px",
                                    "justify-content": "left",
                                    "text-align": "left",
                                    "align-items": "center",
                                    "display": "flex",
                                    "color": "#4a4a4a",
                                    "transition": "background-color 0.3s ease, color 0.3s ease",  
                                    ":hover": {
                                        "color": "#000",  
                                        "background-color": "#f0f0f0"  
                                    }
                                },
                                "nav-link-selected": {
                                    "background-color": "#475b7c",
                                    "color": "#fff",  
                                    "font-weight": "bold", 
                                    "border-left": "4px solid #007BFF"  
                                },
                                "nav-item": {
                                    "margin": "0px",
                                    "padding": "0px",
                                }
                            }
                        )

                        selected_report_details = filtered_reports[filtered_reports['ReportDisplayName'] == reports_option]
                        if not selected_report_details.empty:
                            st.session_state['selected_report'] = selected_report_details['ReportName'].iloc[0]
                        else:
                            st.session_state['selected_report']

                    else:
                        st.write("💬 No reports available for the selected category.")
                else:
                    st.error("Failed to load report headers or report names. Please check the database name or query. Check the Secrets files parameters.")

            except Exception as e:
                # Handle any errors in fetching headers or reports
                st.error(
                    f"An error occurred while loading the left menu: {e}. "
                    "Please make sure the database connection and queries are correct."
                )
        else:
            st.write('To Create Python Reports Menu items')
            
        st.divider()
        footer()

