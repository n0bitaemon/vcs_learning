# Offline password cracking
Chèn đoạn mã xss sau vào trong input "Comment" của chức năng bình luận:

![image](https://user-images.githubusercontent.com/103978452/201256776-0246500b-0e6d-4a94-8552-b43dcf248197.png)

Sau khi submit, ta vào exploit server, truy cập access log thì thấy có request gửi đến với parameter cookie. Ta thu được chuỗi "Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz" chính là stay-logged-in cookie.

![image](https://user-images.githubusercontent.com/103978452/201257292-5f880aef-7718-4c56-b311-3a6a5f12d94e.png)

Tiến hành decode base64, ta được carlos:26323c16d5f4dabff3bb136f2460a943. Sau khi search chuỗi md5 trên md5online.org, ta thu được username=carlos và password=onceuponatime.

Sử dụng thông tin có được để đăng nhập và xóa tài khoản carlos, kết quả thành công.
