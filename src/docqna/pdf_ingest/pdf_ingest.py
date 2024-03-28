from typing import Any,List
from PyPDF2 import PdfReader

from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import tempfile

# Llama Index
from llama_index.core import Document
from llama_index.core.schema import TextNode
from llama_index.core.ingestion import (
    IngestionPipeline
)

# For tracking error
from torch.cuda import OutOfMemoryError

# temp import 
import streamlit as st




def get_pdf_text(pdf_file: Any) -> list[Document]:
    """
    Extract text content from the PDF file and convert it to Llama Index Document.     
 
    Args:
    - pdf_file (Any): A PDF file object to be processed.
 
    Returns:
    - list[Document]: A list of LLama Index Documents containing the extracted text content and metadata. 
                If the document needs OCR, returns the document with an error message
 
    Notes:
    - Each Document object contains the text content of a PDF and a metadata dictionary with the source PDF's name.
    """

    # Get Data from each PDF and convert it To Llama Index Document
    pdf = pdf_file
    # Get File name
    pdf_name: str = pdf.name
    # Get Contents in the PDF as text
    pdf_content: str = "\n\n".join(
        page_content.extract_text() for page_content in PdfReader(pdf).pages
    )
    # Convert to Llama Index Doc Object
    pdf_doc = Document(text=pdf_content, id_ = pdf_name,  metadata={"source": pdf_name})

    # Return contents in PDFs as a list of Llama Index Documents
    print(pdf_doc)
    page_content = pdf_doc.text.strip()
    if page_content == '\n' * len(page_content):
        return Document(text='Error')
    else:
      return pdf_doc
    


def get_pdf_text_ocr(pdf_file: Any) -> List[Document]:
    """
    Extract text content from a list of PDF files by performing OCR and 
    convert them to Llama Index Documents.

    Args:
    - pdf_file (Any): A PDF file object to be processed.
 
    Returns:
    - Document: A LLama Index Document containing the extracted text content and metadata. 
                
 
    Notes:
    - Each Document object contains the text content of a PDF and a metadata dictionary with the source PDF's name.
    """
    pdf_filename = pdf_file.name 
    
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name

    # Converting PDF to images
        images = convert_from_path(pdf_path, 500)

    # Initialize empty string to append the text for each page
    full_text = ''

    # Iterate over the pages and extract the text using pytesseract
    for i, image in enumerate(images):
        image_path = f'{os.path.splitext(pdf_path)[0]}_page_{i}.png'
        image.save(image_path, 'PNG')
        
        # Perform OCR on the image
        custom_config = ' '
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng', config=custom_config)
        full_text += text

        
    # Create a Document object for full text
    pdf_doc = Document(text=full_text, id_ = pdf_filename, metadata={"source": pdf_filename})
    
    print(pdf_doc)
    
    # Clean up the temporary file
    os.unlink(pdf_path)

    return pdf_doc



def get_text_nodes(documents: list[Document],
                   pipeline: IngestionPipeline) -> list[TextNode]:
    """
    Run the full pipeline on the documents to generate TextNodes.
    If there is an error while running the pipeline, prevent the pipeline from tracking the document.

    Args:
    - documents (list[Document]): A list of Llama Index Documents to be split into nodes.
    - embed_model (HuggingFaceEmbedding): An embedding model from Hugging Face to generate embeddings of the data 
    - pipeline (IngestionPipeline): A Llama Index IngestionPipeline class that contains the information for document tracking
                                    vectore storage, and Sentence splitting parameters.

    Returns:
    - list[TextNode]: A list of TextNodes(Llama Index) where each node is a chunk of the extracted text that will be passed as context
                      or returns None if there was an error 

                      
    """
    

    # Run the pipeline on the documents and prevent the pipeline from 
    # tracking the documents that were not succesfully ingested if an error occured
    try:
        nodes = pipeline.run(documents=documents)
        st.info(
            f"PDF processing completed. Number of Nodes Ingested: {len(nodes):,}"
        )

    except (Exception, OutOfMemoryError) as e:
        # Delete all the unprocessed document ids from the docstore
        for document in documents:
            pipeline.docstore.delete_document(document.id_, raise_error=False)

        # Set nodes to None as an Error flag
        nodes = None
        st.error(
            f"A {type(e).__name__} occurred  \n" 
            "Deleting the docs from pipeline to retry"
        )


    # Return list of TextNodes(Llama Index) or None if there was an error 
    return nodes
