#!/usr/bin/python
'''
    Simple socket client
'''
 
import socket
import sys

if len(sys.argv) < 2:
    print('You need to inform server address and port. Ex: python client.py localhost 1213')
    exit()



def LoopEcho():
    server, port = sys.argv[1], int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    resp = s.recv(1024)
    
    if resp != b'accept':
        return

    while True:
    
        msg = b''
        while msg == b'':
            try:
                if sys.version_info.major == 3:
                    msg = bytes(input('Type a message(type -q to exit): '),'utf-8') # python 3 needs to inform charset encoding on cast
                else:
                    msg = bytes(raw_input('Type a message(type -q to exit): '))
                    
            except KeyboardInterrupt:
                msg = b'-q'
                break    
            except EOFError:
                msg = b'-q'
                break 

        if msg == b'-q':
            return s

        try:
            s.send(msg)
            resp = s.recv(1024)
        except socket.error:
            resp = b''


        print(resp)

s = LoopEcho()

print('\nClosing connection.')
s.close()