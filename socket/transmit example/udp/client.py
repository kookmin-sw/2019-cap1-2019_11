import socket 
import sys 

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #dgram : udp

host = '127.0.0.1' 
port=6000 

msg="Trial msg" 

msg=msg.encode('utf-8') 

while 1: 

    s.sendto(msg,(host,port)) 
    data, servaddr = s.recvfrom(1024) 
    data=data.decode('utf-8') 
    print("Server reply:", data) 
    break 
s.settimeout(5) 

filehandle=open("testing.txt","rb") 

finalmsg=filehandle.read(1024) 

s.sendto(finalmsg, (host,port)) 
