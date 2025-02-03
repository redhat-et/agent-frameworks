import streamlit as st
import requests

# FastAPI Endpoint
API_URL = "http://localhost:8000/process/"

# Streamlit UI
st.title("parasol demo")

st.write("Enter your details and check your approval status.")

# User Input Box
user_input = st.text_area("Enter your details:", placeholder="I have 3 years of driving experience, want to apply for driving insurance")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text before submitting.")
    else:
        # Send data to FastAPI
        with st.spinner("Processing..."):
            response = requests.post(API_URL, json={"text": user_input})
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Result:")
                # st.write(result["output"])
                if "steps" in result:
                    st.subheader("🧠 Thinking Process")
                    for step in result["steps"]:
                        st.write(f"👉 {step}")

                st.subheader("✅ Final Decision")
                st.success(result["final_answer"])
            else:
                st.error(f"❌ Error: {response.text}")

st.write("👨‍💻 Powered by bee-agent-framework & FastAPI & Streamlit UI")
