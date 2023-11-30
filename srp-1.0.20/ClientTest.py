import socket
import srp

def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.137.129', 5005))
    
    for j in range(1,6):
        for i in range(5):
            with open('mockclientfiles/test' + str(j) + '.py',"r") as f:
                string = f.read()
            
            username = 'user'
            password = string
            
            usr = srp.User(username, str(password))
            uname, A = usr.start_authentication()

            client.send(username.encode())
            client.send(A)

            salt = client.recv(1024)
            B = client.recv(1024)

            M = usr.process_challenge(salt, B)
            client.send(M)

            HAMK = client.recv(1024)
            if HAMK == '00000000000000000000000':
                print("FILES ARE NOT THE SAME")
                continue
            
            usr.verify_session(HAMK)

            if usr.authenticated():
                print("FILES ARE THE SAME")
            else:
                print("FILES ARE NOT THE SAME")
                
                
        
    client.close()

run_client()
