import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Query Results Viewer", layout="wide")

st.markdown("<h1 style='text-align: center;'>DMQL - Team 23</h1>", unsafe_allow_html=True)

username = "postgres"
password = "password"
host = "database-1.cohgsoe8efzr.us-east-1.rds.amazonaws.com"
port = "5432"
database = "Retail"
default_query = """SELECT c.Name, SUM(p.Amount) AS TotalSpent
        FROM Payments p
        JOIN Sales s ON
        p.OrderNumber = s.OrderNumber
        JOIN Customers c ON
        s.CustomerKey = c.CustomerKey
        GROUP BY c.Name
        ORDER BY TotalSpent DESC
        LIMIT 5;"""


st.subheader("Enter Your SQL Query")
query = st.text_area("SQL Query", value=default_query, height=250)

if st.button("Run Query"):
    try:
        url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        st.success("✅ Query executed successfully")
        st.dataframe(df, use_container_width=True)

        st.download_button("Download Results as CSV", df.to_csv(index=False), "query_results.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
