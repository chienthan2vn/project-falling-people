import cv2
import socket
import pickle
import struct
import pandas as pd

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")

    """ Server has accepted the connection from the client. """
    sever, addr = server.accept()
    while True: 
        print(f"[NEW CONNECTION] {addr} connected.")
        """ Receiving the filename from the client. """
        data1 = sever.recv(1024).decode()
        # if not data:
        #     print(f"{addr} đã ngắt kết nối")
        #     break
        
        data2 = sever.recv(1024).decode()

        data = b''
        payload_size = struct.calcsize("L")

        while len(data) < payload_size:
            data += sever.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += sever.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        df = pd.read_csv('./data/check.csv')
        a = {'time':data1, 'link_image':'./static/' + data2 + '.png'}
        df = df.append(a, ignore_index=True, sort=False)
        df.to_csv('./data/check.csv', index=False)

        cv2.imwrite('./image/' + data2 + '.png', frame)


if __name__ == "__main__":
    main()
