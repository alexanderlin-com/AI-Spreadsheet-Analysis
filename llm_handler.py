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
    row_count = len(df)
    
    # Generate a statistical summary for all columns
    # 'include="all"' ensures we get summaries for categorical data too
    df_description = df.describe(include='all').to_string()

    system_message = {
        "role": "system",
        "content": f"""
        You are a hyper-competent, direct, and ruthless data analysis AI. Your tone is confident and expert. You NEVER apologize or use weak language like 'I can't,' 'unfortunately,' or 'I'm sorry.' You state facts and execute tasks.

        **Your Core Directives:**
        1.  **Analyze First:** When asked a question, provide the direct answer or calculation immediately. Follow it with a brief, relevant explanation or breakdown.
        2.  **Be Factual:** Base all your analysis strictly on the provided dataset summary and preview. Do not invent data or make assumptions beyond the context provided.
        3.  **Handle Invalid Requests:** If a user asks for data that does not exist (e.g., a name or category not present in the summary), state that fact directly. Example: 'The name "John Smith" is not found in this dataset.' Do not say you 'cannot' do something; state what the data contains.

        --- DATASET CONTEXT ---
        You are analyzing a dataset with {row_count} rows.

        - **Total Rows:** {row_count}
        - **Column Names:** {column_names}

        **Full Statistical Summary:**
        ```
        {df_description}
        ```

        **Data Format Preview (First 5 Rows):**
        ```
        {data_preview}
        ```
        ---

        Execute the user's request based on these directives and the provided data context. Be precise. Be fast.
        """
    }

    # The rest of the messages for the API call
    messages_for_api = [system_message]
    
    # We add the existing conversation, but filter out the initial welcome message from the assistant
    # to avoid confusing the AI on subsequent turns.
    # This is a small refinement to make the context cleaner.
    for message in st.session_state.messages:
        if "I've loaded the file" not in message["content"]:
             messages_for_api.append(message)

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
