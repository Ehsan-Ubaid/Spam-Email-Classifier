import streamlit as st
import pickle

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Spam Detection", layout="centered")

# ------------------ PREMIUM CSS ------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

/* Glass Card */
.block-container {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

/* Titles */
h1, h2, h3 {
    color: white !important;
    text-align: center;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
    border: none;
}

/* Inputs */
textarea, input {
    background-color: rgba(255,255,255,0.9) !important;
    color: black !important;
    border-radius: 10px !important;
}

/* Subtext */
p, label {
    color: white !important;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ FUNCTIONS ------------------
def predict_message(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "🚫 Spam" if pred == 1 else "✅ Not Spam"

def login(user, pwd):
    if user in st.session_state.users and st.session_state.users[user] == pwd:
        st.session_state.logged_in = True
        st.session_state.show_login = False
    else:
        st.error("Invalid Credentials")

def register(user, pwd):
    if user not in st.session_state.users:
        st.session_state.users[user] = pwd
        st.session_state.show_register = False
        st.success("Registration Successful")
    else:
        st.error("User already exists")

# ------------------ HOME ------------------
if not st.session_state.logged_in:

    st.markdown("<h1>Spam Detection System</h1>", unsafe_allow_html=True)
    st.markdown("<p>Select an option to continue</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔐 Sign In"):
            st.session_state.show_login = True
            st.session_state.show_register = False

    with col2:
        if st.button("📝 Sign Up"):
            st.session_state.show_register = True
            st.session_state.show_login = False

    with col3:
        if st.button("👤 Guest"):
            st.session_state.logged_in = True

    # -------- SIGN IN --------
    if st.session_state.show_login:
        st.markdown("### 🔐 Sign In")
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            login(user, pwd)

    # -------- SIGN UP --------
    if st.session_state.show_register:
        st.markdown("### 📝 Sign Up")
        new_user = st.text_input("Create Username", key="reg_user")
        new_pwd = st.text_input("Create Password", type="password", key="reg_pass")

        if st.button("Register"):
            register(new_user, new_pwd)

# ------------------ MAIN APP ------------------
else:

    st.markdown("<h1>Spam Detection App</h1>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False

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

    st.markdown("### History")

    if st.session_state.history:
        for msg, res in st.session_state.history[::-1]:
            st.write(f"{res} → {msg[:40]}...")
