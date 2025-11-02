# Parallel File Processing and Keyword Search

**GoIT Computer Systems - Homework #4**  
_Parallel processing implementation using threading and multiprocessing in Python_

## 📋 Task Description

Develop a program that processes and analyzes text files in parallel to search for specific keywords. Create two versions of the program:

1. **Threading version** - using the `threading` module for multi-threaded programming
2. **Multiprocessing version** - using the `multiprocessing` module for multi-process programming

### Requirements

**Threading Implementation:**

-   Divide the list of files between different threads
-   Each thread searches for specified keywords in its assigned files
-   Collect and display search results from all threads

**General Requirements:**

-   Measure and display execution time for each version
-   Implement error handling, especially for file system operations
-   Both versions should return a dictionary where the key is the search word and the value is a list of file paths where the word was found

## 🏗️ Project Structure

```
goit-cs-hw-04/
├── main.py                           # Main application controller
├── README.md                         # Project documentation
└── src/
    ├── files/                        # Text files for searching
    │   ├── text_1.txt               # Python programming content
    │   ├── text_2.txt               # Parallel computing content
    │   └── text_3.txt               # Data processing content
    └── functions/                    # Search implementation modules
        ├── helper_func.py           # Common utility functions
        ├── sync_search.py           # Synchronous search implementation
        ├── threading_search.py      # Multi-threading implementation
        └── multiprocessing_search.py # Multi-processing implementation
```

## 🚀 Implementation Details

### Core Components

#### 1. **helper_func.py** - Common Functions

-   `search_keywords_in_file(file_path, keywords)` - searches keywords in a single file
-   Handles file reading errors (FileNotFoundError, UnicodeDecodeError)
-   Returns a set of found keywords

#### 2. **sync_search.py** - Synchronous Search

-   `search_files_sync(file_paths, keywords)` - processes files sequentially
-   Baseline implementation for performance comparison
-   Returns results dictionary and execution time

#### 3. **threading_search.py** - Multi-Threading Search

-   `search_files_threading(file_paths, keywords, num_threads=3)` - parallel processing with threads
-   Uses `threading.RLock()` for thread-safe access to shared results dictionary
-   `thread_worker()` function processes assigned files in each thread
-   `divide_files_between_threads()` distributes files evenly across threads

#### 4. **multiprocessing_search.py** - Multi-Processing Search

-   `search_files_multiprocessing(file_paths, keywords, num_processes=3)` - parallel processing with processes
-   Uses `multiprocessing.Queue()` for inter-process communication
-   `process_worker()` function processes files in separate processes
-   Collects results from all processes through the queue

#### 5. **main.py** - Application Controller

-   Manages all three search methods
-   Provides formatted output and performance comparison
-   Validates file existence before processing
-   Compares results consistency across methods

## 📊 Sample Output

```
============================================================
KEYWORD SEARCH COMPARISON APPLICATION
============================================================
Files to search: ['text_1.txt', 'text_2.txt', 'text_3.txt']
Keywords to find: ['Python', 'threading', 'multiprocessing', 'file', 'data', 'process']
Search methods: Synchronous, Threading, Multiprocessing

1. Running synchronous search...
Starting synchronous search...
Processing src/files/text_1.txt...
Processing src/files/text_2.txt...
Processing src/files/text_3.txt...
Synchronous search completed

============================================================
Synchronous Search Results
============================================================
Execution time: 0.0001 seconds
Keywords found: 6

  'Python': ['text_1.txt', 'text_2.txt', 'text_3.txt']
  'threading': ['text_1.txt', 'text_2.txt', 'text_3.txt']
  'multiprocessing': ['text_1.txt', 'text_2.txt']
  'file': ['text_1.txt', 'text_2.txt', 'text_3.txt']
  'data': ['text_1.txt', 'text_2.txt', 'text_3.txt']
  'process': ['text_1.txt', 'text_2.txt', 'text_3.txt']

============================================================
Performance Comparison
============================================================
Synchronous:      0.0001 seconds
Threading:        0.0004 seconds
Multiprocessing:  0.0516 seconds

Fastest method: Synchronous
Speed comparison (relative to fastest):
  Synchronous: 1.00x (baseline)
  Threading: 3.67x slower
  Multiprocessing: 478.48x slower
```

