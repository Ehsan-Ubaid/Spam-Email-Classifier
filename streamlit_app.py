import streamlit as st
import pickle

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Spam Detection", page_icon="📧", layout="centered")

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

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
def predict_email(text):
    vector = tfidf.transform([text])
    pred = model.predict(vector)[0]
    return "🚫 Spam" if pred == 1 else "✅ Not Spam"

def login(user, pwd):
    if user in st.session_state.users and st.session_state.users[user] == pwd:
        st.session_state.logged_in = True
        st.session_state.show_login = False

def register(user, pwd):
    if user not in st.session_state.users:
        st.session_state.users[user] = pwd
        st.session_state.show_register = False
        st.success("Registered Successfully!")
    else:
        st.error("User already exists")

# ------------------ HOME SCREEN ------------------
if not st.session_state.logged_in:

    st.title("📧 Spam Detection System")
    st.write("### Welcome! Choose an option")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔐 Login"):
            st.session_state.show_login = True

    with col2:
        if st.button("📝 Register"):
            st.session_state.show_register = True

    with col3:
        if st.button("👤 Continue as Guest"):
            st.session_state.logged_in = True

    # -------- Login Popup --------
    if st.session_state.show_login:
        with st.container():
            st.subheader("🔐 Login")
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")

            if st.button("Submit Login"):
                login(user, pwd)

    # -------- Register Popup --------
    if st.session_state.show_register:
        with st.container():
            st.subheader("📝 Register")
            new_user = st.text_input("Create Username")
            new_pwd = st.text_input("Create Password", type="password")

            if st.button("Submit Register"):
                register(new_user, new_pwd)

# ------------------ MAIN APP ------------------
else:

    st.title("📨 Spam Detection App")

    if st.button("Logout"):
        st.session_state.logged_in = False

    text = st.text_area("Enter your email message:")

    # File upload
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text)

    # Prediction
    if st.button("Predict"):
        if text.strip():
            result = predict_email(text)
            st.success(result)

            st.session_state.history.append((text, result))
        else:
            st.warning("Enter text first")

    # History
    st.subheader("📜 History")

    if st.session_state.history:
        for msg, res in st.session_state.history[::-1]:
            st.write(f"{res} → {msg[:40]}...")
    else:
        st.write("No history yet")
