import pymysql
import re


class StorageSql:
    def __init__(self, file="dict.txt", host="localhost", port=3306, user="root",
                 passwd="zhangl", database="eedict"):
        self.file = file
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.connect_mysql()
        self.storage()
        self.close()

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

    def storage(self, pattern="  +"):
        fd = open(self.file, "r")
        data = fd.readline()
        while data:
            data1 = re.findall("^\w*", data)
            data2 = re.sub("(%s +)|\n" % (data1[0]), "", data)
            # print('========')
            # print(data1)
            # print(data2)
            # print('========')
            sql = "insert into dict (key1,value ) values (%s,%s) "
            # print(data)
            try:
                self.cur.execute(sql, [data1[0], data2])
            except Exception as e:
                self.db.rollback()
                print(e, )
                return False
            self.db.commit()
            data = fd.readline()
        print("finished")
        return True


# fd = open("dict.txt", "r")
# for i in range(50):
#     data = fd.readline()
#
#     print(data_result)
#     print("".join(re.findall(".+", data_result[1])))
#     print("555")
if __name__ == '__main__':
    db = StorageSql()
