import pytimber
from pytimber import BSRT
from datetime import datetime

db = pytimber.LoggingDB()

f = open("crosstalk.txt", "w+")
f.close()

for i in range(495):
    
    i = i + 7000
    fill = db.getLHCFillData(i)
    t1 = fill['startTime']
    t2 = fill['endTime']
    beam1 = db.get('LHC.BCTDC.A6R4.B1:BEAM_INTENSITY', t1, t2)
    beam2 = db.get('LHC.BCTDC.A6R4.B2:BEAM_INTENSITY', t1, t2)
    timestamps1, values1 = beam1['LHC.BCTDC.A6R4.B1:BEAM_INTENSITY']
    value_list1 = list(values1)
    timestamps2, values2 = beam2['LHC.BCTDC.A6R4.B2:BEAM_INTENSITY']
    value_list2 = list(values2)
    var = 0
    c = 0
    
    for k in range(len(value_list1)):
        
        diff = abs(value_list1[k] - value_list2[k])
        if diff >= 2*10**13:
            var += 1
            
        if var >= 120 and c == 0:
            f = open("crosstalk.txt", "a")
            row1 = "Fill number = " + str(i) + "\n"
            f.write(row1)
            print(row1)
            row2 = "start time = " + datetime.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S') + "\n"
            f.write(row2)
            print(row2)
            row3  = "end time = " + datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')  + "\n"
            f.write(row3)
            print(row3)
            c = 1
            f.close()
            
            
            
            