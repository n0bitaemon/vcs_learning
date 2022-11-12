# Basic password reset poisoning
Thử chức năng reset password với user wiener, ta thấy URL chứa token được gửi về email. Khi thử thay đổi HTTP header Host thành example.com thì domain trong URL cũng bị thay đổi thành example.com. Như vậy server tạo URL dựa trên Host header.

Ta tạo một password-reset request với tài khoản của carlos và chỉnh sửa HTTP Host header thành exploit-server của mình, sau đó nhấn submit. Vào Access-log trong exploit-server, ta thấy được một request gửi đến chứa token. Đó chính là token reset password của user carlos

![image](https://user-images.githubusercontent.com/103978452/201499254-7957129b-6794-4929-a161-496b63aab9fe.png)

Truy cập website bằng URL chứa token đã thu được, rồi đổi mật khẩu của carlos. Sử dụng thông tin đã có để đăng nhập, kết quả thành công
