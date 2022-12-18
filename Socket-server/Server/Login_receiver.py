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
DISCONNECT_OP=255
LOGIN_OP=0
REGISTER_OP=1
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
    query=f"SELECT path FROM users WHERE username='{name}' and password='{password}';"
    cursor.execute(query)
    results=cursor.fetchall()
    path=""
    if len(results) == 1:
        found = True
        path=results[0][0]
    else:
        found = False
    cursor.close()
    db.close()
    return found, path

def add_user(name, password):
    db = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_BASE)
    cursor=db.cursor()
    query=f"SELECT username FROM users WHERE username='{name}';"
    cursor.execute(query)
    results=cursor.fetchall()
    path=""
    if len(results) !=0:
        ok=False
    else:
        ok=True
        query=f"INSERT INTO users (username, password) VALUES ('{name}', '{password}');"
        cursor.execute(query)
        query=f"SELECT id FROM users WHERE username='{name}';"
        cursor.execute(query)
        path="/user_" + str(cursor.fetchall()[0][0])
        query=f"UPDATE users SET path='{path}' WHERE username='{name}';"
        cursor.execute(query)
    cursor.close()
    db.commit()
    db.close()
    return ok, path

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        headers = conn.recv(HEADER).decode(FORMAT).split(":")
        msg_length=headers[0]
        op=headers[1].strip()
        if msg_length and op:
            msg_length = int(msg_length)
            op=int(op)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] OP:{op}, {msg}")
            if op==DISCONNECT_OP:
                connected = False
                conn.send("Disconnecting...".encode(FORMAT))
            if op==LOGIN_OP:
                credentials=msg.split(":")
                ok, path=verify_user(credentials[0], credentials[1])
                if ok == True:
                    conn.send(f"{path}".encode(FORMAT))
                else:
                    conn.send("User sau parola incorecte".encode(FORMAT))
            if op==REGISTER_OP:
                credentials=msg.split(":")
                ok, path=add_user(credentials[0], credentials[1])
                if ok == True:
                    conn.send(f"{path}".encode(FORMAT))
                else:
                    conn.send("Numele este folosit deja".encode(FORMAT))
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
