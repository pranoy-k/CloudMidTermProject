import random
import time
import sys
random.seed()


import time
import multiprocessing
def square(x):
    l = []
    for i in range(x):
        l.append(x*x)
start = time.time()
square(10000000)
print(time.time() - start)

import time
import multiprocessing
def square(x):
    l = []
    for i in range(x):
        l.append(x*x)
l = []
for i in range(10):
    l.append(1000000)
times = []
for ii in range(1,11):
    start = time.time()
    pool = multiprocessing.Pool(ii)
    pool.map_async(square, l)
    pool.close()
    pool.join()
    times.append('%d' % int((time.time() - start) * 10000))
    pool.terminate()

print(times)