#!/usr/bin/env python3

import socket
import re
import html
import sys
import getopt

PORT = 80
ENCODING = "utf-8"
HOST = "blogtest.vnprogramming.com"

#Set --url argument value to HOST
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:", ["url="])
except:
    print("Unexpected error")
    exit(1);

if(len(opts) == 0):
    print("No --url parameter specified")
    exit(2)

for opt, arg in opts:
    if opt in ["-u", "--url"]:
        HOST = arg

headers = """
GET / HTTP/1.1\r
Host: {host}\r
Connection: close\r
\r\n""".format(host=HOST)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(headers.encode())
content = ""
while True:
    data = s.recv(1024)
    if(len(data) < 1):
        break
    content += data.decode()
s.close()

try:
    title = re.search(r"<title>(.*?)</title>", content).group(1)
    print(html.unescape(title))
except:
    print("Cannot get title of the webpage")
    exit(2)
