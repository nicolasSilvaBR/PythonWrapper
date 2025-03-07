import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def get_datetime_input():    
    
    try:  
        
        def subtract_timedelta():
            final = st.session_state['end_date']
            today = datetime.now()
            
            if st.session_state['radio_range'] == "Today":                
                st.session_state['start_date'] = today
                st.session_state['end_date'] = today
            
            elif st.session_state['radio_range'] == "Yesterday":
                st.session_state['start_date'] = today - timedelta(days=1)
                st.session_state['end_date'] = today - timedelta(days=1)

            elif st.session_state['radio_range'] == "Last 7 days":
                st.session_state['start_date'] = today - timedelta(days=6)
                st.session_state['end_date'] = today

            elif st.session_state['radio_range'] == "Last 30 days":
                st.session_state['start_date'] = today - timedelta(days=29)
                st.session_state['end_date'] = today 
                
            if st.session_state['radio_range'] == "Quarter":
                # Usa pandas para obter o primeiro dia do trimestre baseado na data 'final'
                quarter_start = pd.Period(final.strftime('%Y-%m-%d'), freq='Q').start_time
                st.session_state['start_date'] = quarter_start
            
            elif st.session_state['radio_range'] == "Year":
                st.session_state['start_date'] = datetime(final.year, 1, 1)
                st.session_state['end_date'] = datetime(final.year, 12, 31)
            
            elif st.session_state['radio_range'] == "Year to Date":
                st.session_state['start_date'] = datetime(final.year, 1, 1)
                st.session_state['end_date'] = datetime.now()
            
            else:
                pass    
        
        # Columns to show in the datetime parameters
        col_radio,col_min,col_max,col_text,space_col1 = st.columns([2,2,2,3,13])  
            
        with col_radio:
            st.radio(
                "Select a range", 
                ["Custom","Today","Yesterday","Last 7 days", "Last 30 days", "Year to Date","Year"], 
                horizontal=False, 
                key="radio_range", 
                on_change=subtract_timedelta,                
            )
            interval_options = {
                15: "15 Minutes",
                60: "1 Hour",
                1440: "1 Day",
                10080: "1 Week",
                40320: "4 Weeks"
}
            if st.session_state['selected-project'] == 'Enecoms':
                selected_value = st.selectbox("Select a time frame:", list(interval_options.values()))  
                selected_index = [key for key, value in interval_options.items() if value == selected_value][0]                
                st.session_state['selected_timeframe_index'] = selected_index
                
        if "Quarter" not in st.session_state['radio_range']:
            st.session_state['radio_range'] == None  
        
            
        with col_min:            
            minDate = st.date_input("Start date", key="start_date", on_change=subtract_timedelta,format="DD/MM/YYYY")
            StartHour = st.selectbox(label='Start Hour',options=list(range(24)),index=0)
            StartMinute = st.selectbox(label='Start Minute',options=list(range(60)),index=0)
            
        with col_max:
            if "Quarter" not in st.session_state['radio_range']:
                maxDate = st.date_input("End date", key="end_date", on_change=subtract_timedelta,format="DD/MM/YYYY")
            else:
                maxDate = st.date_input("End date", key="end_date", on_change=subtract_timedelta,format="DD/MM/YYYY",disabled=True)
                
            EndHour = st.selectbox(label='End Hour',options=list(range(24)),index=23)
            EndMinute = st.selectbox(label='End Minute',options=list(range(60)),index=59)  
        
        
        return minDate,maxDate,StartHour,EndHour,StartMinute,EndMinute
    
    except Exception as e:
        # Tratamento para erros genéricos (qualquer outro tipo de exceção)
        st.write(f"Check the get_datetime_input() : {e} Columns to show in the datetime parameters")