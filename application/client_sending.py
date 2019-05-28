import socket
import sys

PORT = 5000

def sendFile(host, filename):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, PORT))
    print("[+] Connected with Server")

    # open file
    f=open(filename, "rb")
    # send file
    print("[+] Sending file...")
    data = f.read()
    s.sendall(data)

    # close connection
    print("[-] file transfered")
    f.close()
    s.close()
    #sending ends
    print("[-] Client disconnected")




