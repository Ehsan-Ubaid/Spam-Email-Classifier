import streamlit as st
import pickle

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "history" not in st.session_state:
    st.session_state.history = []
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}   # default user

# ------------------ FUNCTIONS ------------------
def predict_email(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "🚫 Spam" if pred == 1 else "✅ Not Spam"

def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        return True
    return False

def register(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = password
    return True

# ------------------ THEME / UI ------------------
st.set_page_config(page_title="Spam Detection", page_icon="📧", layout="centered")

st.title("📧 Spam Detection System")

# ------------------ LOGIN / REGISTER ------------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if menu == "Login":
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success("Login Successful")
            else:
                st.error("Invalid Credentials")

    elif menu == "Register":
        st.subheader("📝 Register")

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Register"):
            if register(new_user, new_pass):
                st.success("Registered Successfully")
            else:
                st.error("User already exists")

# ------------------ MAIN APP ------------------
else:

    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    st.subheader("📨 Enter Email Text")

    text = st.text_area("Type your message here...")

    # -------- File Upload --------
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text)

    # -------- Predict --------
    if st.button("Predict"):
        if text.strip() != "":
            result = predict_email(text)
            st.success(result)

            # Save history
            st.session_state.history.append((text, result))
        else:
            st.warning("Please enter some text")

    # -------- History --------
    st.subheader("📜 Prediction History")

    if st.session_state.history:
        for i, (msg, res) in enumerate(st.session_state.history[::-1]):
            st.write(f"{i+1}. {res} → {msg[:50]}...")
    else:
        st.write("No history yet")
