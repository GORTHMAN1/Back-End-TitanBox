import base64
import socket
import sys
import json


def send_file_to_server(file, port, address):
    """
    This function takes 3 parameters and send the file to the admin server side
    :param file: the file we want to send
    :param port: port
    :param address: adress
    :return: None
    """
    enc_data = base64.b64encode(file)
    # daca nu functioneaza asa incercam direct cu file
    jsonResult = {"file": enc_data}
    jsonResult = json.dumps(jsonResult)

    sock = socket.socket()

    try:
        sock.connect((address, port))
        sock.send(jsonResult)
    except socket.gaierror:
        print('There an error resolving the host')
        sys.exit()

    print(jsonResult, 'was sent!')
    sock.close()


def receive_file_from_client_side():
    """
    :return: None
    """
    sock = socket.socket()

    # filename = ''
    # numele unde se salveaza datele

    port = 0000
    # portul din proiect

    sock.bind(('', port))
    sock.listen(5)

    while True:
        file, addr = sock.accept()

        encoded_file = file.recv(1024)
        dec_data = base64.b64decode(encoded_file)
        # decodam daca am lasat varianta cu encode file

        print(dec_data)
        file.close()

        # with open(filename, "w") as f:
        # f.write(json.dumps(dec_data))
