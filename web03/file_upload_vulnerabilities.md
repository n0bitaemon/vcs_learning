# 1. Remote code execution via web shell upload
Ta thấy chức năng upload avatar cho phép ta upload bất kì loại file nào. Như vậy ta thử upload file payload.php với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Sau khi upload file, ta truy cập `/files/avatars/payload.php` thì thấy nội dung file /home/carlos/secret đã được hiển thị:

![image](https://user-images.githubusercontent.com/103978452/202854734-8fa1c18b-4117-4a3c-b75e-547b67b16588.png)

# 2. Web shell upload via Content-Type restriction bypass
Khi upload file có đuôi .php thì website trả về lỗi, thông báo rằng chỉ cho phép uplaod file với MIME type image/jpeg hoặc image/png.

Ta thử upload file payload.php với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
rồi thay đổi Content-Type từ `application/x-php` thành `image/jpeg` rồi submit (sử dụng Burp Repeater)

Kết quả thành công. Ta truy cập `/files/avatars/payload.php` thì thấy nội dung file /home/carlos/secret được hiển thị

![image](https://user-images.githubusercontent.com/103978452/202857559-21ced5bd-38e0-47f0-a627-0b64162b40f7.png)

# 3. Web shell upload via path traversal
Ta thử upload file payload.php với nội dung
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
rồi truy cập `/files/avatars/payload.php` thì thấy nội dung file được hiển thị thay vì được execute. Ta sẽ thử upload file payload.php vào các folder khác sử dụng kĩ thuật directory traversal.

Trong tab Repeater của BurpSuite,ta thấy POST request đến /my-account/avatar như sau:

![image](https://user-images.githubusercontent.com/103978452/202960724-6834b606-d122-43ba-8f10-b716b5a1f5f9.png)

Thay đổi `filename="../payload.php"`, kết quả trả về `The file avatars/payload.php has been uploaded`. Thử với các relative path, absolute path khác cũng có kết quả tương tự. Như vậy có thể server lọc ra filename trước rồi mới upload.

Thử dùng URL encode, thay `filename="%2E%2E%2F%70%61%79%6C%6F%61%64%2E%70%68%70"` (tương ứng `payload="../payload.php sau khi decode) thì thấy kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/202961066-81908b20-efee-4af1-8076-2c0754a00c5b.png)

Truy cập `/files/payload.php`, ta thấy đoạn code được execute và trả về nội dung file /home/carlos/secret

![image](https://user-images.githubusercontent.com/103978452/202961174-fed4b7c5-a005-4096-b909-b56917ff110d.png)

# 4.
