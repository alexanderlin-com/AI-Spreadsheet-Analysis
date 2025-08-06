import openai
import streamlit as st

def initialize_client(api_key):
    """
    Initializes and returns the OpenAI client, ensuring no system proxies are used.

    Args:
        api_key (str): The user's OpenAI API key.

    Returns:
        An instance of the openai.OpenAI client if the key is valid, otherwise None.
    """
    try:
        # Create an HTTP client that explicitly ignores system proxy settings.
        # This is the core of the fix for the 'proxies' error.
        
        # Pass our custom, proxy-free HTTP client to the OpenAI client.
        client = openai.OpenAI(api_key=api_key, http_client=http_client)
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return None

def construct_prompt(df, user_question):
    """
    Constructs the detailed prompt to be sent to the AI, including the
    system message, data preview, and conversation history.

    Args:
        df (pd.DataFrame): The dataframe containing the user's data.
        user_question (str): The latest question from the user.

    Returns:
        A list of message dictionaries, formatted for the OpenAI API.
    """
    data_preview = df.head().to_string()
    column_names = ", ".join(map(str, df.columns))

    system_message = {
        "role": "system",
        "content": f"""
        You are a world-class data analyst AI. Your task is to help a user
        understand their uploaded spreadsheet.

        The data has the following columns: {column_names}.
        Here is a preview of the first 5 rows:
        ---
        {data_preview}
        ---
        
        Analyze the data based on the user's questions. Provide clear, concise,
        and helpful answers. When providing explanations, be direct and easy to
        understand.
        """
    }

    messages_for_api = [system_message]
    messages_for_api.extend(st.session_state.messages)

    return messages_for_api

def get_ai_response(client, messages):
    """
    Sends the prompt to the OpenAI API and gets a response.

    Args:
        client: The initialized OpenAI client instance.
        messages (list): The list of message dictionaries to send to the API.

    Returns:
        The content of the AI's response as a string, or an error message.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"An error occurred while communicating with the AI: {e}"
        st.error(error_message)
        return error_message