## 🔧 Usage

### Prerequisites

-   Python 3.7+
-   No external dependencies required (uses standard library only)

### Running the Application

```bash
# Clone the repository
git clone <repository-url>
cd goit-cs-hw-04

# Run the main application
python3 main.py
```

### Running Individual Modules

```bash
# Test synchronous search only
python3 -c "
import sys, os
sys.path.append(os.path.join('src', 'functions'))
from sync_search import search_files_sync
files = ['src/files/text_1.txt', 'src/files/text_2.txt', 'src/files/text_3.txt']
keywords = ['Python', 'threading']
result, time = search_files_sync(files, keywords)
print(f'Results: {result}')
print(f'Time: {time:.4f}s')
"

# Test threading search only
python3 -c "
import sys, os
sys.path.append(os.path.join('src', 'functions'))
from threading_search import search_files_threading
files = ['src/files/text_1.txt', 'src/files/text_2.txt', 'src/files/text_3.txt']
keywords = ['Python', 'threading']
result, time = search_files_threading(files, keywords)
print(f'Results: {result}')
print(f'Time: {time:.4f}s')
"
```

## 🧵 Threading vs Multiprocessing

### When to Use Threading

-   **I/O-bound tasks** (file reading, network operations)
-   **Shared memory access** needed
-   **Lower resource overhead**
-   **Quick context switching**

### When to Use Multiprocessing

-   **CPU-intensive tasks** (calculations, data processing)
-   **True parallelism** required (bypasses Python's GIL)
-   **Process isolation** needed
-   **Multiple CPU cores** available

### Performance Notes

For this specific task (small text files, simple keyword search):

-   **Synchronous** is fastest due to minimal overhead
-   **Threading** has small overhead for thread management
-   **Multiprocessing** has significant overhead for process creation and IPC

For larger files or more complex processing, the parallel approaches would show greater benefits.

## 🔒 Synchronization Mechanisms

### Threading Implementation

-   **RLock (Reentrant Lock)**: Ensures thread-safe access to shared results dictionary
-   **Thread.join()**: Waits for all threads to complete before collecting results

```python
with lock:  # Thread-safe access
    for keyword in found_keywords:
        if keyword not in results_dict:
            results_dict[keyword] = []
        results_dict[keyword].append(file_path)
```

### Multiprocessing Implementation

-   **Queue**: Inter-process communication for result collection
-   **Process.join()**: Ensures all processes complete before final result aggregation

```python
# Each process sends results through queue
results_queue.put(dict(process_results))

# Main process collects all results
for _ in range(len(processes)):
    process_results = results_queue.get()
    # Merge results...
```

## 🛠️ Error Handling

The application includes comprehensive error handling:

-   **File Operations**: FileNotFoundError, UnicodeDecodeError
-   **Process/Thread Management**: Proper cleanup and resource management
-   **Input Validation**: File existence checking before processing
-   **Result Verification**: Consistency checking across methods

## 📈 Educational Value

This project demonstrates:

1. **Parallel Programming Concepts**

    - Threading vs Multiprocessing trade-offs
    - Synchronization mechanisms (Locks, Queues)
    - Resource sharing and isolation

2. **Python Concurrency**

    - Global Interpreter Lock (GIL) implications
    - Standard library threading and multiprocessing modules
    - Best practices for parallel task execution

3. **Software Architecture**

    - Modular design patterns
    - Separation of concerns
    - Code reusability and maintainability

4. **Performance Analysis**
    - Benchmarking different approaches
    - Understanding overhead costs
    - Choosing appropriate parallelization strategy

## 📚 Further Improvements

Potential enhancements for learning:

-   **Async/await implementation** using `asyncio`
-   **Process pools and thread pools** for better resource management
-   **Advanced synchronization** primitives (Semaphores, Events, Conditions)
-   **Memory mapping** for large file processing
-   **Distributed processing** using `concurrent.futures`
-   **Performance profiling** and optimization techniques

## 👨‍💻 Author

**Eduard Bolma** - Computer Systems Course  
_Homework Assignment #4_

---

_This project is part of the GoIT Computer Systems curriculum, focusing on practical implementation of parallel programming concepts in Python._
