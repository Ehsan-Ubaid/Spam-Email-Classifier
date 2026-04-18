import streamlit as st
import pickle

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Spam Detection", layout="centered")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(102,126,234,0.6), rgba(118,75,162,0.6)),
                url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    background-position: center;
}

/* Glass Card */
.card {
    width: 420px;
    margin: auto;
    margin-top: 120px;
    padding: 50px 30px 30px 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    text-align: center;
}

/* Title FIXED POSITION */
.title {
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: white;
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 25px;
    background: white;
    color: black;
    font-weight: bold;
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
}

/* Text */
.text {
    color: white;
    font-size: 14px;
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

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ✅ FIXED TITLE POSITION
    st.markdown('<div class="title">Spam Detection System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Welcome</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    # -------- SIGN IN --------
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
        if st.button("Go to Sign Up"):
            st.session_state.mode = "signup"
            st.rerun()

    # -------- SIGN UP --------
    else:
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if pwd == confirm:
                st.session_state.users[user] = pwd
                st.success("Account created")
                st.session_state.mode = "signin"
                st.rerun()
            else:
                st.error("Passwords do not match")

        st.markdown('<p class="text">Already have an account?</p>', unsafe_allow_html=True)
        if st.button("Go to Sign In"):
            st.session_state.mode = "signin"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    st.title("Spam Detection System")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.mode = "signin"
        st.rerun()

    text = st.text_area("Enter your message")

    uploaded_file = st.file_uploader("Upload text file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text)

    if st.button("Predict"):
        if text.strip():
            result = predict_message(text)
            st.success(result)
            st.session_state.history.append((text, result))
        else:
            st.warning("Enter some text")

    st.subheader("History")

    if st.session_state.history:
        for msg, res in st.session_state.history[::-1]:
            st.write(f"{res} → {msg[:40]}...")
    else:
        st.write("No history yet")
