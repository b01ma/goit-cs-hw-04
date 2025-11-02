"""
Threading-based file search implementation
"""
import threading
import time
from helper_func import search_keywords_in_file

def thread_worker(thread_id, file_paths, keywords, results_dict, lock):
    """
    Worker function for a single thread
    Processes assigned files and updates shared results dictionary
    """
    print(f"Thread-{thread_id} started with files: {file_paths}")
    
    for file_path in file_paths:
        print(f"Thread-{thread_id} processing {file_path}...")
        found_keywords = search_keywords_in_file(file_path, keywords)
        
        # Use RLock to safely update shared dictionary
        with lock:
            for keyword in found_keywords:
                if keyword not in results_dict:
                    results_dict[keyword] = []
                results_dict[keyword].append(file_path)
                print(f"Thread-{thread_id} found '{keyword}' in {file_path}")
    
    print(f"Thread-{thread_id} completed")

def divide_files_between_threads(file_paths, num_threads):
    """
    Divide files between threads as evenly as possible
    Returns list of file lists for each thread
    """
    thread_files = [[] for _ in range(num_threads)]
    
    for i, file_path in enumerate(file_paths):
        thread_index = i % num_threads
        thread_files[thread_index].append(file_path)
    
    return thread_files

def search_files_threading(file_paths, keywords, num_threads=3):
    """
    Search keywords using multiple threads with RLock
    Returns: {keyword: [list_of_files_where_found]}
    """
    results_dict = {}
    lock = threading.RLock()  # Reentrant Lock for thread safety
    start_time = time.time()
    
    print(f"\nStarting threading search with {num_threads} threads...")
    
    # Divide files between threads
    thread_file_lists = divide_files_between_threads(file_paths, num_threads)
    
    # Create and start threads
    threads = []
    for i, thread_files in enumerate(thread_file_lists):
        if thread_files:  # Only create thread if it has files to process
            thread = threading.Thread(
                target=thread_worker,
                args=(i+1, thread_files, keywords, results_dict, lock)
            )
            threads.append(thread)
            thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    execution_time = time.time() - start_time
    print("All threads completed")
    return results_dict, execution_time




