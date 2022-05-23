from RF_lib.Rfid_reader_lib import UHF_Reader
from Com_lib.Port_lib import Port
from Yb_500_lib.locker import Locker
from AWS import API
import requests

"""Lock Controller Port.Get_P_V_ID('COM12')
Out[21]: [1659, 9123]"""

"""UHF reader Port.Get_P_V_ID('COM4')
Out[4]: [1659, 8963]"""
####################################CreatingHardware's Objects ###########################################
try:
    Lock=Locker(1659, 9123)
    UHF=UHF_Reader(1659,8963)
except Exception:
    print("Please unplug the devices")
#####################################Initilize Parameters########################################
Opened_Lock=False
try:
    API.POST_inventory([UHF.Get_Inventory()])
    Change_status = API.PUT_status("CLOSED")
except Exception:
    print(Exception)
###################################################################################################
while(1):
    try:
        response_status = API.Get_status()
    except Exception :
        print(Exception)
    #################################Opening the Canteen Procedure#########################################
    try:
        if (Lock.is_open()==False)and(response_status.json()["canteenStatus"]=='OPEN')and(Opened_Lock==False):
            Opened_Lock=True
            Lock.Open_L()    
    except Exception :
            print(Exception)
    #################################Closing the Canteen Procedure#########################################
    try:

        if(Lock.is_open()==False)and (response_status.json()["canteenStatus"]=='OPEN')and(Opened_Lock==True):        
            Change_status = API.PUT_status("CLOSED")
            API.POST_inventory([UHF.Get_Inventory()])
            Opened_Lock=False
    except Exception :
            print(Exception)
