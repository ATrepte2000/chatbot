import streamlit as st
from openai import OpenAI


# Titel und Begrüßung mit Smileys
st.title("Rflect - Dein Reflektionsbegleiter 📝")
st.write("👋 **Hallo!** Ich bin der Rflect-Chatbot und unterstütze dich beim Reflektieren.")

# Farbschema und Stil anpassen mit Pastelltönen
st.markdown(
    """
    <style>
    /* Gesamt-Hintergrundfarbe */
    .stApp {
        background-color: #F5F5F5; /* Sanftes Grau-Pastell */
        font-family: 'Helvetica', sans-serif;
    }
    /* Titelstil */
    h1 {
        color: #6A5ACD; /* Pastell-Lavendel */
    }
    /* Anpassung von Text und Links */
    .stMarkdown {
        color: #4B0082; /* Indigoblau */
    }
    a {
        color: #FF69B4; /* Sanftes Pink */
    }
    /* Eingabefelder */
    input {
        background-color: #E6E6FA; /* Lavendel */
        color: #4B0082;
        border: 1px solid #D8BFD8; /* Thistle */
    }
    /* Buttons */
    button {
        background-color: #DDA0DD; /* Pflaume */
        color: #FFFFFF;
        border: None;
        border-radius: 10px;
        padding: 0.5em 1em;
    }
    /* Scrollbar anpassen */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #D8BFD8;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Weiterer Text mit Smileys
st.write("🌟 **Lass uns gemeinsam deine Gedanken erkunden!**")
st.write("💡 **Tipp:** Sei ehrlich zu dir selbst, um das Beste aus der Reflexion zu ziehen.")


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
