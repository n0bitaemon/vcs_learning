import socket
import re
import mimetypes
import os
import sys
import getopt
from urllib.parse import urlparse

host = usr = pwd = path = None
port = 80
buffer_size = 1024
boundary = "----WebKitFormBoundaryDqHqvOH31XsoF7ih"

#Send POST /wp-login and retrieves authenticated cookies
def get_auth_cookies(username, password, host, port):
    #Config request
    payload = "log={username}&pwd={password}&wp-submit=Log+In".format(username=username, password=password)
    headers = ""\
        "POST /wp-login.php HTTP/1.1\r\n"\
        "Host: {host}\r\n"\
        "Content-Length: {content_length}\r\n"\
        "Content-Type: application/x-www-form-urlencoded\r\n"\
        "Connection: close\r\n"\
        "\r\n"\
    .format(host=host, content_length=len(payload))
    req = headers + payload 

    #Connect and read response
    res = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(req.encode())

            res = ""
            while True:
                data = s.recv(buffer_size)
                if(len(data) < 1):
                    break
                res += data.decode()
    except socket.error:
        print("Cannot connect to %s/wp-login.php" % host)
        print("Upload failed")
        exit(1)
    
    #Login fails
    if(not "Location: http://blogtest.vnprogramming.com/wp-admin/" in res):
        print("Wrong username or password")
        print("Upload failed")
        exit(6)

    auth_cookies = ""
    for line in res.split("\r\n"):
        if "Set-Cookie:" in line:
            auth_cookies += line.split(" ")[1]
    return auth_cookies

#Send GET /wp-admin/upload.php and get _wpnonce
def get_wpnonce(auth_cookies, host, port):
    #Config request
    req = ""\
        "GET /wp-admin/upload.php HTTP/1.1\r\n"\
        "Host: {host}\r\n"\
        "Cookie: {cookies}\r\n"\
        "Connection: close\r\n"\
        "\r\n"\
    .format(host=host, cookies=auth_cookies)

    #Connect and read response
    res = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(req.encode())

            while True:
                data = s.recv(buffer_size)
                if(len(data) < 1):
                    break
                res += data.decode()
    except socket.error:
        print("Cannot connect to %s/wp-admin/upload.php" % host)
        print("Upload failed")
        exit(2)

    #Search for _wpnonce value
    _wpnonce = re.search(r'"_wpnonce":"(.*?)"', res).group(1)
    return _wpnonce

def upload_file(path, auth_cookies, _wpnonce, host, port):
    #Config request
    #Read image's content
    content = b""
    try:
        with open(path, "rb") as f:
            while True:
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    break
                content += bytes_read
    except:
        print("Cannot open file with given path")
        print("Upload failed")
        exit(5)
    
    #Get mime type of the file
    mime_type = mimetypes.MimeTypes().guess_type(path)
    filename = os.path.basename(path).split('/')[-1]

    #Construct body
    payload = ""\
        "--{boundary}\r\n"\
        "Content-Disposition: form-data; name=\"name\"\r\n"\
        "\r\n"\
        "{filename}\r\n"\
        "--{boundary}\r\n"\
        "Content-Disposition: form-data; name=\"action\"\r\n"\
        "\r\n"\
        "upload-attachment\r\n"\
        "--{boundary}\r\n"\
        "Content-Disposition: form-data; name=\"_wpnonce\"\r\n"\
        "\r\n"\
        "{_wpnonce}\r\n"\
        "--{boundary}\r\n"\
        "Content-Disposition: form-data; name=\"async-upload\"; filename=\"{filename}\"\r\n"\
        "Content-Type: {mime_type}\r\n"\
        "\r\n"\
    .format(
        boundary = boundary,
        filename = filename,
        _wpnonce = _wpnonce,
        mime_type = mime_type
    )
   
    body = payload.encode() + content + "\r\n--{boundary}--".format(boundary=boundary).encode()
    content_length = len(body)

    #Construct headers
    headers = ""\
        "POST /wp-admin/async-upload.php HTTP/1.1\r\n"\
        "Host: {host}\r\n"\
        "Content-Type: multipart/form-data; boundary={boundary}\r\n"\
        "Cookie: {cookies}\r\n"\
        "Connection: close\r\n"\
        "Content-Length: {content_length}\r\n"\
        "\r\n"\
    .format(
        host=host,
        boundary = boundary,
        cookies = auth_cookies,
        content_length = content_length
    )

    req = headers.encode() + body 

    #Connect and read response
    res = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(req)

            while True:
                data = s.recv(buffer_size)
                if(len(data) < 1):
                    break
                res += data.decode()
    except:
        print("Cannot connect to %s/wp-admin/aysnc-upload.php" % host)

    #Get upload URL
    upload_url = re.search(r'"url":"(.*?)"', res).group(1).replace("\\", "")
    return upload_url

#Set host, usr, pwd, path
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "u:a:p:f:", ["url=", "user=", "password=", "local-file="])
except:
    print("Unexpected error")
    print("Upload failed")
    exit(1);

for opt, arg in opts:
    if opt in ["-u", "--url"]:
        host = urlparse(arg).hostname
    elif opt in ["-a", "--user"]:
        usr = arg
    elif opt in ["-p", "--password"]:
        pwd = arg
    elif opt in ["-f", "--local-file"]:
        path = arg
if not (host and usr and pwd and path):
    print("Invalid parameters")
    print("Upload failed")
    exit(2)

auth_cookies = get_auth_cookies(usr, pwd, host, port)
_wpnonce = get_wpnonce(auth_cookies, host, port)
upload_url = upload_file(path, auth_cookies, _wpnonce, host, port)
print(upload_url)
