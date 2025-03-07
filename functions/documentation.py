import sys
import os
import streamlit as st
from streamlit_option_menu import option_menu

# Add the parent directory of the current script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules from the 'functions' directory
from functions.database_connection import mydb
from functions.road_map import road_map
from functions.version_log_database import get_database_version_log_tfs_update

st.set_page_config(layout="wide")
engine = mydb()
def run_documentation():
    # Read the content of the README.md file
    with open('README.md', 'r', encoding='utf-8') as file:
        readme_text = file.read()

    # Read the content of the .streamlit/secrets.toml file
    with open('.streamlit/secrets.toml', 'r', encoding='utf-8') as file:
        secrets_toml = file.read()

    # Read the content of the requirements.txt file
    with open('requirements.txt', 'r', encoding='utf-8') as file:
        requirements_txt = file.read()

    # Read the content of the database_connection.py file
    with open('functions/database_connection.py', 'r', encoding='utf-8') as file:
        database_connection = file.read()
        
    # Read the content of the main.py file
    with open('main.py', 'r', encoding='utf-8') as file:
        main_py_code = file.read()

    # Read the content of the left_menu/left_menu.py file
    with open('left_menu/left_menu.py', 'r', encoding='utf-8') as file:
        left_menu_code = file.read()

    # Read the content of the setup.bat file
    with open('setup.bat', 'r', encoding='utf-8') as file:
        setup_bat_code = file.read()

    # Read the contents of config.toml into the streamlit_config variable
    with open('.streamlit/config.toml', 'r', encoding='utf-8') as file:
        streamlit_config = file.read()

    # Read the content of the embeddedSSRS.py file
    with open('functions/embedded_SSRS.py', 'r', encoding='utf-8') as file:
        embeddedSSRS = file.read()

    # Read the content of the embeddedSSRS.py file
    with open('assets/css/style.css', 'r', encoding='utf-8') as file:
        style_css = file.read()
    
    # Read the content of the Application Error Troubleshooting Guide file
    with open('error_troubleshooting_guide.md', 'r', encoding='utf-8') as file:
        troubleshooting_guide = file.read()

    # Textos e códigos para as seções
    Overview = '''\
    The Infeed700 application is a sophisticated interactive platform developed by **ICM Computer Systems ltd** utilizing **Streamlit**. This project aims to transition from the existing SSRS reporting system to a new solution using Python Streamlit. The new system will enhance interactivity, visual quality, and ease of report development and maintenance. 

    Designed to serve multiple clients, Infeed700 prioritizes user experience with its responsive interface and intuitive navigation. Users can effortlessly switch between different reporting modules, including "Intake", "Blending", and "Press", allowing for dynamic data analysis tailored to their specific needs.

    ### Key Features:
    - **User-Friendly Interface**: The application’s layout is designed for ease of use, minimizing the learning curve for new users.
    - **Data Visualization**: With integrated SSRS reports, users can visualize data effectively, leading to informed decision-making.
    - **Customizable Reports**: The application supports various report types, enabling tailored data presentations for different operational needs.

    The project will be executed in multiple phases, with defined responsibilities across various teams. The solution will be implemented on-premises, and existing stored procedures will be used to maintain continuity with the current system. 

    Infeed700 is not only a tool for data visualization but also a comprehensive solution for business intelligence, providing valuable insights through advanced data analytics and reporting capabilities.
    '''
    project_structure = '''\
    Infeed700/
    │
    ├── .pycache__                  # Python cache directory
    │
    ├── .streamlit/                 # Streamlit configuration and secrets
    │   ├── secrets.toml            # Secrets for database connection
    │   └── config.toml             # Streamlit configuration settings [theme][server]
    │
    ├── assets/                     # Static assets like CSS, images, and diagrams
    │   ├── css/
    │   │   └── style.css           # Main stylesheet for the app
    │   ├── images/                 # Additional images used in the app
    │   └── diagrams/               # Diagrams or flowcharts for reference
    │
    ├── dev_lab/                    # Development lab files and scripts
    │
    ├── documentation/              # Project documentation
    │
    ├── functions/                  # Additional helper functions
    │   ├── config.py               # Configuration-related functions
    │   ├── create_card.py          # Function to create cards in the UI
    │   ├── data_lab.py             # Data processing functions for lab data
    │   ├── database_connection.py  # Database connection logic
    │   ├── documentation.py        # Documentation functions
    │   ├── embedded_SSRS.py        # Embedded SSRS report handling
    │   ├── get_base64_image.py     # Helper function for image encoding
    │   ├── get_datetime_input.py   # Functions for handling date/time inputs
    │   ├── load_local_css.py       # Function to load local CSS files
    │   ├── load_svg.py             # Function for loading SVG images
    │   ├── report_header_name.py   # Logic for report headers
    │   ├── road_map.py             # Roadmap and progress-related functions
    │   ├── secrets_config.py       # Helper for managing secrets configuration
    │   ├── sites.py                # Site-specific functions
    │   └── utilities.py            # Utility functions
    │
    ├── left_menu/                  # Directory for left menu-related files
    │   ├── left_menu.py            # Contains the logic for the left menu
    │
    ├── libs/                       # Libraries used in the project
    │
    ├── python_offline_installer/   # Offline installer for Python packages
    │
    ├── reports/                    # Directory for different report categories
    │   ├── blending/               # Reports related to blending
    │   ├── intake/                 # Reports related to intake
    │   │   ├── charts/             # Charts specific to intake reports
    │   │   │   ├── line_chart_nett_weight_by_day.py  # Line chart example
    │   │   │   └── (other charts)
    │   │   ├── intake_columns.json  # JSON configuration for intake columns
    │   │   ├── intake_parameters.py # Intake parameters functions
    │   │   └── intake.py            # Main logic for intake reports
    │   └── press/                   # Reports related to press operations
    │
    ├── __init__.py                 # Initialization file for the project package
    ├── .gitignore                  # Git ignore file for the project
    ├── index.html                  # HTML file for the project
    ├── main.py                     # Main entry point for the Streamlit application
    ├── README.md                   # Project README with setup instructions
    ├── requirements.txt            # List of dependencies for the application
    ├── run_streamlit_apps.bat      # Batch file to run Streamlit apps
    ├── setup.bat                   # Batch file for setting up the environment
    ├── streamlit.log               # Log file for Streamlit
  
    '''
    dependency_support = '''\
    - **Streamlit** (>=1.38.0): [Streamlit Documentation](https://docs.streamlit.io/)
    - **Pandas** (>=2.1.0): [Pandas Documentation](https://pandas.pydata.org/)
    - **NumPy** (>=1.25.0): [NumPy Documentation](https://numpy.org/)
    - **SQLAlchemy** (>=2.0.0): [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
    - **PyODBC** (>=4.0.0): [PyODBC Documentation](https://github.com/mkleehammer/pyodbc/wiki)
    - **Matplotlib** (>=3.9.2): [Matplotlib Documentation](https://matplotlib.org/)
    - **Plotly** (>=5.24.1): [Plotly Documentation](https://plotly.com/)
    - **Requests** (==2.32.3): [Requests Documentation](https://docs.python-requests.org/)
    - **Altair** (>=5.0.0): [Altair Documentation](https://altair-viz.github.io/)
    - **Openpyxl** (>=3.1.0): [Openpyxl Documentation](https://openpyxl.readthedocs.io/en/stable/)
    - **Requests NTLM** (>=1.3.0): [Requests NTLM Documentation](https://pypi.org/project/requests-ntlm/)
    - **Streamlit Option Menu** (>=0.3.13): [Streamlit Option Menu Documentation](https://pypi.org/project/streamlit-option-menu/)   
    '''
    # Configuração do menu lateral usando `streamlit_option_menu` no sidebar
    with st.sidebar:
        selected = option_menu(
            menu_title="Documentation",  # Título do menu
            options=["Overview", 
                    "Infrastructure",                 
                    "README.md", 
                    "Project Structure", 
                    "Dependency Support", 
                    "Requirements.txt", 
                    "Setup.bat",
                    "Secrets.toml",
                    "Config.toml",
                    "Last TFS Update",                   
                    "Error Troubleshooting Guide"],
                    
            icons=["book", 
                "book",            
                "file-text", 
                "folder", 
                "link", 
                "filetype-txt", 
                "windows", 
                "filetype-py",              
                "bug"],  # Ícones
            menu_icon="list",  # Ícone do menu
            default_index=0,  # Índice padrão selecionado
        )

    # Exibe o conteúdo correspondente com base na seleção
    if selected == "Overview":
        st.title("Overview")
        st.markdown(Overview)

    elif selected == "README.md":
        st.subheader("README.md")
        st.markdown(readme_text)

    elif selected == "Project Structure":
        st.title("Project Structure")
        st.code(project_structure, language='plaintext')

    elif selected == "Dependency Support":
        st.title("Dependency Support")
        st.markdown(dependency_support)
        
    elif selected == "Error Troubleshooting Guide":       
        st.markdown(troubleshooting_guide)
    
    elif selected == "Main":
        st.title("main.py")
        st.code(main_py_code, language='python')

    elif selected == "Left Menu":
        st.title("left_menu/left_menu.py")
        st.code(left_menu_code, language='python')

    elif selected == "Secrets.toml":
        st.title(".streamlit/secrets.toml")
        st.write("Dont forget to add the secrets file in the right directory")
        st.code("""
            Infeed700/
            ├── main.py                     # Main entry point for the Streamlit application
            │
            ├── requirements.txt             # List of dependencies for the application
            │        
            └── .streamlit/
                └── secrets.toml            # Secrets for database connection
                └── config.toml             # Streamlit Configuration Settings [theme][server] 
        """, language='toml')

        st.code("""
            # This file contains the secrets required to connect to the SQL Server database and SSRS server.
            # This file is not included in the repository, as it contains sensitive information.
            # Please contact the project team for access to this file.

            [sidebar]
            selected_item_color = "#056003"      #Color of the selected item in the sidebar menu 
            icon_color = "#022601"               # Color of the icons in the sidebar menu

            [secrets_config]
            secrets_name = "secrets_das"

            [site_info]
            site_name = 'DAS'

            [release]
            current_release = 'Release 1.1'
        """, language='toml')

        st.subheader("Current secrets.toml:")
        st.code(secrets_toml, language='toml')

    elif selected == "Config.toml":
        st.title(".streamlit/config.toml")
        st.write("Dont forget to add the Config file in the right directory")
        st.code("""
            Infeed700/
            ├── main.py                     # Main entry point for the Streamlit application
            │
            ├── requirements.txt             # List of dependencies for the application
            │        
            └── .streamlit/
                └── secrets.toml            # Secrets for database connection
                └── config.toml             # Streamlit Configuration Settings [theme][server] 
        """,language='toml') 
        st.subheader("Current config.toml:")
        st.code(streamlit_config, language='toml')

    elif selected == "Requirements.txt":
        st.title("requirements.txt")    
        st.subheader("Current requirements:")
        st.code(requirements_txt, language='python')
        
    elif selected == "Data base connection":
        st.title("functions/database_connection.py")    
        st.subheader("Data base connection:")
        st.code(database_connection, language='python')

    elif selected == "Setup.bat":
        st.title("setup.bat")
        st.subheader("Current setup:")
        st.code(setup_bat_code, language='batch')

    elif selected == "Embed SSRS":
        st.title("Embed SSRS")
        st.subheader("Current Embed SSRS:")
        st.code(embeddedSSRS, language='python')

    elif selected == "Styles CSS":    
        st.subheader("Styles CSS:")
        st.code(style_css, language='css')

    elif selected == "Infrastructure":       
        road_map()
        
    elif selected == "Last TFS Update":   
        get_database_version_log_tfs_update(engine)
        
# LOGIN FORM     
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Função de login para verificar as credenciais
def login(username, password):
    if username == "admin" and password == "1984Icm000":
        st.session_state.authenticated = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")

# Exibir o formulário de login se o usuário não estiver autenticado
if not st.session_state.authenticated:
    st.title("Login")
    
    # Campos de entrada para o login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Botão de login
    if st.button("Login"):
        login(username, password)

# Exibir o conteúdo da aplicação após o login
else:    
    run_documentation()