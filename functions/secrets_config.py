import os
import streamlit as st
import toml

def get_secrets_config():
    # Retrieve the configuration file name from Streamlit secrets
    secrets_config = st.secrets.get("secrets_config", {"secrets_name": ".streamlit/secrets.toml"})
    secrets_name = secrets_config.get("secrets_name", ".streamlit/secrets.toml")

    # Ensure the file has the .toml extension and is in the .streamlit folder
    if not secrets_name.endswith(".toml"):
        secrets_name = f".streamlit/{secrets_name}.toml"
    else:
        secrets_name = f".streamlit/{secrets_name}"

    # Convert to absolute path and display for debugging
    absolute_path = os.path.abspath(secrets_name)
    #st.write(f"Absolute path for configuration file: {absolute_path}")

    # Check if the file exists
    if not os.path.isfile(absolute_path):
        st.error(f"The configuration file '{absolute_path}' was not found. Please check the path and file name.")
        return None

    # Load configuration from the TOML file
    try:
        # Load the entire configuration file and access the "mydb" section
        db_config = toml.load(absolute_path)["mydb"]
    except KeyError:
        st.error("The 'mydb' section was not found in the configuration file.")
        return None
    except Exception as e:
        st.error(f"Error loading the configuration file: {e}")
        return None
    
    return db_config