#exemple
#~\xff\x06@\x00\x00\x03\xfe\xb8\xef
#version perso
out_bytes = bytearray(10)
out_bytes[0]=0x7E#~
out_bytes[1]=0xFF
out_bytes[2]=6
out_bytes[3]=0x40 #@
out_bytes[4]=0
out_bytes[5]=0
out_bytes[6]=3
out_bytes[9]=0xEF
somme = out_bytes[1]+out_bytes[2]+out_bytes[3]+out_bytes[4]+out_bytes[5]+out_bytes[6]
checksum = 0xFFFF - somme + 1   

print(hex(checksum))
out_bytes[7] = checksum>>8
out_bytes[8] = checksum & 0xFF
print(out_bytes)

#version initiale 
checksum = 0
for i in range(1,7):
    checksum=checksum+out_bytes[i]
print(hex(checksum))    
out_bytes[7]=(checksum>>7)-1
out_bytes[7]=~out_bytes[7]
out_bytes[8]=checksum-1
out_bytes[8]=~out_bytes[8]
print(out_bytes)
