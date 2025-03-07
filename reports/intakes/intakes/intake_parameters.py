import streamlit as st
import pandas as pd

def intake_parameters():
    '''
    This function is used to display the input parameters for the intake report.    
    '''
    st.session_state.run_report = True

    with st.container():
        col1, col2 = st.columns([10, 1])

        with col1:
            with st.expander("📶 Input Parameters", expanded=False):

                # Section for selecting dates with a calendar icon                
                dateCol1, dateCol2 = st.columns(2)
                with dateCol1:
                    minDate = st.date_input("Start Date", value=pd.to_datetime("2024-10-01"))
                with dateCol2:
                    maxDate = st.date_input("End Date", value=pd.to_datetime("2024-10-30"))

                # Save the selected dates in session_state for later use
                st.session_state['minDate'] = minDate
                st.session_state['maxDate'] = maxDate  

                input_col1, input_col2, input_col3 = st.columns(3)
                
                with input_col1:
                    loadId = st.text_input('Load Id',  value='NULL',key='input_loadId')       
                    KeyId = st.text_input('Key Id',  value='NULL',key='input_KeyId')            
                    
                # with input_col2:
                #     intakestatustypes = st.text_input('Intake Status Types', value='1,2,3', key='input_intakestatustypes')                  

                # with input_col3:
                #     calloff = st.text_input('Call Off', value='NULL', key='input_calloff')
                 

        with col2:
            if st.button('Run Report', key='run_report_button'):
                st.session_state.run_report = True

        return (loadId,KeyId)
