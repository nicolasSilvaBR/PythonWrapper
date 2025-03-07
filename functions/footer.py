import streamlit as st

release = st.secrets['release']['current_release']

# Function to display the footer
def display_footer():
    """Display footer with custom CSS at the bottom of the sidebar."""
    st.markdown(
        """
        <style>
            /* Style for the footer to position it at the bottom of the sidebar */
            .sidebar-content {
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            .footer {
                margin-top: auto;
                padding: 20px 0;
                text-align: center;
                font-size: 12px;
                color: #555;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="footer">
            <p>               
                <a href="https://icmcsl.com/contact/" target="_blank">Contact Us</a> |
                {release}                            
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )