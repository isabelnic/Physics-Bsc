import urllib.request
import tempfile
import shutil
import time
import numpy as np
import re


def get_num(mystring):  # get numbers from string
    nums = re.findall("\d+\.\d+", mystring)
    return float(nums[0])


def get_tempNhum(IP):
    temps = []
    humids = []
    levels = []
    count = 0
    
    while count < 10:
        with urllib.request.urlopen(IP + 'temp') as response:
            tempf = get_num(response.read())
            tempc = (tempf - 32) * 5/9
            temps.append(tempc)
        with urllib.request.urlopen(IP + 'humidity') as response:
            hum = get_num(response.read())
            humids.append(hum)
        with urllib.request.urlopen(IP + 'water_level') as response:
            lev = get_num(response.read())
            levels.append(lev)
        count += 1
        time.sleep(2)
    
    return np.mean(temps), np.mean(humids), np.mean(levels)