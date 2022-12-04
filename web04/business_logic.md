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
Ta thấy ở phía dưới trang "Home" có chức năng nhận thư qua email. Sau khi nhập email, ta có được coupon SIGNUP30 cho phép giảm tổng tiền phải trả 30%.

Ta để ý rằng không thể 1 coupon 2 lần liên tiếp, sẽ hiểu thị lỗi "Coupon already applied". Tuy nhiên khi ta luân phiên nhập các coupon SIGNUP30 và NEWCUST5 thì lại thành công. Thực hiện như vậy 1 vài lần, ta đưa tổng tiền phải trả trở về $0.00. Sau đó click "Place order", kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205235665-de90b0c5-3e3c-4f0b-a636-f64002b0c613.png)

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
Ta thấy để vào trang admin, cần phải có email với domain là "dontwannacry.com".

Dùng Burp Repeater để bắt request `POST /register`, sau đó chỉnh sửa email có độ dài thật lớn (khoảng vài trăm ký tự). Sau khi vào email client để xác thực tài khoản, ta tiến hành đăng nhập. Tại trang "My acccount", ta thấy email đã bị cắt đi chỉ còn 255 ký tự

![image](https://user-images.githubusercontent.com/103978452/205214644-9c86001a-8e46-4395-baf3-35887dceb3dd.png)

Ta chỉnh sửa request `POST /register` như sau:
```
csrf=5hZVO5h4P2LgB7wXU9aqS1gpiTCKw1vD&username=dekisugi&email=dekisugi@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.dontwannacry.com.exploit-0a65002404d424e5c05519a301ef0008.exploit-server.net&password=nomatter
```
Như vậy, email sẽ bị cắt đi chỉ còn 255 ký tự, tức là đến hết phần "dontwannacry.com", trong khi đó email yêu cầu xác thực tài khoản vẫn được gửi về email client của chúng ta.

![image](https://user-images.githubusercontent.com/103978452/205215289-8a93d6ee-4db5-46e0-8f30-4b37c939ae1d.png)

Xác thực và đăng nhập, ta thấy menu "Admin panel" đã hiển thị. Truy cập /admin và xóa user carlos, kết quả thành công.

# 7. Weak isolation on dual-use endpoint
Trong trang "My Account" có chức năng đổi mật khẩu. Dùng BurpSuite để intercept request, sau đó đặt username=administrator và xóa đi trường current-password. Kết quả, password đã được đổi thành công.

![image](https://user-images.githubusercontent.com/103978452/204959770-a011f04b-0588-4aa2-ae2d-887f885781ac.png)

Dùng password mới để đăng nhập với tư cách administrator và xóa user carlos, kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/205215067-8da84ef2-dfda-4fe5-a3ad-dfba69b530c4.png)

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
2) Truy cập Home (bước 3)

Trong trang Home có hiển thị menu "Admin panel". Như vậy role của ta sẽ mặc định là administrator. Truy cập trang Admin và xóa user carlos, kết quả thành công.

# 10. Infinite money logic flaw
Ta thấy trong trang "Home" có sản phẩm "Gift card" được bán với giá $10.00, sau khi sử dụng ta nhận lại được $10.00. Nếu sử dụng coupon SIGNUP30 thì giá phải trả chỉ còn $7.00, trong khi bán đi vẫn được $10.00. Như vậy nếu lặp lại quy trình mua-bán này liên tục, ta có thể kiếm ra số tiền không giới hạn.

Quy trình exploit:
1) Cho sản phầm vào giỏ: `POST /cart`
2) Sử dụng coupon: `POST /cart/coupon`
3) Đặt hàng: `POST /cart/checkout`
4) Xác nhận đặt hàng: `GET /cart/order-confirmation?order-confirmed=true`
5) Nhập gift-card: `POST /gift-card`, trong đó gift-card được lấy từ response của bước 4

Ta có thể sử dụng chức năng Macros và Session Handling Rules trong tab Sessions để thực hiện gửi đi nhiều request. Cấu hình macros và rules tương ứng rồi dùng Intruder để thực thi chuỗi requests này đến khi đạt đủ số tiền cần thiết, sau đó mua sản phẩm "Lightweight "l33t" Leather Jacket", kết quả thành công.

# 11. Authentication bypass via encryption oracle
Nhận thấy rằng khi khi đăng nhập với chức năng "Stay logged in", nếu có cookie `stay-logged-in` mà không có session thì ta vẫn đăng nhập được.

Trong trang "My account", ta thấy khi nhập một invalid email thì thông báo "Invalid email address: <invalid-email>" sẽ được hiển thị, cùng với đó một cookie là `notification` với dữ liệu được encrypted được thiết lập. Ta giả sử rằng dòng thông báo lỗi trên chính là giá trị của cookie `notification` sau khi được decrypt.
  
![image](https://user-images.githubusercontent.com/103978452/205499913-8e696b1e-9b71-462e-80fe-920a9933e000.png)
  
Thử copy và paste value của cookie `stay-logged-in` vào trong cookie `notification`, ta thấy thông báo lỗi được hiển thị là: `wiener:1670167212682`, trong đó 1670167212682 chính là timestampt khi ta login
 
![image](https://user-images.githubusercontent.com/103978452/205499065-4a0b7b90-8be1-4539-bb6c-a52a596d4f4f.png)

Như vậy ta có thể encrypt và decrypt một dữ liệu bất kỳ bằng cách:
1) Encrypt: Đặt input vào trường email sau đó submit => value của cookie `notification` chính là dữ liệu được encrypt của chuỗi "Invalid email address: <input>"
2) Decrypt: Đặt input thành giá trị của cookie `notification` trong trang "My-account", sau đó refresh. Thông báo lỗi chính là giá trị của input sau khi decrypt
  
Tiến hành encrypt `administrator:1670167212682` rồi đưa vào Decoder. Thực hiện decode URL và base64, sau đó xóa 23 bytes đầu của chuỗi hex thu được (tương ứng "Invalid email address: "), rồi encode trở lại. Thử gán giá trị thu được vào cookie `notification`, ta thu được lỗi "Input length must be multiple of 16 when decrypting with padded cipher"
  
Như vậy số bytes xóa đi cần phải là bội của 16. Do chuỗi "Invalid email address: " có 32 bytes, nên ta thêm "xxxxxxxxx" vào trước email address. Tiến hành encrypt `xxxxxxxxxadministrator:1670167212682`, sau đó decode, xóa 32 byte rồi encode trở lại. Sau khi đổi giá trị của cookie, ta thu được giá tị mong muốn
  
![image](https://user-images.githubusercontent.com/103978452/205499797-22468dad-f2fc-435d-bd7b-9cbdadf2f4ae.png)

Copy giá trị từ cookie `notification` sang `stay-logged-in` và xóa cookie session rồi refresh, ta thấy ta đã đăng nhập với tư các administrator. Vào trang "Admin panel" rồi xóa user carlos, kết quả thành công.
