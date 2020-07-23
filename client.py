from multiprocessing import Process
from socket import *


def receive(sockfd):
    # print("12")
    while True:
        data = sockfd.recv(1024)
        # print(data)
        if  data:
            print(data.decode()+"\n")
            print()
        else:
            return

def tcp_conn():
    sockfd = socket()
    sockfd.connect(("0.0.0.0", 9921))
    p1 = Process(target=receive, args=(sockfd,))
    p1.start()
    while True:
        try:
            data = input("send:")
            sockfd.send(data.encode())

            print("2")

        except KeyboardInterrupt:
            print("exit")
            return


if __name__ == '__main__':
    tcp_conn()
