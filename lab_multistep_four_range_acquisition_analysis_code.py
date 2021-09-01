
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:39:31 2020

@author: ardau
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from numpy.fft import fft, fftfreq
from decimal import Decimal
from datetime import datetime
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%d')

def std_calc(list_of_voltages):
    sum_square = 0
    summ = 0
    counter = 0
    
    for item in list_of_voltages:
        
        counter += 1
        sum_square += item**2
        summ += item
        
    value = abs(sum_square/counter - (summ/counter)**2)
    
    if value != 0:
        std = np.sqrt(value)
    else:
        std = 0
        
    return std

def statistical_analysis(range_name, voltage_column_name, step_number):
    """ This function does statistical analysis on data"""
    step_mean = []
    maximum = []
    minimum = []
    current_list = []
    step_list = []
    std_list = []
    pp = []
    
    for i in range(step_number):
        
        filter1 = range_name['step'] == i + 1                                                                               # This 2 lines filters data according to step number
        filtered_range = range_name[filter1]
        volt_list = filtered_range[voltage_column_name]                                                                     # This line takes voltage's values from filter data
        current_level = float(filtered_range["current[mA]"].unique())
        volt_values = []                                                                                                    # For every step it clears list of voltage's values
        
        for volt in volt_list:
            volt_values.append(float(volt))
                
        volt_values = volt_values[5::]                                                                                      # ignore first 5 values 
        std_list.append('%.2E' % Decimal(std_calc(volt_values)))                                                            # Standart Deviation Calculation
        current_list.append(current_level)                                                                                  # Add only one current's value 
        step_list.append(i+1)                                                                                               # Step number
        maximum.append('%.2E' % Decimal(max(volt_values)))                                                                  # Max calcualiton
        minimum.append('%.2E' % Decimal(min(volt_values)))                                                                  # Min Calculation
        step_mean.append('%.2E' % Decimal(np.mean(volt_values)))   
        pp.append('%.2E' % Decimal(max(volt_values) - min(volt_values))) 
        
    statistic_list = [step_list, current_list, step_mean, std_list, maximum, minimum, pp]                                   # Results in a list
    return statistic_list                                                                                                   # Function return list

def histogram_of_steps(range_name, voltage_column_name, path, step_number):
    
    if voltage_column_name == "24bit[bin]":
        range_path = path + "\\" + voltage_column_name[:-5] + "_Histograms" 
    else:
        range_path = path + "\\" + voltage_column_name[:-3] + "_Histograms" 
        
    try:
        os.mkdir(range_path)
    except OSError:
        print ("Creation of the directory %s failed" % range_path)
    else:
        print ("Successfully created the directory %s " % range_path)

    plt.figure(figsize = (10, 8))

    for i in range(step_number):
        
        filter1 = range_name['step'] == i + 1                                                                              # This 2 lines filters data according to step number
        new_range = range_name[filter1]
        volt_list = new_range[voltage_column_name]                                                                         # This line takes voltage's values from filter data
        volt_values = []                                                                                                   # For every step it clears list of voltage's values
        
        for volt in volt_list:
            volt_values.append('%.2E' % Decimal(float(volt)))

        volt_values = volt_values[5::]                                                                                     # ignore first 100 values
        current_level = float(new_range["current[mA]"].unique())
        tittle = "Current Level of Histogram : {} [Amp]".format(current_level)
        plot_path = range_path + "\\hist_step" + str(i + 1) + ".jpg"
        
        plt.hist(volt_values, bins = 20)
        
        if voltage_column_name == "24bit[bin]":
            plt.xlabel("Bin Values")
        else:
            plt.xlabel("Voltage Values")
            
        plt.ylabel("Frequencies")
        plt.title(tittle)
        plt.savefig(plot_path)
        plt.clf()

    plt.close()

