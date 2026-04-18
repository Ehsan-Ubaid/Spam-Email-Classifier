import streamlit as st
import pickle

st.set_page_config(page_title="Spam Detection", layout="wide")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Remove scroll */
html, body {
    overflow: hidden;
}

/* Background */
.stApp {
    background: linear-gradient(rgba(102,126,234,0.6), rgba(118,75,162,0.6)),
                url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    background-position: center;
}

/* Center box */
.center {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 320px;
    text-align: center;
}

/* Title */
.title {
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 15px;
}

/* 🔥 GLASS INPUTS */
input, textarea {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px !important;
    color: white !important;
}

/* File uploader glass */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.15);
    padding: 10px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.3);
}

/* Button */
.stButton>button {
    width: 100%;
    border-radius: 25px;
    background: white;
    color: black;
    font-weight: bold;
}

/* Text */
label, p {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "mode" not in st.session_state:
    st.session_state.mode = "signin"
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- FUNCTION ----------------
def predict_message(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "Spam" if pred == 1 else "Not Spam"

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.markdown('<div class="center">', unsafe_allow_html=True)

    st.markdown('<div class="title">Login</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user] == pwd:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Continue as Guest"):
        st.session_state.logged_in = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    # Enable scroll after login
    st.markdown("""
    <style>
    html, body {
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Spam Detection System")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    text = st.text_area("Enter your message")

    uploaded_file = st.file_uploader("Upload text file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

    if st.button("Predict"):
        if text.strip():
            result = predict_message(text)
            st.success(result)
            st.session_state.history.append((text, result))
        else:
            st.warning("Enter some text")

    st.subheader("History")

    for msg, res in st.session_state.history[::-1]:
        st.write(f"{res} → {msg[:40]}...")
