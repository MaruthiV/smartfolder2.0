import os
import re
from ai_summarization import extract_and_summarize

def clean_text_for_filename(text):
    """Cleans text to make it safe for filenames"""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = "_".join(text.split())[:50]  # Replace spaces with underscores, limit length
    return text if text else "Document"

def rename_text_file(file_path):
    """Renames a text-based file based on its content summary"""
    summary = extract_and_summarize(file_path)

    if summary:
        new_name = f"{clean_text_for_filename(summary)}{os.path.splitext(file_path)[-1]}"
    else:
        new_name = f"TextFile_{os.path.basename(file_path)}"

    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    return new_path
