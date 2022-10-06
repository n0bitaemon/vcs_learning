#!/usr/bin/env python3
import socket
import sys
import getopt

HOST = "blogtest.vnprogramming.com"
PORT = 80

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:p:", ["user=", "password="])
except:
    print("Unexpected error")
    exit(1);

if(len(opts) != 2):
    print("The program requires 2 parameters")
    exit(2)

usr = ""
pwd = ""
for opt, arg in opts:
    if opt in ["-u", "--user"]:
        usr = arg
    if opt in ["-p", "--password"]:
        pwd = arg
payload = "log={usr}&pwd={pwd}&wp-submit=Log+In".format(usr=usr,pwd=pwd)
headers = """\
POST /wp-login.php HTTP/1.1\r
Host: blogtest.vnprogramming.com\r
Content-Length: {content_length}\r
Content-Type: application/x-www-form-urlencoded\r
Connection: close\r
\r
""".format(
        content_length = len(payload),
        host = HOST,
    )
req = headers + payload
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(req.encode())

res = ""
while True:
    data = s.recv(1024)
    if(len(data) < 1):
        break
    res += data.decode()

if("Location: http://blogtest.vnprogramming.com/wp-admin/" in res):
    print("User", usr, "dang nhap thanh cong")
else:
    print("User", usr, "dang nhap that bai")
