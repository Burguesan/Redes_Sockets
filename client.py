#!/usr/bin/python
'''
    Simple socket client
'''
 
import socket
import sys
import os
from prettytable import PrettyTable

if len(sys.argv) < 2:
    print('You need to inform server address and port. Ex: python client.py localhost 1213')
    exit()

def movimentacaoMateriaPrima(option, s):
    itemid = 0

    while itemid <= 0:
        try:
            itemid = int(input('Digite o id do item: '))
        except:
            pass
        if itemid <= 0:
            print('Digite um numero valido acima de 0')
    itemid = bytes(str(itemid), 'utf-8')

    s.send(option)
    s.send(itemid)
    response = s.recv(2)

    if response == b'no':
        print('Item ID nao encontrado.')
        return

    quantidade = 0
    while quantidade <= 0:
        try:
            quantidade = int(input('Digite a quantidade: '))
        except:
            pass
        if quantidade <= 0:
            print('Digite um numero valido acima de 0')
    quantidade = bytes(str(quantidade), 'utf-8')

    s.send(quantidade)
    response = s.recv(2)

    if response == b'no':
        print('Quantidade requisita acima do disponivel.')
        return

    print('Movimentacao de materia prima cadastrada com sucesso.')

def client():
    server, port = sys.argv[1], int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server, port))
    except:
        print('Connection refused.')
        return s

    resp = s.recv(1480)
    
    if resp != b'accept':
        return

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        print('1-Cadastrar materia prima')
        print('2-Consultar estoque')
        print('3-Entrada de materia prima')
        print('4-Solicitar saida de materia prima')
        print('5-Consultar ultimas movimentacoes')
        print('0-Sair')

        try:
            option = bytes(input('Escolha uma opcao: '),'utf-8') # python 3 needs to inform charset encoding on cast
            if option == b'0':
                s.send(option)
                break
            elif option == b'1':
                msg = bytes(input('Digite o nome do item: '),'utf-8')
                s.send(option)
                s.send(msg)
                s.recv(2)
                print('Item cadastrado com sucesso')
            elif option == b'2':
                s.send(option)
                itemid = 0

                tabela = PrettyTable(['ID', 'Materia Prima', 'Quantidade'])

                while True:
                    itemid += 1
                    item = s.recv(1480)
                    if item == b'--fim--':
                        break
                    s.send(b'ok')
                    quantidade = s.recv(1480)
                    s.send(b'ok')
                    tabela.add_row([itemid, item.decode(), quantidade.decode()])
                
                print(tabela)
            elif option == b'3' or option == b'4':
                movimentacaoMateriaPrima(option, s)
            elif option == b'5':
                s.send(option)
                movid = 0

                tabela = PrettyTable(['ID', 'Materia Prima', 'Tipo de Movimentacao', 'Quantidade'])

                while True:
                    movid += 1
                    item = s.recv(1480)
                    if item == b'--fim--':
                        break
                    s.send(b'ok')
                    tipo = s.recv(1480)
                    s.send(b'ok')
                    quantidade = s.recv(1480)
                    s.send(b'ok')
                    tabela.add_row([movid, item.decode(), 'Entrada' if tipo == b'0' else 'Saida' , quantidade.decode()])
                
                print(tabela)
            else:
                print('Opcao invalida')

            input("Aperte 'Enter' para continuar...")

        except KeyboardInterrupt:
            option = b'0'
            break
        except EOFError:
            option = b'0'
            break

    return s

s = client()

print('\nClosing connection.')
try:
    s.close()
except:
    pass