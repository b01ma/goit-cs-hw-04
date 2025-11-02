"""
Multiprocessing-based file search implementation
"""
import multiprocessing
import time
from collections import defaultdict
from helper_func import search_keywords_in_file


def process_worker(file_paths, keywords, results_queue):
    """
    Worker function for a single process
    Processes assigned files and sends results through queue
    """
    process_results = defaultdict(list)
    
    for file_path in file_paths:
        print(f"Process {multiprocessing.current_process().name} processing {file_path}...")
        found_keywords = search_keywords_in_file(file_path, keywords)
        
        # Collect results for this process
        for keyword in found_keywords:
            process_results[keyword].append(file_path)
    
    # Send results through queue
    results_queue.put(dict(process_results))
    print(f"Process {multiprocessing.current_process().name} completed")


def divide_files_between_processes(file_paths, num_processes):
    """
    Divide files between processes as evenly as possible
    Returns list of file lists for each process
    """
    process_files = [[] for _ in range(num_processes)]
    
    for i, file_path in enumerate(file_paths):
        process_index = i % num_processes
        process_files[process_index].append(file_path)
    
    return process_files


def search_files_multiprocessing(file_paths, keywords, num_processes=3):
    """
    Search keywords using multiple processes with Queue
    Returns: {keyword: [list_of_files_where_found]}, execution_time
    """
    start_time = time.time()
    
    print(f"Starting multiprocessing search with {num_processes} processes...")
    
    # Create queue for results
    results_queue = multiprocessing.Queue()
    
    # Divide files between processes
    process_file_lists = divide_files_between_processes(file_paths, num_processes)
    
    # Create and start processes
    processes = []
    for i, process_files in enumerate(process_file_lists):
        if process_files:  # Only create process if it has files to process
            process = multiprocessing.Process(
                target=process_worker,
                args=(process_files, keywords, results_queue)
            )
            processes.append(process)
            process.start()
    
    # Collect results from all processes
    final_results = defaultdict(list)
    for _ in range(len(processes)):
        process_results = results_queue.get()
        for keyword, files in process_results.items():
            final_results[keyword].extend(files)
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    execution_time = time.time() - start_time
    print("All processes completed")
    return dict(final_results), execution_time
