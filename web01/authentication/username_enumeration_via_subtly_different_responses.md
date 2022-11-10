# Username enumeration via subtly different responses
Đầu tiên ta dùng Burpsuite bắt request tới /login

![image](https://user-images.githubusercontent.com/103978452/201005030-410fd4ed-e3ee-4298-8a77-b274476ec19c.png)

Khi nhập sai username hoặc password, lỗi "Incorrect username or password" sẽ xuất hiện. Thử bruteforce với các payload khác nhau, ta thấy length của responses không cố định và status code cũng không đổi. Như vậy không thể đoán username dựa trên length và status code.

Ta sẽ thử so sánh các response để xem có response nào trả về kết quả khác biệt hay không. Chuyển request sang Intruder, đặt username làm payload rồi vào Options, đến phần Grep-Extract, chọn phần "Invalid username or password" trong responses làm dấu hiệu rồi tiến hành bruteforce. Ta tìm được với username=albuquerque thì response khác với responses của các request khác. Như vậy có khả năng username là "albuquerque"

Đặt username=albuquerque và chuyển payload sang password, thực hiện bruteforce với wordlist có sẵn, ta thấy chỉ với password=klaster thì mới cho ra status code là 302.

![image](https://user-images.githubusercontent.com/103978452/201006100-8f3fe7a9-7c64-42a0-8f97-6fe7b72ffb18.png)


Thử đăng nhập với username=albuquerque và password=klaster, kết quả trả về đăng nhập thành công. 
