import base64
import socket
import os
import hashlib  # needed to verify file hash


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8],byteorder='big')


def upload_file(server_socket: socket, file_name: str, file_size: int):
    # create a SHA256 object to verify file hash
    verify_file = hashlib.sha256(file_name.encode())

    # create a new file to store the received data
    with open(file_name+'.temp', 'wb') as file:

        bytes_received = 0
        while bytes_received < file_size:
            chunk, address = server_socket.recvfrom(BUFFER_SIZE)
            file.write(chunk)
            bytes_received += chunk
            verify_file.update(chunk)
            server_socket.sendto(b'received', address)


    # get hash from client to verify
    verify_client_hash, address = server_socket.recv(BUFFER_SIZE)
    verify_client_hash = verify_client_hash.decode()
    server_hash = verify_file.digest()

    if verify_client_hash == server_hash:
        server_socket.sendto(b'success', address)
    else:
        os.remove(file_name+'.temp')
        server_socket.sendto(b'failed', address)



def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:

            # expecting an 8-byte byte string for file size followed by file name
            info, address = server_socket.recvfrom(BUFFER_SIZE)
            file_name, file_size = get_file_info(info)

            server_socket.sendto(b'go ahead', address)
            upload_file(server_socket, file_name, file_size)
    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        print(f'An error occurred while receiving the file:str {e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
