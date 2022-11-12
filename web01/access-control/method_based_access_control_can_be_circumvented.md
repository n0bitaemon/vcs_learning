# Method-based access control can be circumvented
Đăng nhập với tài khoản administrator:admin rồi vào Admin panel, ta thấy có chức năng cho phép thăng cấp/hạ cấp một user bất kỳ. Dùng BurpSuite để bắt request, ta thấy khi thăng cấp 1 user thì browser sẽ gửi một POST request tới /admin-roles, body chứa hai tham số username=carlos&action=upgrade

Thử thay method POST thành GET, server trả về lỗi "Missing parameter 'username'". Ta thay đổi URL thành /admin-roles?username=carlos&action=upgrade, kết quả trả về nâng cấp thành công user carlos.

Ta hạ cấp user carlos rồi đăng nhập tài khoản wiener:peter thì thấy với request POST /admin-roles sẽ hiện lỗi "Unauthorized", như vậy ta thử dùng GET /admin-roles&username=wiener&action=upgrade. Kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/201468010-c16c5818-f047-459f-999f-aa27cc2b7269.png)
