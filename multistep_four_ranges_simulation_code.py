#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 08:00:38 2020

@author: arda
"""

import random
import csv

""" 12 hours data acquasition from 4 ranges and every range has 4 steps. Totally
40 steps -> (12*60) / 40 = 18 mintues for each step.
If every second we can take data from all ranges,then
18*60 = 1080 data for every step from all ranges.
for each range 1080 / 4 = 270 data in a step."""

# Scaling factors of ranges
scaling_factor = [180E-6, 1.8E-3, 18E-3, 180E-3]


values = []

def volt_calc(current, scaling_factor):
    """ For each range and current level return voltage """
    # with gaussian noise (sigma = 1uA)
    voltage = (current * 5 + + random.gauss(0, 0.00001) )  / scaling_factor    
    return voltage

def data_creator(current_list):

    """ Creates Datas """
    step_counter = 1
    # Scaling factors of ranges
    scaling_factor = [180E-6, 1.8E-3, 18E-3, 180E-3]
    voltage_ranges = []
    
    while step_counter != 41:
        """ Create CSV File """
        features = ["Yokogawa", "RANGE1", "RANGE2", "RANGE3", "RANGE4"] # Columns for csv file
        with open(csv_path + "step" + str(step_counter) + ".csv", "w") as csv_file: # Write columns into csv file
            csv_writer = csv.DictWriter(csv_file, fieldnames = features)
            csv_writer.writeheader()
            
        """ Calculate Voltages for every range write into csv file """    
        for i in range(270):
            for j in range(4):
                # Voltage calculator 
                voltage_ranges.append( volt_calc(float(current_list[step_counter-1]), float(scaling_factor[j])) )
            
            with open(csv_path + "step" + str(step_counter) + ".csv", "a") as csv_files: # Add datas into the csv file
                csv_writer = csv.DictWriter(csv_files, fieldnames = features)
                info = {
                    "Yokogawa" : current_list[step_counter - 1],
                    "RANGE1" : voltage_ranges[3],
                    "RANGE2" : voltage_ranges[2],
                    "RANGE3" : voltage_ranges[1],
                    "RANGE4" : voltage_ranges[0]
                }
                csv_writer.writerow(info)
                voltage_ranges.clear()
        step_counter += 1
            

if __name__ == "__main__":

    csv_path = "/home/arda/Desktop/Code_Examples/mywork/datas/"
    current_list = [18E-6, 36E-6, 54E-6, 72E-6, 90E-6, 108E-6, 126E-6, 144E-6, 162E-6, 180E-6,
                    0.342E-3, 0.504E-3, 0.666E-3, 0.828E-3, 0.990E-3, 1.152E-3, 1.314E-3, 1.476E-3, 1.638E-3, 1.8E-3,
                    3.42E-3, 5.04E-3, 6.66E-3, 8.28E-3, 9.9E-3, 11.52E-3, 13.14E-3, 14.76E-3, 16.38E-3, 18E-3,
                    34.2E-3, 50.4E-3, 66.6E-3, 82.8E-3, 99E-3, 115.2E-3, 131.4E-3, 147.6E-3, 163.8E-3, 180E-3]
    
    N = 5 # N is number of turns

    for i in range(len(current_list)):
            current_list[i] = current_list[i] / N

    data_creator(current_list)
    






    