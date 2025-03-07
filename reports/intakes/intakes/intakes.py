import streamlit as st
import pandas as pd
import json
import os
import reports.intakes.intakes.intake_parameters as intake_parameters
from functions.database_connection_DW import mydb
from reports.intakes.intakes.charts.line_chart_nett_weight_by_day import echarts_line_chart_nett_weight_by_day # import line_chart_nett_weight_by_day
from reports.intakes.intakes.charts.line_chart_nett_weight_by_day import tree_chart
from reports.intakes.intakes.charts.line_chart_nett_weight_by_day import create_tree_figure

# Step 1 = Corrected the path to the JSON file, columns names.
# Step 2 = Correct the name of the Main function for the intakes report page, dont take "_page" out !.
# Step 3 = Get report parameters, update the file intake_parameters.py to get all the necessary paramaters.
# Step 4 = Use None for NULL handling in SQL.
# Step 5 = Execute the stored procedure.
# Step 6 = Make sure to have all parameters listed in the params=.
# Step 7 Update Report Name

# Cache for loading column mapping
@st.cache_data
def load_columns_mapping():
    """
    Loads column mapping from a JSON file to rename columns in the dataset.
    """
    
    # Step 1 = Corrected the path to the JSON file
    json_file_path = 'reports/intakes/intakes/intake_columns.json'  

    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            # Padroniza os nomes das colunas para minúsculas
            return {key.lower(): value for key, value in json.load(f).items()}
    else:
        st.error(f"⚠️ Mapping file '{json_file_path}' not found.")
        return {}

# Cache for the database connection
@st.cache_resource
def get_db_dw_engine():
    """
    Returns the database connection engine.
    """
    return mydb()

# Step 2 Main function for the intakes report page
def intakes_page(mindate, maxdate):
    """
    Defines the interface and logic for the intakes report page.
    """    
    # Step 3 Get report parameters
    loadId, KeyId = intake_parameters.intake_parameters()

    # Check if the report execution flag is set
    if 'run_report' not in st.session_state:
        st.session_state.run_report = False

    if st.session_state.run_report:
        try:
            with st.spinner('⏳ Loading report...'):
                
                # Step 4 Use None for NULL handling in SQL
                loadId = None if loadId in [None, 'NULL'] else loadId 
                KeyId = None if KeyId in [None, 'NULL'] else KeyId             
                
                # Connect to the database infeed700DW
                engine = get_db_dw_engine()                  
                    
                # Step 5 Execute the stored procedure
                query = """
                EXEC Report.factCompletedIntakes 
                @loadId = ?,
                @KeyId = ?
                """
                
                # Step 6 make sure to have all parameters listed in the params=
                dataSource = pd.read_sql_query(query, engine, params=(loadId, KeyId,))     

                # Check if data is returned
                if dataSource.empty:
                    st.warning("💬 No data available for display.")
                else:
                    # Convert column names to lowercase
                    dataSource.columns = dataSource.columns.str.lower()

                    # Load column mapping
                    columns_to_display = load_columns_mapping()

                    if columns_to_display:
                        # Filter columns that exist in the DataFrame
                        existing_columns = [col for col in columns_to_display.keys() if col in dataSource.columns]
                        dataSource_filtered = dataSource[existing_columns]
                        dataSource_filtered.rename(columns=columns_to_display, inplace=True)

                        # Create a filtered DataFrame
                        dataSource_filtered = dataSource[existing_columns]
                        dataSource_filtered.rename(columns=columns_to_display, inplace=True)

                        # Create tabs for display
                        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                            "📅 Table", "📊 Charts", "📈 Statistics", "🔍 Insights",
                            "📚 Explanation", "⬇️ Export", "🔑 KPIs"
                        ])
                        
                        # Convert dates to European format (DD/MM/YYYY)
                        mindate_eu = pd.to_datetime(mindate).strftime('%d/%m/%Y')
                        maxdate_eu = pd.to_datetime(maxdate).strftime('%d/%m/%Y')

                        # Full Table Tab
                        with tab1:
                            dateCol1, dateCol2 = st.columns([6, 1])
                            with dateCol1:
                                st.markdown(
                                    '<span style="color:#006010;font-size:20px;">Intake Report</span>',
                                    unsafe_allow_html=True
                                )
                            with dateCol2:
                                st.markdown(
                                    f'<span style="color:black;font-size:13px;">From: {mindate_eu} to {maxdate_eu}</span>',
                                    unsafe_allow_html=True
                                )
                            # Display the full DataFrame
                            st.dataframe(dataSource_filtered, hide_index=True, use_container_width=True, height=670)
                        # Charts Tab
                        with tab2:
                            st.subheader("Charts tab")
                            echarts_line_chart_nett_weight_by_day()
                            tree_chart()
                            st.plotly_chart(create_tree_figure(),use_container_width=True) 
                        # Statistics Tab
                        with tab3:
                            st.subheader("Statistics tab")
                            st.write("### Descriptive Statistics of the Data")
                            st.write(dataSource_filtered.describe())
                        # Insights Tab
                        with tab4:
                            st.subheader("Insights tab")
                        # Explanation Tab
                        with tab5:
                            st.subheader("Explanation tab")
                        # Export Tab
                        with tab6:
                            st.subheader("Export tab")
                        # KPIs Tab
                        with tab7:
                            st.subheader("KPIs tab")

                    else:
                        st.error("⚠️ No column mapping found. Please check the JSON file.")

            # Reset the report execution flag
            st.session_state.run_report = False    
           

        except Exception as e:
            st.error(f"🚨 An unexpected error occurred: {str(e)}")
