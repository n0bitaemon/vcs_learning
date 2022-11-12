# Referer-based access control
Đăng nhập với tài khoản administrator:admin, ta thấy trong Admin panel có chức năng thăng cấp/hạ cấp một user bất kỳ. Dùng BurpSuite để bắt request khi thăng cấp user carlos, request GET /admin-roles?username=carlos&action=upgrade được gửi đi.

Trong HTTP header có Referer, ta thử xóa đi thì thấy lỗi "Unauthorized" xuất hiện. Như vậy việc phân quyền dựa vào HTTP header Referer.

Đăng nhập với tài khoản wiener:peter rồi gửi request đến /admin-roles?username=wiener&action=upgrade, cùng với HTTP header "Referer: https://0a7f003003e9668ac082149a0088002f.web-security-academy.net/admin". Sau khi submit, ta thu được kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201468890-7b7eb020-6804-4e05-bee4-2bb3e1f73088.png)
