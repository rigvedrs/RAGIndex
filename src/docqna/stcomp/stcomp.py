# Standard Libraries
from time import perf_counter
from typing import Any
import copy

# Third-Party Libraries
import streamlit as st

# Module Imports
from ..chat import get_conversation_engine
from ..pipeline import get_pipeline
from ..pdf_ingest import get_pdf_text, get_pdf_text_ocr, get_text_nodes
from ..HTMLTemplates import bot_template, user_template


# Initialising pipeline and embed model
pipeline = get_pipeline()['pipeline']
embed_model = get_pipeline()['embed_model']



def initialize_session_state():
    """
    Initialize or reset session states for Streamlit application.


    Notes:
    - Initializes the conversation chain, documents processed flag, and chat history in the session state.
    - It checks if the session state variable already exists before initializing to avoid overwriting.
    """
    if "conversation" not in st.session_state:
        st.session_state.conversation = get_conversation_engine(embed_model, pipeline.vector_store)
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


def file_processing(files: list[Any]) -> None:
    """
    Process uploaded PDF files: Extract text, segment them, and add them to the vector store.
 
    Args:
    - files (list[Any]): A list of uploaded PDF files to be processed.
 
    Notes:
    - The function provides user feedback using Streamlit's info and spinner functionalities.
    - It updates the session state to indicate that documents have been processed.
    - Passes PDFs for performing OCR on them if they dont contain any text.
    - Any exceptions raised during processing are caught and displayed as errors in Streamlit.
    """
    try:
        # While Everything is being processed run the spinner
        with st.spinner("Processing your PDF documents..."):
            copy_files = copy.deepcopy(files)
            # Initialise documents to store all the Documents in the list
            documents = []
            # Loop across every file that has been uploaded
            for i,file in enumerate(files):
                document = get_pdf_text(file)
                # Check if document contains an error
                # Fallback to OCR if extracting text from PDF fails
                if document.text == 'Error':
                    st.warning("Error extracting text from PDFs using the first method. Trying OCR...")
                    document = get_pdf_text_ocr(copy_files[i])
                
                documents.append(document)
            st.info(
                f"PDF processing completed."
            ) 
            # st.write(documents)
            
            # Initialise performance counter
            t0 = perf_counter()
            # Get text nodes
            nodes = get_text_nodes(documents, pipeline)
            t_delta = (perf_counter() - t0) / 60

            #  if Every thing moves smoothly Update session state
            if nodes is not None:
                st.info(
                    f"Data preparation complete in {t_delta:.2f} minutes. You can now initiate queries."
                )
                st.session_state.documents_processed = True
            else: 
                st.info(
                    "An Error occured. You can try passing the documents again..."
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")

def handle_user_input(user_query: str) -> None:
    """
    Process user input, retrieve relevant responses, and display them in Streamlit.

    Args:
    - user_query (str): The query or question input by the user.

    Notes:
    - The function retrieves a response using the conversation chain from the session state.
    - It updates the chat history in the session state.
    - Displays user input and bot responses using predefined HTML templates.
    """
    # Get response
    response = st.session_state.conversation.chat(user_query, tool_choice="query_engine_tool")

    # Create new session state Variable
    st.session_state.chat_history = st.session_state.conversation.chat_history

    # Loop Through Your Chats
    for idx, msg in enumerate(st.session_state.chat_history):
        # Output empty string if response is None (handling an exception)
        if msg.content is None:
            continue

        if msg.role.name=='ASSISTANT':
            # This is the response from the bot
            st.write(
                bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True
            )
        elif msg.role.name=='USER':
            # Adding styles to Chat Boxes and messages
            st.write(
                user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True
            )
        # Skipping messages from other role (TOOL)
        else:
            continue





