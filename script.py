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
import numpy as np
import math
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--min', default=1, type=int, help='Starting Number of Processes involved')
parser.add_argument('-e', '--max', default=10, type=int, help='Ending Number of Processes involved')
parser.add_argument('-f', '--in_files_format', default='./file*', help='pattern to match text input files')
args = parser.parse_args()


x_process = list(range(args.min, args.max + 1))
number_of_times_to_repeat = 20

def square_numbers_in_file(file):

    with open(file, 'r') as f:
        answer = []
        for line in f:
            num = int(line)
            answer.append(num*num)

    return answer


in_files = sorted(glob.glob(args.in_files_format))

print('Testing for process range %d to %d' % (args.min, args.max))

multip_stats = {}

for processes in range(args.min, args.max + 1):
    multip_stats[processes] = np.empty(number_of_times_to_repeat)
    for i in range(number_of_times_to_repeat):
        pool = multiprocessing.Pool(processes)
        start = time.time()
        pool.map_async(square_numbers_in_file, in_files)
        pool.close()
        pool.join()
        total_time = (time.time() - start) * 1000
        multip_stats[processes][i] = total_time
        pool.terminate()

serial_time = multip_stats[1].mean()
keys = list(multip_stats.keys())
keys.sort()
keys = np.array(keys)

execution_time = []
speed_up = []
efficiency = []
for number_processes in keys:
    factor = 1.725 / math.sqrt(20)
    execution_time.append(str(multip_stats[number_processes].mean()) + '+-' +  str(factor* np.std(multip_stats[number_processes])))
    speed_up_temp=[]
    efficiency_temp=[]
    for i in range(number_of_times_to_repeat):
        speed_up_temp.append(serial_time/multip_stats[number_processes][i])
        efficiency_temp.append(serial_time/(multip_stats[number_processes][i]*number_processes))
    speed_up.append(str(np.mean(speed_up_temp)) + '+-' +  str(factor* np.std(speed_up_temp)))
    efficiency.append(str(np.mean(efficiency_temp)) + '+-' +  str(factor* np.std(efficiency_temp)))

file_name = './Results/' + '_'.join(str(datetime.datetime.utcnow()).split()) + '.txt'

with open(file_name, 'w') as file:
    file.write('Processes\t\tExecTime\t\tSpeedup\t\tEfficiency\n')
    for x, y1, y2, y3 in zip(x_process, execution_time, speed_up, efficiency):
        file.write(str(x) + '\t' + str(y1) + '\t' + str(y2) + '\t' + str(y3) + '\t' + '\n')
