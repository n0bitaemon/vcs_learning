# 1. Excessive trust in client-side controls
Trong chức năng thêm vào giỏ hàng, ta thấy một request `POST /cart` được gửi đến với body như sau:
```
productId=1&redir=PRODUCT&quantity=1&price=133700
```
Như vậy ta thay đổi `price=100` và thử lại. Kết quả sản phẩm được thêm vào giỏ hàng thành công với giá 1.00$

![image](https://user-images.githubusercontent.com/103978452/204499779-41b815cd-8cf4-4d28-9231-4c08a9748e56.png)

Như vậy ta submit và bài lab được giải.

# 2. High-level logic vulnerability
Ta thấy trong request`POST /cart` (thêm sản phẩm vào giỏ hàng), phần body có nội dung như sau:
```
productId=2&redir=PRODUCT&quantity=1
```
Thử thay đổi quantity = -1 cho đến khi số lượng sản phẩm bị âm, ta thấy kết quả thành công, và tổng tiền phải trả cũng bị âm. 

![image](https://user-images.githubusercontent.com/103978452/204502427-86970535-f625-4a1b-a960-e5735101c9d4.png)

Click nút "Place Order" thì hiển thị lỗi "Cart total price cannot be less than zero". Như vậy ta sẽ đặt 1 sản phẩm `Lightweight "l33t" Leather Jacket` (id=1, price=$1337.00), và 23 sản phẩm `Poo Head - It's not just an insult anymore.` (id=2, price=$56.36), và tổng tiền phải trả sẽ là $40.72. Sau khi nhấn "Place order", kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/204930394-c5b88c45-efaf-4396-8a0c-cc6344f4bc01.png)

# 3. Inconsistent security controls
Ta thấy website có chức năng đăng ký users với thông báo `If you work for DontWannaCry, please use your @dontwannacry.com email address`. Như vậy ta đăng ký tài khoản: username="helloworld", password="helloworld", email="attacker@exploit-0a26003d03e10b4ac1a25988014900ad.exploit-server.net". Sau khi vào email vào xác nhận tài khoản thành công, tiến hành đăng nhập.

Trong trang 'My Account', có chức năng thay đổi email. Ta thay đổi email của exploit-server thành `hello@dontwannacry.com`, kết quả 'Admin panel' đã được hiển thị trên menu.

![image](https://user-images.githubusercontent.com/103978452/204931324-edfef2ea-ab7f-453a-9a64-2e33133cadb0.png)

Vào trang admin và xóa user carlos, kết quả thành công.

# 4. Flawed enforcement of business rules

# 5. Low-level logic flaw

# 6. Inconsistent handling of exceptional input

# 7. Weak isolation on dual-use endpoint

# 8. Insufficient workflow validation

# 9. Authentication bypass via flawed state machine

# 10. Infinite money logic flaw

# 11. Authentication bypass via encryption oracle
