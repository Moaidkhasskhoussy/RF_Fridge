# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:38:21 2022

@author: Moaid Khasskhoussy
"""
#VID = 1659
#PID = 8963
#UHF=UHF_Reader(1659,8963)

import sys
import serial
import time

if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from Com_lib.Port_lib import Port
else:
    from Com_lib.Port_lib import Port
    
#############################################HEX UHF-RD1882 ISO1800-c##################################
"""C_inventory="05 40 FF 21 00 07 00 13 01 01 02 02 03 03 04 04 05 05 06 06 07 07 08 08 09 09 0A 0A 0B 0B 0C 0C 0D 0D 0E 0E 0F 0F 10 10 11 11 12 12 13 13 01 01 00 06 78 00 00 00 FF 00 03 88 13 00 00 00 00 74 0F"
C_inventory_left="05 07 FF 22 00 01 8C 62"
C_inventory_empty="05 0A 01 22 00 00 00 00 00 BC 48"""""
########################################################################################################
class UHF_Reader:
    def __init__(self,VID:int,PID:int):
        #Run Validation to the received arguments
        assert len(str(VID)) ==4,f"The VID that you entred {VID} is not valid , 4 CARACTERS"
        assert len(str(PID)) ==4,f"The VID that you entred {PID} is not valid , 4 CARACTERS"
        self.port=Port.Get_Port(VID, PID)
        self.VID=VID
        self.PID=PID
        self.baudrate=38400
        self.timeout=None
        self.parity=serial.PARITY_EVEN
        self.ser=self.__Serial()
        self.ser.close()
        
    def __repr__(self):
        return f"UHF_Reader('{self.port}','{self.vid}','{self.pid}')"
    
    def __Serial (self):
        ser = serial.Serial(
        self.port, 
        self.baudrate, 
        timeout=self.timeout,
        parity=self.parity, 
        rtscts=False,xonxoff = False,
        dsrdtr = False,
        write_timeout = None,
        inter_byte_timeout = None)
        return ser
    
    def __Get_BUF(self,ser):
        time.sleep(5)
        BUF=ser.read_all()
        return BUF
    
    def Get_left(self,Frames,REPORTS,TRANSF,EPC):
        REP_Len=24
        i=0    
        REP_AD=0        
        left=0
        
        while True:                
                self.ser.write(bytearray.fromhex(Port.Invl_Frame()))
                #print(self.__Get_BUF(self.ser))
                Frames[i]=self.__Get_BUF(self.ser)
                
                #print(Frames)
                
                if Frames[i]==bytearray.fromhex(Port.InvE_Frame()):
                    FRAMES_left=list(range(i))
                    FRAMES_left_DATA=list(range(i))
                    for j in range(i):
                        FRAMES_left[j]=Frames[j]
                        FRAMES_left_DATA[j]=FRAMES_left[j][6:len(FRAMES_left[j])-2]
                        REP_AD=0  
                        for Tag_index in range(int.from_bytes(FRAMES_left_DATA[j][2:3], byteorder=sys.byteorder)):
                            REPORTS[left+TRANSF]=FRAMES_left_DATA[j][3+REP_AD:3+REP_Len+REP_AD]
                            EPC[left+TRANSF]=REPORTS[left+TRANSF][6:len(REPORTS[Tag_index])-2].hex()
                            REP_AD+=REP_Len
                            left+=1
                            print(EPC[i])
                    left+=1
                    break
                i+=1
        return EPC
            
    def Get_Inventory(self):
        if(self.ser.isOpen() == False):
            self.ser.open()
        self.ser.write(bytearray.fromhex(Port.Inv_Frame()))
        BUF=self.__Get_BUF(self.ser)
        #BUF_Hex=BUF.hex()
        #SOF=BUF[0]
        #LEN=BUF[1]
        #ADR=BUF[2]
        #CMD=BUF[3]
        #SOF=BUF[0]
        #LEN=BUF[1]
        #ADR=BUF[2]
        #CMD=BUF_Hex[6:10]
        #STA=BUF[5]
        #CRC=BUF[len(BUF)-2::]
        #INVENTORY RESPONSE FUNCTION DATA 
        #RSTOP=DATA[0]
        DATA=BUF[6:len(BUF)-2]
        TOTAL=int.from_bytes(DATA[1:3], byteorder=sys.byteorder)#Number of all inventory tags 
        TRANSF=DATA[3]#Numbers of tags for actuel tranfer
        REP_Len=24
        REP_AD=0
        REPORTS = list(range(TOTAL))
        EPC=list(range(TOTAL))
        for Tag_index in range(TRANSF):
            REPORTS[Tag_index]=DATA[4+REP_AD:4+REP_Len+REP_AD]       #4=len(RSTOP)+len(TOTAL)+len(TRANSF)
            EPC[Tag_index]=REPORTS[Tag_index][6:len(REPORTS[Tag_index])-2].hex()
            REP_AD+=REP_Len
        if TOTAL!=0:
            Frames=list(range(TOTAL))
            Frames[0]=BUF
        if TOTAL!=TRANSF:
            EPC=self.Get_left(Frames,REPORTS,TRANSF,EPC)
        EPC_S=list(range(len(EPC)))
        for Tag_index in range(len(EPC)):
            EPC_S[Tag_index]= bytearray.fromhex(EPC[Tag_index])
            EPC_S[Tag_index]=EPC_S[Tag_index][4::].decode("ASCII")
        self.ser.close()
        return {"TOTAL":TOTAL,"EPC_hex":EPC,"EPC_S":EPC_S}
            
