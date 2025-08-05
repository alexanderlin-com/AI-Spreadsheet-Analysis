import streamlit as st
import os
from dotenv import load_dotenv

# --- IMPORTS FROM OUR MODULES ---
# All our custom modules are now being used.
import ui_components
import file_handler
import llm_handler

def main():
    """
    The main function that orchestrates the entire application.
    """
    # --- PAGE CONFIGURATION ---
    st.set_page_config(
        page_title="DataChat AI",
        page_icon="📊",
        layout="centered"
    )

    st.title("📊 DataChat AI")
    st.write("Your personal AI assistant for analyzing spreadsheets.")

    # --- LOAD ENVIRONMENT VARIABLES ---
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # --- INITIALIZE SESSION STATE ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "dataframe" not in st.session_state:
        st.session_state.dataframe = None
    if "client" not in st.session_state:
        st.session_state.client = None
    if "current_file_name" not in st.session_state:
        st.session_state.current_file_name = None

    # --- INITIALIZE AI CLIENT ---
    # We initialize the client only once, if the key is available and client is not set.
    if api_key and st.session_state.client is None:
        st.session_state.client = llm_handler.initialize_client(api_key)

    # --- RENDER THE UI ---
    uploaded_file = ui_components.render_sidebar(api_key_loaded=(st.session_state.client is not None))

    # --- FILE HANDLING LOGIC ---
    if uploaded_file:
        if uploaded_file.name != st.session_state.current_file_name:
            st.session_state.current_file_name = uploaded_file.name
            with st.spinner("Parsing spreadsheet..."):
                df = file_handler.parse_spreadsheet(uploaded_file)
                if df is not None:
                    st.session_state.dataframe = df
                    st.session_state.messages = []
                    st.sidebar.success(f"File '{uploaded_file.name}' loaded!")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I've loaded the file '{uploaded_file.name}'. What would you like to know?"
                    })
                else:
                    st.session_state.dataframe = None
                    st.session_state.current_file_name = None

    # --- RENDER CHAT HISTORY ---
    ui_components.render_chat_history()

    # --- MAIN CHAT LOGIC ---
    # This is the primary interaction loop.
    if prompt := st.chat_input("Ask a question about your data..."):
        # First, check for prerequisites
        if st.session_state.client is None:
            st.warning("Please ensure your API key is set up correctly in your .env file.")
        elif st.session_state.dataframe is None:
            st.warning("Please upload a spreadsheet file first.")
        else:
            # Add user's message to history and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get the AI's response
            with st.chat_message("assistant"):
                with st.spinner("AI is analyzing..."):
                    # Construct the full prompt for the AI
                    messages_for_api = llm_handler.construct_prompt(st.session_state.dataframe, prompt)
                    # Get the response from the AI
                    ai_response = llm_handler.get_ai_response(st.session_state.client, messages_for_api)
                    
                    st.markdown(ai_response)
                    # Add AI's response to the chat history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})


# --- SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    main()
