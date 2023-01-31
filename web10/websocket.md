# 1. Manipulating WebSocket messages to exploit vulnerabilities

Trong chức năng live chat, thử exploit XSS bằng cách gửi message `<img src=1 onerror=alert(1)>`, thì nhận thấy các kí tự đặc biệt đã bị HTML encoded, khiến chúng ta không thể exploit XSS. Sử dụng BurpRepeater, ta thấy dữ liệu gửi lên server cũng bị encode.

Trong file `chat.js` có đoạn code sau:

![image](https://user-images.githubusercontent.com/103978452/215007534-39c1a61f-0105-459e-82c2-8ee8d97ed5f9.png)
Như vậy website thực hiện encode phía client side rồi mới gửi đi, và chỉ encode nếu trong form có thuộc tính `encode=true`. Dùng Dev Tools xóa thuộc tính `encode` của thẻ form, sau đó gửi message `<img src=1 onerror=alert(1)>`, kết quả thành công.

# 2. Manipulating the WebSocket handshake to exploit vulnerabilities
Trong ứng dụng live chat, thử với đoạn tin nhắn `<img src=1 onerror=alert(1)`, kết quả website đã chặn truy cập do phát hiện XSS payload. Sử dụng BurpRepeater để gửi lại request thì thấy website trả về response `{"error":"Attack detected: Event handler"}`. Thử Reconnect thì có thông báo lỗi `"This address is blacklisted"`. Như vậy, website có XSS filter, sẽ kiểm tra XSS payload, nếu có thì sẽ chặn người dùng.

Thử thêm header `X-Forwarded-For: 1.1.1.1` thì thấy Reconnect thành công, như vậy ta có thể dùng header này để bypass. Sau khi thử nhiều payload thì ta nhận thấy:

+) Nếu xuất hiện `onerror=...` thì sẽ bị chặn, nhưng `onerror = ...` (thêm space ở giữa) thì lại thành công

+) Nếu xuất hiện `alert()` thì sẽ bị chặn với lỗi `{"error":"Attack detected: Alert"}`, tuy nhiên `alert ()` thì lại được cho phép.

Như vậy, ta cấu hình một message với nội dung sau:

```
{"message":"<img src=1 onerror = 'alert ()'>"}
```
Sau khi submit, kết quả bài lab được giải.

# 3. 
