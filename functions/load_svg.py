import streamlit as st
import logging

@st.cache_resource
def load_svg(file_path):
    """Load the content of an SVG file or return a default icon if it fails."""
    default_icon = "bar-chart-fill"  # Default icon to use if SVG loading fails

    try:
        with open(file_path, "r") as svg_file:
            # Read the content of the SVG file
            return svg_file.read()
    except FileNotFoundError:
        # Log a warning if the SVG file is not found and return the default icon
        logging.warning(f"SVG file not found: {file_path}. Using default icon.")
        return default_icon
    except Exception as e:
        # Log an error for any other exceptions that occur during SVG loading
        logging.error(f"Error loading SVG: {e}. Using default icon.")
        return default_icon
    