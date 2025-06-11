import fitz
from PIL import Image
import re
import streamlit as st
def show_image(file_path,page_num):
    pattern = r'\.pdf$|\.txt$'
    # Use re.sub() to replace the matched pattern with an empty string
    cleaned_filename = re.sub(pattern, '', file_path)

    # Opening the PDF file and creating a handle for it
    file_handle = fitz.open(file_path)

    # The index within the square brackets is the page number
    page = file_handle[page_num-1]

    # Obtaining the pixelmap of the page
    page_img = page.get_pixmap()

    # Saving the pixelmap into a png image file
    image_path = f"{cleaned_filename}_{page_num}.png"
    page_img.save(image_path)

    # Reading the PNG image file using pillow
    img = Image.open(image_path)
    return img, image_path
   

# show_image(r"D:\vscode\DocQnA_v3\data\ASMV-ADNOC OFFSHORE-2019.pdf",7)