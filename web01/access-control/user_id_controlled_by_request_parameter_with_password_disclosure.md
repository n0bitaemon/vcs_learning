# User ID controlled by request parameter with password disclosure
Đăng nhập với tài khoản wiener:peter rồi vào "My Account", ta thấy:
+ URL có một tham số là id=wiener, thử thay đổi thành id=carlos thì ta thấy có thể truy cập vào profile của user carlos.
+ Phần đổi mật khẩu có một input với value là mật khẩu hiện tại, như vậy nếu vào được /my-account với id của admin, ta có thể có được mật khẩu của admin.

Như vậy, để xóa user carlos thì ta cần biết id của admin là gì.

Sau một vài lần thử, ta đoán được id=administrator trỏ đến profile của admin. Dùng dev tool để lấy mật khẩu của administrator rồi đăng nhập, xóa user carlos, ta được kết quả thành công

![image](https://user-images.githubusercontent.com/103978452/201451962-16c2f92f-5b14-4118-a1de-2cad197793c7.png)
