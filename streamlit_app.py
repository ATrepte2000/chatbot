import streamlit as st
from PIL import Image



# Titel und Begrüßung mit Smileys
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>Rflect - Dein Reflektionsbegleiter 📝</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #708090;'>👋 Hallo! Ich bin der Rflect-Chatbot und freue mich darauf, dich beim Reflektieren zu unterstützen!</h3>", unsafe_allow_html=True)

# Farbschema und Stil anpassen mit Pastelltönen und variierenden Schriftarten
st.markdown(
    """
    <style>
    /* Gesamt-Hintergrundfarbe */
    .stApp {
        background-color: #FFFAF0; /* Floral White */
        font-family: 'Georgia', serif;
    }
    /* Titelstil */
    h1 {
        color: #6A5ACD; /* Pastell-Lavendel */
        font-family: 'Brush Script MT', cursive;
    }
    /* Untertitelstil */
    h3 {
        color: #708090; /* Slate Gray */
        font-family: 'Comic Sans MS', cursive;
    }
    /* Anpassung von Text und Links */
    .stMarkdown, .stTextInput, .stButton {
        color: #4B0082; /* Indigo */
        font-family: 'Arial', sans-serif;
    }
    /* Eingabefelder */
    input {
        background-color: #E6E6FA; /* Lavender */
        color: #4B0082;
        border: 1px solid #D8BFD8; /* Thistle */
        border-radius: 10px;
        padding: 10px;
    }
    /* Buttons */
    button {
        background-color: #FFDAB9; /* Peach Puff */
        color: #4B0082;
        border: None;
        border-radius: 10px;
        padding: 0.5em 1em;
        font-size: 16px;
    }
    /* Hover-Effekt für Buttons */
    button:hover {
        background-color: #FFE4E1; /* Misty Rose */
        cursor: pointer;
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

# Weitere freundliche Nachrichten mit Smileys
st.write("🌟 **Lass uns gemeinsam deine Gedanken erkunden und neue Erkenntnisse gewinnen!**")
st.write("💡 **Tipp:** Offenheit und Ehrlichkeit sind der Schlüssel zu einer tiefgehenden Reflexion. Ich bin gespannt auf deine Ideen! 😊")



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