def fft_of_ranges_with_zero_current(path, range_name, voltage_column_name):
    
    if voltage_column_name == "24bit[bin]":
        plots_path = path + '\\' + str(voltage_column_name[:-5]) + "_fft_plots"
    else:
        plots_path = path + '\\' + str(voltage_column_name[:-3]) + "_fft_plots"

    try:
        os.mkdir(plots_path)
    except OSError:
        print ("Creation of the directory %s failed" % plots_path)
    else:
        print ("Successfully created the directory %s " % plots_path)
    
    filter1 = range_name["step"] == 1                                                                                      # These 2 lines filter data for zero current of the corresponding range
    filtered_range = range_name[filter1]
    column_name = voltage_column_name
    volt_list = filtered_range[column_name]                                                                                # This line takes voltage's values from filter data
    volt_values = []                                                                                                       # For every step it clears list of voltage's values
    
    for volt in volt_list:
        volt_values.append(float(volt))
            
    volt_values = volt_values[5::]                                                                                         # Ignore first 5 values
    signal = np.array(volt_values[0:1024])                                                                                 # Use 2^10 values of the list
    sample_freq = fftfreq(signal.size)
    mask = sample_freq > 0 
    fft_signal = np.abs(fft(signal))
    
    if voltage_column_name == "24bit[bin]":
        plot_path = plots_path + "\\fft_plot_of_" + str(voltage_column_name[:-5]) + ".jpg"
    else:
        plot_path = plots_path + "\\fft_plot_of_" + str(voltage_column_name[:-3]) + ".jpg"

    plt.figure(figsize = (10, 8))    
    plt.plot(sample_freq[mask], fft_signal[mask], color = 'blue', linewidth = 1)
    plt.title('FFT of ' + str(voltage_column_name[:-3]) + ' at Zero Current')
    plt.xlabel('Frequency[Hz]'); plt.ylabel('Absolute Magnitude [au]')
    plt.grid('on')
    plt.savefig(plot_path)
    plt.close()


def step_by_step_plot(path, range_name, voltage_column_name, step_number):
    
    if voltage_column_name == "24bit[bin]":
        plots_path = path + '\\' + str(voltage_column_name[:-5]) + "_plots"
    else:
        plots_path = path + '\\' + str(voltage_column_name[:-3]) + "_plots"

    try:
        os.mkdir(plots_path)
    except OSError:
        print ("Creation of the directory %s failed" % plots_path)
    else:
        print ("Successfully created the directory %s " % plots_path)

    plt.figure(figsize = (10, 8))
        
    for i in range(step_number):
        
        filter1 = range_name["step"] == i + 1                                                                              # These 2 lines filter data according to step number
        filtered_range = range_name[filter1]
        column_name = voltage_column_name
        volt_list = filtered_range[column_name]                                                                            # This line takes voltage's values from filter data
        times = filtered_range["time"]
        current_level = float(filtered_range["current[mA]"].unique())
        

        time_list = []
        for time in times:
            date_time_str = time
            time_list.append(datetime.strptime(date_time_str, '%H:%M:%S'))

        volt_values = []                                                                                                  # For every step it clears list of voltage's values
        for volt in volt_list:
            volt_values.append(float(volt))
                
        time_list = time_list[5::]        
        volt_values = volt_values[5::]                                                                                    # ignore first 5 values
        plot_path = plots_path + "\\raw_plot_of_step" + str(i + 1) + ".jpg"
        
        plt.plot(time_list, volt_values)
        plt.xlabel('Time in sec')
        
        if voltage_column_name == "24bit[bin]":
            plt.ylabel('Bin Values')
            plt.title('Time versus Bins with ' + str(current_level) + ' [Amp]')
        else:
            plt.ylabel('Voltage Values')
            plt.title('Time versus Voltages with ' + str(current_level) + ' [Amp]')
            
        xfmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(xfmt)
        plt.gcf().autofmt_xdate()
        plt.savefig(plot_path)
        plt.clf()

    plt.close()

def raw_plot(range_name, voltage_column_name, path):

    column_name = voltage_column_name
    volt_list = range_name[column_name]                                                                                 # This line takes voltage's values from filter data
    times = range_name["time"]

    time_list = []
    for time in times:
        date_time_str = time
        time_list.append(datetime.strptime(date_time_str, '%H:%M:%S'))

    volt_values = []                                                                                                  # For every step it clears list of voltage's values
    for volt in volt_list:
        volt_values.append(float(volt))
        
    time_list = time_list[5::]        
    volt_values = volt_values[5::]                                                                                    # ignore first 5 values
    plot_path = path + "\\" + voltage_column_name + ".jpg"
    plt.figure(figsize = (10, 8))
    plt.plot(time_list, volt_values)
    plt.xlabel('Time in sec')
    
    if voltage_column_name == "24bit[bin]":
        plt.ylabel('Bin Values')
    else:
        plt.ylabel('Voltage Values')
        
    plt.title('Time versus ' + voltage_column_name)
    xfmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.gcf().autofmt_xdate()
    plt.savefig(plot_path)
    plt.close()

