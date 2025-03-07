import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Lab", page_icon=":bar_chart:", layout="wide")
# Título da página
st.subheader("Upload CSV, Visualize Data, and Get Insights")

# Função para carregar e exibir os dados
def load_and_display_data(uploaded_file):
    # Carrega o arquivo CSV em um DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Exibe as colunas disponíveis
    st.write("### Columns in the CSV file:")
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to display:", all_columns, default=all_columns)
    
    # Exibe as colunas selecionadas
    st.write("### Data from the CSV file (selected columns):")
    st.dataframe(df[selected_columns])
    
    return df, all_columns

# Função para gerar insights
def generate_insights(df):
    # Criando as abas para organizar os insights
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Insights", "Descriptive Statistics", "Unique Values", "Missing Values", "Correlations"])

    # Aba 1: Data Insights
    with tab1:
        st.write("### Data Insights")
        st.write(f"**Number of rows:** {df.shape[0]}")
        st.write(f"**Number of columns:** {df.shape[1]}")
        st.write("**Column Types:**")
        st.write(df.dtypes)

    # Aba 2: Descriptive Statistics para colunas numéricas
    with tab2:
        st.write("### Descriptive Statistics (Numerical Columns Only)")
        numeric_df = df.select_dtypes(include=['number'])  # Filtra apenas colunas numéricas
        st.write(numeric_df.describe())

    # Aba 3: Contagem de valores únicos
    with tab3:
        st.write("### Unique Value Counts by Column")
        unique_counts = df.nunique().to_frame(name="Unique Values").reset_index()
        unique_counts.columns = ['Column', 'Unique Values']
        st.dataframe(unique_counts)

    # Aba 4: Verificar e exibir valores ausentes
    with tab4:
        st.write("### Missing Values")
        missing_values = df.isnull().sum().to_frame(name="Missing Values").reset_index()
        missing_values.columns = ['Column', 'Missing Values']
        st.dataframe(missing_values)

    # Aba 5: Correlação entre colunas numéricas
    with tab5:
        if not numeric_df.empty:
            st.write("### Correlation Between Numeric Columns")
            st.write(numeric_df.corr())
        else:
            st.write("No numeric columns available for correlation.")

# Componente para upload de arquivo CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    # Carrega os dados e exibe as colunas
    df, all_columns = load_and_display_data(uploaded_file)

    # Se o DataFrame não estiver vazio
    if not df.empty:
        # Gera os insights do DataFrame com as abas
        generate_insights(df)
else:
    st.write("Please upload a CSV file to view its content.")
