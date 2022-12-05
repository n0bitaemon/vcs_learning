# 1. Basic SSRF against the local server
Truy cập /admin, ta nhận được thông báo: "Admin interface only available if logged in as an administrator, or if requested from loopback".

Khi sử dụng chức năng checkStock, request `POST /product/stock` với parameter `stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D3%26storeId%3D1`. Như vậy ta sẽ thử thay đổi stockApi để access trang admin với tư cách localhost.

Thay đổi tham số `stockApi=http://localhost/admin`, kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205523955-5692177a-7acd-42ba-ac37-2f98bbff4ebb.png)

Thay đổi `stockApi=http://localhost/admin/delete?username=carlos` để giải bài lab.

# 2. Basic SSRF against another back-end system

# 3. SSRF with blacklist-based input filter

# 4. SSRF with filter bypass via open redirection vulnerability

# 5. Blind SSRF with out-of-band detection

# 6. SSRF with whitelist-based input filter

# 7. Blind SSRF with Shellshock exploitation
