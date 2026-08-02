import streamlit as st
from inference import generate_sql

st.set_page_config(
    page_title="SQLMind AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================
# Custom CSS
# ==========================

st.markdown("""
<style>

.stApp{
    background:#0f172a;
}

.hero{
    text-align:center;
    padding:45px 20px 30px;
}

.hero-badge{
    display:inline-block;
    padding:8px 18px;
    background:rgba(124,92,255,.15);
    border:1px solid rgba(124,92,255,.35);
    border-radius:50px;
    color:#a78bfa;
    font-size:14px;
    font-weight:600;
    margin-bottom:25px;
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

<h3>Talk to Your Database in Natural Language</h3>

<p>
Describe your request in plain English and let SQLMind AI generate
accurate, optimized SQL queries in seconds.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================
# Session State
# ==========================

if "question" not in st.session_state:
    st.session_state.question = ""

# ==========================
# Suggested Queries
# ==========================

st.markdown("##  Suggested Queries")

col1, col2 = st.columns(2)

with col1:

    if st.button("Employees", use_container_width=True):
        st.session_state.question = "Show all employees earning more than 7000."

    if st.button("Students", use_container_width=True):
        st.session_state.question = "List the names of all students."

with col2:

    if st.button("Sales", use_container_width=True):
        st.session_state.question = "Show total sales by month."

    if st.button("Customers", use_container_width=True):
        st.session_state.question = "List customers from Cairo."

st.divider()

# ==========================
# Input
# ==========================

question = st.text_area(
    "Enter your request",
    key="question",
    height=180,
    placeholder="Example: Show all employees whose salary is greater than 5000"
)
# ==========================
# Generate SQL
# ==========================

if st.button(" Generate Query", use_container_width=True):

    if question.strip():

        with st.spinner("Generating SQL query..."):

            try:

                sql = generate_sql(question)

                st.divider()

                st.markdown("""
                <h2 style="
                    color:white;
                    margin-bottom:15px;
                ">
                 Generated SQL
                </h2>
                """, unsafe_allow_html=True)

                st.code(sql, language="sql")

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(
                        label="⬇ Download SQL",
                        data=sql,
                        file_name="query.sql",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:

                    if st.button(" Clear", use_container_width=True):
                        st.session_state.question = ""
                        st.rerun()

            except Exception as e:

                st.error(str(e))

    else:

        st.warning("⚠️ Please enter a request first.")

# ==========================
# Footer
# ==========================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
margin-top:30px;
padding:22px 0;
border-top:1px solid rgba(255,255,255,.08);
text-align:center;
">

<p style="
font-size:24px;
font-weight:700;
color:white;
margin-bottom:6px;
">
 SQLMind AI
</p>

<p style="
color:#94a3b8;
margin-bottom:8px;
font-size:15px;
">
Natural Language → SQL
</p>

<p style="
color:#7c82a8;
font-size:14px;
margin-bottom:14px;
">
Powered by <b>Qwen2.5</b> • Fine-Tuned with <b>QLoRA</b>
</p>

<p style="
color:#64748b;
font-size:13px;
">
© 2026 Sana Elbakry
</p>

</div>
""", unsafe_allow_html=True)