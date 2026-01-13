
import streamlit as st
import google.genai as genai

st.title("Study Buddy Quiz Generator")

try:
    # Get the API key from the secrets
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # If the secret is not found, fall back to the text input
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
notes = st.text_area("Paste your study notes here:")
button = st.button("Generate Quiz")

if button:
    if not api_key:
        st.error("Please enter your API Key.")
    elif not notes:
        st.error("Please paste your study notes.")
    else:
        try:
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                api_key=api_key,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]
            )

            prompt = f"""
            You are a helpful study assistant. Your task is to generate a multiple-choice quiz based on the provided study notes.

            **Instructions:**
            1.  Create a 3-question multiple-choice quiz from the notes.
            2.  Each question should have 4 options (A, B, C, D).
            3.  Provide the correct answer key at the very end, clearly separated from the questions.

            **Study Notes:**
            {notes}
            """

            response = model.generate_content(prompt)

            st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
