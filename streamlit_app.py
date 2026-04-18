import streamlit as st
import pickle

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Spam Detection", layout="centered")

# ------------------ CUSTOM BACKGROUND + STYLING ------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: #000000 !important;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }

    textarea, input {
        background-color: #ffffff !important;
        color: black !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ------------------ SESSION STATE ------------------
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
    return "Spam" if pred == 1 else "Not Spam"

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

# ------------------ HOME SCREEN ------------------
if not st.session_state.logged_in:

    st.title("Spam Detection System")
    st.write("Welcome. Choose an option below")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Sign In"):
            st.session_state.show_login = True
            st.session_state.show_register = False

    with col2:
        if st.button("Sign Up"):
            st.session_state.show_register = True
            st.session_state.show_login = False

    with col3:
        if st.button("Continue as Guest"):
            st.session_state.logged_in = True

    # -------- SIGN IN --------
    if st.session_state.show_login:
        st.markdown("---")
        st.subheader("Sign In")

        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pass")

        if st.button("Submit Sign In"):
            login(user, pwd)

    # -------- SIGN UP --------
    if st.session_state.show_register:
        st.markdown("---")
        st.subheader("Sign Up")

        new_user = st.text_input("Create Username", key="reg_user")
        new_pwd = st.text_input("Create Password", type="password", key="reg_pass")

        if st.button("Submit Sign Up"):
            register(new_user, new_pwd)

# ------------------ MAIN APP ------------------
else:

    st.title("Spam Detection App")

    if st.button("Logout"):
        st.session_state.logged_in = False

    st.subheader("Enter Message")
    text = st.text_area("Type your message here...")

    # -------- FILE UPLOAD --------
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text)

    # -------- PREDICT --------
    if st.button("Predict"):
        if text.strip():
            result = predict_message(text)
            st.success(result)
            st.session_state.history.append((text, result))
        else:
            st.warning("Please enter some text")

    # -------- HISTORY --------
    st.subheader("Prediction History")

    if st.session_state.history:
        for i, (msg, res) in enumerate(st.session_state.history[::-1]):
            st.write(f"{i+1}. {res} → {msg[:50]}...")
    else:
        st.write("No history yet")
