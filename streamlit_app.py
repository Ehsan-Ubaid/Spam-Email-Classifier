import streamlit as st
import pickle

st.set_page_config(page_title="Spam Detection", layout="wide")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("spam_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Disable scrolling */
html, body, [class*="css"] {
    overflow: hidden;
}

/* Full screen background */
.stApp {
    background: linear-gradient(rgba(102,126,234,0.7), rgba(118,75,162,0.7)),
                url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    background-position: center;
}

/* Center everything */
.center {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* Title */
.title {
    color: white;
    font-size: 50px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    color: white;
    margin-bottom: 30px;
}

/* Buttons */
.stButton>button {
    width: 250px;
    margin: 8px;
    border-radius: 25px;
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    color: white;
    font-weight: bold;
    border: none;
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

# ---------------- LANDING SCREEN ----------------
if not st.session_state.logged_in:

    st.markdown('<div class="center">', unsafe_allow_html=True)

    st.markdown('<div class="title">Spam Detection System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Welcome</div>', unsafe_allow_html=True)

    # -------- SIGN IN --------
    if st.session_state.mode == "signin":

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if user in st.session_state.users and st.session_state.users[user] == pwd:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.rerun()

        if st.button("Go to Sign Up"):
            st.session_state.mode = "signup"
            st.rerun()

    # -------- SIGN UP --------
    else:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if pwd == confirm:
                st.session_state.users[user] = pwd
                st.success("Account created")
                st.session_state.mode = "signin"
                st.rerun()
            else:
                st.error("Passwords do not match")

        if st.button("Go to Sign In"):
            st.session_state.mode = "signin"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    # Enable scrolling again for main app
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)

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
