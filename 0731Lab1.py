import threading
import numpy as np
import time
import multiprocessing
import random

matA = np.random.randint(10, size = (1000, 1000))
matB = np.random.randint(10, size = (1000, 1000))
result1 = np.zeros((matA.shape[0], matB.shape[1]))
result2 = multiprocessing.Manager().dict()

number = 10

start_time = time.time()
numpy_result = np.matmul(matA, matB)
end_time = time.time()
print('Time elapsed (numpy) : ', end_time - start_time)


def thread_func(lower, upper):
    for i in range(lower, upper):
        x = np.matmul(matA[i], matB)
        result1[i] = x

def pro_func(lower, upper, result_queue):
    for i in range(lower, upper):
        x = np.matmul(matA[i], matB)
        result2[i] = x
       
# =============================

def thread_main():
    start_time = time.time()
    threads = []
    count = 0
    for i in range(number):
        limit = int(matA.shape[0]/number)*(i+1)
        thread = threading.Thread(target = thread_func, args=(count, limit))
        count = count + int(matA.shape[0]/number)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()
    print('Time elapsed (thread) : ', end_time - start_time)
    # print(result)
    print('Answer is correct:', np.all(numpy_result == result1))

# ==============================================================================

def process_main():
    # Generate queue for communication
    start_time = time.time()
    result_queue = multiprocessing.Manager().Queue()
    
    jobs = []
    count = 0
    for i in range(number):
        limit = int(matA.shape[0]/number)*(i+1)
        process = multiprocessing.Process(target = pro_func, args=(count, limit, result_queue))
        count = count + int(matA.shape[0]/number)
        jobs.append(process)
        # result2 = pro_func

    for process in jobs:
        process.start()

    for process in jobs:
        process.join()
    
    # while not result_queue.empty():
    #     pro_result = result_queue.get()
    #     print(pro_result)

    pro_result = []
    for i in range(matA.shape[0]):
        pro_result.append(result2[i])
    end_time = time.time()

    print('Time elapsed (process) : ', end_time - start_time)
    print('Answer is correct:', np.all(numpy_result == pro_result))
    # print(pro_result)



if __name__ == "__main__":
    thread_main()
    process_main()
