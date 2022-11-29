# 1. Information disclosure in error messages
Trang xem thông tin product của website có url `/product?productId=2`. 

Ta thử xem website có lỗ hổng SQL injection không bằng cách thay đổi URL thành `/product?productId=2'`. Kết quả hiển thị lỗi. Từ đó ta thu được tên framework là `Apache Struts 2 2.3.31`

# 2. Information disclosure on debug page
Dùng chức năng "View Page Source" của trình duyệt, ta thấy có một dòng comment có chứa path tới trang debug
```
<!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->
```
Truy cập `/cgi-bin/phpinfo.php`, ta thấy trang thông tin về version php đang sử dụng được hiển thị. Dòng `SECRET_KEY` có value là `z9k2d4u63wdrwb5x7dp4swyfk7eu54pf`

