"""
Main application for keyword search comparison
Demonstrates synchronous, threading, and multiprocessing approaches
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'functions'))

from sync_search import search_files_sync
from threading_search import search_files_threading
from multiprocessing_search import search_files_multiprocessing


def print_results(results, execution_time, method_name):
    """Print search results in a formatted way"""
    print(f"\n{'='*60}")
    print(f"{method_name} Results")
    print(f"{'='*60}")
    print(f"Execution time: {execution_time:.4f} seconds")
    print(f"Keywords found: {len(results)}")
    print()
    
    if results:
        for keyword, files in results.items():
            # Show only filenames, not full paths for cleaner output
            filenames = [os.path.basename(file) for file in files]
            print(f"  '{keyword}': {filenames}")
    else:
        print("  No keywords found in any files")
    print()


def print_performance_comparison(sync_time, threading_time, multiprocessing_time):
    """Print detailed performance comparison"""
    print("="*60)
    print("Performance Comparison")
    print("="*60)
    print(f"Synchronous:      {sync_time:.4f} seconds")
    print(f"Threading:        {threading_time:.4f} seconds") 
    print(f"Multiprocessing:  {multiprocessing_time:.4f} seconds")
    print()
    
    # Find fastest method
    times = {
        'Synchronous': sync_time,
        'Threading': threading_time,
        'Multiprocessing': multiprocessing_time
    }
    
    fastest_method = min(times, key=times.get)
    fastest_time = times[fastest_method]
    
    print(f"Fastest method: {fastest_method}")
    print()
    print("Speed comparison (relative to fastest):")
    
    for method, time_taken in times.items():
        if time_taken == fastest_time:
            print(f"  {method}: 1.00x (baseline)")
        else:
            ratio = time_taken / fastest_time
            print(f"  {method}: {ratio:.2f}x slower")


def validate_files(file_paths):
    """Check if all files exist"""
    missing_files = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("Error: The following files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    return True


def main():
    """Main function to run all search methods and compare results"""
    
    # Configuration
    base_path = os.path.join("src", "files")
    file_names = ["text_1.txt", "text_2.txt", "text_3.txt"]
    file_paths = [os.path.join(base_path, filename) for filename in file_names]
    keywords = ["Python", "threading", "multiprocessing", "file", "data", "process"]
    
    # Application header
    print()
    print("="*60)
    print("KEYWORD SEARCH COMPARISON APPLICATION")
    print("="*60)
    print(f"Files to search: {file_names}")
    print(f"Keywords to find: {keywords}")
    print(f"Search methods: Synchronous, Threading, Multiprocessing")
    print()
    
    # Validate files exist
    if not validate_files(file_paths):
        return
    
    # Store results for comparison
    all_results = {}
    
    try:
        # 1. Synchronous search
        print("1. Running synchronous search...")
        sync_results, sync_time = search_files_sync(file_paths, keywords)
        all_results['sync'] = sync_results
        print_results(sync_results, sync_time, "Synchronous Search")
        
        # 2. Threading search  
        print("2. Running threading search...")
        threading_results, threading_time = search_files_threading(file_paths, keywords, num_threads=3)
        all_results['threading'] = threading_results
        print_results(threading_results, threading_time, "Threading Search")
        
        # 3. Multiprocessing search
        print("3. Running multiprocessing search...")
        multiprocessing_results, multiprocessing_time = search_files_multiprocessing(file_paths, keywords, num_processes=3)
        all_results['multiprocessing'] = multiprocessing_results
        print_results(multiprocessing_results, multiprocessing_time, "Multiprocessing Search")
        
        # Performance comparison
        print_performance_comparison(sync_time, threading_time, multiprocessing_time)
        
    except Exception as e:
        print(f"Error during execution: {e}")
        return
    
    print("\n" + "="*60)
    print("Search completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
