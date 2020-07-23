from socket import *
import pymysql
from multiprocessing import Process
import time


class MysqlControler:
    def __init__(self, file="dict.txt", host="localhost", port=3306, user="root",
                 passwd="zhangl", database="eedict"):
        self.file = file
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.connect_mysql()

    def connect_mysql(self):
        try:
            self.db = pymysql.connect(host=self.host,
                                      port=self.port,
                                      user=self.user,
                                      passwd=self.passwd,
                                      database=self.database)
            self.cur = self.db.cursor()
        except Exception as e:
            print(e, "connect")

    def close(self):
        self.db.close()
        self.cur.close()

    def query(self, target):
        sql = "select value from dict where key1 = '%s' limit 1" % (target)
        self.cur.execute(sql)
        # print(self.cur.fetchall()[0][0])
        try:
            return self.cur.fetchall()[0][0]
        except IndexError:
            return "Not found"

    def login(self, user, passwd):
        sql = "select * from user where user = '%s'" % (user)

        if not self.cur.execute(sql):
            sql = "insert into user (user,passwd) values ('%s','%s')" % (user, passwd)
            try:
                self.cur.execute(sql)
            except Exception as e:
                print(e)
                self.db.rollback()
                return False
            self.db.commit()
            return True
        else:
            return False

    def log_in(self,user,passwd):
        sql = "select * from user where user = '%s'" % (user)
        try:
            if self.cur.execute(sql):
                data = self.cur.fetchall()
                print(data)
                if data[0][2] == passwd:
                    return True
        except Exception as e:
            print(e)

        return False

class TcpServer:
    def __init__(self, db):
        self.socket = socket()
        self.add = ("0.0.0.0", 9921)
        self.db = db
        self.connect()

    def handle(self, conn):
        self.socket.close()
        us = None
        while True:
            try:
                conn.send("欢迎使用NMM英英词典~".encode())
                time.sleep(0.5)
                conn.send("-=-=-=-=-=-=-=-=-=-=-=-=".encode())
                time.sleep(0.5)
                conn.send("输入 1 进行注册  输入 2 进行登录".encode())
                data = conn.recv(1024)
                # print(data)
                data = data.decode()
                # print(b"12".decode())
            except Exception as e:
                print(e,1)
                return
            print(data)
            if data == "1":
                conn.send("请输入帐号~".encode())
                user = conn.recv(1024)
                user = user.decode()
                conn.send("请输入密码~".encode())
                passwd = conn.recv(1024)
                passwd = passwd.decode()

                if self.db.login(user, passwd):
                    conn.send("注册成功 输入 1 输入帐号密码登录 输入 2 直接用注册帐号登录".encode())
                    data = conn.recv(1024)
                    data = data.decode()
                    if data == "2":
                        us = user
                        break
                    elif data == "1":
                        data = "2"
                else:
                    conn.send("注册失败 ".encode())
                    continue
            elif data == "2":
                conn.send("请输入帐号~".encode())
                user = conn.recv(1024)
                user = user.decode()
                conn.send("请输入密码~".encode())
                passwd = conn.recv(1024)
                passwd = passwd.decode()
                if self.db.log_in(user,passwd):
                    conn.send("登录成功~".encode())
                    us = user
                    break
                else:
                    conn.send("登录失败 请重新登录~".encode())


        while True:
            data = "尊敬的用户%s  请输入要查找的单词"%us
            conn.send(data.encode())
            data = conn.recv(1024)
            if data:
                data = self.db.query(data.decode())
                print(data)
                try:
                    conn.send(data.encode())
                except TypeError as e:
                    print(e)
                    print("nnn")
                    conn.send(b"Not found")
            else:
                return
            time.sleep(1)

    def connect(self):
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(self.add)
        self.socket.listen(5)
        while True:
            try:
                conn, add = self.socket.accept()
            except KeyboardInterrupt:
                print("exit")
                return




            print(add)
            p1 = Process(target=self.handle, args=(conn,))
            p1.start()
            conn.close()


if __name__ == '__main__':
    db = MysqlControler()
    start = TcpServer(db)
