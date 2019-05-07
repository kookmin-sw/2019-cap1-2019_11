import socket 

host='127.0.0.1' 

port=6000 

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

s.bind(("",port)) 

print("waiting on port:", port) 

while 1: 

    data, clientaddr= s.recvfrom(1024) 
    data=data.decode('utf-8') 
    print(data) 
    s.settimeout(4) 
    break 

reply="Got it thanks!" 

reply=reply.encode('utf-8') 

s.sendto(reply,clientaddr) 

clientmsg, clientaddr=s.recvfrom(1024) 
