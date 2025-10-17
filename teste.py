import streamlit as st
import pyodbc

st.set_page_config(page_title="Teste de Conexão SQL", layout="centered")
st.title("🔬 Testador de Conexão com Banco de Dados")

# Use st.secrets para segurança! NÃO coloque usuário e senha no código.
DB_SERVER = st.secrets["db_credentials"]["server"]
DB_DATABASE = st.secrets["db_credentials"]["database"]
DB_USERNAME = st.secrets["db_credentials"]["username"]
DB_PASSWORD = st.secrets["db_credentials"]["password"]

st.info(f"Tentando conectar ao servidor: **{DB_SERVER}**")
st.info(f"Banco de dados: **{DB_DATABASE}**")

if st.button("🚀 Testar Conexão Agora"):
    try:
        with st.spinner("Conectando..."):
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={DB_SERVER};"
                f"DATABASE={DB_DATABASE};"
                f"UID={DB_USERNAME};"
                f"PWD={DB_PASSWORD};"
                f"TrustServerCertificate=yes;" # Adicionado para flexibilidade
            )
            
            # Tenta estabelecer a conexão
            cnxn = pyodbc.connect(conn_str, timeout=10)
            
            st.success("✅ CONEXÃO BEM-SUCEDIDA! O banco de dados está acessível.")
            st.balloons()
            
            # Opcional: Tenta fazer uma consulta simples
            cursor = cnxn.cursor()
            cursor.execute("SELECT @@VERSION;")
            row = cursor.fetchone()
            st.write("Versão do SQL Server:", row[0])
            
            cnxn.close()

    except Exception as e:
        st.error("❌ FALHA NA CONEXÃO!", icon="🔥")
        st.error("A aplicação NÃO conseguiu se conectar ao banco de dados.")
        st.subheader("Possíveis Causas:")
        st.markdown("""
        *   **Firewall:** O IP do Streamlit Cloud pode não estar liberado no firewall do seu servidor de banco de dados.
        *   **Credenciais Erradas:** Verifique se o IP, nome do banco, usuário e senha estão 100% corretos nos `secrets`.
        *   **Driver Incorreto:** O `DRIVER` na string de conexão pode precisar de ajuste (ex: `ODBC Driver 17 for SQL Server`).
        """)
        st.exception(e)