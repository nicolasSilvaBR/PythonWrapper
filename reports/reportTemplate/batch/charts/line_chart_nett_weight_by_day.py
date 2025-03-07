import plotly.express as px
import streamlit as st
import pandas as pd

# Line Chart: Nett Weight Over Time
# Objective: Visualize how the net weight of materials changed over time (based on "Time In").
# The chart is a line plot showing the sum of net weight transactions per day.

@st.cache_resource  # Cache the function to optimize performance
def line_chart_nett_weight_by_day(dataSource_filtered):
    # Convert "Time In" column to datetime format
    dataSource_filtered['Time In'] = pd.to_datetime(dataSource_filtered['Time In'])
    
    # Extract only the date (removing time component)
    dataSource_filtered['Time In'] = dataSource_filtered['Time In'].dt.date
    
    # Select relevant columns
    net_weight_by_day = dataSource_filtered[['Time In', 'Nett Weight']]
    
    # Aggregate net weight by day (sum)
    net_weight_by_day = net_weight_by_day.groupby('Time In')['Nett Weight'].sum()

    # Create a line chart using Plotly
    line = px.line(
        net_weight_by_day,
        x=net_weight_by_day.index,  # X-axis: Date
        y='Nett Weight',  # Y-axis: Sum of Nett Weight
        title='Nett Weight by Day',
        labels={'Time In': 'Date', 'Nett Weight': 'Nett Weight (kg)'},
        color_discrete_sequence=['#0072B2'],  # Set the line color
        template='plotly_white',  # Apply a clean template
        markers=True,  # Enable data point markers
        text='Nett Weight',  # Display data labels  
    )

    # Customize marker and text label appearance
    line.update_traces(
        textposition='bottom right',  # Position of data labels
        textfont_size=14,  # Font size of labels
        marker_size=6,  # Marker size
        line_width=2,  # Line thickness
    )

    # Adjust layout settings for better readability
    line.update_layout(
        xaxis_title_font={'size': 12},  # X-axis title font size
        yaxis_title_font={'size': 12},  # Y-axis title font size
        title_font={'size': 14},  # Chart title font size
        width=600,  # Chart width
        height=600  # Chart height
    )

    # Display the chart in the Streamlit app
    st.plotly_chart(line, use_container_width=True)
