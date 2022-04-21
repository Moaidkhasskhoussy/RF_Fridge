from Rfid_lib.Rfid_reader_lib import UHF_Reader
from Com_lib.Port_lib import Port
from Yb_500_lib.locker import Locker




Lock=Locker(1659, 8963)
Lock.Open_L()

B=Lock.Get_status()