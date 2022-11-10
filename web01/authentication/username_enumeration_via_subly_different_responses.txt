Đầu tiên, ta dùng Burpsuite để bắt request /login.

Sau đó, chuyển request vào intruder rồi để username trở thành payload. 
`username=$abc$&password=def`
Thực hiện bruteforce với wordlist cho sẵn, ta thấy với username=ad thì sẽ báo lỗi "Incorrect password". Từ đó suy ra username=ad
Chuyển payload sang cho password rồi thực hiện bruteforce với wordlist cho sẵn, ta thấy với password=pepper thì response có độ dài khác với những request còn lại.
Sử dụng username=ad và password=pepper để đăng nhập, kết quả thành công
