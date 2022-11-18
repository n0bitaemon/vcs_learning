# 1. Filepath traversal, simple case
Click vào ảnh một sản phẩm, ta thấy URL của ảnh có dạng `/image?filename=63.jpg`. Như vậy, ta thử tấn công directory traversal bằng cách thay URL thành `/image?filename=../../../../../etc/passwd`

Kết qủa, ta được nội dung file /etc/passwd

![image](https://user-images.githubusercontent.com/103978452/202731585-d3bc8547-7401-4784-b688-c4cbb4f75815.png)

# 2. File path traversal, traversal sequences blocked with absolute path bypass
Thử thay đổi filename giống như bài #1, ta thấy không thành công và hiển thị lỗi "No such file"

![image](https://user-images.githubusercontent.com/103978452/202727508-3ebd9a16-b76e-4458-9755-30ec6c8f00c7.png)

Tiếp theo, ta thử dùng absolute path `/image?filename=/etc/passwd`. Kết quả, nội dung file /etc/passwd đã được hiển thị

![image](https://user-images.githubusercontent.com/103978452/202727704-7315b7c3-3060-4ad2-9675-5b90b596b93e.png)

# 3. File path traversal, traversal sequences stripped non-recursively
Trong URL một file ảnh bất kỳ, thử thay filename sử dụng relative path hay absolute path như trong bài #1 và #2 thì đều thất bại.

Ta thử `filename=../73.jpg` thì thấy trả về kết quả giống với `/image?filename=73.jpg`. Như vậy, có thể server đã ngăn directory traversal bằng cách bỏ đi những chuỗi `../`. Trong trường hợp đó, ta sẽ thay filename như sau: `/image?filename=....//....//....//....//....//etc/passwd`: sau khi bị xóa đi những đoạn `../`, nó sẽ trở thành `/image?filename=../../../../../../etc/passwd`

Kết quả, ta có được nội dung file /etc/passwd

![image](https://user-images.githubusercontent.com/103978452/202730889-c4c4c85f-e7fd-45c8-b941-7d28b621df29.png)

# 4. File path traversal, traversal sequences stripped with superfluous URL-decode
Trong URL một file ảnh bất kỳ, sau một vài lần thử thay filename thì ta phát hiện server sẽ xóa các ký tự `.` và `/` trong URL (`/image?filename=.././././//.././5.jpg` và `/image?filename=5.jpg` trả về kết quả như nhau)

Ta thử dùng URL encode để bypass: `/image?filename=%2E%2E%2F%2E%2E%2F%2E%2E%2F%2E%2E%2F%65%74%63%2F%70%61%73%73%77%64` (tương ứng `/image?filename=../../../../etc/passwd`) thì kết quả trả về "No such file"

Thử dùng double URL encode để bypass: `/image?filename=%25%32%45%25%32%45%25%32%46%25%32%45%25%32%45%25%32%46%25%32%45%25%32%45%25%32%46%25%32%45%25%32%45%25%32%46%25%36%35%25%37%34%25%36%33%25%32%46%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34` (tương ứng `../../../../etc/passwd` sau khi double decode). Kết quả, ta thu được nội dung file /etc/passwd

![image](https://user-images.githubusercontent.com/103978452/202734712-1102bbc1-8af5-4609-911b-e7bd8cd7bdb5.png)

# 5. File path traversal, validation of start of path
Ta thấy URL một image bất kỳ có dạng `/image?filename=/var/www/images/11.jpg`. Thử thay đổi phần '/var/www/images/' thì thấy kết quả không thành công.

Tuy nhiên, ta có thể đơn giản trở về root directory bằng cách sử dụng `/var/www/images/../../../etc/passwd`. Kết quả, ta thu được nội dung file /etc/passwd

![image](https://user-images.githubusercontent.com/103978452/202736241-b985df81-b787-46b2-ad1b-636c515c8125.png)

# 6. File path traversal, validation of file extension with null byte bypass
Ta thấy một URL của một image bất kỳ có dạng `/image?filename=65.jpg`. Sử dụng relative path hay absolute path tới /etc/passwd đều trả kết quả "No such file".

Thử sử dụng null byte để bypass: `/image?filename=../../../../etc/passwd%00.png`, ta thu được kết quả thành công

![image](https://user-images.githubusercontent.com/103978452/202738203-d56c957e-82f3-48a2-9605-a07c015878b7.png)
