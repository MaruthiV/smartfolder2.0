import os
import pdfplumber
import docx
from transformers import pipeline

# Initialize text summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_txt(file_path):
    """Extracts text from a .txt file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file"""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = " ".join(page.extract_text() or "" for page in pdf.pages)
        return text if text.strip() else None
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extracts text from a .docx file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else None
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None

def summarize_text(text):
    """Summarizes extracted text using AI"""
    if not text:
        return None
    
    text = text[:1024]  # Limit input to prevent model overload
    summary = summarizer(text, max_length=50, min_length=10, do_sample=False)
    return summary[0]["summary_text"] if summary else None

def extract_and_summarize(file_path):
    """Extracts text from a file and generates a summary for renaming"""
    file_ext = os.path.splitext(file_path)[-1].lower()

    if file_ext == ".txt":
        text = extract_text_from_txt(file_path)
    elif file_ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        return None

    return summarize_text(text)
