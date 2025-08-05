import streamlit as st

def render_sidebar(api_key_loaded):
    """
    Renders the sidebar of the application, including the API key status
    and the file uploader.

    Args:
        api_key_loaded (bool): A flag indicating if the API key was
                               successfully loaded from the environment.

    Returns:
        The uploaded file object if a file is uploaded by the user, otherwise None.
    """
    with st.sidebar:
        st.header("Configuration")

        # Display the status of the API key
        if not api_key_loaded:
            st.error("API Key not found. Please create a .env file with OPENAI_API_KEY='your_key'")
        else:
            st.success("✅ API Key loaded successfully!")

        st.markdown("---") # Visual separator

        # File uploader widget
        uploaded_file = st.file_uploader(
            "Upload your spreadsheet",
            type=["csv", "xlsx"],
            help="Upload a CSV or Excel file to start the analysis."
        )
        return uploaded_file


def render_chat_history():
    """
    Renders the chat history from the session state.

    It iterates through all messages stored in st.session_state.messages
    and displays them using the appropriate chat message role (user or assistant).
    """
    if not st.session_state.messages:
        # Display a welcome message if the chat is empty
        st.info("Upload a file and ask a question to get started!")

    for message in st.session_state.messages:
        # Use the 'with' syntax to create a chat message container
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

