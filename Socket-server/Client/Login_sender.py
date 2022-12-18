import  socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_OP=255
LOGIN_OP=0
REGISTER_OP=1
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg, op):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_length = str(msg_lenght).encode(FORMAT) + b':' + str(op).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

user=input("User:")
passwd=input("Parola:")
send(f'{user}:{passwd}', REGISTER_OP)
send(f'{user}:{passwd}', LOGIN_OP)
send("DISCONNECT", DISCONNECT_OP)






