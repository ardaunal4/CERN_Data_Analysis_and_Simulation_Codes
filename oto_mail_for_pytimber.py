from time import sleep
import pytimber
from pytimber import BSRT
from datetime import datetime
import smtplib

#global message_level
mail_dict = {"message_16bit_AB1" : 2, "message_16bit_AB2" : 2, "message_16bit_BB1" : 2, "message_16bit_BB2" : 2, 
             "message_24bit_AB1" : 2, "message_24bit_AB2" : 2, "message_24bit_BB1" : 2, "message_24bit_BB2" : 2}

EMAIL_ADDRESS = "lhcdcctpytimber@gmail.com"
EMAIL_PASSWORD = "pytimber123"

db = pytimber.LoggingDB()

def send_mail(message):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
         smtp.ehlo()
         smtp.starttls()
         smtp.ehlo()
         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
         subject = "LHC DCCT PYTIMBER DATAS"
         body = message
         msg = f'Subject: {subject}\n\n{body}'
         smtp.sendmail(EMAIL_ADDRESS, 'ardaunal4@gmail.com', msg)
         #smtp.sendmail(EMAIL_ADDRESS, 'patrick.odier@cern.ch', msg)

def fill_csv_files(data_base, ts, tf, mail):

    message_template1 = "Hi,\n" + "\n" + "There is a problem with " + str(data_base) + ".\n" + "\n"  + "Cheers,\n" + "Automatic Mail"
    message_template2 = "Hi,\n" + "\n" + str(data_base) + " works well again.\n" + "\n" + "Cheers\n" + "Automatic Mail"

    data = db.get(data_base, ts, tf)
    timestamps, values = data[data_base]
    time_list = list(timestamps)
    value_list = list(values)
   	
    check = 3
    if len(value_list) == 0 and len(time_list) == 0:
        check = 0 
    else:
        check = 1 

    if mail_dict[mail] != check and check == 0:
        mail_dict[mail] = check
        send_mail(message_template1)
    elif mail_dict[mail] != check and check == 1:
        mail_dict[mail] = check
        send_mail(message_template2)
    elif mail_dict[mail] == check:
        print("message_level = ", mail_dict[mail])
        print("check = ", check)

def getData():
    
    year = datetime.now().strftime("%Y")
    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%m")    
    now = datetime.now().strftime("%H:%M:%S")

    parsedate_date_string = year + "-" + month + "-" + day
    parsedate_time_string = now + ".000"

    start_time_parsedate_chain = parsedate_date_string + " " + parsedate_time_string
    
    ts = pytimber.parsedate(start_time_parsedate_chain)
    print("ts = ", ts)
    
    sleep(120)
  
    while True:
        
        year = datetime.now().strftime("%Y")
        day = datetime.now().strftime("%d")
        month = datetime.now().strftime("%m")
        now = datetime.now().strftime("%H:%M:%S")

        parsedate_date_string = year + "-" + month + "-" + day
        parsedate_time_string2 = now + ".000"

        if int(now[0:2]) == 0 and int(now[3:5]) < 3 :

            now = datetime.now().strftime("%H:%M:%S")        
            year = datetime.now().strftime("%Y")
            day = datetime.now().strftime("%d")
            month = datetime.now().strftime("%m")

            parsedate_date_string = year + "-" + month + "-" + day
            parsedate_time_string = now + '.000'

            start_time_parsedate_chain = parsedate_date_string + " " + parsedate_time_string

            ts = pytimber.parsedate(start_time_parsedate_chain)
            print("ts = ", ts)
        
            sleep(120)

            now = datetime.now().strftime("%H:%M:%S")
            parsedate_time_string2 = now + ".000"

        final_time = parsedate_date_string + " " + parsedate_time_string2
        tf = pytimber.parsedate(final_time)
        print("tf = ", tf)
    
        sleep(120)
    
        #System A Beam 1 16 bit ADC
        data_16bit_AB1 =  "LHC.BCTDC.A6R4.B1:BEAM_INTENSITY"
        fill_csv_files(data_16bit_AB1, ts, tf, "message_16bit_AB1")
    
        #System A Beam 1 24 bit ADC
        data_24bit_AB1 =  "LHC.BCTDC.A6R4.B1:BEAM_INTENSITY_ADC24BIT"
        fill_csv_files(data_24bit_AB1, ts, tf, "message_24bit_AB1")
    
        #System B Beam 1 16 bit ADC
        data_16bit_BB1 =  "LHC.BCTDC.B6R4.B1:BEAM_INTENSITY"
        fill_csv_files(data_16bit_BB1, ts, tf, "message_16bit_BB1")
    
        #System B Beam 1 24 bit ADC
        data_24bit_BB1 =  "LHC.BCTDC.B6R4.B1:BEAM_INTENSITY_ADC24BIT"
        fill_csv_files(data_24bit_BB1, ts, tf, "message_24bit_BB1")
    
        #System A Beam 2 16 bit ADC
        data_16bit_AB2 =  "LHC.BCTDC.A6R4.B2:BEAM_INTENSITY"
        fill_csv_files(data_16bit_AB2, ts, tf, "message_16bit_AB2")
    
        #System A Beam 2 24 bit ADC
        data_24bit_AB2 =  "LHC.BCTDC.A6R4.B2:BEAM_INTENSITY_ADC24BIT"
        fill_csv_files(data_24bit_AB2, ts, tf, "message_24bit_AB2")

        #System B Beam 2 16 bit ADC
        data_16bit_BB2 =  "LHC.BCTDC.B6R4.B2:BEAM_INTENSITY"
        fill_csv_files(data_16bit_BB2, ts, tf, "message_16bit_BB2")
    
        #System B Beam 2 24 bit ADC
        data_24bit_BB2 =  "LHC.BCTDC.B6R4.B2:BEAM_INTENSITY_ADC24BIT"
        fill_csv_files(data_24bit_BB2, ts, tf, "message_24bit_BB2")
        
        ts = tf
        sleep(120)

if __name__ == "__main__":

    getData()
        