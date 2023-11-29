import socket
import srp

def handle_client(client_socket):
    try:
        # Receive client's username and A value
        username = client_socket.recv(1024)
        A = client_socket.recv(1024)

        # Generate salt and verifier for the given username
        # This should be stored from the time of user registration
        with open('/Users/shreykoduru/Desktop/server files/test copy1.py',"r") as f:
            string = f.read()
        print(string)
        salt, vkey = srp.create_salted_verification_key(username, str(string))

        svr = srp.Verifier(username, salt, vkey, A)
        s, B = svr.get_challenge()

        # Send salt and B to client
        client_socket.send(salt)
        client_socket.send(B)

        # Receive M from client and verify session
        M = client_socket.recv(1024)
        HAMK = svr.verify_session(M)

        if HAMK is None:
            print("authentification Failed")
            client_socket.close()
            exit(0)

        # Send HAMK to client
        client_socket.send(HAMK)

        if svr.authenticated():
            print("Files are the Same")
            client_socket.close()
            exit(0)

        else:
            print("Files Not the Same")
            client_socket.close()
            exit(0)

    finally:
        client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.137.129', 5005))
    server.listen(5)
    print("Server listening on port 12345")

    try:
        while True:
            client_socket,  = server.accept()
            print("accept")
            handle_client(client_socket)
    finally:
        server.close()

run_server()