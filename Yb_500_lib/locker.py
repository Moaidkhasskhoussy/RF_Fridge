import serial
import time
#Pid and Vid 1659, 9123
if __package__ is None:
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from Com_lib.Port_lib import Port
else:
    from Com_lib.Port_lib import Port
class Locker:
    
    def __init__(self,VID:int,PID:int):
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
        return f"Locker('{self.port}','{self.VID}','{self.PID}')"
    
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
    
    def Get_BUF(self,ser):
        time.sleep(0.09)
        BUF=ser.read_all()
        return BUF
    
    #Sending a frame to the serial port that should open the lock 
    def Open_L(self):
        if(self.ser.isOpen() == False):
            self.ser.open()

        self.ser.write(bytearray.fromhex(Port.Open_Lock_Frame()))
        self.ser.close()
        time.sleep(0.2)
    #Geting the Locker status False :closed True:open
    def is_open(self):
        if(self.ser.isOpen() == False):
            self.ser.open()
        self.ser.write(bytearray.fromhex(Port.Status_Frame()))
        BUF=self.Get_BUF(self.ser)
        self.ser.close()
        DATA=BUF[6:len(BUF)-2]
        ERR_STA_GET=DATA[0:2]
        OPEN_STA_GET=DATA[2:4]
        PASS_STA_GET=DATA[4:6]
        TEMP_GET=DATA[6:8]
        TEMP=DATA[8::] 
        
        for i in range(len(OPEN_STA_GET.hex())):
            if (OPEN_STA_GET.hex()[i] == '1'):
                Lock_open=True
                break
            else:
                Lock_open=False

        return Lock_open

"""    
Lock=Locker(1659, 8963)
B=Lock.Get_status()
DATA=B[6:len(B)-2]
ERR_STA_GET=DATA[0:2]
OPEN_STA_GET=DATA[2:4]
PASS_STA_GET=DATA[4:6]
TEMP_GET=DATA[6:8]
TEMP=DATA[8::]"""