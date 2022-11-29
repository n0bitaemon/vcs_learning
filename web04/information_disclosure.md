# 1. Information disclosure in error messages
Trang xem thông tin product của website có url `/product?productId=2`. 

Ta thử xem website có lỗ hổng SQL injection không bằng cách thay đổi URL thành `/product?productId=2'`. Kết quả hiển thị lỗi. Từ đó ta thu được tên framework là `Apache Struts 2 2.3.31`

# 2. Information disclosure on debug page
Dùng chức năng "View Page Source" của trình duyệt, ta thấy có một dòng comment có chứa path tới trang debug
```
<!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->
```
Truy cập `/cgi-bin/phpinfo.php`, ta thấy trang thông tin về version php đang sử dụng được hiển thị. Dòng `SECRET_KEY` có value là `z9k2d4u63wdrwb5x7dp4swyfk7eu54pf`

# 3. Information disclosure via backup files
Truy cập `/backup`, kết quả thành công. Như vậy server chưa chặn quyền truy cập vào folder này. Đọc nội dung file `ProductTemplate.java.bak` thì ta lấy được mật khẩu của database là `619j0tpvzqoyd99viwdnmw3fvmqi5ytt`.

![image](https://user-images.githubusercontent.com/103978452/204494419-d9fcc5c3-1f90-4219-8e0b-79f85eefceae.png)

# 4. Authentication bypass via information disclosure
Truy cập `GET /admin`, thông báo `Admin interface only available to local users` xuất hiện. Như vậy ta sẽ thử fake local IP address để bypass.

Thay đổi method GET thành TRACE, ta thấy trong response có trả về `X-Custom-IP-Authorization: 27.72.58.160`

![image](https://user-images.githubusercontent.com/103978452/204488829-d1dda0f8-5c9f-4989-8255-034e0ba36ff1.png)

Thử thay đổi header trên bằng cách thêm `X-Custom-IP-Authorization: 127.0.0.1` trong request. Kết quả trả về trang admin thành công. Như vậy ta truy cập `GET /admin/delete?username=carlos` với header như trên, và user carlos được xóa thành công.

![image](https://user-images.githubusercontent.com/103978452/204489686-83a92399-161a-42dc-ba5c-76087e9c9e92.png)

# 5. Information disclosure in version control history
Ta download folder .git của website về bằng lệnh
```
git-dumper https://0a3b0062048ceab5c0ad8d2e004e00aa.web-security-academy.net/.git ./source
```

![image](https://user-images.githubusercontent.com/103978452/204493827-0c658164-e337-4124-98af-bbae8c27b5f2.png)

Đọc file `source/admin.conf` thì thấy dòng `ADMIN_PASSWORD=env('ADMIN_PASSWORD')`. Tiếp tục đọc file `source/.git/COMMIT_EDITMSG`, nội dung là `Remove admin password from config`. Như vậy trong 1 lần commit, password của admin đã bị xóa đi. Tuy nhiên folder .git có lưu lại các phiên bản project sau mỗi lần commit.

Truy cập folder `source/.git/objects`, ta sẽ lần lượt dùng lệnh `git cat-file -p <object-name>` để đọc các object. Trong đó object-name là 'tên thư mục + tên file object'. Ví dụ, trong folder `0f` có file object `f53d1953540a10f37e1708f0b93687c453c7f4`. Như vậy ta sẽ dùng lệnh `git cat-file -p 0ff53d1953540a10f37e1708f0b93687c453c7f4`.
  
Sau một vài lần thử, ta thu được admin password như trong hình. Dùng password có được để đăng nhập và xóa user carlos, kết quả thành công.
  
![image](https://user-images.githubusercontent.com/103978452/204493484-75b61db3-85fc-493c-be38-2feac3d3df2d.png)
