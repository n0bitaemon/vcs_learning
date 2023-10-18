import socket
import re
import html
import sys
import getopt
from urllib.parse import urlparse

port = 80
host = None

#Set host
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:", ["url="])
except:
    print("Syntax error")
    exit(1);

for opt, arg in opts:
    if opt in ["-u", "--url"]:
        host = urlparse(arg).hostname

if not host:
    print("Invalid parameters")
    exit(2)

headers = """
GET / HTTP/1.1\r
Host: {host}\r
Connection: close\r
\r\n""".format(host=host)

content = ""
try: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(headers.encode())

        #Get response
        while True:
            data = s.recv(1024)
            if(len(data) < 1):
                break
            content += data.decode()
except socket.error:
    print("Cannot connect to", host)
    exit(3)

#Search for title
try:
    title = re.search(r"<title>(.*?)</title>", content).group(1)
    print(html.unescape(title))
except:
    print("The website has no title")
    exit(4)
