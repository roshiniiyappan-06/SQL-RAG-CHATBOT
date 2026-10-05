
import streamlit as st
import sqlite3
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq

st.set_page_config(page_title="CHITTI SQL Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp{
background:linear-gradient(135deg,#0f172a,#1e3a8a,#38bdf8);
}
.block-container{
padding-top:2rem;
}
.main-card{
background:rgba(255,255,255,0.12);
backdrop-filter:blur(12px);
padding:20px;
border-radius:20px;
border:1px solid rgba(255,255,255,.2);
}
h1,h3,p,label{color:white!important;}
div[data-testid="stDataFrame"]{
background:white;
border-radius:12px;
padding:8px;
}
</style>
""", unsafe_allow_html=True)

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

if "history" not in st.session_state:
    st.session_state.history=[]

with st.sidebar:
    st.title("🤖 CHITTI")
    st.write("### Sample Questions")
    samples=[
        "Show all students",
        "Show CSE students",
        "Who has highest CGPA?",
        "Average CGPA",
        "Show students with CGPA above 8.5"
    ]
    for q in samples:
        if st.button(q):
            st.session_state["sample"]=q

    if st.button("🗑 Clear Chat"):
        st.session_state.history=[]

st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("🎓 CHITTI - College SQL Chatbot")
st.caption("Ask questions in plain English and get answers from your SQLite database.")

question = st.chat_input("Ask something about students...")

if "sample" in st.session_state and not question:
    question=st.session_state.pop("sample")

for role,msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)

if question:
    st.session_state.history.append(("user",question))
    with st.chat_message("user"):
        st.write(question)

    prompt=f"""
You are an expert SQLite assistant.

Database: college.db

Tables may include:
students(id,name,department,cgpa)

Return ONLY a valid SQLite query.

Question:
{question}
"""

    with st.spinner("Generating SQL..."):
        sql=llm.invoke(prompt).content.strip().replace("```sql","").replace("```","").strip()

    with st.chat_message("assistant"):
        st.subheader("Generated SQL")
        st.code(sql,language="sql")

        try:
            conn=sqlite3.connect("college.db")
            df=pd.read_sql_query(sql,conn)
            conn.close()

            if len(df):
                st.success(f"{len(df)} record(s) found.")
                st.dataframe(df,use_container_width=True)
            else:
                st.info("No matching records found.")
        except Exception as e:
            st.error(str(e))

    st.session_state.history.append(("assistant",sql))

st.markdown("</div>", unsafe_allow_html=True)
