import streamlit as st
import importlib
from functions.get_datetime_input import get_datetime_input
from functions.report_an_issue import report_an_issue_button

def embed_python_report(report_name, minDate, maxDate):
    """
    Function to embed and dynamically call a report page.
    """
    # Initialize Sessions
    if 'selected_header' not in st.session_state:
        st.session_state['selected_header'] = None
    if 'selected_report' not in st.session_state:
        st.session_state['selected_report'] = None
    if 'select_report_options' not in st.session_state:
        st.session_state['select_report_options'] = None  
    if 'master_minDate' not in st.session_state:
        st.session_state['master_minDate'] = None
    if 'master_maxDate' not in st.session_state:
        st.session_state['master_maxDate'] = None
        
    def clean_report_session():
            """Clears the selected report session."""
            st.session_state['selected_report'] = False
                    
    # Section for selecting dates using a date picker
    with st.expander(label=f"📆 Date Report Parameters ", expanded=False):  
        # Capture date and time inputs
        master_minDate, master_maxDate, StartHour, EndHour, StartMinute, EndMinute = get_datetime_input() 
    
    st.session_state['master_mimDate']= master_minDate
    st.session_state['master_maxDate']= master_maxDate 
         
    # Format time parameters as strings
    StartHour, EndHour = str(StartHour), str(EndHour)
    StartMinute, EndMinute = str(StartMinute), str(EndMinute)
    site_id = str(st.session_state.get('selected_site_id', ''))        

    try:                         
        header = st.session_state['selected_header']
        report_name = st.session_state['selected_report']        
        
        # Dynamically construct the module path
        if header != None and report_name:
            module_path = f"reports.{header}.{report_name}.{report_name}"
            clean_report_session()
            
            # Try to dynamically import the module
            report_module = importlib.import_module(module_path.lower())

            # Check if the corresponding function exists in the module
            report_function_name = f"{report_name}_page"
            if hasattr(report_module, report_function_name):
                # Retrieve the function dynamically
                report_function = getattr(report_module, report_function_name)                
                # Call the function from the module and pass minDate and maxDate as arguments
                report_function(master_minDate,master_maxDate)                
            else:
                st.error(f"The function '{report_function_name}' was not found in module {module_path}.")            
            
        else:
            st.warning('💬 Please select a Category and Report from the left menu.')

    except ModuleNotFoundError:
        st.error(f"Report path: '{module_path}' not found. Please check the project structure. Check the report name.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

    # Create a button to report an issue with additional details
    report_an_issue_button(master_minDate, StartHour, StartMinute, master_maxDate, EndHour, EndMinute)
