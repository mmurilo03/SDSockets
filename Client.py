import socket
import threading
import sys

nickname = ""
stop = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 3000))
command = input("Digite seu nick com !nick: ")
if (command.startswith("!nick ")):
    nickname = command.removeprefix("!nick ")
    client.send(command.encode('ascii'))
else:
    print("Inicie a mensagem com !nick para definir seu usuário.")
    client.close()

def receive_msg():
    while True:
        try:
            message = client.recv(1024).decode("ascii")

            if (message.startswith("!users ")):
                users = message.removeprefix("!users ")
                print(f"Online agora: {users}")
            elif (message.startswith("!msg ")):
                receivedMessage = message.removeprefix("!msg ")
                messageNickname = receivedMessage.split(" ")[0]
                messageContent = receivedMessage.removeprefix(f"{messageNickname} ")
                print(f"{messageNickname}: {messageContent}")
            elif (message.startswith("!changenickname ")):
                receivedMessage = message.removeprefix("!changenickname ")
                nickname1 = receivedMessage.split(" ")[0]
                nickname2 = receivedMessage.split(" ")[1]
                print(f"O usuário {nickname1} trocou de nome e agora é {nickname2}")
            elif (message.startswith("!poke ")):
                receivedMessage = message.removeprefix("!poke ")
                nickname1 = receivedMessage.split(" ")[0]
                nickname2 = receivedMessage.split(" ")[1]
                print(f"O usuário {nickname1} cutucou {nickname2}")
            elif (message.startswith("!left ")):
                receivedMessage = message.removeprefix("!left ")
                print(f"O usuário {receivedMessage} saiu")
            else:
                print(message)
        except:
            print("Você foi desconectado.")
            client.close()
            stop_connect()
            break

def write_msg():
    while True:
        if (stop):
            stop_connect()
        global nickname
        if (len(nickname) >= 1):
            message = input("")
            if (not message.startswith("!sendmsg ") and not message.startswith("!changenickname ") and not message.startswith("!poke ")): 
                print("Comando inválido, use apenas os comandos: !sendmsg <mensagem> | !changenickname <novo-nick> | !poke <nome-de-usuario>")
            else :
                client.send(message.encode('ascii'))
            
def stop_connect():
    global stop
    stop = True
    sys.exit()
        
receive_msg_thread = threading.Thread(target=receive_msg)
receive_msg_thread.start()

write_msg_thread = threading.Thread(target=write_msg)
write_msg_thread.start()