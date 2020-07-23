from socket import *


def tcp_conn():
    sockfd = socket()
    sockfd.connect(("0.0.0.0", 9921))
    while True:
        try:
            data = input("send:")
            sockfd.send(data.encode())
            data = sockfd.recv(1024)
            print(data.decode())
        except KeyboardInterrupt:
            print("exit")
            return


if __name__ == '__main__':
        tcp_conn()
