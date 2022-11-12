# Password brute-force via password change
Đăng nhập với tài khoản wiener:peter rồi test thử chức năng đổi mật khẩu. Ta thấy:
+ Khi current-password đúng và new-password-1 = new-password-2 thì đổi mật khẩu thành công
+ Khi current-password đúng và new-password-1 != new-password-2 thì hiện lỗi "New passwords do not match"
+ Khi current-password sai và new-password-1 = new-password-2 thì bị logout và tính là 1 lần đăng nhập sai
+ Khi current-password sai và new-password-1 != new-password-2 thì hiện lỗi "Current password is incorrect"

Như vậy ta có thể dùng trường hợp cuối để tấn công bruteforce. Dùng BurpSuite bắt request đổi mật khẩu trong trường hợp cuối, thay đổi username=carlos và gửi đến Intruder để thực hiện tấn công bruteforce password. Ta thấy chỉ có password=biteme thì lỗi "New password do not match" mới xuất hiện.

![image](https://user-images.githubusercontent.com/103978452/201498712-0705e1b6-22fb-4877-9cff-2896e82beeca.png)

Như vậy ta thu được username=carlos và password=biteme. Sử dụng thông tin này để đăng nhập, kết quả thành công
