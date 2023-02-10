# 1. Modifying serialized objects

Đăng nhập với credentials wiener:peter, thấy session cookie có giá trị 

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d
```
Thực hiện base64 decode thì ta được 

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
``` 
chính là object User với hai thuộc tính "username" và "admin" được serialize bởi PHP.

Sửa thành 

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
```
rồi thực hiện base64 encode, thay thế giá trị cookie hiện tại. Sau khi refresh, link dẫn đến Admin panel xuất hiện.

Vào admin panel và xóa user carlos, kết quả thành công.

# 2. Modifying serialized data types

Đăng nhập với credentials wiener:peter, thấy session cookie có giá trị:

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJiNThuaDhwNWo4Z3czM3k2eXF2ZXB6c2k3eWRqd280NSI7fQ%3d%3d
```
Thực hiện base64 decode thì ta được 
```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"b58nh8p5j8gw33y6yqvepzsi7ydjwo45";}
```
Như vậy nếu access token và username đúng thì ta sẽ truy cập được vào tài khoản.

Website sử dụng hàm serialize() của PHP, như vậy ta có thể thay đổi data type của access token thành int, và nếu website không convert access token thành kiểu string, đồng thời trong access token của administrator không có chữ số, và website so sánh access token bằng loose comparision thì ta có thể bypass.

Cấu hình một serialized object mới với `username=administrator` và `access_token=0` (kiểu integer):
```
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```
Thực hiện base64 encode và thay thế cookie hiện tại, kết quả truy cập thành công. Vào admin panel và xóa user carlos, bài lab được giải.

# 3. Using application functionality to exploit insecure deserialization
Đăng nhập với credentials wiener:peter, thực hiện base64 decode session cookie ta được:

```
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"q1eh79na8deste009sniaq0ytxnirwh5";s:11:"avatar_link";s:19:"users/wiener/avatar";}
```
Dự đoán khi thực hiện chức năng Delete Account, ứng dụng sẽ xóa cả ảnh avatar sử dụng thuộc tính "avatar_link" trong object "User" (session cookie sau khi được serialized). Như vậy thay đổi thành `"avatar_link";s:23:"/home/carlos/morale.txt"`, sau đó click "Delete Account". Kết quả, bài lab được giải thành công.

# 4. Arbitrary object injection in PHP
Đăng nhập với credentials wiener:peter, thực hiện base64 decode session cookie, ta được một object User. Như vậy website sử dụng cơ chế xác thực dựa trên serialized session. Nếu ta truyền vào một object thì object đó sẽ được deserialized.

Nhìn vào trong source code client, ta thấy dòng comment:

```
<!-- TODO: Refactor once /libs/CustomTemplate.php is updated -->
```
Thử truy cập `/libs/CustomTemplate.php` thì không thấy hiển thị gì cả, như vậy developer đã thay đổi file này để giấu đi source code. Trong Bash, các backup files sẽ có `~` ở cuối tên file. Như vậy ta thử truy cập `/libs/CustomTemplate.php~`, kết quả source code đã được hiển thị.

![image](https://user-images.githubusercontent.com/103978452/218042042-8521d715-4df1-44d0-baa7-e3eccb86b470.png)
Nhận thấy hàm `__destruct` của object "CustomTemplate" sẽ xóa đi file có tên trùng với thuộc tính "lock_file_path" của nó. Như vậy ta cấu hình serialized object sau:

```
O:14:"CustomTemplate":2:{s:18:"template_file_path";s:9:"hello.txt";s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```
Nếu ứng dụng deserialie object trên, hàm `__construct` sẽ được gọi, xóa đi file `/home/carlos/morale.txt`. Thực hiện base64 object, sau đó thay thế cho session cookie hiện tại. Refresh website, kết quả thành công.

# 5. Exploiting Java deserialization with Apache Commons

# 6. Exploiting PHP deserialization with a pre-built gadget chain

# 7. Exploiting Ruby deserialization using a documented gadget chain

# 8. Developing a custom gadget chain for Java deserialization

# 9. Developing a custom gadget chain for PHP deserialization

# 10. Using PHAR deserialization to deploy a custom gadget chain
