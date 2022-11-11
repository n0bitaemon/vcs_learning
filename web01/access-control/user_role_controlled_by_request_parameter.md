# User role controlled by request parameter
Sau khi đăng nhập với tài khoản wiener:peter, ta không truy cập được /admin vì không có quyền.
Nhận thấy trong cookie có Admin=false, như vậy trang web sử dụng cookie này để kiểm tra người dùng có quyền hay không. Ta thử thay đổi Admin=true rồi tải lại trang, truy cập được vào trang admin.

![image](https://user-images.githubusercontent.com/103978452/201270837-187dcdde-59b1-4035-ae50-a049069f6bb4.png)

Từ trang admin ta xóa user carlos, kết quả thành công.
