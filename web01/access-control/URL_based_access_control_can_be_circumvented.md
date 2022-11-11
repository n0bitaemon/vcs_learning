# URL-based access control can be circumvented
Đầu tiên ta đăng nhập với tài khoản wiener:peter rồi bắt request tới /admin, kết quả trả về "Access Denied"

Ta thử dùng HTTP header "X-Original-URL: /admin" để ghi đè lên URL gốc, kết quả trả về trang admin thành công.

Tiếp theo, config request sao cho có query parameter là username=carlos, cùng với header "X-Original-URL: /admin/delete" để xóa user carlos. Kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/201358056-3c7e0c09-5e68-4605-b291-25e6dc4c050c.png)
