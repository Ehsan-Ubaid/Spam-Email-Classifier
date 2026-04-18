import streamlit as st
import pickle
import base64

# -------------------- LOAD MODEL --------------------
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf.pkl", "rb"))

# -------------------- BACKGROUND --------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}

    .card {{
        background: rgba(255,255,255,0.85);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }}

    .title {{
        text-align:center;
        color:white;
        font-size:40px;
        font-weight:bold;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("bg.jpg")

# -------------------- SESSION --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "users" not in st.session_state:
    st.session_state.users = {}

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- LOGIN --------------------
def login():
    st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    option = st.radio("", ["Sign In", "Sign Up", "Guest"])

    if option == "Sign In":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u in st.session_state.users and st.session_state.users[u] == p:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid login")

    elif option == "Sign Up":
        u = st.text_input("Create Username")
        p = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            st.session_state.users[u] = p
            st.success("Account created!")

    else:
        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- MAIN APP --------------------
def app():
    st.markdown(f'<div class="title">📧 Spam Detector</div>', unsafe_allow_html=True)
    st.write(f"Welcome **{st.session_state.username}**")

    # -------- TEXT INPUT --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    text = st.text_area("Enter Email Text", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- FILE UPLOAD --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload .txt Email", type=["txt"])

    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
        st.success("File loaded successfully")
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- BUTTONS --------
    col1, col2, col3 = st.columns(3)

    with col1:
        analyze = st.button("Analyze")

    with col2:
        clear = st.button("Clear")

    with col3:
        logout = st.button("Logout")

    # -------- ANALYSIS --------
    if analyze:
        if text.strip() == "":
            st.warning("Enter text first")
        else:
            vec = vectorizer.transform([text])
            pred = model.predict(vec)[0]

            result = "Spam" if pred == 1 else "Not Spam"

            if pred == 1:
                st.error("🚫 Spam Email")
            else:
                st.success("✅ Not Spam")

            # Save history
            st.session_state.history.append({
                "text": text[:50],
                "result": result
            })

    if clear:
        st.rerun()

    if logout:
        st.session_state.logged_in = False
        st.rerun()

    # -------- HISTORY --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🕘 History")

    if len(st.session_state.history) == 0:
        st.write("No history yet")
    else:
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.write(f"{i}. {item['text']} → **{item['result']}**")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- ROUTING --------------------
if st.session_state.logged_in:
    app()
else:
    login()
