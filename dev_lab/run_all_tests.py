import streamlit as st
# Import each test file
from test_set_page_config import run_test as set_page_run_test
from test_secrets_config import run_test as secrets_run_test
from test_database_connection import run_test as db_run_test
from test_embed_ssrs_report import run_test as embed_ssrs_report_run_test
from test_report_header_name import run_test as report_header_name_run_test

st.subheader("Function Tests")

# Run tests for each function
set_page_run_test()
db_run_test()
secrets_run_test()
embed_ssrs_report_run_test()
report_header_name_run_test()
