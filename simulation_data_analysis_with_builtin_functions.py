#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:57:04 2020

@author: arda
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

def std_calc(data):
    
    sum_square = 0
    summ = 0
    counter = 0
    
    for item in data:
        
        counter += 1
        sum_square += item**2
        summ += item
        
    std = np.sqrt(abs(sum_square/counter - (summ/counter)**2))
    return std

def statistical_analysis(range_name, step_number,voltage_column_name):
    """ This function does statistical analysis on data"""
    range_mean = []
    maximum = []
    minimum = []
    current_list = []
    step_list = []
    std_list = []
    
    for i in range(step_number):
        
        filter1 = range_name.step == i # This 2 lines filters data according to step number
        new_range = range_name[filter1]
        volt_list = new_range[voltage_column_name] # This line takes voltage's values from filter data
        currents = new_range["current[mA]"] # This line takes current's values from filter data
        current_values = [current_value for current_value in currents]
        volt_values = [] # For every step it clears list of voltage's values
        for volt in volt_list:
            volt_values.append(float(volt)) # This loop add voltage's values to a list for calculations 
        std_list.append(std_calc(volt_values)) # Standart Deviation Calculation
        current_list.append(current_values[0]) # Add only one current's value 
        step_list.append(i) # Step number
        maximum.append(max(volt_values)) # Max calcualiton
        minimum.append(min(volt_values)) # Min Calculation
        range_mean.append(np.mean(volt_values)) # Mean Calculation
        
    statistic_list = [step_list, current_list, range_mean, std_list, maximum, minimum] # Results in a list
    return statistic_list # Function return list

def histogram_of_steps(range_name, step_number, voltage_column_name, path):
    
    range_path = path + "\\" + voltage_column_name + "_Histograms" # Creates new directory for plots
    
    try:
        os.mkdir(range_path)
    except OSError:
        print ("Creation of the directory %s failed" % range_path)
    else:
        print ("Successfully created the directory %s " % range_path)

    for i in range(step_number):
        
        filter1 = range_name['step'] == i # This 2 lines filters data according to step number
        new_range = range_name[filter1]
        volt_list = new_range[voltage_column_name] # This line takes voltage's values from filter data
        volt_values = [] # For every step it clears list of voltage's values
        for volt in volt_list:
            volt_values.append(float(volt)) # This loop add voltage's values to a list
        plot_path = range_path + "\\hist_step" + str(i) + ".jpg"
        plt.hist(volt_values, bins = 50) #bins means that number of details in the x-axis range
        plt.xlabel("Voltage Values")
        plt.ylabel("Frequencies")
        plt.title("Histogram")
        plt.savefig(plot_path)
        plt.clf()

def configuration(csv_path):

    path_name, file_name = os.path.split(csv_path)    
    path = path_name + "\\Analysis2"
    
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    data = pd.read_csv(csv_path) # Read csv file as data frame
    
    # Seperate the range columns and step column from all data file
    range1 = data[["step", "current[mA]", "RANGE1[V]"]]
    range2 = data[["step", "current[mA]", "RANGE2[V]"]]
    range3 = data[["step", "current[mA]", "RANGE3[V]"]]
    range4 = data[["step", "current[mA]", "RANGE4[V]"]]
    Adc_24bit = data[["step", "current[mA]", "24bit[bin]"]]
    
    # Filters of data up to saturation points
    filter_for_range4 = range4.step <= 10
    range4 = range4[filter_for_range4]
    
    filter_for_range3 = range3.step <= 20
    range3 = range3[filter_for_range3]
    
    filter_for_range2 = range2.step <= 30
    range2 = range2[filter_for_range2]

    # Draws Histograms step by step for all ranges and 24 Bit ADC
    histogram_of_steps(range4, 11, 'RANGE4[V]', path)
    histogram_of_steps(range3, 21, 'RANGE3[V]', path)
    histogram_of_steps(range2, 31, 'RANGE2[V]', path)
    histogram_of_steps(range1, 41, 'RANGE1[V]', path)
    histogram_of_steps(Adc_24bit, 41, '24bit[bin]', path)
    
    # Statistic Calculations for ranges
    range4_results = statistical_analysis(range4, 10, 'RANGE4[V]')
    range3_results = statistical_analysis(range3, 20, 'RANGE3[V]')
    range2_results = statistical_analysis(range2, 30, 'RANGE2[V]')
    range1_results = statistical_analysis(range1, 40, 'RANGE1[V]')
    Adc_24bit_results = statistical_analysis(Adc_24bit, 40, '24bit[bin]')
    
    # Make results dictionary
    range4_results_dict = {'step':range4_results[0], 'current[mA]':range4_results[1], 'average[V]':range4_results[2],
                           'sd[V]':range4_results[3], 'max[V]':range4_results[4], 'min[V]':range4_results[5]}
    range3_results_dict = {'step':range3_results[0], 'current[mA]':range3_results[1], 'average[V]':range3_results[2],
                           'sd[V]':range3_results[3], 'max[V]':range3_results[4], 'min[V]':range3_results[5]}
    range2_results_dict = {'step':range2_results[0], 'current[mA]':range2_results[1], 'average[V]':range2_results[2],
                           'sd[V]':range2_results[3], 'max[V]':range2_results[4], 'min[V]':range2_results[5]}
    range1_results_dict = {'step':range1_results[0], 'current[mA]':range1_results[1], 'average[V]':range1_results[2],
                           'sd[V]':range1_results[3], 'max[V]':range1_results[4], 'min[V]':range1_results[5]}
    Adc_24bit_dict = {'step':Adc_24bit_results[0], 'current[mA]':Adc_24bit_results[1], 'average[V]':Adc_24bit_results[2],
                           'sd[V]':Adc_24bit_results[3], 'max[V]':Adc_24bit_results[4], 'min[V]':Adc_24bit_results[5]}
    dict_results = [range4_results_dict, range3_results_dict, range2_results_dict, range1_results_dict, Adc_24bit_dict]
    
    # Create Statistical Analysis csv file    
    name_list = ["\\range4.csv", "\\range3.csv", "\\range2.csv", "\\range1.csv", "\\24bit.csv"]
    features = ['step', 'current[mA]', 'average[V]', 'sd[V]', 'max[V]', 'min[V]']
    
    for item in name_list:         # This for loop creates csv files 
        with open(path + item, "w") as csv_file: # Write columns into csv file
            csv_writer = csv.DictWriter(csv_file, fieldnames = features)
            csv_writer.writeheader()
            
    # Write analyzed datas into data frame
    df4 = pd.DataFrame(dict_results[0], columns = features)
    df3 = pd.DataFrame(dict_results[1], columns = features)
    df2 = pd.DataFrame(dict_results[2], columns = features)
    df1 = pd.DataFrame(dict_results[3], columns = features)
    df0 = pd.DataFrame(dict_results[4], columns = features) # 24 Bit results
    dataFrame_list = [df4, df3, df2, df1, df0]
    
    i = 0
    for frame in dataFrame_list:    # This for loop fills csv files 
        frame.to_csv (path + name_list[i], index = False, header = True)
        i += 1

if __name__ == "__main__":
    
    csv_path = "/home/arda/Desktop/Code_Examples/mywork/datas/02-04-20/Simulation/simulation.csv"
    configuration(csv_path)