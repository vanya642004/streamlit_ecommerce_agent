import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from llama_cpp import Llama
from langchain.llms import LlamaCpp
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain
from streamlit_chat import message

# Paths
DB_PATH = "ecom.db"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "ggml-model.bin")

@st.cache_data(show_spinner=False)
def init_db():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    for fname, table in [
        ("total_sales.csv", "total_sales"),
        ("ad_sales.csv", "ad_sales"),
        ("eligibility.csv", "eligibility")
    ]:
        path = os.path.join(DATA_DIR, fname)
        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists="replace", index=False)
    return engine

@st.cache_resource(show_spinner=False)
def load_chain(engine):
    llm = LlamaCpp(model_path=MODEL_PATH, n_ctx=2048)
    db = SQLDatabase(engine)
    return SQLDatabaseChain.from_llm(llm, db, verbose=False)

# App UI
st.set_page_config(page_title="E‑com Data Chatbot", layout="centered")
st.title("📊 E-commerce Data Chatbot")
engine = init_db()
chain = load_chain(engine)

if "history" not in st.session_state:
    st.session_state.history = []

# Input
query = st.text_input("Ask me about your e-commerce data:")
if query:
    st.session_state.history.append((query, True))
    with st.spinner("Thinking..."):
        resp = chain.run(query)
    st.session_state.history.append((resp, False))

# Chat history
for text, is_user in st.session_state.history:
    message(text, is_user=is_user)
