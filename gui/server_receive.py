import socket
import sys

PORT = 5000

def receiveFile(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(5)

    print("Listening ...")

    conn, addr = s.accept()
    print("[+] Client connected: ", addr)

    # get file name to download
    f = open(filename, "wb")
    while True:
        # get file bytes
        data = conn.recv(4096)
        if not data:
            break
        # write bytes on file
        f.write(data)
    f.close()
    print("[+] Download complete!")

    conn.close()
    print("[-] Client disconnected")
    sys.exit(0)