def average_plot(path, step_list, average_list, data_name):

    steps = step_list
    means = average_list

    plots_path = path + "\\mean_plots"
    try:
        os.mkdir(plots_path)
    except OSError:
        print ("Creation of the directory %s failed" % plots_path)
    else:
        print ("Successfully created the directory %s " % plots_path)

    plot_path = plots_path + "\\" + data_name + '_mean_plot' + ".jpg"
    plt.figure(figsize = (10, 8))
    plt.plot(steps, means)
    plt.xlabel('Steps')
    
    if data_name == "adc_24bit":
        plt.ylabel('Average Bins')
        plt.title('Step versus ' + data_name + " Bin Average")
    else:
        plt.ylabel('Average Voltage')
        plt.title('Step versus ' + data_name + " Voltage Average")
        
    plt.savefig(plot_path)
    plt.close()

def configuration(csv_path):

    path_name, file_name = os.path.split(csv_path)    
    path = path_name + "\\analysis"
    
    try:                                                                                                              # This lines try to create a new directory 
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    data = pd.read_csv(csv_path)                                                                                      # Read CSV file as data frame and skip first 10 lines
    step_num = len(data["step"].unique())

                                                                                                                      # Seperate the range columns and step column from all data file
    range1 = data[["time", "step", "current[mA]", "RANGE1[V]"]]
    range2 = data[["time", "step", "current[mA]", "RANGE2[V]"]]
    range3 = data[["time", "step", "current[mA]", "RANGE3[V]"]]
    range4 = data[["time", "step", "current[mA]", "RANGE4[V]"]]
    Adc_24bit = data[["time", "step", "current[mA]", "24bit[bin]"]]

    plots_path1 = path + "\\raw_plots"
    try:
        os.mkdir(plots_path1)
    except OSError:
        print ("Creation of the directory %s failed" % plots_path1)
    else:
        print ("Successfully created the directory %s " % plots_path1)

    raw_plot(range4, 'RANGE4[V]', plots_path1)
    raw_plot(range3, 'RANGE3[V]', plots_path1)
    raw_plot(range2, 'RANGE2[V]', plots_path1)
    raw_plot(range1, 'RANGE1[V]', plots_path1)
    raw_plot(Adc_24bit, '24bit[bin]', plots_path1)

    # Draws Histograms step by step for all ranges and ADC
    histogram_of_steps(range4, 'RANGE4[V]', path, step_num)
    histogram_of_steps(range3, 'RANGE3[V]', path, step_num)
    histogram_of_steps(range2, 'RANGE2[V]', path, step_num)
    histogram_of_steps(range1, 'RANGE1[V]', path, step_num)
    histogram_of_steps(Adc_24bit, '24bit[bin]', path, step_num)
    
    # Statistic Calculations for ranges
    range4_results = statistical_analysis(range4, 'RANGE4[V]', step_num)
    range3_results = statistical_analysis(range3, 'RANGE3[V]', step_num)
    range2_results = statistical_analysis(range2, 'RANGE2[V]', step_num)
    range1_results = statistical_analysis(range1, 'RANGE1[V]', step_num)
    Adc_24bit_results = statistical_analysis(Adc_24bit, '24bit[bin]', step_num)
    
    # Make results dictionary
    range4_results_dict = {'step':range4_results[0], 'current[mA]':range4_results[1], 'average[V]':range4_results[2],
                           'sd[V]':range4_results[3], 'max[V]':range4_results[4], 'min[V]':range4_results[5], "peak-to-peak[V]":range4_results[6]}
    range3_results_dict = {'step':range3_results[0], 'current[mA]':range3_results[1], 'average[V]':range3_results[2],
                           'sd[V]':range3_results[3], 'max[V]':range3_results[4], 'min[V]':range3_results[5], "peak-to-peak[V]":range3_results[6]}
    range2_results_dict = {'step':range2_results[0], 'current[mA]':range2_results[1], 'average[V]':range2_results[2],
                           'sd[V]':range2_results[3], 'max[V]':range2_results[4], 'min[V]':range2_results[5], "peak-to-peak[V]":range2_results[6]}
    range1_results_dict = {'step':range1_results[0], 'current[mA]':range1_results[1], 'average[V]':range1_results[2],
                           'sd[V]':range1_results[3], 'max[V]':range1_results[4], 'min[V]':range1_results[5], "peak-to-peak[V]":range1_results[6]}
    Adc_24bit_dict = {'step':Adc_24bit_results[0], 'current[mA]':Adc_24bit_results[1], 'average[bin]':Adc_24bit_results[2],
                           'sd[bin]':Adc_24bit_results[3], 'max[bin]':Adc_24bit_results[4], 'min[bin]':Adc_24bit_results[5], "peak-to-peak[bin]":Adc_24bit_results[6]}
    dict_results = [range4_results_dict, range3_results_dict, range2_results_dict, range1_results_dict, Adc_24bit_dict]

    average_plot(path, range1_results_dict["step"], range1_results_dict["average[V]"], "RANGE1")
    average_plot(path, range2_results_dict["step"], range2_results_dict["average[V]"], "RANGE2")
    average_plot(path, range3_results_dict["step"], range3_results_dict["average[V]"], "RANGE3")
    average_plot(path, range4_results_dict["step"], range4_results_dict["average[V]"], "RANGE4")
    average_plot(path, Adc_24bit_dict["step"], Adc_24bit_dict["average[bin]"], "adc_24bit")
    
                                                                                                                           # Create Statistical Analysis csv file    
    name_list = ["range4", "range3", "range2", "range1", "24bit"]
    features1 = ['step', 'current[mA]', 'average[V]', 'sd[V]', 'max[V]', 'min[V]', "peak-to-peak[V]"]
    features2 = ['step', 'current[mA]', 'average[bin]', 'sd[bin]', 'max[bin]', 'min[bin]', "peak-to-peak[bin]"]

    statistical_analysis_path = path + "\\statistical_results"
    try:                                                                                                                   # This lines try to create a new directory 
        os.mkdir(statistical_analysis_path)
    except OSError:
        print ("Creation of the directory %s failed" % statistical_analysis_path)
    else:
        print ("Successfully created the directory %s " % statistical_analysis_path)            
  
    for item in name_list:
        if item == "24bit":
            with open(statistical_analysis_path + '\\' + item + '.csv', "w") as csv_file:                                   # Write columns into csv file
                csv_writer = csv.DictWriter(csv_file, fieldnames = features2)
                csv_writer.writeheader()
        else:
            with open(statistical_analysis_path + '\\' + item + '.csv', "w") as csv_file:                                   # Write columns into csv file
                csv_writer = csv.DictWriter(csv_file, fieldnames = features1)
                csv_writer.writeheader()
            
                                                                                                                            # Write datas into csv file
    df4 = pd.DataFrame(dict_results[0], columns = features1)                                                                # Range4
    df3 = pd.DataFrame(dict_results[1], columns = features1)
    df2 = pd.DataFrame(dict_results[2], columns = features1)
    df1 = pd.DataFrame(dict_results[3], columns = features1)
    df0 = pd.DataFrame(dict_results[4], columns = features2)                                                                # 24 Bit results
    dataFrame_list = [df4, df3, df2, df1, df0]

                                                                                                                            # Line plots
    step_by_step_plot(path, range1, "RANGE1[V]", step_num)
    step_by_step_plot(path, range2, "RANGE2[V]", step_num)
    step_by_step_plot(path, range3, "RANGE3[V]", step_num)
    step_by_step_plot(path, range4, "RANGE4[V]", step_num)
    step_by_step_plot(path, Adc_24bit, "24bit[bin]", step_num)

                                                                                                                            # FFT plots
    fft_of_ranges_with_zero_current(path, range1, "RANGE1[V]")
    fft_of_ranges_with_zero_current(path, range2, "RANGE2[V]")
    fft_of_ranges_with_zero_current(path, range3, "RANGE3[V]")
    fft_of_ranges_with_zero_current(path, range4, "RANGE4[V]")
    fft_of_ranges_with_zero_current(path, Adc_24bit, "24bit[bin]")    

    i = 0
    for frame in dataFrame_list:                                                                                            # This for loop fills csv files 
        frame.to_csv (statistical_analysis_path + '\\' + name_list[i] + '.csv', index = False, header = True)
        i += 1

if __name__ == "__main__":
    
    csv_path = "C:\\Users\\aunal\\Downloads\\17-07-2020\\corrected_data.csv"
    configuration(csv_path)
