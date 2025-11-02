"""
Synchronous file search implementation
"""
import time
from collections import defaultdict
from helper_func import search_keywords_in_file

def search_files_sync(file_paths, keywords):
    """
    Search keywords in files synchronously
    Returns: {keyword: [list_of_files_where_found]}, execution_time
    """
    results = defaultdict(list)
    start_time = time.time()
    
    print("Starting synchronous search...")
    for file_path in file_paths:
        print(f"Processing {file_path}...")
        found_keywords = search_keywords_in_file(file_path, keywords)
        
        # Add file to each found keyword
        for keyword in found_keywords:
            results[keyword].append(file_path)
    
    execution_time = time.time() - start_time
    print("Synchronous search completed")
    return dict(results), execution_time
