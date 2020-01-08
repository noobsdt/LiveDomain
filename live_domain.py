#!/usr/bin/python3

import os
import sys
import time
import random
import requests
import multiprocessing

    
def worker(input_queue):
    while True:
        url = input_queue.get()
        u = url.strip()
        
        if url is None:
            break
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/    39.0.2171.95 Safari/537.36'}
        
        codes = [200, 201, 202, 204, 301, 302, 307, 308, 401, 403, 500]
        try:
            r = requests.get(u, headers=header, allow_redirects=False, timeout=10)
            c = r.status_code
            print(u, c)
            
            if c in codes:
                with open('live.txt', 'a') as file:
                    file.write(u + '\n')
            else:
                with open('check_manually.txt', 'a') as file:
                    file.write(u + '\n')
        except:
            print('\033[0;31m' + u +' Timeout(Check Manually!)\033[0m')
            with open('check_manually.txt', 'a') as file:
                file.write(u + '\n')
            
        if input_queue.empty() is True:
            sys.exit(0)
        
def master(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()
        
    input_queue = multiprocessing.Queue()
    processes = []
    
    for _ in range(10):
        p = multiprocessing.Process(target=worker, args=(input_queue,))
        processes.append(p)
        p.start()
        
        
    for url in urls:
        input_queue.put(url)
        
        
    for ps in processes:
        ps.join()


if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        f = sys.argv[1]
        if os.path.exists(f):
            master(f)
        else:
            print(f'{f} does not exist!')
    else:
        print('Usage: python3 ' + sys.argv[0] + ' domains.txt')
     
