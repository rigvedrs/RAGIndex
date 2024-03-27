# Third-Party Libraries
import streamlit as st
from dotenv import load_dotenv

# Module Imports
from docqna.HTMLTemplates import css
from docqna.stcomp import initialize_session_state, file_processing, handle_user_input


# Load environment variables
load_dotenv(dotenv_path="../.env", verbose=True)


def main() -> None:
    """
    Main function to run the Streamlit application for Document Insight.

    The application offers a user-friendly interface to:
    1. Upload multiple PDF documents.
    2. Process these documents by converting PDFs to text, segmenting the text, and storing them in a Chroma Vector Database.
    3. Submit queries about the processed documents and get relevant insights.

    Features:
    - Customized page title and icon.
    - Utilizes session management to retain the state of processed documents.
    - A sidebar for document uploads with relevant feedback messages.
    - A main area for processing user queries regarding the uploaded documents.

    Note:
    The actual file processing and query functionalities are encapsulated in separate functions and modules for modularity and maintainability.
    """
    # Basic Page layout
    st.set_page_config(
        page_title="Document Insight", page_icon=":books:", layout="wide"
    )
    # Set our CSS
    st.write(css, unsafe_allow_html=True)

    # Initialize session-state
    initialize_session_state()

    # Set Title of the page
    st.title(body="Document Insight :books:")

    try:
        # Handle user's query (Placeholder)
        user_query = st.text_input(label="Enter your query about the documents:")
        # If user Question is not empty string then Get Reply from the BOT
        if user_query != "":
            handle_user_input(user_query)
    except Exception as e:
        st.error(f"Query Error: {e}")

    # The sidebar for the user to input the document
    with st.sidebar:
        # The message for the user
        st.subheader(body="Upload Your Documents")
        # The element that allows user to upload PDFs from the user
        files = st.file_uploader(
            label="Upload PDF documents for processing:",
            accept_multiple_files=True,
            type="pdf",
        )
        # The Button to press, the Files are uploaded
        # The condition to proceed is that both file and button should not return None
        if st.button(label="Analyze"):
            # If the session state contains that the file was processed
            if st.session_state.documents_processed:
                st.warning(
                    "You've already processed some documents. Uploading more will add to the existing data."
                )
            # if `files` list in not empty then proceed
            if files:
                # This function will processs the files i.e.
                # 1. Convert PDFs to text
                # 2. Split the text to Documents
                # 3. Push the Documents into Chroma Vector DB
                file_processing(files)


if __name__ == "__main__":
    # Run the Streamlit show
    main()
