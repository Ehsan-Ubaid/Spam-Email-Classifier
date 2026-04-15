import streamlit as st
import pickle

# Load model
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf.pkl", "rb"))

# Page config
st.set_page_config(page_title="Spam Detector", page_icon="📧", layout="wide")

# Sidebar
st.sidebar.title("📌 About")
st.sidebar.write("Spam Email Classifier using Machine Learning")
st.sidebar.info("Built with Streamlit")

# Title
st.title("🚀 Spam Email Detector")
st.markdown("Detect whether an email is spam or not")

# Layout
col1, col2 = st.columns(2)

with col1:
    email_text = st.text_area("📩 Enter Email", height=200)

    analyze = st.button("Analyze 🔍")
    clear = st.button("Clear 🧹")

with col2:
    st.subheader("📊 Result")

    if analyze:
        if email_text.strip() == "":
            st.warning("⚠️ Please enter email text")
        else:
            transformed = vectorizer.transform([email_text])
            prediction = model.predict(transformed)[0]

            if prediction == 1:
                st.error("🚫 Spam Email Detected")
            else:
                st.success("✅ Safe Email")

    if clear:
        st.rerun()