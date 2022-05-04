# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:37:03 2022

@author: khass : for hex Frames please Check the documentation 
"""
import serial.tools.list_ports as list_ports
import sys
import glob
import serial
#VID = 1659
#PID = 8963
class Port:
    def __init__(self):
        pass
    
    @staticmethod
    def Get_All_COMS():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
    @staticmethod
    def Get_Port(VID:int,PID:int):
        try:
            device_list = list_ports.comports()
            for device in device_list:
                    if (device.vid != None or device.pid != None):
                        if (device.vid) == VID and device.pid == PID:
                            port = device.device
                            break
            return port                        
        except Exception :
            print ("the device Vid"+str(VID)+"PID"+str(PID)+"is not found")
        else:
            return port
           
        
    
    
    @staticmethod
    def Get_P_V_ID(port:str):
        ID=["VID","PID"]
        device_list = list_ports.comports()
        for device in device_list:
                if (device.vid != None or device.pid != None):
                    if (device.device) == port :
                        ID[0] = device.vid
                        ID[1] = device.pid
                        break
        return ID
    
    #Hex String with ISO1800_C to get the Inventory 
    @staticmethod
    def Inv_Frame():
        C_inventory="05 40 FF 21 00 07 00 13 01 01 02 02 03 03 04 04 05 05 06 06 07 07 08 08 09 09 0A 0A 0B 0B 0C 0C 0D 0D 0E 0E 0F 0F 10 10 11 11 12 12 13 13 01 01 00 06 78 00 00 00 FF 00 03 88 13 00 00 00 00 74 0F"
        return C_inventory
    
    #Hex String with ISO1800_C to get the Inventory  left
    @staticmethod
    def Invl_Frame():
        C_inventory_left="05 07 FF 22 00 01 8C 62"
        return C_inventory_left
    
    #Hex String of empty waiting inventory 
    @staticmethod
    def InvE_Frame():
        C_inventory_empty="05 0A 01 22 00 00 00 00 00 BC 48"
        return C_inventory_empty
    
    #Hex String to open YB-500 lock 
    @staticmethod
    def Open_Lock_Frame():
        Open_Lock= "05 08 ff 30 00 01 00 58 89"
        return Open_Lock
    
    #Hex String of empty waiting inventory 
    @staticmethod
    def Status_Frame():
        Status_Frame= "05 0E 01 31 00 01 00 01 00 01 00 01 00 A6 15"
        return Status_Frame




    