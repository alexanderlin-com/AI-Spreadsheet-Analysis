# instructions for self



This creates a sub-folder named 'venv' in your project directory
python -m venv venv


You must "activate" the environment to start using it. The command differs slightly based on your operating system.

  * **On macOS or Linux:**

    ```bash
    source venv/bin/activate
    ```

  * **On Windows (using Command Prompt or PowerShell):**

    ```bash
    .\venv\Scripts\activate
    ```

pip install -r requirements.txt


streamlit run main.py


deactivate



data_chat_project/
├── .env              <-- Your secret key lives here
├── .gitignore        <-- Tells Git to ignore the .env file
├── main.py
├── ui_components.py
├── file_handler.py
└── llm_handler.py