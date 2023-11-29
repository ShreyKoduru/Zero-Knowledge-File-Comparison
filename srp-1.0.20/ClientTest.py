import socket
import srp

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    # SRP Client Logic
    username = 'user'
    password = 'password'

    usr = srp.User(username, password)
    uname, A = usr.start_authentication()

    # Send username and A to server
    client.send(username.encode())
    client.send(A.encode())

    # Receive salt and B from server
    salt = client.recv(1024).decode()
    B = client.recv(1024).decode()

    # Process challenge
    M = usr.process_challenge(salt, B)
    client.send(M.encode())

    # Receive HAMK from server and verify session
    HAMK = client.recv(1024).decode()
    usr.verify_session(HAMK)

    if usr.authenticated():
        print("Authentication Successful")
    else:
        print("Authentication Failed")

    client.close()

run_client()
