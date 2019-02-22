'''
MultiProcessing Testing in different Cloud Platforms for speed and memory overload

Run the script like this 
python script.py -n 10 -f ./file*
'''

import time
import argparse
import multiprocessing
import glob
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--min', default=1, type=int, help='Starting Number of Processes involved')
parser.add_argument('-e', '--max', default=10, type=int, help='Ending Number of Processes involved')
parser.add_argument('-f', '--in_files_format', default='./file*', help='pattern to match text input files')
args = parser.parse_args()


x_process = list(range(args.min, args.max + 1))
y_metric = []

def square_numbers_in_file(file):
    with open(file, 'r') as file:
        for line in file:
            num = int(line)
            answer = num*num

in_files = sorted(glob.glob(args.in_files_format))

for processes in range(args.min, args.max + 1):

    print('Starting processing using %d processes' % processes)

    pool = multiprocessing.Pool(processes)
    start = time.time()
    pool.map_async(square_numbers_in_file, in_files)
    pool.close()
    pool.join()
    pool.terminate()

    total_time = (time.time() - start)*1000
    y_metric.append(total_time)
    print("Completed processing in %f milli_seconds" % total_time) 


file_name = './Results/' + '_'.join(str(datetime.datetime.utcnow()).split()) + '.txt'

with open(file_name, 'w') as file:
    for x, y in zip(x_process, y_metric):
        file.write(str(x) + ' '+  str(y) + '\n')




