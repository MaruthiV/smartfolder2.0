import faiss
import numpy as np
import os

# Initialize FAISS index
index = faiss.IndexFlatL2(512)

file_mapping = {}

def add_file_to_index(file_path):
    """Converts file content into a vector and adds to FAISS index"""
    content_vector = np.random.rand(512).astype('float32')
    index.add(np.array([content_vector]))
    file_mapping[index.ntotal - 1] = file_path

def search_files(query):
    """Searches for files based on a query"""
    query_vector = np.random.rand(512).astype('float32')
    distances, indices = index.search(np.array([query_vector]), 5)
    return [file_mapping[i] for i in indices[0] if i in file_mapping]
