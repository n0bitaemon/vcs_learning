# Username enumeration via different responses
Đầu tiên, ta dùng Burpsuite để bắt request /login.

![image](https://user-images.githubusercontent.com/103978452/200995668-dec26a4f-0275-421c-abb0-783efcf5c4fb.png)

Sau đó, sử dụng Intruder để thực hiện bruteforce username với wordlist cho trước. Sau một thời gian, ta thấy chỉ với payload username=am thì lỗi "Incorrect password" xuất hiện. Từ đó suy ra username=am

Tiếp tục thực hiện bruteforce password với wordlist có sẵn, ta thấy chỉ với payload password=monitor thì response có status=302 , khác với các response khác (status=200) 
![image](https://user-images.githubusercontent.com/103978452/200998008-5aa01d30-dd4c-40da-b8c4-6ebd3cb70fb6.png)


Sử dụng username=am và password=monitor để đăng nhập, kết quả thành công
