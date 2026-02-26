# This file handles extracting text from different document types
# Supports PDF, DOCX and TXT files

import fitz  # PyMuPDF library for reading PDF files
import docx  # python-docx library for reading Word documents

def extract_text(filepath):
    # This is the main function that checks file type and calls the right extractor
    # filepath = the local path of the downloaded file
    
    if filepath.endswith('.pdf'):
        # If file is a PDF, use PDF extractor
        return extract_from_pdf(filepath)
    
    elif filepath.endswith('.docx'):
        # If file is a Word document, use DOCX extractor
        return extract_from_docx(filepath)
    
    elif filepath.endswith('.txt'):
        # If file is a plain text file, use TXT extractor
        return extract_from_txt(filepath)
    
    # If file type is not supported, return empty string
    return ""


def extract_from_pdf(filepath):
    # This function extracts all text from a PDF file
    # It reads the PDF page by page and combines all text
    
    text = ""
    
    # Open the PDF file
    with fitz.open(filepath) as doc:
        # Loop through every page in the PDF
        for page in doc:
            # Extract text from this page and add to our text variable
            text += page.get_text()
    
    return text


def extract_from_docx(filepath):
    # This function extracts all text from a Word (.docx) file
    # It reads each paragraph and joins them together
    
    doc = docx.Document(filepath)
    
    # Get text from every paragraph and join with newline
    return "\n".join([para.text for para in doc.paragraphs])


def extract_from_txt(filepath):
    # This function reads a plain text file and returns its content
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()