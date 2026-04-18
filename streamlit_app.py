import streamlit as st
import pickle

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Spam Detection", layout="centered")

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ------------------ CSS (PREMIUM UI) ------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(102,126,234,0.6), rgba(118,75,162,0.6)),
                url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    background-position: center;
}

/* Glass card */
.card {
    width: 400px;
    margin: auto;
    margin-top: 100px;
    padding: 40px;
    border-radius: 20px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Title */
.title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
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
    text-align: center;
}

/* Hide top padding */
.block-container {
    padding-top: 0rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ FUNCTIONS ------------------
def predict_message(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "Spam" if pred == 1 else "Not Spam"

# ------------------ LOGIN / REGISTER UI ------------------
if not st.session_state.logged_in:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Title
    if st.session_state.mode == "login":
        st.markdown('<div class="title">Login</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="title">Register</div>', unsafe_allow_html=True)

    # Inputs
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.session_state.mode == "register":
        confirm = st.text_input("Confirm Password", type="password")

    # Button
    if st.session_state.mode == "login":
        if st.button("Login"):
            if user in st.session_state.users and st.session_state.users[user] == pwd:
                st.session_state.logged_in = True
            else:
                st.error("Invalid credentials")
    else:
        if st.button("Register"):
            if pwd == confirm:
                st.session_state.users[user] = pwd
                st.success("Registered successfully")
                st.session_state.mode = "login"
            else:
                st.error("Passwords do not match")

    # Switch
    if st.session_state.mode == "login":
        st.markdown('<p class="text">Don’t have an account?</p>', unsafe_allow_html=True)
        if st.button("Go to Register"):
            st.session_state.mode = "register"
    else:
        st.markdown('<p class="text">Already have an account?</p>', unsafe_allow_html=True)
        if st.button("Go to Login"):
            st.session_state.mode = "login"

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ MAIN APP ------------------
else:

    st.title("Spam Detection App")

    if st.button("Logout"):
        st.session_state.logged_in = False

    text = st.text_area("Enter your message")

    # File upload
    uploaded_file = st.file_uploader("Upload text file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text)

    # Prediction
    if st.button("Predict"):
        if text.strip():
            result = predict_message(text)
            st.success(result)
            st.session_state.history.append((text, result))
        else:
            st.warning("Enter some text")

    # History
    st.subheader("History")
    if st.session_state.history:
        for msg, res in st.session_state.history[::-1]:
            st.write(f"{res} → {msg[:40]}...")
    else:
        st.write("No history yet")
