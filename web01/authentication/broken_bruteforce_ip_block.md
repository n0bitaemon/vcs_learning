# Broken bruteforce protection - IP block
Đầu tiên bắt request /login với Burpsuite

Sau một vài lần test, ta thấy cứ đăng nhập sai 3 lần thì sẽ IP sẽ bị khóa trong vòng 1 phút, và không thể dùng X-Forwarded-For để đánh lừa server. Do đó ta sẽ config bruteforce attack với Intruder bằng cách:
+ Tạo 1 list username và password tương ứng, sao cho cứ cách 2 hàng sẽ xuất hiện username=wiener và password=peter
+ Cấu hình Resource Pool sao cho chỉ gửi 1 request mỗi lần
+ Bruteforce username và password với wordlist đã tạo, sử dụng chế độ Pitchfork

![image](https://user-images.githubusercontent.com/103978452/201044762-f1da5de3-3dda-47d0-b853-95e21c6ff66c.png)
![image](https://user-images.githubusercontent.com/103978452/201044909-6234f0f0-8441-48c2-b8d6-7d570e804cd8.png)

Sau một thời gian ta thấy request chứa payload username=carlos và password=love trả HTTP status code là 302

![image](https://user-images.githubusercontent.com/103978452/201044436-f6c9448d-5419-403a-b9da-2afb9d387882.png)

Sử dụng tài khoản trên để đăng nhập, kết quả thành công.
