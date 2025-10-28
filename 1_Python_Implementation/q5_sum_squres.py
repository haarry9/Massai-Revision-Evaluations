import time
import threading

def normal_sum_squares(n):
    sum = 0
    for i in range(1,n+1):
        sum += (i * i)
    print(sum)

def multithread_sum_squares(n):
    sum = 0
    for i in range(1,n+1):
        sum += (i * i)
    print(sum)
    time.sleep(1)

t = threading.Thread(target=multithread_sum_squares, args=(1000000,))

start1 = time.time()
normal_sum_squares(1000000)
end1 = time.time()
print(f"time taken for normal loop: {start1-end1}")

start2 = time.time()
t.start()
t.join()
end2 = time.time()
print(f"time taken for threading approach: {start1-end1}")


