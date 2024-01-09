import machine
import time

class DFPlayer:
    def __init__(self,uart_id,tx_pin_id=None,rx_pin_id=None):
#         self.uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
        self.uart_id=uart_id
        #init with given baudrate
        self.uart = machine.UART(uart_id, 9600)
        if tx_pin_id or rx_pin_id:
            self.tx_pin=machine.Pin(tx_pin_id,machine.Pin.OUT)
            self.rx_pin=machine.Pin(rx_pin_id,machine.Pin.IN)     
            self.uart.init(9600, bits=8, parity=None, stop=1, tx=self.tx_pin, rx=self.rx_pin)
            self.uart.init(9600, bits=8, parity=None, stop=1, tx=tx_pin_id, rx=rx_pin_id)
        else:
            self.uart.init(9600, bits=8, parity=None, stop=1)        
        
    def flush(self):
        self.uart.flush()
        if self.uart.any():
            self.uart.read()
    
    def stop(self):
        self.send_cmd(0x16,0,0)
        
    def send_cmd(self,cmd,param1=0,param2=0):
        out_bytes = bytearray(10)
        out_bytes[0]=0x7E
        out_bytes[1]=0xFF
        out_bytes[2]=0x06
        out_bytes[3]=cmd 
        out_bytes[4]=0    
        out_bytes[5]=param1
        out_bytes[6]=param2
        somme = out_bytes[1]+out_bytes[2]+out_bytes[3]+out_bytes[4]+out_bytes[5]+out_bytes[6]
        checksum = 0xFFFF - somme + 1   
        out_bytes[7] = checksum >> 8 #8 bits de poids forts
        out_bytes[8] = checksum & 0xFF # 8 bits de poids faibles
        out_bytes[9]=0xEF
        #envoi trame 
        self.uart.write(out_bytes)     
    
    def send_query(self,cmd,param1=0,param2=0):
        retry=True
        while (retry):
            self.flush()
            self.send_cmd(cmd,param1,param2)
            time.sleep(0.2)
            in_bytes = 0
            if self.uart.any() > 0: 
                #Lire le message reçu
                in_bytes = self.uart.read()
            if not in_bytes: #timeout
                print('timeout')
                return -1
            if len(in_bytes)==10 and in_bytes[1]==0xFF and in_bytes[9]==0xEF:
                retry=False
        return in_bytes
     
    def Next(self):  #next mot réservé
        self.send_cmd(0x01,0,0)
    
    def previous(self):  #next mot réservé
        self.send_cmd(0x02,0,0)
    
    def increase_volume(self):  #next mot réservé
        self.send_cmd(0x04,0,0)
    
    def decrease_volume(self):  #next mot réservé
        self.send_cmd(0x05,0,0)
    
    def volume(self,vol=20):
        self.send_cmd(0x06,0,vol)
    
    def EQ(self,mode=1): # 1 Normal/ 2 Pop/ 3 Rock/4 Jazz/ 5 Classic/Base
        self.send_cmd(0x07,0,mode)
    
    def playback_mode(self,mode=0): # 0 Repeat/1 folder repeat/2single repeat/3 random
        self.send_cmd(0x08,0,mode)
        
    def standy(self):
        self.send_cmd(0x0A,0,0)
    
    def normal_working(self):
        self.send_cmd(0x0B,0,0)
        
    def reset(self):
        self.send_cmd(0x0C,0,1)
    
    def play(self):
        self.send_cmd(0x0D,0,0)
    
    def pause(self):
        self.send_cmd(0x0E,0,0)   
        
    def specify_play(self,folder,file):
        self.stop()
        time.sleep(0.2)
        self.send_cmd(0x0F,folder,file)
        
    def volume_adjust(self,set_volume=30): 
        self.stop()
        time.sleep(0.2)
        self.send_cmd(0x10,1,set_volume)
    
        
    def is_playing(self):
        in_bytes = self.send_query(66)
        if in_bytes==-1 or in_bytes[5]!=2:
            return -1
        return in_bytes[6]
    
    
    def get_volume(self):
        in_bytes = self.send_query(0x43)
        if in_bytes==-1 or in_bytes[3]!=0x43:
            print(in_bytes) #b'~\xff\x06@\x00\x00\x03\xfe\xb8\xef' -->@ =  erreur transmission
            return -1
        volume = 'Volume actuel : '+ str(in_bytes[6])    
        return volume  #return in_bytes[6] pour avoir juste un chiffre (int)
        
    def get_files_in_folder(self,folder):
        in_bytes = self.send_query(78,0,folder)
        if in_bytes==-1:
            return -1
        if in_bytes[3]!=78:
            return 0
        return in_bytes[6]
    
    def test_ram(self):
        in_bytes = self.send_query(0x3F,0,0)
        if in_bytes==-1 or in_bytes[3]!=0x3F :
            return 'erreur connexion',''
        if in_bytes[6]== 1:
            return 'Connexion valide','U-Disk on-line'
        elif in_bytes[6]== 2:
            return 'Connexion valide','TF Card on-line'
        elif in_bytes[6]== 4:
            return 'Connexion valide', 'PC on-line'
        elif in_bytes[6]== 8:
            return 'Connexion valide','FLASH on-line'
