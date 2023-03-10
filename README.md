# CSCI-320 Mini-Project: UDP File Transfer


## Setup and Installation

This mini-project should be forked.  Forking the repo will create a copy on your own  GitHub repo.  Once the repo is forked, you can clone **YOUR** repo using PyCharm.  Submission entails committing and pushing your changes to your repo. 

## Introduction

This exercise aims to create a simple UDP file transfer system, where a client will send a file to a server, and the server will receive the file and save it to disk.  There are no limits on the size of the file.

In this mini-project, you will implement a simple protocol for file transfer over UDP.  Because the socket is UDP, the application layer is responsible for ensuring that the file is transferred without error.  While this algorithm addresses some of the reliability transfer issues, many problems related to reliable transfer still need to be addressed.

Note: This mini-project is intended to provide practice in socket programming.  File transfer should be done over a TCP socket.  This will be the subject of the next mini-project.

The algorithms described below implement the following simple protocol.

<figure style="text-align:center;">
	<img src="fileTransferProtocol.png" height="600"></div>
	<figcaption style="font-weight:bold; color:#0055ee;">Figure 1: Simple file transfer protocol.</figcaption>
</figure>

## 1. Implementing the Server

The server should:

1. Create a socket using the `socket` function and bind it to the (ip, port) pair. **(Implemented)**
2. Receive a message from the client using the `recvfrom` function.
3. Decompose the message into an 8-byte integer representing file size. The rest of the bytes should be decoded into a string representing the file name. Use `get_file_info()`.
4. send `b'go ahead'` message to the client.
5. To upload the file, Create an SHA256 object to compute the sha256 hash of the received file
6. Using the filename provided, open the file for writing using the with python statement. **NOTE: since you will be transferring a file over localhost to the same directory, it is important that you modify the filename, say by adding a *.temp* extension, to avoid overwriting the original file.** (Implemented)
7. Inside the *with* statement, 
	<ol type="a">
	<li>Receive a chunk of data.</li>
	<li>Write the data to the file.</li>
	<li>Update the sha256 hash.</li>
	<li> Send the message `b'received'` back to the client.  The client should not send the next chunk until a `b'received'` message is received by client.</li>
	<li>Continue to perform steps 7a-c until all bytes have been received.</li>
	</ol>
8. The server should then wait to receive the file hash calculated by the client and compare it to the hash calculated by the server.
9. If the hashes are the same, the server should send a 'success' message to the client; otherwise, it should remove the file and send a 'failed' message to the client.
10. Repeat steps 2 - 9. 

## 2. Implementing the Client

The client should:

1.	Obtain the name of the file to transfer from the command line using sys.argv. **(Implemented)**
2. Obtain the size of the file in bytes by using the os.path module.(use `get_file_size()`)
3. Convert the file size to an 8-byte string using big endian.
4. Create a SHA256 object using the hashlib module, to calculate the sha256 hash of the file.
5. Create a socket using the `socket` function. **(Implemented)**
6. Send the 8-byte file size concatenated with the encoded filename to the server.
7. Wait for the server to send `b'go ahead'` message. If any other message is sent, `raise Exception('Bad server response - was not go ahead!')`
8. Open the file for reading in binary mode using the *with* python statement.
	<ol type="a">
	<li>Read a chunk of data from the file.</li>
	<li>If the length of the chunk > 0, then
	<ol type="i">
	<li>Update the hash.</li>
	<li>Send the chunk to the server.</li>
	<li>Receive a 'received' acknowledgment from the server. If a message other than 'received' is received, then `raise Exception('Bad server response - was not received')`.</li>
	</ol>
	</li>
	<li>If the length of the chunk read is 0, then go to step 9. No more chunks to read and send.</li>
	<li>Repeat steps 8a - 8d</li>
	</ol>
9. Send the server the calculated hash value as a byte string.
10. Receive a `b'success'` or `b'failed'` message.  
11. If a `b'failed'` message is received, ```raise Exception('Transfer failed!')``` else `print('Transfer completed!')`
12. Close the client socket. **(Implemented)**

## 3. Testing Your Implementation

You can test your implementation by running the server and client on the same machine. Make sure to run the server first and then the client. **<span style="color:red">NOTE: as mentioned in section 1 above, it is important that you modify the filename, say by adding a *.temp* extension, to avoid overwriting the original file.</span>** This has already been done on the server's with statement. Such a filename change is only necessary when running both server and client on the same machine and using the same working directory. You do not have to modify the filename if you set the run configuration of the server to use a different working directory from that of the client.

Your instructor will provide further information as to how to test both your client and server on a remote instance.

## 4. Submitting This Work

You are required to commit and push your code to your forked repo.


## Tips

- Make sure to handle errors in your code.
- Pay attention to the TODO tasks and how they are mapped to the algorithm steps above.  This will help guide you in implementing the code.
- Read the Python documentations for the hashlib, sys, os, and os.path modules along with associated examples.  Avoid Googling the answer as this will get you into the habit of reading documentaton.

Good luck and happy coding!
