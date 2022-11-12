# Multi-step process with no access control on one step
Thử đăng nhập với tài khoản administrator:admin, ta thấy trong Admin panel có chức năng upgrade/downgrade một user bất kỳ. Dùng BurpSuite để bắt request, ta thấy chỉ khi có biến confirmed=true trong request body (sau khi nhấn nút xác nhận) thì hành động mới được thực hiện.

Đăng nhập với tài khoản wiener:peter rồi thực hiện request tới /admin-roles, với các tham số action=upgrade&confirmed=true&username=wiener, kết quả upgrade thành công.

![image](https://user-images.githubusercontent.com/103978452/201459489-4197b6b9-461b-45f9-8eb0-3893c6759736.png)
