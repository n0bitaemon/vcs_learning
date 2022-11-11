# User ID controlled by request parameter with data leakage in redirect
Đăng nhập với tài khoản wiener:peter rồi truy cập /my-account?id=wiener, ta thấy bị chuyển hướng đến trang login. Như vậy không thể xem thông tin của user khác.

Tuy vậy, khi ta dùng BurpSuite bắt request này sẽ thấy response trả về có status code là 302, nhưng phần body của trang web (chứa thông tin của carlos) vẫn bị lộ ra.

![image](https://user-images.githubusercontent.com/103978452/201445219-fe38b500-ed48-43fd-9c73-2787d237466e.png)

Như vậy, ta có thể lấy được API key của user carlos.
