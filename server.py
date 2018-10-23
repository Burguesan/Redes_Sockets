#!/usr/bin/python
'''
    Simple socket server using threads
'''
 
import socket
import sys
import threading

def EchoServer(conn,addr):
    print('Created a thread for echo server')

    while True:
        #Receiving from client
        data = conn.recv(1024)
        if data == b'':
            break
        reply = SERVERNAME + b': ' + data

        conn.send(reply)

    conn.close()

    print('Closed connection with ' + addr[0] + ':' + str(addr[1]) )

if len(sys.argv) < 2:
    print('You need to inform a server port. Ex: python server.py 1213')
    exit()

if sys.version_info.major == 3:
    SERVERNAME = bytes(sys.argv[1], 'utf-8') # python 3 needs to inform charset encoding on cast
else:
    SERVERNAME = bytes(sys.argv[1])

HOST = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1]) # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
print('Hosting on: '+HOST+':'+str(PORT))
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print(msg)
    print('Bind failed. Error Code. ')
    sys.exit()
     
print('Socket bind complete')
 
s.listen(10)
print('Socket now listening')
 
while True:

    try:
        conn, addr = s.accept()
    except KeyboardInterrupt:
        print('Closing Server...')
        s.close()
        break

    conn.send(b'accept')

    print('Connected with ' + addr[0] + ':' + str(addr[1]) )

    thread = threading.Thread(target=EchoServer, args=(conn,addr))
    thread.daemon = True
    thread.start()