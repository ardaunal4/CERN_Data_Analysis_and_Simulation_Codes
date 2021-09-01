import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
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

def statistical_analysis(range_name, voltage_column_name):
    
    mean = 0
    maximum = 0
    minimum = 0
    current = 0
    std = 0
    pp = 0
    volt_list = range_name[voltage_column_name] 
    current = float(range_name["current[mA]"].unique()) * 5 # 5 is number of turns !!!!
    current_value = '%.2E' % Decimal(current)
    volt_values = [] 

    for volt in volt_list:
        volt_values.append(float(volt))       

    #volt_values = volt_values[1::]  
    std = '%.2E' % Decimal(std_calc(volt_values))
    maximum = '%.2E' % Decimal(max(volt_values)) 
    minimum = '%.2E' % Decimal(min(volt_values)) 
    mean = '%.2E' % Decimal(np.mean(volt_values))
    pp = '%.2E' % Decimal(max(volt_values) - min(volt_values))
    statistic_list = [current_value, mean, std, maximum, minimum, pp] 

    return statistic_list 

def histograms(range_name, voltage_column_name, path):
    
    volt_list = range_name[voltage_column_name] 
    
    volt_values = [] 
    for volt in volt_list:
        volt_values.append(float(volt))
        
    #volt_values = volt_values[1::] 
    current_level = '%.2E' % Decimal(float(range_name["current[mA]"].unique()) * 5) # 5 is number of turns !!!!
    tittle = voltage_column_name + " Current Level of Histogram : {} [Amp]".format(current_level)
    maximum = max(volt_values)
    minimum = min(volt_values)
    plot_path = path + "\\" + voltage_column_name + "_histogram.jpg"
    plt.hist(volt_values, bins = 20, range = (minimum, maximum))
    
    if voltage_column_name == "24bit[bin]":
        plt.xlabel('Bins')
    else:
        plt.xlabel("Voltage Values")
        
    plt.ylabel("Frequencies")
    plt.title(tittle)
    plt.savefig(plot_path)
    plt.clf()

def plot(range_name, voltage_column_name, path):

    volt_list = range_name[voltage_column_name]
    times = range_name["time"]

    volt_values = [] 
    for volt in volt_list:
        volt_values.append(float(volt))

    time_list = []
    for time in times:
        time_list.append(datetime.strptime(time, '%H:%M:%S'))

    #volt_values = volt_values[1::] 
    #time_list = time_list[1::] 
    current_level = '%.2E' % Decimal(float(range_name["current[mA]"].unique()) * 5) # 5 is number of turns !!!!
    title = voltage_column_name + " Plot with " + str(current_level) + "[Amp]"
    plot_path = path + "\\" + voltage_column_name + "_plot.jpg"
    plt.plot(time_list, volt_values) 
    plt.xlabel('Time in sec')

    if voltage_column_name == "24bit[bin]":
        plt.ylabel('Bin Values')
    else:
        plt.ylabel('Voltage Values')

    plt.title(title)
    xfmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.gcf().autofmt_xdate()
    plt.savefig(plot_path)
    plt.clf()

def configuration(csv_path, name):
    
    path_name, file_name = os.path.split(csv_path)    
    path = path_name + "\\Analysis"
    range_name = name
  
    try:                        
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
        
    data = pd.read_csv(csv_path) 
    
    range_data = data[["time",  "current[mA]", range_name]]
    Adc_24bit = data[["time",  "current[mA]", "24bit[bin]"]]

    histograms(range_data, range_name, path)
    histograms(Adc_24bit, '24bit[bin]', path)

    plot(range_data, range_name, path)
    plot(Adc_24bit, '24bit[bin]', path)
    
    range_data_results = statistical_analysis(range_data, range_name)
    Adc_24bit_results = statistical_analysis(Adc_24bit, '24bit[bin]')
    index = ['current[mA]', 'average', 'sd', 'max', 'min', 'peak_to_peak']
    
    data_results_dict = {"Index":index, "24bit[bin]":Adc_24bit_results, str(range_name):range_data_results}

    features = ["Index", "24bit[bin]", range_name]
            
    df = pd.DataFrame(data_results_dict, columns = features) 
    df.set_index('Index')

    df.to_csv(path + '\\analysis_results.csv', index = False, header = True)
        
if __name__ == "__main__":
    
    csv_path = "C:\\Users\\aunal\\Downloads\\range1\\corrected_data.csv"
    range_data = "RANGE1[V]"
    configuration(csv_path, range_data)