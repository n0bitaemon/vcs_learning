# User role can be modified in user profile
Đăng nhập với tài khoản wiener:peter ta thấy không truy cập được tới /admin.
Bắt request /change-email rồi thêm trường "roleid":2 vào chuỗi json được gửi đi, ta thấy kết quả trả về thành công.

![image](https://user-images.githubusercontent.com/103978452/201271770-d50a7a7e-e264-475f-8827-6ad440d10b2b.png)

Thử truy cập lại vào trang /admin, truy cập thành công và xóa người dùng carlos.
