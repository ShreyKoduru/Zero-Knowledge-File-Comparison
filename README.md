# Hash Hounds CS 355 Implementation Project
Version 1.0

### Introduction
This implementation of SRP intends to fulfill the criteria of the CS project. It is heavily based on Tom Cocagne’s ‘pysrp’ library and is made entirely in python. It connects two users with 5 files each and checks if the contents of those files match or not in a Zero Knowledge manner. 

### Specifications
This project implements a secure file comparison protocol between two parties - referred to as Alice and Bob - without revealing the contents of the files being compared. Utilizing socket programming and Secure Remote Password (SRP) protocols, this system ensures that both parties can verify if they possess the same file contents without any direct file content exchange.

This implementation of SRP intends to fulfill the criteria of the CS 355 project. It is heavily based on Tom Cocagne’s ‘pysrp’ library and is made entirely in python. It connects two users with 5 files each and checks if the contents of those files match or not, in a Zero Knowledge manner. 

### Key Components
- Communication - Established using socket programming, facilitating the exchange of protocol-related messages, including ciphertext, signatures, or MACs necessary for different phases of the protocol.
- Protocol - Interactive protocol execution to perform secure file comparison without revealing actual file contents.

### Implementation Details
- Communication - This project is intended for users to interact in a server client structure. One user will choose to be the server while the other is the client, similar to a peer to peer connection. For the purposes of this project the ‘server’ user must pass his ip to the client user and be on the same network (in our testing we connected via client’s laptop hotspot).
- Language & Libraries:
  - Language - Python
  - Main Libraries: socket for networking, pysrp for implementing SRP protocol.
- Socket Programming - Used to create a communication channel between Alice and Bob, allowing for the transmission of SRP-related data.
- SRP Protocol - Ensures that each party can verify the presence of identical files through cryptographic means without exposing file data. 
### Security Goals and Analysis
- SRP:
  - SRP stands for Secure Remote Password (protocol) and enables a client to prove to a server that they are in possession of some password, all without sending the passwords or any information that could possibly reconstruct the password. SRP is a type of Password Authenticated Key Exchange which generally follows that pattern. SRP initially exchanges public keys which is at least as strong as Diffie Hellman.
- File Content Confidentiality:
  - Goal - Ensure that the user's file content is never exposed, not even to the server or any eavesdroppers. With all the information from the users’ exchange, no meaningful information about the file content can be extracted.
  - Achievement - In SRP, the file content is never transmitted over the network. Instead, a verifier (derived from the file content, salt, and username) is stored on the server. During authentication, only values derived from the file content are exchanged, not the file content itself.
- Protection Against Eavesdropping:
  - Goal - Prevent eavesdroppers from gaining useful information by listening to the authentication exchange.
  - Achievement - The exchanged values in SRP (like the public values A and B) do not reveal the password or the session key. The difficulty of the discrete logarithm problem underpins the security against eavesdropping.
- Resistance to Man-in-the-Middle (MitM) Attacks:
  - Goal - Prevent attackers from intercepting or altering the authentication process.
  - Achievement - SRP includes mutual verification steps where both client and server prove knowledge of the password (or its verifier) without revealing it. Successful mutual authentication ensures that both parties are legitimate and that a MitM attacker cannot impersonate either side.

### Usage
- Connection:
  - See ‘communication’ section


- Both Users:
  - For the purpose of portability we have provided mock client and server files.
  - For real world testing server and client can change the directory (line 11 for ClientTest.py for client’s use and line 8 for ServerTest.py) in their respective file to point to the location of a folder containing only those 5 files.
  - Both server and client must ensure that the 5 files they wish to compare are named in the following scheme: [name_of_file][n].py
    - Where n is 1 to 5
    - And [name_of_file] stays constant
  - The directory then should be changed to’ /folder_with_5_files_path/[name_of_file]’ while keeping the + str(i)... the same.
  - Furthermore in this real world testing scenario, ensure that both users have the ip address of the server (line 7 in ClientTest.py and line 52 on ServerTest.py) have the ip address of the server.
- Server (Alice):
  - Run ServerTest.py to initiate the server on Alice's machine.
  - Server listens for connection from the client (Bob).
- Client (Bob):
  - Run ClientTest.py to start the client on Bob's machine.
  - Client connects to the server and initiates the file comparison protocol.
- Both Users:
  - Observe the terminal to see if there is a match.

### Repository Structure
Main implementations are within ServerTest.py, and ClientTest.py:
- ServerTest.py - Server-side implementation.
- ClientTest.py - Client-side implementation.
- mockclientfiles - Directory containing client’s test files (for portability).
- mockserverfiles - Directory containing server’s test files

### Additional Notes
- Ensure that the server and client are executed in the proper order.
- The system is designed for demonstration purposes and might require additional security measures for production deployment.
