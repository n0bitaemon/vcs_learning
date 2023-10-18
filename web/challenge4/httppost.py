import socket
import sys
import getopt
from urllib.parse import urlparse

port = 80
usr = pwd = host = None

#Set host, usr, pwd
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:a:p:", ["url=", "user=", "password="])
except:
    print("Syntax error")
    exit(1);
for opt, arg in opts:
    if opt in ["-u", "--url"]:
        host = urlparse(arg).hostname
    elif opt in ["-u", "--user"]:
        usr = arg
    elif opt in ["-p", "--password"]:
        pwd = arg

if(not (host and usr and pwd)):
    print("Parameters not valid")
    exit(3)

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
        host = host,
    )
req = headers + payload

res = ""
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(req.encode())

        while True:
            data = s.recv(1024)
            if(len(data) < 1):
                break
            res += data.decode()
except socket.error:
    print("Cannot connect to", host)
    exit(4)

if("Location: http://blogtest.vnprogramming.com/wp-admin/" in res):
    print("User", usr, "dang nhap thanh cong")
else:
    print("User", usr, "dang nhap that bai")
