import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Query Results Viewer", layout="wide")

st.markdown("<h1 style='text-align: center;'>AWS RDS Query Viewer</h1>", unsafe_allow_html=True)

username = ""
password = ""

with st.sidebar:
    st.header("Database Connection")
    db_type = st.selectbox("Database Type", ["postgresql", "mysql"])
    host = st.text_input("Host", "your-db-endpoint.rds.amazonaws.com")
    port = st.text_input("Port", "5432" if db_type == "postgresql" else "3306")
    database = st.text_input("Database Name")

st.subheader("Enter Your SQL Query")
query = st.text_area("SQL Query", height=180)

if st.button("Run Query"):
    try:
        if db_type == "postgresql":
            url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        else:
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        st.success("✅ Query executed successfully")
        st.dataframe(df, use_container_width=True)

        st.download_button("Download Results as CSV", df.to_csv(index=False), "query_results.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
