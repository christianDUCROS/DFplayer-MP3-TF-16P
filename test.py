import time
import dfplayer

#instanciation player
df=dfplayer.DFPlayer(uart_id=1,tx_pin_id=4,rx_pin_id=5) #uart1
#wait some time till the DFPlayer is ready
time.sleep(1)
print(df.test_ram()) #renvoi le type de mémoire utilisée : TF card = microSD 

df.volume() #20 par défaut #df.volume(30) pour ajuster le niveau entre 0-30
print("---------------------------------------")
print("Objet 'df' créé  : Tester vos commandes dans la console ci-dessous pour contrôler en direct")
print('df.play() pour lancer le titre 01/001.mp3 ')  
print('df.specify_play(1,2) pour lancer le titre folder=1 , file=2  ')
print('df.volume(30) pour mettre le volume au maximum')



#fader
# for i in range (0,31) : 
#     df.volume(i)
#     print(i)
#     time.sleep(0.5)
# for i in range (31,0,-1) : 
#     df.volume(i)
#     print(i)
#     time.sleep(0.5)
# print(df.get_volume())
# print(df.get_files_in_folder(1))


