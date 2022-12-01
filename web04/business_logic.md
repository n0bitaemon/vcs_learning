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
Ta thấy số lượng đơn hàng không thể là số âm. Như vậy ta sẽ thử tăng số lượng lên thật lớn để kiểm tra, nếu quá giới hạn thì chuyện gì sẽ xảy ra.

Chuyển request `POST /cart` vào Intruder với body như sau:
```
productId=1&redir=PRODUCT&quantity=99
```
Thực hiện tăng liên tục số lượng sản phẩm bằng cách sử dụng Null payloads. Sau một thời gian, ta thấy tổng tiền phải trả đạt giới hạn rồi chuyển thành một số âm rất nhỏ

![image](https://user-images.githubusercontent.com/103978452/205054446-7461976a-46b3-47a8-a63d-7da78ef2d147.png)

Tiếp tục tăng số lượng sản phẩm lên đến gần 0, sau đó dừng Intruder lại và thêm một vài sản phẩm sao cho tổng tiền nhỏ hơn $100. Sau đó click "Place Order", kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205059962-30f8a882-2eb2-4458-af4f-2e8ce1a9926e.png)

# 6. Inconsistent handling of exceptional input

# 7. Weak isolation on dual-use endpoint
Trong trang "My Account" có chức năng đổi mật khẩu. Dùng BurpSuite để intercept request, sau đó đặt username=administrator và xóa đi trường current-password. Kết quả, password đã được đổi thành công.

![image](https://user-images.githubusercontent.com/103978452/204959770-a011f04b-0588-4aa2-ae2d-887f885781ac.png)

Dùng password mới để đăng nhập với tư cách administrator và xóa user carlos, kết quả thành công.

# 8. Insufficient workflow validation
Dùng Burp Repeater để intercept request, ta thấy trình tự của chức năng mua hàng như sau:
1) Người dùng thêm hàng vào giỏ: `POST /cart`
2) Click "Place Order" để đặt hàng: `POST /cart/checkout`
3) Xác nhận mua hàng: `GET /cart/order-confirmation?order-confirmation=true`

Như vậy, ta sẽ thử thực hiện mua hàng theo một thứ tự khác. 
1) Đưa sản phẩm "Six Pack Beer Belt" giá $39.03 vào giỏ (bước 1)
2) Thực hiện đặt hàng (bước 2).
3) Đưa sản phẩm "Lightweight "l33t" Leather Jacket" vào giỏ (bước 1)
4) Xác nhận đặt hàng (bước 2)

Kết quả, bài lab được giải thành công.

# 9. Authentication bypass via flawed state machine
Ta thấy trình tự đăng nhập như sau:
1) Đăng nhập: `GET /login` => `POST /login`
2) Chọn role: `GET /role-selector` => `POST /role-selector`
3) Truy cập Home

Ta thử thực hiện việc login bằng trình tự như sau (bỏ qua việc chọn role):
1) Đăng nhập (bước 1)
2) Truy cập Home

Trong trang Home có hiển thị menu "Admin panel". Như vậy role của ta sẽ mặc định là administrator. Truy cập trang Admin và xóa user carlos, kết quả thành công.

# 10. Infinite money logic flaw

# 11. Authentication bypass via encryption oracle
