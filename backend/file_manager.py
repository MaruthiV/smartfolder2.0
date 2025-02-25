import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_naming import rename_text_file
from ocr_extraction import rename_image_by_caption
from ai_summarization import summarize_text
from ai_search import add_file_to_index

# Define watched directory (Smart Folder)
WATCHED_DIR = "/Users/maruthi/Documents/dev/smartfolder2.0/testing"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggers when a new file is added"""
        if event.is_directory:
            return

        file_path = event.src_path
        print(f"New file detected: {file_path}")

        # Process file based on type
        process_file(file_path)

def process_file(file_path):
    """Processes the file based on its type"""
    file_ext = os.path.splitext(file_path)[-1].lower()

    if file_ext in [".jpg", ".png", ".jpeg"]:
        new_path = rename_image_by_caption(file_path)
        print(f"Renamed Image: {new_path}")

    elif file_ext in [".txt", ".pdf", ".docx"]:
        new_path = rename_text_file(file_path)
        print(f"Renamed Text File: {new_path}")

def process_file(file_path):
    """Processes the file based on its type"""
    file_ext = os.path.splitext(file_path)[-1].lower()

    if file_ext in [".jpg", ".png", ".jpeg"]:
        new_path = rename_image_by_caption(file_path)
        print(f"Renamed Image: {new_path}")


    elif file_ext in [".pdf", ".docx", ".txt"]:
        summary = summarize_text(file_path)
        print(f"Summary: {summary}")

    add_file_to_index(file_path)

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
