import socket
import sys
import getopt
from urllib.parse import urlparse

remote_file = host = ""
port = 80

#Set host, remote_file
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:r:", ["url=", "remote-file="])
except:
    print("Unexpected error")
    exit(1);

for opt, arg in opts:
    if opt in ["-u", "--url"]:
        host = urlparse(arg).hostname
    if opt in ["-r", "--remote-file"]:
        remote_file = arg

if not host or not remote_file:
    print("Invalid parameters")
    exit(2)

req = """\
GET {file} HTTP/1.1\r
Host: {host}\r
Connection: close\r
\r\n""".format(host=host, file=remote_file)

res = b""
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(req.encode())

        res = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            res += data
except socket.error:
    print("Cannot connect to", host)
    exit(3)

if b"404 Not Found" in res:
    print("File not found")
    exit(4)
for line in res.split(b"\r\n"):
    if b"Content-Length:" in line:
        filesize = int(line.split()[1])
        break

res_headers = res.split(b"\r\n\r\n")[0]
image = res.split(b"\r\n\r\n")[1]

with open(remote_file.split("/")[-1], "wb") as f:
    f.write(image)

print("Image's size:", str(filesize), "bytes")
