# Password reset broken logic
Test thử chức năng reset password với user wiener, ta thấy sau khi nhập username và submit, một URL chứa token tương ứng sẽ được gửi đến email của user wiener. Khi truy cập URL thì hiện ra form yêu cầu nhập password mới. Sau khi đổi mật khẩu, request POST /forgot-password sẽ được gửi đi với các tham số gồm temp-forget-password-token, username, new-password-1 và new-password-2

Dùng BurpSuite để bắt request đổi mật khẩu mới. Ta sẽ kiểm tra xem liệu server có chấp nhận trường hợp không có temp-forgot-password-token hay không. Thử xóa trường này trong body đi thì thấy hiện thông báo "Please check your email for a reset password link => thất bại. Thử đặt temp-forgot-password-token là chuỗi rỗng, kết quả là đổi mật khẩu thành công.

![image](https://user-images.githubusercontent.com/103978452/201511116-6b775f31-ccf5-4ff8-8129-ca28f694444a.png)

Vậy ta thay temp-forgot-password-token thành empty string và đổi username=carlos, sau khi nhấn Send thì mật khẩu của carlos sẽ bị đổi. Dùng thông tin có được để đăng nhập, kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201511103-20deff01-8493-4564-aeb0-e804cbe04dc4.png)
