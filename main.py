import streamlit as st
import os
# from dotenv import load_dotenv  <-- DELETE THIS LINE

# --- IMPORTS FROM OUR MODULES ---
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
    st.write("Your personal AI assistant for analyzing spreadsheets 6:03")

    # --- LOAD ENVIRONMENT VARIABLES ---
    # load_dotenv() <-- DELETE THIS LINE
    # On Streamlit Cloud, the secret is automatically set as an environment variable.
    # For local development, set the environment variable in your terminal.
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
    if prompt := st.chat_input("Ask a question about your data..."):
        if st.session_state.client is None:
            st.warning("Please set up your OpenAI API key.")
        elif st.session_state.dataframe is None:
            st.warning("Please upload a spreadsheet file first.")
        else:
            # Add user's message to history and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # This is the new execution flow
            with st.chat_message("assistant"):
                with st.spinner("AI is writing code..."):
                    # 1. Construct the prompt to ask the AI for code
                    messages = llm_handler.construct_prompt(st.session_state.dataframe, prompt)
                    
                    # 2. Get the code string back from the AI
                    ai_code_response = llm_handler.get_ai_response(st.session_state.client, messages)

                # (Optional but useful for us) Show the generated code
                with st.expander("View Generated Code"):
                    st.code(ai_code_response, language="python")

                with st.spinner("Executing code..."):
                    # 3. Execute the code using our new executor
                    final_result = code_executor.safe_execute_code(
                        code_string=ai_code_response,
                        df=st.session_state.dataframe
                    )

                # 4. Display the final, verified result
                st.markdown(final_result)
                
                # Add the actual result to the chat history
                st.session_state.messages.append({"role": "assistant", "content": final_result})


# --- SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    main()
