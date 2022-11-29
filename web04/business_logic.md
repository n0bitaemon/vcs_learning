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
productId=1&redir=PRODUCT&quantity=1
```
Thử thay đổi quantity = -1 cho đến khi số lượng sản phẩm bị âm, ta thấy kết quả thành công, và tổng tiền phải trả cũng bị âm. Click nút "Place Order" thì hiển thị lỗi "Cart total price cannot be less than zero". Như vậy ta thêm 17 sản phẩm Com-Tool để giá cả trở thành $31.67

![image](https://user-images.githubusercontent.com/103978452/204502427-86970535-f625-4a1b-a960-e5735101c9d4.png)

![image](https://user-images.githubusercontent.com/103978452/204502348-ad5fbb45-8a02-4bd5-9ebe-67d66325636c.png)
