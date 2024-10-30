import streamlit as st
from PIL import Image
from openai import OpenAI

# Lade das Logo
logo = Image.open("logo.png")
st.image(logo, width=100)  # Passe die Breite nach Wunsch an


# Show title and description.
st.title("Rflect - Chatbot")
st.write("👋 Hallo! Ich bin der Rflect-Chatbot. Ich bin hier, um dich beim Reflektieren zu unterstützen.")

#Colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f3f4f6;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput, .stButton {
        color: #1e3a8a;
        background-color: #e0e7ff;
    }
    h1 {
        color: #1e40af;
    }
    </style>
    """, unsafe_allow_html=True
)


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
