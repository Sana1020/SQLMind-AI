import streamlit as st
from inference import generate_sql
from database import execute_query
import pandas as pd
import io
import time

st.set_page_config(
    page_title="SQLMind AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.title("🗄️ Database")

    st.write("**Database:** Northwind")

    st.write("**Engine:** SQLite")

    st.write("**Tables:** 10")

    st.divider()

    st.subheader("Schema")

    tables = [
        "Categories",
        "Customers",
        "Employees",
        "Orders",
        "Order Details",
        "Products",
        "Regions",
        "Shippers",
        "Suppliers",
        "Territories"
    ]

    for table in tables:
        st.write(f"• {table}")

# ==========================
# Custom CSS
# ==========================

st.markdown("""
<style>

.stApp{
    background:#0f172a;
}

/* Titles */
h2{
    color:white !important;
    font-size:18px !important;
    font-weight:600 !important;
}

/* Text Area Label */
label{
    color:white !important;
    font-size:18px !important;
    font-weight:600 !important;
}

.hero{
    text-align:center;
    padding:45px 20px 30px;
}

.hero h1{
    font-size:64px;
    font-weight:800;
    color:white;
    margin-bottom:12px;
    letter-spacing:-2px;
}

.gradient{
    background:linear-gradient(90deg,#8b5cf6,#60a5fa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero h3{
    color:#cbd5e1;
    font-size:30px;
    font-weight:600;
    margin-bottom:20px;
}

.hero p{
    max-width:700px;
    margin:auto;
    color:#94a3b8;
    font-size:18px;
    line-height:1.8;
}

.stButton>button{
    background:linear-gradient(90deg,#6d5efc,#6d7cff);
    color:white;
    border:none;
    border-radius:12px;
    height:52px;
    font-weight:600;
    transition:.3s;
}

.stButton>button:hover{
    transform:translateY(-2px);
    box-shadow:0 0 18px rgba(109,94,252,.35);
}

textarea{
    border-radius:12px !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# Hero
# ==========================

st.markdown("""
<div class="hero">

<h1>
SQLMind <span class="gradient">AI</span>
</h1>

<h3>AI-Powered Database Assistant</h3>

<p>
Transform natural language into production-ready SQL queries,
execute them against your database, and export the results instantly.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================
# Session State
# ==========================

if "question" not in st.session_state:
    st.session_state.question = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "sql" not in st.session_state:
    st.session_state.sql = None

if "df" not in st.session_state:
    st.session_state.df = None

if "error" not in st.session_state:
    st.session_state.error = None

if "execution_time" not in st.session_state:
    st.session_state.execution_time = None

# ==========================
# Quick Examples
# ==========================

st.markdown("""
<p style="
color:white;
font-size:18px;
font-weight:600;
margin-bottom:12px;
">
Quick Examples
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    if st.button("Employees", use_container_width=True):
        st.session_state.question = "List all employees."

    if st.button("Products", use_container_width=True):
        st.session_state.question = "Show all products."

with col2:

    if st.button("Customers", use_container_width=True):
        st.session_state.question = "Show all customers from Germany."

    if st.button("Orders", use_container_width=True):
        st.session_state.question = "List all orders."

st.divider()

# ==========================
# Input
# ==========================

question = st.text_area(
    "Ask your database",
    key="question",
    height=180,
    placeholder="Example: Show all customers from Germany"
)

# ==========================
# Run Query
# ==========================

if st.button("Run Query", use_container_width=True):

    if question.strip():

        with st.spinner("Executing query..."):

            try:

                start_time = time.time()

                sql = generate_sql(question)

                df, error = execute_query(sql)

                execution_time = time.time() - start_time

                st.session_state.sql = sql
                st.session_state.df = df
                st.session_state.error = error
                st.session_state.execution_time = execution_time

                st.session_state.history.insert(
                    0,
                    {
                        "Question": question,
                        "SQL": sql
                    }
                )

            except Exception as e:

                st.session_state.error = str(e)

    else:

        st.warning("Please enter a request.")

# ==========================
# Generated SQL
# ==========================

if st.session_state.sql:

    st.divider()

    st.markdown("""
    <h2 style="color:white;">
    Generated SQL
    </h2>
    """, unsafe_allow_html=True)

    st.code(st.session_state.sql, language="sql")

# ==========================
# Results
# ==========================

if st.session_state.error:

    st.error(st.session_state.error)

elif st.session_state.df is not None:

    if st.session_state.df.empty:

        st.info("The query executed successfully, but no rows were returned.")

    else:

        st.markdown("""
        <h2 style="color:white;">
        Results
        </h2>
        """, unsafe_allow_html=True)

        st.success(
            f"Query executed successfully • {len(st.session_state.df)} rows returned"
        )

        st.caption(
            f"Execution Time: {st.session_state.execution_time:.2f} sec"
        )

        st.dataframe(
            st.session_state.df,
            use_container_width=True,
            hide_index=True
        )
# ==========================
# Downloads
# ==========================

if st.session_state.sql:

    st.divider()

    st.markdown("""
    <h2 style="color:white;">
    Export Results
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.download_button(
            label="📄 SQL",
            data=st.session_state.sql,
            file_name="query.sql",
            mime="text/plain",
            use_container_width=True,
            on_click="ignore"
        )

    if st.session_state.df is not None and not st.session_state.df.empty:

        csv = st.session_state.df.to_csv(index=False).encode("utf-8")

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            st.session_state.df.to_excel(writer, index=False)

        excel_data = excel_buffer.getvalue()

        with col2:

            st.download_button(
                label="📊 CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
                use_container_width=True,
                on_click="ignore"
            )

        with col3:

            st.download_button(
                label="📑 Excel",
                data=excel_data,
                file_name="results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                on_click="ignore"
            )

    with col4:

        if st.button("🗑️ Clear", use_container_width=True):

            st.session_state.question = ""
            st.session_state.sql = None
            st.session_state.df = None
            st.session_state.error = None
            st.session_state.execution_time = None

            st.rerun()

# ==========================
# Query History
# ==========================

if st.session_state.history:

    st.divider()

    st.markdown("""
    <h2 style="color:white;">
    Query History
    </h2>
    """, unsafe_allow_html=True)

    for item in st.session_state.history[:5]:

        with st.expander(item["Question"]):

            st.code(item["SQL"], language="sql")

    if st.button("Clear History", use_container_width=True):

        st.session_state.history = []
        st.rerun()

# ==========================
# Footer
# ==========================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
margin-top:30px;
padding:24px 0;
border-top:1px solid rgba(255,255,255,.08);
text-align:center;
">

<p style="
font-size:24px;
font-weight:700;
color:white;
margin-bottom:8px;
">
SQLMind AI
</p>

<p style="
color:#94a3b8;
font-size:15px;
margin-bottom:10px;
">
AI-Powered Database Assistant
</p>

<p style="
color:#7c82a8;
font-size:14px;
margin-bottom:16px;
">
Powered by <b>Qwen2.5-3B</b> • Fine-Tuned with <b>QLoRA</b> • SQLite
</p>

<p style="
color:#64748b;
font-size:13px;
">
© 2026 Sana Elbakry
</p>

</div>
""", unsafe_allow_html=True)
