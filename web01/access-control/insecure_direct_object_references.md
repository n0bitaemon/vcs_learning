# Insecure direct object references
Đăng nhập với tài khoản wiener:peter, thử chức năng live chat rồi nhấn nút "View transcript". Ta thấy browser gửi request tới /download-transcript/2.txt và một file chứa đoạn hội thoại được tải về.

Bắt request với BurpSuite rồi sửa 2.txt thành 1.txt, ta thấy có những tin nhắn của một user khác. Trong đó có thông tin "my pasword is pnohengv1xfel7p674gt".

![image](https://user-images.githubusercontent.com/103978452/201459004-5a9fbd0b-dadd-416e-9ce2-43bb177b497c.png)

Thử đăng nhập với username=carlos và password=pnohengv1xfel7p674gt, kết quả thành công.
