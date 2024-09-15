import threading
import os
import time
from collections import defaultdict

def search_keywords_in_files(file_list, keywords, result_dict, lock):
    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        with lock:
                            result_dict[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

def threaded_file_search(file_paths, keywords):
    result_dict = defaultdict(list)
    threads = []
    lock = threading.Lock()

    num_threads = min(4, len(file_paths))
    chunk_size = len(file_paths) // num_threads
    file_chunks = [file_paths[i:i + chunk_size] for i in range(0, len(file_paths), chunk_size)]

    start_time = time.time()
    
    for chunk in file_chunks:
        thread = threading.Thread(target=search_keywords_in_files, args=(chunk, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading version executed in {end_time - start_time:.4f} seconds")
    return dict(result_dict)

if __name__ == "__main__":
    files = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['error', 'exception', 'critical']
    results = threaded_file_search(files, keywords)
    print("Threading results:", results)
