import streamlit as st
import pickle

st.set_page_config(page_title="Spam Detection", layout="wide")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ---------------- CSS (NEXT LEVEL) ----------------
st.markdown("""
<style>

/* 🔥 Animated Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #6a11cb, #2575fc);
    background-size: 400% 400%;
    animation: gradientMove 10s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Center Layout */
.center-box {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 95vh;
}

/* Glass Card */
.card {
    width: 420px;
    padding: 40px;
    border-radius: 20px;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
}

/* Title */
.title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #ddd;
    margin-bottom: 20px;
}

/* Inputs */
input, textarea {
    border-radius: 12px !important;
}

/* 🔥 Buttons */
.stButton>button {
    width: 100%;
    border-radius: 30px;
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255,255,255,0.6);
}

/* Text */
.text {
    color: white;
    text-align: center;
}

/* Result styles */
.spam {
    color: #ff4b4b;
    font-weight: bold;
    font-size: 20px;
}

.ham {
    color: #00ff9d;
    font-weight: bold;
    font-size: 20px;
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

# ---------------- AUTH UI ----------------
if not st.session_state.logged_in:

    st.markdown('<div class="center-box"><div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">Spam Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart Email Classifier</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.session_state.mode == "signin":

        if st.button("Sign In"):
            if user in st.session_state.users and st.session_state.users[user] == pwd:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.rerun()

        st.markdown('<p class="text">Don’t have an account?</p>', unsafe_allow_html=True)
        if st.button("Sign Up"):
            st.session_state.mode = "signup"
            st.rerun()

    else:
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if pwd == confirm:
                st.session_state.users[user] = pwd
                st.success("Account created")
                st.session_state.mode = "signin"
                st.rerun()
            else:
                st.error("Passwords do not match")

        st.markdown('<p class="text">Already have an account?</p>', unsafe_allow_html=True)
        if st.button("Back to Sign In"):
            st.session_state.mode = "signin"
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    st.title("🚀 Spam Detection Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.mode = "signin"
        st.rerun()

    text = st.text_area("Enter your message")

    uploaded_file = st.file_uploader("Upload text file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

    if st.button("Analyze Message"):
        if text.strip():
            result = predict_message(text)

            if result == "Spam":
                st.markdown('<p class="spam">⚠️ Spam Detected</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="ham">✅ Not Spam</p>', unsafe_allow_html=True)

            st.session_state.history.append((text, result))
        else:
            st.warning("Enter some text")

    st.subheader("📜 History")

    for msg, res in st.session_state.history[::-1]:
        st.write(f"{res} → {msg[:50]}...")
