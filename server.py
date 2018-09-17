import socket
import threading
import sqlite3

conn = sqlite3.connect('test', check_same_thread=False)

# 建立 TCP server socket 物件
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_ip = "120.105.129.104"
bind_port = 5050
server.bind((bind_ip, bind_port))
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):
    kind = client_socket.recv(1024).decode()
    print("kind=%s" % kind)
    date = client_socket.recv(1024).decode()
    print("date=%s" % date)
    if kind=="0":
        #sqlstr = "select * from lotto where datenumber='{}'".format(date)
        date = "第"+date+"期"
        sqlstr = "SELECT * FROM lotto WHERE datenumber='{}'".format(date)
        
    elif kind=="1":
        date = "第"+date+"期"
        sqlstr = "SELECT * FROM lotto2 WHERE datenumber='{}'".format(date)
        
    else:
        sqlstr = "SELECT * FROM invoice WHERE date='{}'".format(date)
        
    cursor = conn.execute(sqlstr)
    row = cursor.fetchone()
    if row==None:
        ans = "1 {} 不存在！".format(date)
    else:

        if kind=="0":
            ans = "2 "+row[1]+"+"+row[2]
        elif kind=="1":
            ans = "3 "+row[1]+"+"+row[2]
        else:
            ans = "4 "+row[1]
    
    print(ans)
    client_socket.send(str(ans).encode())
    client_socket.close()


while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

# server.close()