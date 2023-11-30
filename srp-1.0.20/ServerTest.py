import socket
import srp

def handle_client(client_socket):
    try:
        for j in range(5):
            for i in range(1, 6): 
                filepath = 'mockserverfiles/test copy' + str(i) + '.py'
                with open(filepath, "r") as f:
                    file_content = f.read()
            
                username = client_socket.recv(1024)
                A = client_socket.recv(1024)

                
                salt, vkey = srp.create_salted_verification_key(username, str(file_content))

                svr = srp.Verifier(username, salt, vkey, A)
                s, B = svr.get_challenge()

                
                client_socket.send(salt)
                client_socket.send(B)

    
                M = client_socket.recv(1024)
                HAMK = svr.verify_session(M)
                
        
                if HAMK is None:
                    print("Files Not the Same ")
                    HAMK = b'00000000000000000000000'
                    client_socket.send(HAMK)
                    continue
                
                client_socket.send(HAMK)

                if svr.authenticated():
                    print("Files are the Same")
                    
                else:
                    print("Files Not the Same")
            if j == 4:
                exit()
            
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
