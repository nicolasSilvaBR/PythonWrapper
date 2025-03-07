import streamlit as st
import pandas as pd
import plotly.express as px
from functions.database_connection import mydb
import json
import os
import reports.intakes.intakes_summary.intake_parameters as intake_parameters
import reports.intakes.intakes_summary.charts.line_chart_nett_weight_by_day as line_chart_nett_weight_by_day

# Cache the loading of the column mapping to avoid repeated file I/O
@st.cache_data
def load_columns_mapping():
    """
    Loads a column mapping from a JSON file for renaming columns in the dataset.
    """
    
    json_file_path = 'reports/intakes/intakes_summary/intake_summary_columns.json'  # Path to the JSON file
    
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            return json.load(f)
    else:
        st.error(f"Mapping file '{json_file_path}' not found.")
        return {}

# Memorize the database connection function to prevent multiple connections
@st.cache_resource
def get_db_engine():
    return mydb()

# Function to create and display cards for key metrics
def display_metrics(data):
    """
    Displays 'cards' for key metrics such as row count, unique materials, total weight.
    """

# Main function to handle the intake page
def intakes_summary_page(mindate, maxdate):
    """
    Defines the layout and logic for the intake report page where users can input
    parameters and generate a report with statistics and charts.
    """    
    
    # Input parameters   
    # Importing the intake_parameters function from the reports/intake/intake_parameters.py file
    # This function returns the values of the input parameters    
    # The function is called only once and the results are cached for subsequent runs    
    # The function is also used to generate the SQL query for the report    
    suppliercode, supplier, hauliercode, haulier, intakestatustypes, rminclude, keytypes, calloff, siteid = intake_parameters.intake_parameters()
    
    # Run the report logic
    if 'run_report' not in st.session_state:
        st.session_state.run_report = False

    if st.session_state.run_report:
        try:
            with st.spinner('Running Report...'):
                # Use None for NULL handling in SQL
                suppliercode = f"'{suppliercode}'" if suppliercode not in [None, 'NULL'] else 'NULL'
                hauliercode = f"'{hauliercode}'" if hauliercode not in [None, 'NULL'] else 'NULL'
                haulier = f"'{haulier}'" if haulier not in [None, 'NULL'] else 'NULL'
                supplier = f"'{supplier}'" if supplier not in [None, 'NULL'] else 'NULL'
                calloff = f"'{calloff}'" if calloff not in [None, 'NULL'] else 'NULL'
                keytypes = f"'{keytypes}'" if keytypes not in [None, 'NULL'] else 'NULL'

                # Use cached database connection
                engine = get_db_engine()

                # SQL Stored Procedure execution
                storedProcedure = f"""
                    EXEC [Report].[SSRS_IntakeReport]
                    @mindate = '{mindate}',
                    @maxdate = '{maxdate}',
                    @suppliercode = {suppliercode},
                    @hauliercode = {hauliercode},
                    @intakestatustypes = '{intakestatustypes}',
                    @rminclude = '{rminclude}',
                    @haulier = {haulier},
                    @supplier = {supplier},
                    @calloff = {calloff},
                    @siteid = {siteid},
                    @keytypes = {keytypes}
                """
                dataSource = pd.read_sql(storedProcedure, engine)
                dataSource.sort_values(by='timein',axis=0, ascending=False,inplace=False,kind='quicksort')
                dataSource['timein'] = pd.to_datetime(dataSource['timein'], errors='coerce')
                dataSource['date'] = dataSource['timein'].dt.date
                dataSource['nettweight'] = dataSource['nettweight'].fillna(0)

                if dataSource.empty:
                    st.write("💬 No data available to display.")
                else:
                    columns_to_display = load_columns_mapping()
                    if columns_to_display:
                        existing_columns = [col for col in columns_to_display.keys() if col in dataSource.columns]
                        dataSource_filtered = dataSource[existing_columns]
                        dataSource_filtered.rename(columns=columns_to_display, inplace=True)
                        dataSource_filtered.sort_values(by='Time In', axis=0, ascending=False, inplace=True, kind='quicksort')

                       
                        # Organize the content in tabs
                        tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["📅 Table", "📊 Charts", "📈 Statistics", "🔍 Insights","📚 Explainer","⬇️ Export","🔑 KPI`s"])
                        
                        # Convert dates to European format (DD/MM/YYYY)
                        mindate_eu = pd.to_datetime(mindate).strftime('%d/%m/%Y')
                        maxdate_eu = pd.to_datetime(maxdate).strftime('%d/%m/%Y')

                        # Full table tab
                        with tab1:
                            dateCol1,dateCol2 = st.columns([6,1])
                            with dateCol1:
                                #st.write(f"##### Intake Report")
                                st.markdown(f'<span style="color:#006010;font-size:20px;">Intake Report</span>', unsafe_allow_html=True)
                            with dateCol2:
                                #st.write(f"Date from: {mindate_eu}  To: {maxdate_eu}")
                                st.markdown(f'<span style="color:black;font-size:13px;">Date from: {mindate_eu}  To: {maxdate_eu}</span>', unsafe_allow_html=True)
                            st.dataframe(dataSource_filtered, hide_index=True, use_container_width=True, height=670)
                            #st.data_editor(data=dataSource_filtered,height=670,hide_index=True,use_container_width=True,)

                        # Charts tab
                        # Charts using plotly library  
                        with tab2:    
                            # Line Chart of Net Weight Intake by Day
                            line_chart_nett_weight_by_day.line_chart_nett_weight_by_day(dataSource_filtered)

                            st.divider()                          
                              
                            # Grouping data sources to use in the charts 
                            sum_rm_name_groupped = dataSource_filtered.groupby('RM Name').agg({'Nett Weight': 'sum'}).reset_index()   

                            # Bar Chart of Net Weight Intake by Raw Material Name
                            # Bar Chart of Net Weight Intake by Raw Material Name
                            chart = px.bar(
                                sum_rm_name_groupped.sort_values("Nett Weight"),                                     
                                y="RM Name",
                                x="Nett Weight",
                                orientation="h",
                                title="Net Weight Intake by Raw Material Name",
                                labels={'Nett Weight': 'Net Weight', 'RM Name': 'Raw Material Name'},
                                color_discrete_sequence=['#475b7d'],
                                text_auto=',.2f',  # format numbers with 2 decimal places
                                opacity=1,                                 
                            )

                            # Increase the size of the text inside the bars
                            chart.update_traces(
                                textposition='outside',  # Position of the text outside the bars
                                textfont=dict(size=36),  # Increase the size of the text labels
                                cliponaxis=False,        # Avoid text clipping outside the bars
                            )

                            # Increase the size of the font and title of the axes
                            chart.update_layout(
                                xaxis_title_font={'size': 14},  # Font size of the X-axis title
                                yaxis_title_font={'size': 14},  # Font size of the Y-axis title 
                                title_font={'size': 16},        # Font size of the chart title
                                width=600,                      # Adjust the width 
                                height=600                      # Adjust the height
                            )

                            # Display the chart
                            st.plotly_chart(chart, use_container_width=True, key="bar_chart_rm_name_chart1")


                        # Statistics tab
                        with tab3:
                            st.write("### Descriptive Statistics of the Data")
                            st.write(dataSource_filtered.describe())

                        # Insights tab
                        with tab4:                            
                            st.write("### Key Insights")
                            
                            # Insight 1: Raw Material with the highest total weight
                            st.write(f"- The raw material with the highest total intake weight is: **{sum_rm_name_groupped.iloc[0]['RM Name']}** "
                                    f"with a total of **{sum_rm_name_groupped.iloc[0]['Nett Weight']:,} kg**.")
                            
                            # Insight 2: Number of different raw materials processed
                            st.write(f"- A total of **{len(dataSource_filtered['RM Name'].unique())}** distinct raw materials were processed during the reporting period.")
                                                  
                            # Insight 4: Total processed weight
                            total_weight = dataSource_filtered['Ordered Weight'].sum()
                            st.write(f"- The total weight of all raw materials processed amounts to **{total_weight:,} kg**.")
                            
                            # Insight 5: Most frequent bay used for deliveries
                            most_frequent_bay = dataSource_filtered['Bay Number'].mode()[0]
                            st.write(f"- The bay most frequently used for deliveries is Bay **{most_frequent_bay}**.")                            
                           

                        with tab5:
                            st.markdown("""
                                        ##### Intake 

                                        The **Intake 700** report tracks the intake of raw materials into the production system. It records essential details related to the timing, identification, and logistics of material deliveries. Below are the key aspects of the report:

                                        ##### 1. Timing Information:
                                        - **Time In / Time Out**: These fields record the exact timestamps when raw materials arrive and leave the intake area.
                                        - **Created On**: The date and time when the record was created, likely reflecting when the delivery process started.

                                        ##### 2. Material Information:
                                        - **RM Code / RM Name**: The "Raw Material Code" and the corresponding "Raw Material Name" provide identification of the material being delivered (e.g., Wheatfeed, Maize Gluten, etc.).
                                        - **Ordered Weight**: Indicates the quantity of the raw material ordered, measured in kilograms or tons.

                                        ##### 3. Logistics and Tracking:
                                        - **Bay Number**: The intake bay where the material is offloaded.
                                        - **Docket Number**: A unique identifier tracking the delivery and receipt of the materials.
                                        - **Supplier Docket / Lot Number**: Additional tracking information provided by the supplier, ensuring traceability of the material.

                                        ##### 4. Other Relevant Details:
                                        - **Notes**: These columns may contain additional information related to the delivery, such as remarks from the supplier or intake personnel.
                                        - **Site Description**: Information about the site where the materials were delivered, ensuring clarity about the intake location.

                                        ---

                                        This report aids in tracking raw material deliveries, confirming received quantities, and overseeing the timing and logistics of the intake process. It offers a clear and organized approach to verifying delivery details and managing the material flow efficiently.

                            """)
                        with tab6:
                            # Converter o DataFrame para CSV
                            csv = dataSource_filtered.to_csv(index=False)

                            with st.container():
                                col1, col2 = st.columns([1,8])
                                # Adicionar botão de download para CSV
                                with col1:
                                    st.download_button(
                                        label="Download as CSV",
                                        data=csv,
                                        file_name='dataSource_filtered.csv',
                                        mime='text/csv'
                                    )
                                    st.download_button(
                                        label="Download as PDF",
                                        data=csv,
                                        file_name='dataSource_filtered.csv',
                                        mime='text/csv'
                                    )
                        with tab7:
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Temperature", "70 °C", "1.2 °C")
                            col2.metric("Wind", "9 Km/h", "-8%")
                            col3.metric("Humidity", "86%", "4%")


                    else:
                        st.write("No column mapping found. Please check the mapping file.")

                st.session_state.run_report = False

        except Exception as e:
            st.error(f"An error occurred: {e}")
