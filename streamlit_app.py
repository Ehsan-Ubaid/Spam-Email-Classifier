import streamlit as st
import pickle

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Spam Detection", layout="centered")

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}  # default user

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ FUNCTIONS ------------------
def predict_email(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "Spam
