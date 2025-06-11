# Standard Libraries
from time import perf_counter
from typing import Any
import copy
import os
import hashlib
import time
import subprocess
import io
import toml
from pathlib import Path

# Third-Party Libraries
import streamlit as st
import nltk
from docx import Document
from fpdf import FPDF
try:
    nltk.download('punkt_tab')
except:
    # Fallback to older punkt if punkt_tab is not available
    nltk.download('punkt')

# Module Imports
from ..chat import get_conversation_engine
from ..pipeline import get_pipeline
from ..pdf_ingest import get_pdf_text, get_pdf_text_ocr, get_text_nodes
from ..HTMLTemplates import bot_template, user_template
from ..display_image import show_image
from ..context import get_context
from nltk.tokenize import sent_tokenize

# Testing
import re

# Initialising pipeline and embed model
pipeline = get_pipeline()['pipeline']
embed_model = get_pipeline()['embed_model']


# Get the directory of the current file and construct path to config.toml
current_dir = Path(__file__).parent
config_path = current_dir / '..' / '..' / '..' / 'config.toml'
with open(config_path, 'r') as f:
    params = toml.load(f)
# Create the directories if they dont exist
data_path = params['paths']['data_path']
os.makedirs(data_path, exist_ok=True)
dir_path = data_path



class CustomUploadedFile(io.BytesIO):
    def __init__(self, data, name):
        super().__init__(data)
        self.name = name

    def __repr__(self):
        return f"CustomUploadedFile(name={self.name}, size={len(self.getvalue())})"
    


def convert_docx_to_pdf(input_file, output_file):
    subprocess.run(["pandoc", "-o", output_file, input_file])



def split_into_sentences(text):
    sentences = sent_tokenize(text)
    return sentences


    



# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    try:
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
        
        # Save the file to the specified directory
        file_path = os.path.join(dir_path, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f'Error saving file: {e}')





