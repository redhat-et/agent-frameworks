import streamlit as st
import requests

# Streamlit interface
def run_chat_interface():
    st.title("Insurance Agent")
    st.write("Welcome! Chat with the agent to calculate your insurance score and eligibility.")

    # Text input for user query
    user_input = st.text_area("Describe your driving history and insurance details:", 
                              height=150, placeholder="Tell the agent about your driving habits...")

    # Check if the submit button is pressed
    if not st.button("Submit"):
        return

    # Validate if there is input from the user
    if not user_input:
        st.write("Please enter some information about your driving history.")
        return

    # Call FastAPI backend with the user input
    url = "http://127.0.0.1:8000/process_input/"
    response = requests.post(url, json={"text": user_input})

    # Handle the response from the backend
    if response.status_code != 200:
        st.write("There was an error processing the request.")
        return

    # If the response is successful, display the result
    result = response.json()
    st.write(f"Generated Insurance Score: {result['response']}")
    st.write(f"Approval Status: {result['approval_status']}")

if __name__ == "__main__":
    run_chat_interface()
