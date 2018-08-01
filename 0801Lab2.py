import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue
    queue_buffer.put(top_dir,timeout=3)
    files = os.listdir(top_dir)
    for i in files:
        filepath = os.path.join(top_dir, i)
        if os.path.isdir(filepath):
            producer(filepath, queue_buffer)   
    
def consumer(queue_buffer):
    global file_count
    # search file in directory
    try:
        data = queue_buffer.get(timeout=1) # dic
        files = os.listdir(data) 
        lock.acquire()
        for i in files:
            x = os.path.join(data, i)
            # print(x)
            if os.path.isfile(x) == True:
                file_count += 1
        lock.release()

    except Exception as e:
        return
    # print(file_count)


def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))
    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()