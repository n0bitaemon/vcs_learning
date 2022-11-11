# User ID controlled by request parameter, with unpredictable user IDs
Đăng nhập tài khoản wiener:peter rồi click vào "My account", ta thấy trang chuyển hướng tới /my-account?id=43b37354-3032-4fea-ac2a-33adb2af46bd. Như vậy id của users là một chuỗi các kĩ tự và không thể đoán được.

Truy cập vào trang chủ và vào xem chi tiết một bài viết bất kỳ, rồi dùng dev tool để inspect tên tác giả, ta thấy một đường dẫn chứa ID của người đó.

![image](https://user-images.githubusercontent.com/103978452/201379128-da76ce74-5d2d-4015-b736-3e81480afc42.png)

Như vậy, ta có thể lấy thông tin ID của bất kỳ ai nếu họ là tác giả của một bài viết nào đó. Tìm trong danh sách ta thấy có bài "Football for dummies" được viết bởi carlos. Dùng dev tools ta lấy được id của user carlós là 4ded5e75-ca32-4644-9841-7651d6b52fb3

![image](https://user-images.githubusercontent.com/103978452/201380351-7d568e15-365b-445a-93f1-c45afb958c29.png)

Truy cập /my-account?id=4ded5e75-ca32-4644-9841-7651d6b52fb3, ta lấy được API key của carlos.
