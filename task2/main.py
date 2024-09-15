import multiprocessing
import os
import time
from collections import defaultdict

def search_keywords_in_files(file_list, keywords, queue):
    result_dict = defaultdict(list)
    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result_dict[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    queue.put(dict(result_dict))

def multiprocessing_file_search(file_paths, keywords):
    result_dict = defaultdict(list)
    processes = []
    queue = multiprocessing.Queue()

    num_processes = min(4, len(file_paths))
    chunk_size = len(file_paths) // num_processes
    file_chunks = [file_paths[i:i + chunk_size] for i in range(0, len(file_paths), chunk_size)]

    start_time = time.time()
    
    for chunk in file_chunks:
        process = multiprocessing.Process(target=search_keywords_in_files, args=(chunk, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        result_chunk = queue.get()
        for keyword, files in result_chunk.items():
            result_dict[keyword].extend(files)

    end_time = time.time()
    print(f"Multiprocessing version executed in {end_time - start_time:.4f} seconds")
    return dict(result_dict)

if __name__ == "__main__":
    files = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['error', 'exception', 'critical']
    results = multiprocessing_file_search(files, keywords)
    print("Multiprocessing results:", results)
