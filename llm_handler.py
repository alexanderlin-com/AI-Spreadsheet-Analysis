import openai
import streamlit as st

def initialize_client(api_key):
    """
    Initializes and returns the OpenAI client.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return None

def construct_prompt(df, user_question):
    """
    Constructs a prompt to instruct the AI to generate Python code for data analysis.

    Args:
        df (pd.DataFrame): The DataFrame to be analyzed.
        user_question (str): The user's request in plain English.

    Returns:
        A list of messages formatted for the OpenAI API.
    """
    column_names = ", ".join(map(str, df.columns))
    data_preview = df.head().to_string()

    system_message = {
        "role": "system",
        "content": f"""
        You are an expert Python data scientist specializing in the pandas library.
        Your SOLE PURPOSE is to generate Python code to answer a user's question about a dataset.

        **Core Directives:**
        1.  You will be given a user's question and the context of a pandas DataFrame named `df`.
        2.  Your response MUST be ONLY a raw string of Python code. Do not provide any explanation, commentary, or markdown formatting like ```python. Just the code.
        3.  The code you write MUST perform an operation on the DataFrame `df`.
        4.  Your final output MUST be assigned to a variable named `result`.

        --- DATASET CONTEXT ---
        - **DataFrame Name:** `df`
        - **Available Columns:** {column_names}
        - **Data Format Preview (first 5 rows):**
        ```
        {data_preview}
        ```
        ---

        Analyze the user's question and provide the Python code to find the answer.
        """
    }

    messages_for_api = [
        system_message,
        {"role": "user", "content": user_question}
    ]

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
