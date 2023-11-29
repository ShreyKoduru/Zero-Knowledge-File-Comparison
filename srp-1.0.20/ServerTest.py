import socket
import srp

def handle_client(client_socket):
    try:
        # Receive client's username and A value
        username = client_socket.recv(1024).decode()
        A = client_socket.recv(1024).decode()

        # Generate salt and verifier for the given username
        # This should be stored from the time of user registration
        salt, vkey = srp.create_salted_verification_key(username, 'password')

        svr = srp.Verifier(username, salt, vkey, A)
        s, B = svr.get_challenge()

        # Send salt and B to client
        client_socket.send(salt.encode())
        client_socket.send(B.encode())

        # Receive M from client and verify session
        M = client_socket.recv(1024).decode()
        HAMK = svr.verify_session(M)

        # Send HAMK to client
        client_socket.send(HAMK.encode())

        if svr.authenticated():
            print("Authentication Successful")
        else:
            print("Authentication Failed")
    finally:
        client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Server listening on port 12345")

    try:
        while True:
            client_socket, _ = server.accept()
            handle_client(client_socket)
    finally:
        server.close()

run_server()