def txt_to_pdf(txt_file_path, pdf_file_path):
    # Create a new PDF object
    pdf = FPDF()
    # Open the text file for reading
    with open(txt_file_path, 'r', encoding='latin-1') as txt_file:
        # Get the content of the text file
        txt_content = txt_file.read()
    # Split the text content into lines
    lines = txt_content.splitlines()
    # Add a new page to the PDF
    pdf.add_page()
    # Set the font and font size
    pdf.set_font('Arial', size=12)
    # Loop through the lines and add them to the PDF
    for line in lines:
        pdf.cell(w=200, h=10, txt=line, ln=1, align='L') # type: ignore
    # Save the PDF
    pdf.output(pdf_file_path)





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
        with st.spinner("Processing your documents..."):
            copy_files = copy.deepcopy(files)
            # Initialise documents to store all the Documents in the list
            documents = []


            

            # Loop across every file that has been uploaded
            for i,file in enumerate(files):
                if file.name.endswith(".pdf") :
                    save_uploaded_file(file)
                    document_list = get_pdf_text(file)
                    # Check if document contains an error
                    # Fallback to OCR if extracting text from PDF fails
                    if document_list[0].text == 'Error':
                        st.warning("Error extracting text from PDFs using the first method. Trying OCR...")
                        document_list = get_pdf_text_ocr(copy_files[i])
                    
                    # documents.extend(document_list)
                
                elif file.name.endswith(".docx"):
                    docx_file = file
                    docx_path = os.path.join(data_path, docx_file.name)
                    pdf_path = os.path.join(data_path, os.path.splitext(docx_file.name)[0] + ".pdf")
                    
                    # Save the docx file
                    with open(docx_path, "wb") as f:
                        f.write(docx_file.read())
                        # Convert the docx file to pdf
                        convert_docx_to_pdf(docx_path, pdf_path)

                        # Read the PDF file
                        if os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                            uploaded_file = CustomUploadedFile(pdf_bytes, os.path.splitext(docx_file.name)[0] + ".pdf")
                            document_list = get_pdf_text(uploaded_file)  
                        else:
                            st.write(f"PDF file {os.path.basename(pdf_path)} not found.")


                                
                elif file.name.endswith(".txt"):
                    txt_file = file
                    txt_path = os.path.join(data_path, txt_file.name)
                    pdf_path = os.path.join(data_path, os.path.splitext(txt_file.name)[0] + ".pdf")
                    # Save the txt file
                    with open(txt_path, "wb") as f:
                        f.write(txt_file.read())
                    # Convert the txt file to pdf
                    txt_to_pdf(txt_path, pdf_path)
                    # Read the PDF file
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        uploaded_file = CustomUploadedFile(pdf_bytes, os.path.splitext(txt_file.name)[0] + ".pdf")
                        document_list = get_pdf_text(uploaded_file)
                    else:
                        st.write(f"PDF file {os.path.basename(pdf_path)} not found.")

                # Append all the extracted pages in main document list
                documents.extend(document_list)
            
            st.info(
                f"Document processing completed."
            ) 
            
            # Initialise performance counter time
            t0 = perf_counter()
            # Get text nodes
            nodes = get_text_nodes(documents, pipeline)
            t_delta = (perf_counter() - t0) / 60

            #  if Every thing moves smoothly Update session state
            if nodes is not None:
                st.success(
                    f"Data preparation complete in {t_delta:.2f} minutes. You can now initiate queries."
                )
                st.session_state.documents_processed = True
            else: 
                st.info(
                    "An Error occured. You can try passing the documents again..."
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")




def get_page_num(text: str):
    # Regular expression pattern to find page number references
    pattern = r'PAGE_NUM=(\d+)'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # Use a set to store unique page numbers
    unique_page_numbers = set()

    # Extract the numbers from the matches and store them in a set to ensure uniqueness
    for match in matches:
        unique_page_numbers.add(int(match))

    return list(unique_page_numbers)




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
    for idx, msg in enumerate(st.session_state.chat_history):
        # Output empty string if response is None (handling an exception)
        if msg.content is None: 
            continue

        if msg.role.name == 'ASSISTANT':
            # Split the bot's response into sentences
            bot_response = msg.content
            bot_sentences = split_into_sentences(bot_response)
            # Concatenate the first two sentences into a single response
            if len(bot_sentences) > 2:
                truncated_response = ' '.join(bot_sentences[:2])
                st.write(
                    bot_template.replace("{{MSG}}", truncated_response), unsafe_allow_html=True
                )  
                with st.expander(label = "More Options",expanded = False):
                    tab1 , tab2, tab3 = st.tabs(["Know More","Get Full Context","View Page"])
                    with tab1:
                        # Display the entire response
                            st.write(
                                bot_template.replace("{{MSG}}", bot_response), unsafe_allow_html=True
                            )
                    with tab2:
                        # Initialize empty lists to store file names and page numbers
                        file_names = []
                        # Iterate through response.source_nodes
                        for node in response.source_nodes:
                            # Append file name and page number to respective lists
                            file_names.append(node.metadata['source'])
                        # Use set to remove duplicates
                        unique_file_names = list(set(file_names))

                        # Display unique file names and page numbers
                        st.write(f"#### The answer generated by Document Insight is from below file")
                        st.write(f"File Name: {unique_file_names[0]}")

                        # Display additional context only once
                        if len(response.source_nodes) > 0:
                            st.write("#### Exact Paragraph from where answer is derived: ")
                            node = response.source_nodes[0]  # Only consider the first node
                            st.markdown(get_context(node.text, bot_response),unsafe_allow_html=True)

                    with tab3:
                        for node_idx, node in enumerate(response.source_nodes):
                            path = data_path+node.metadata['source']
                            print(path)
                            # page_num = int(node.metadata['page_num'])-1
                            page_nums = get_page_num(node.text)
                            if page_nums is []:
                                st.error('NO PAGE NUM FOUND')
                            for page_idx, page_num in enumerate(page_nums):
                                st.write('PAGE_NUM found:' + str(page_num))
                                images,image_path = show_image(path,page_num)
                                st.image(images, caption=f"Page {page_num}", use_column_width=True)
                                with open(image_path, "rb") as file:
                                    key = hashlib.sha256((image_path + str(idx) + str(node_idx) + str(page_idx) + str(page_num) + "_tab3_long" + user_query).encode()).hexdigest() 
                                    st.download_button(
                                        label="Download Page⬇️",
                                        data=file,
                                        file_name=image_path,
                                        mime="image/png",
                                        key=key
                                    )
                    break
            else:
                st.write(
                    bot_template.replace("{{MSG}}", bot_response), unsafe_allow_html=True
                )
                with st.expander(label = "More Options",expanded = False):
                    tab1,tab2= st.tabs(["Get Full Context","View Page"])
                    with tab1:
                        # Initialize empty lists to store file names and page numbers
                        file_names = []
                        # Iterate through response.source_nodes
                        for node in response.source_nodes:
                            # Append file name and page number to respective lists
                            file_names.append(node.metadata['source'])
                        # Use set to remove duplicates
                        unique_file_names = list(set(file_names))

                        # Display unique file names and page numbers
                        st.write(f"#### The answer generated by Document Insight is from below file")
                        st.write(f"File Name: {unique_file_names[0]}")

                        # Display additional context only once
                        if len(response.source_nodes) > 0:
                            st.write("#### Exact Paragraph from where answer is derived: ")
                            node = response.source_nodes[0]  # Only consider the first node
                            st.markdown(get_context(node.text, bot_response),unsafe_allow_html=True)

                    with tab2:
                        for node_idx, node in enumerate(response.source_nodes):
                            path = data_path+node.metadata['source']
                            # page_num = int(node.metadata['page_num'])-1
                            page_nums = get_page_num(node.text)
                            if page_nums is []:
                                st.error('NO PAGE NUM FOUND')
                            for page_idx, page_num in enumerate(page_nums):
                                st.write('PAGE_NUM found:' + str(page_num))
                                images,image_path = show_image(path,page_num)
                                st.image(images, caption=f"Page {page_num}", use_column_width=True)
                                with open(image_path, "rb") as file:
                                    key = hashlib.sha256((image_path + str(idx) + str(node_idx) + str(page_idx) + str(page_num) + "_tab2_short" + user_query).encode()).hexdigest() 
                                    st.download_button(
                                        label="Download Page⬇️",
                                        data=file,
                                        file_name=image_path,
                                        mime="image/png",
                                        key=key
                                    )               
        elif msg.role.name == 'USER':
            # Adding styles to Chat Boxes and messages
            st.write(
                user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True
            )
        # Skipping messages from other roles (TOOL)
        else:
            continue