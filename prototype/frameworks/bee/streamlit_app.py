import requests
import streamlit as st

st.title("AI Risk Scoring")

user_input = st.text_area("Enter text for evaluation:")
if st.button("Evaluate"):
    response = requests.post("http://localhost:3000/evaluate", json={"text": user_input})

    if response.status_code == 200:
        result = response.json()

        # Display the raw thinking process exactly as the console does
        st.write("### Thinking Process:")
        for step in result["thinking_process"]:
            st.write(step)  # No extra formatting, just raw output

        # Display the final result exactly like in the console
        st.write("### Final Decision:")
        st.write(result["result"])  # No extra formatting
    else:
        st.error("Error: Could not get a valid response from the server.")
