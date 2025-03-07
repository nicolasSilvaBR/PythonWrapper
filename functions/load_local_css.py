import streamlit as st

# Function to load local CSS file
def load_local_css(file_name):
    """Load local CSS for custom styles.
    Args:
        file_name (str): Name of the CSS file to load.       
    
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found.")