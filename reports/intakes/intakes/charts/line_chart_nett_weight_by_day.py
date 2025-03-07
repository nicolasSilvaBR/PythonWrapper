import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import plotly.express as px

#@st.cache_resource  # Cache the function to optimize performance
# https://echarts.apache.org/examples/en/index.html
# echarts java script

def echarts_line_chart_nett_weight_by_day():
    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "legend": {"data": ["Wheat", "Barley", "Corn", "Rice", "Oats"]},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": [
            {
                "type": "category",
                "boundaryGap": False,
                "data": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            }
        ],
        "yAxis": [{"type": "value", "name": "Net Weight (kg)"}],
        "series": [
            {"name": "Wheat", "type": "line", "stack": "Total", "areaStyle": {}, "data": [120, 132, 101, 134, 90, 230, 210]},
            {"name": "Barley", "type": "line", "stack": "Total", "areaStyle": {}, "data": [220, 182, 191, 234, 290, 330, 310]},
            {"name": "Corn", "type": "line", "stack": "Total", "areaStyle": {}, "data": [150, 232, 201, 154, 190, 330, 410]},
            {"name": "Rice", "type": "line", "stack": "Total", "areaStyle": {}, "data": [320, 332, 301, 334, 390, 330, 320]},
            {"name": "Oats", "type": "line", "stack": "Total", "label": {"show": True, "position": "top"}, "areaStyle": {}, "data": [820, 932, 901, 934, 1290, 1330, 1320]},
        ],
    }

    st_echarts(options=options, height="400px", key="net_weight_chart")  # 🔹 Adicionado key único




def tree_chart():
    tree_data = {
        "name": "1 - Mains In",
        "children": [
            {
                "name": "150 - PL3 Meters Total",
                "children": [
                    {"name": "151 - PL3 Press"},
                    {"name": "152 - PL3 BOA 3"}
                ]
            },
            {
                "name": "130 - PL1 Meters Total",
                "children": [
                    {"name": "131 - PL1 BOA 1"},
                    {"name": "132 - PL1 Cooler Fan"}
                ]
            },
            {
                "name": "140 - PL2 Meters Total",
                "children": [
                    {"name": "141 - PL2 BOA 2"},
                    {"name": "142 - PL2 Press"},
                    {"name": "143 - PL2 Cooler Fan"}
                ]
            },
            {
                "name": "160 - BL1 Meters Total",
                "children": [
                    {"name": "161 - BL1 Grinder 1"},
                    {"name": "162 - BL1 Grinder 2"}
                ]
            }
        ]
    }

    options = {
        "tooltip": {
            "trigger": "item",
            "triggerOn": "mousemove"
        },
        "series": [
            {
                "type": "tree",
                "data": [tree_data],
                "top": "1%",
                "left": "7%",
                "bottom": "1%",
                "right": "20%",
                "symbolSize": 7,
                "label": {
                    "position": "left",
                    "verticalAlign": "middle",
                    "align": "right",
                    "fontSize": 9
                },
                "leaves": {
                    "label": {
                        "position": "right",
                        "verticalAlign": "middle",
                        "align": "left"
                    }
                },
                "emphasis": {
                    "focus": "descendant"
                },
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750
            }
        ]
    }

    st_echarts(options=options, height="500px", key="tree_chart")

def create_tree_figure():
    data = {
        "Ingredient": ["Corn", "Soybean Meal", "Wheat", "Fish Meal", "Salt", "Minerals", "Vitamins"],
        "Percentage": [50, 25, 10, 5, 3, 4, 3]
    }
    
    fig = px.bar(
        data, x="Ingredient", y="Percentage",
        title="Animal Feed Composition",
        labels={"Percentage": "Proportion (%)", "Ingredient": "Feed Ingredient"},
        color="Ingredient"
    )
    
    fig.update_layout(margin=dict(t=40, l=40, r=40, b=40))
    return fig