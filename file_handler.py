import pandas as pd
import streamlit as st

def parse_spreadsheet(uploaded_file):
    """
    Parses an uploaded spreadsheet file (CSV or Excel) into a pandas DataFrame.

    This function checks the file extension to use the correct pandas reading
    function. It includes error handling to gracefully manage issues with
    file parsing, such as incorrect file formats or corrupted data.

    Args:
        uploaded_file: The file-like object uploaded via Streamlit's
                       file_uploader. This object has attributes like 'name'.

    Returns:
        A pandas DataFrame containing the data from the spreadsheet if parsing
        is successful.
        Returns None if the file is not of a supported type or if an error
        occurs during parsing.
    """
    try:
        # Check the file name to determine the file type
        if uploaded_file.name.endswith('.csv'):
            # For CSV files, use read_csv
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            # For modern Excel files, use read_excel
            df = pd.read_excel(uploaded_file)
        else:
            # If the file type is not supported, inform the user and return None
            st.error("Unsupported file format. Please upload a CSV or XLSX file.")
            return None
        
        return df

    except Exception as e:
        # If any other error occurs during parsing (e.g., corrupted file)
        # show an error message to the user and return None.
        st.error(f"Error reading or parsing file: {e}")
        return None

