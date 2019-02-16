'''
MultiProcessing Testing in different Cloud Platforms for speed and memory overload

Run the script like this 
python script.py -n 10 -f ./file*
'''

import time
import argparse
import multiprocessing
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num_processes', default=10, type=int, help='Number of Processes involved')
parser.add_argument('-f', '--in_files_format', default='./file*', help='pattern to match text input files')
args = parser.parse_args()

queue = multiprocessing.Queue()
queue.put(0)
lock = multiprocessing.Lock()

def square_numbers_in_file(file):
    with open(file, 'r') as file:
        for line in file:
            num = int(line)
            answer = num*num


in_files = sorted(glob.glob(args.in_files_format))

start = time.time()

print('Starting processing using %d processes' % args.num_processes)

pool = multiprocessing.Pool(args.num_processes)
pool.map_async(square_numbers_in_file, in_files)
pool.close()
pool.join()
pool.terminate()

total_time = (time.time() - start)*1000
print("Completed processing in %f milli_seconds" % total_time) 

