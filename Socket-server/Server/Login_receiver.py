import socket
import threading
import mysql.connector
#necesita mysql-connector-python

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = "85.120.207.243"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
DB_USER="YOUR_USER_HERE"
DB_PASS="YOUR_PASSWORD_HERE"
DB_HOST="localhost"
DB_BASE='user_server'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def verify_user(name, password):
    db = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_BASE)
    cursor=db.cursor()
    query=f"SELECT * FROM users WHERE username='{name}' and password='{password}';"
    cursor.execute(query)
    results=cursor.fetchall()
    if len(results) == 1:
        found = True;
    else:
        found = False;
    cursor.close()
    db.close()
    return found

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MSG:
                connected = False
                conn.send("Disconnecting...".encode(FORMAT))
            else:
                credentials=msg.split(":")
                ok=verify_user(credentials[0], credentials[1])
                if ok == True:
                    conn.send("Autentificat".encode(FORMAT))
                else:
                    conn.send("User sau parola incorecte".encode(FORMAT))
    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
