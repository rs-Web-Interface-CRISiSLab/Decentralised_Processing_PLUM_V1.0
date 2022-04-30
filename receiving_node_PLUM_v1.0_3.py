#------------------------------------------
#--- Author: Chanthujan Chandrakumar
#--- Date: 08th Feb 2022
#--- Version: 1.0
#--- Python Ver: 2.7
#------------------------------------------

import socket
import time
import json
import numpy as np
from datetime import datetime
from tcp_sender import tcp_Sender



###########################TCP_SOCKET_Details###########################
port = 5005
host_IP = input("Please enter the IP address of the receiver RS4D:")
sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host_IP, port))
sock.listen(0)
#######################################################################
FMT = '%H:%M:%S:%f' 
print("Listener" + host_IP + "started")



alert_Count = []
time_Count = []
def trigger_Alert(val, val2):
    global alert_Count
    global time_Count
    if( val not in alert_Count):
        alert_Count.append(val)
        time_Count.append(val2)
    if(len(alert_Count) == 2):
        time= (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f").split()
        rec_time  = (time[1][:-1])
        print(("Earthquake detected time at first sensor:", time_Count[0]))
        print(("Alert generated time :", rec_time))
        tdelta = datetime.strptime(rec_time, FMT) - datetime.strptime(time_Count[0] ,FMT) 
        print(("Detection time is:", tdelta))

        if(host_IP in alert_Count):
            print("Generating the Alert and sending to the sensors within the 30km area !!!")
            tcp_Sender(nodeList, host_IP, port, "Alarm", "Get Ready for a Shake !!!")
        else:
            print("Generating the Alert within the sensor and sends message to users connected to the sensor = GET READY FOR THE SHAKE !!!")
        alert_Count =[]
        time_Count = []
        text_file = open("time_distributed_sys_latency.txt", "a+")
        text_file.write(str(tdelta))  
        text_file.write("\n")
        text_file.close()



nodeList =[]
nodeList = ['10.241.1.5', '10.241.1.7', '10.241.1.9', '10.241.1.25']


counter_1 = 0 
while True:
    conn, addr = sock.accept()
    recieved = conn.recv(1024)
    print(recieved)
    json_obj = json.loads(recieved)
    print(("Message Type:", str(json_obj.get('AlertType'))))
    data = str(json_obj.get('Date'))
    sent_time = data.split()      
    if( (str(json_obj.get('AlertType')) == "Alert")):
        sensor_Data_Handler( str(json_obj.get('AlertType')), recieved)
        print("Calling the Alert Function !!!")
        trigger_Alert(str(json_obj.get('Sensor_ID')),sent_time[1])
        text_file = open("receiver_marion.txt", "a+")                                                    
        text_file.write(str(counter_1))                                                                  
        text_file.write("\n")                                                                            
        text_file.close() 
