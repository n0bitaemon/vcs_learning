# Password reset poisoning via middleware
Thử chức năng đăng nhập với tài khoản wiener và dùng BurpSuite để intercept request GET /forgot-password. Ta thấy khi thay đổi Host header thì server sẽ trả về lỗi "Client Error".

Thử dùng header "X-Forwarded-Host: test.com", nhấn "Send" thì thấy trong Email client xuất hiện một email với URL có domain là test.com

![image](https://user-images.githubusercontent.com/103978452/201553696-0bdbf2bd-4ba7-4a75-a774-7d7179633311.png)

Ta thay đổi username=carlos, thiết lập X-Forwarded-Host thành domain của exploit-server. Sau khi gửi, ta vào access log của exploit-server thì thấy một request chứa reset password token.

![image](https://user-images.githubusercontent.com/103978452/201553805-6d2ee2c6-5824-4c73-9e89-90822b202e39.png)

Sử dụng token để truy cập GET /forgot-password?temp-forgot-password-token=<token_lay_duoc> rồi đổi mật khẩu của user carlos. Sử dụng thông tin có được để đăng nhập, kết quả thành công.
