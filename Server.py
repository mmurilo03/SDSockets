import socket
import threading

host = '127.0.0.1'
port = 3000
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def sendAll(msg):
    for client in clients:
        client.send(msg)

def runClient(client):
    while True:
        try:
            command = client.recv(1024).decode('ascii')
            if (command.startswith("!sendmsg ")):
                clientIndex = clients.index(client)
                nickname = nicknames[clientIndex]
                msg = f"!msg {nickname} {command.removeprefix('!sendmsg ')}"
                print(f"{nickname}: {command.removeprefix('!sendmsg ')}")
                sendAll(msg.encode("ascii"))
            elif (command.startswith("!changenickname ")):
                clientIndex = clients.index(client)
                newNick = command.removeprefix('!changenickname ').replace(" ", "-")
                msg = f"!changenickname {nicknames[clientIndex]} {newNick}"
                print(f"O usuário {nicknames[clientIndex]} trocou de nome e agora é {newNick}")
                nicknames[clientIndex] = newNick
                sendAll(msg.encode("ascii"))
            elif (command.startswith("!poke ")):
                clientIndex = clients.index(client)
                msg = f"!poke {nicknames[clientIndex]} {command.removeprefix('!poke ')}"
                nicknames[clientIndex] = command.removeprefix('!poke ')
                print(f"O usuário {nicknames[clientIndex]} cutucou {command.removeprefix('!poke ')}")
                sendAll(msg.encode("ascii"))
            else:
                print(command)

        except:
            clientIndex = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[clientIndex]
            sendAll(f"!left {nickname}".encode("ascii"))
            nicknames.remove(nickname)
            break


def connect():
    while True:
        client, address = server.accept()
        print(f"Conexão estabelecida com {str(address)}")
        
        try:
            msg = client.recv(1024)
            msg = msg.decode('ascii')

            if (msg.startswith("!nick ")):
                nickname = msg.removeprefix("!nick ")
                nickname = nickname.replace(" ", "-")
                nicknames.append(nickname)
                clients.append(client)

                sendAll(f"!users {len(nicknames)} {' '.join(nicknames)}".encode('ascii'))
                
                print(f"O nick do cliente conectado é {nickname}")
                
                thread = threading.Thread(target=runClient, args=(client,))
                thread.start()
        except:
            client.close()
            break

print(f"Servidor sendo executado na porta {port}")
connect()