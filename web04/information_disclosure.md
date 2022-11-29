# 1. Information disclosure in error messages
Trang xem thông tin product của website có url `/product?productId=2`. 

Ta thử xem website có lỗ hổng SQL injection không bằng cách thay đổi URL thành `/product?productId=2'`. Kết quả hiển thị lỗi. Từ đó ta thu được tên framework là `Apache Struts 2 2.3.31`

# 2. Information disclosure on debug page
Dùng chức năng "View Page Source" của trình duyệt, ta thấy có một dòng comment có chứa path tới trang debug
```
<!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->
```
Truy cập `/cgi-bin/phpinfo.php`, ta thấy trang thông tin về version php đang sử dụng được hiển thị. Dòng `SECRET_KEY` có value là `z9k2d4u63wdrwb5x7dp4swyfk7eu54pf`

# 3. Authentication bypass via information disclosure
Truy cập `GET /admin`, thông báo `Admin interface only available to local users` xuất hiện. Như vậy ta sẽ thử fake local IP address để bypass.

Thay đổi method GET thành TRACE, ta thấy trong response có trả về `X-Custom-IP-Authorization: 27.72.58.160`

![image](https://user-images.githubusercontent.com/103978452/204488829-d1dda0f8-5c9f-4989-8255-034e0ba36ff1.png)

Thử thay đổi header trên bằng cách thêm `X-Custom-IP-Authorization: 127.0.0.1` trong request. Kết quả trả về trang admin thành công. Như vậy ta truy cập `GET /admin/delete?username=carlos` với header như trên, và user carlos được xóa thành công.

![image](https://user-images.githubusercontent.com/103978452/204489686-83a92399-161a-42dc-ba5c-76087e9c9e92.png)

# 4.
