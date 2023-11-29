import socket
import srp

def handle_client(client_socket):
    try:
        for i in range(1, 6):  # Assuming 5 files to compare
            filepath = '/Users/shreykoduru/Desktop/server files/test copy' + str(i) + '.py'
            with open(filepath, "r") as f:
                file_content = f.read()
        # Receive client's username and A value
            username = client_socket.recv(1024)
            A = client_socket.recv(1024)

            # Generate salt and verifier for the given username
            # This should be stored from the time of user registration
            salt, vkey = srp.create_salted_verification_key(username, str(file_content))

            svr = srp.Verifier(username, salt, vkey, A)
            s, B = svr.get_challenge()

            # Send salt and B to client
            client_socket.send(salt)
            client_socket.send(B)

            # Receive M from client and verify session
            M = client_socket.recv(1024)
            HAMK = svr.verify_session(M)
            
            #HAMK = b'r2\xa7\xd8\xfaXy\xbd\xfc\x0cN\xa4\x9b\xfaf\xb62\xef\x02\xcc'
            
            if HAMK is None:
                print("Files Not the Same ")
                HAMK = b'00000000000000000000000'
                client_socket.send(HAMK)
                continue

                
            

            # Send HAMK to client
            client_socket.send(HAMK)

            if svr.authenticated():
                print("Files are the Same")
                
            else:
                print("Files Not the Same")
            
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
            client_socket, _ = server.accept()
            handle_client(client_socket)
    finally:
        server.close()

run_server()
