# 1. Manipulating WebSocket messages to exploit vulnerabilities

Trong chức năng live chat, thử exploit XSS bằng cách gửi message `<img src=1 onerror=alert(1)>`, thì nhận thấy các kí tự đặc biệt đã bị HTML encoded, khiến chúng ta không thể exploit XSS. Sử dụng BurpRepeater, ta thấy dữ liệu gửi lên server cũng bị encode.

Trong file `chat.js` có đoạn code sau:

![image](https://user-images.githubusercontent.com/103978452/215007534-39c1a61f-0105-459e-82c2-8ee8d97ed5f9.png)
Như vậy website thực hiện encode phía client side rồi mới gửi đi, và chỉ encode nếu trong form có thuộc tính `encode=true`. Dùng Dev Tools xóa thuộc tính `encode` của thẻ form, sau đó gửi message `<img src=1 onerror=alert(1)>`, kết quả thành công.

# 2. Manipulating the WebSocket handshake to exploit vulnerabilities

# 3. 
