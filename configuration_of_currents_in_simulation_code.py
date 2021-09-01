#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:29:11 2020

@author: arda
"""
from datetime import datetime
import csv
import os
""" It is configuration file for controling source. """

path = "C:\\something" # Suitable path file with '\\' instead of '\'

now = str(datetime.now().strftime("%D"))
date_of_path = now[3:5] + '-' + now[0:2] + '-' + now[6:8]

path = path + "\\" + str(date_of_path) + "\\" + "Configuration"


try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

calibration_current_list = [0, 18E-6, 36E-6, 54E-6, 72E-6, 90E-6, 108E-6, 126E-6, 144E-6, 162E-6, 180E-6,
                    0.342E-3, 0.504E-3, 0.666E-3, 0.828E-3, 0.990E-3, 1.152E-3, 1.314E-3, 1.476E-3, 1.638E-3, 1.8E-3,
                    3.42E-3, 5.04E-3, 6.66E-3, 8.28E-3, 9.9E-3, 11.52E-3, 13.14E-3, 14.76E-3, 16.38E-3, 18E-3,
                    34.2E-3, 50.4E-3, 66.6E-3, 82.8E-3, 99E-3, 115.2E-3, 131.4E-3, 147.6E-3, 163.8E-3, 180E-3]

#beam_equ_current_list = []

#N = 5 # N is number of turns
#for i in range(len(calibration_current_list)):
#    beam_equ_current_list.append(calibration_current_list[i] * N) 

features = ["time[sec]", "step", "current[mA]"]   
with open(path  + "\\control" + ".csv", "w") as csv_file: # Write columns into csv file
    csv_writer = csv.DictWriter(csv_file, fieldnames = features)
    csv_writer.writeheader()
    
time = 0
step_counter = 0
while step_counter != 41:
    with open(path +  "\\control" + ".csv", "a", newline = "") as csv_filess: # Add datas into the csv file
        csv_writer = csv.DictWriter(csv_filess, fieldnames = features)                
        info = {
                "time[sec]" : time,
                "step" : step_counter,
                "current[mA]" : calibration_current_list[step_counter]
            }
        csv_writer.writerow(info)
    time += 60
    step_counter += 1    