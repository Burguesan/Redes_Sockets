#!/usr/bin/python
'''
    Simple socket server using threads
'''
 
import socket
import sys
import threading

items = []
movimentacoes = []

def cadastrarMateriaPrima(conn):
    global items
    #Receive Value
    data = conn.recv(1480) #default MTU size
    conn.send(b'ok')

    items.append([data, 0])
    print('Created item', data)

def consultarEstoque(conn):
    global items
    for item in items:
        conn.send(item[0])
        conn.recv(2)
        conn.send(bytes(str(item[1]),'utf-8'))
        conn.recv(2)
    
    conn.send(b'--fim--')

def entradaMateriaPrima(conn):
    global movimentacoes, items

    itemid = conn.recv(1480) #default MTU size
    itemid = int(itemid.decode())
    if itemid <= len(items):
        conn.send(b'ok')
        itemid -= 1
    else:
        conn.send(b'no')
        return
    quantidade = conn.recv(1480) #default MTU size
    quantidade = int(quantidade.decode())
    conn.send(b'ok')

    print('Recebi entrada de ' + str(quantidade) + ' para o item ' + str(items[itemid][0]))

    movimentacoes.append([itemid, 0, quantidade])
    items[itemid][1] += quantidade

def saidaMateriaPrima(conn):
    global movimentacoes, items

    itemid = conn.recv(1480) #default MTU size
    itemid = int(itemid.decode())
    if itemid > len(items):
        conn.send(b'no') #invalid item id
        return

    conn.send(b'ok')
    itemid -= 1
    quantidade = conn.recv(1480) #default MTU size
    quantidade = int(quantidade.decode())
    
    if quantidade > items[itemid][1]:
        conn.send(b'no') #quantity not available
        return

    conn.send(b'ok')

    print('Recebi saida de ' + str(quantidade) + ' para o item ' + str(items[itemid][0]))

    movimentacoes.append([itemid, 1, quantidade])
    items[itemid][1] -= quantidade

def consultarMovimentacoes(conn):
    global items, movimentacoes
    for movimentacao in movimentacoes:
        conn.send(items[movimentacao[0]][0]) #item name
        conn.recv(2)
        conn.send(bytes(str(movimentacao[1]),'utf-8')) #moviment type
        conn.recv(2)
        conn.send(bytes(str(movimentacao[2]),'utf-8')) #quantity
        conn.recv(2)

    conn.send(b'--fim--')

def server(conn,addr):
    print('Created a new thread server')

    while True:

        #Receive Option
        option = conn.recv(1)

        if option == b'0':
            break

        if option == b'1':
            cadastrarMateriaPrima(conn)
        elif option == b'2':
            consultarEstoque(conn)
        elif option == b'3':
            entradaMateriaPrima(conn)
        elif option == b'4':
            saidaMateriaPrima(conn)
        elif option == b'5':
            consultarMovimentacoes(conn)

    try:
        conn.close()
    except AttributeError:
        pass

    print('Closed connection with ' + addr[0] + ':' + str(addr[1]) )

if len(sys.argv) < 2:
    print('You need to inform a server port. Ex: python server.py 1213')
    exit()

SERVERNAME = bytes(sys.argv[1], 'utf-8') # python 3 needs to inform charset encoding on cast
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

    thread = threading.Thread(target=server, args=(conn,addr))
    thread.daemon = True
    thread.start()

