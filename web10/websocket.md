# 1. Manipulating WebSocket messages to exploit vulnerabilities

Trong chức năng live chat, thử exploit XSS bằng cách gửi message `<img src=1 onerror=alert(1)>`, thì nhận thấy các kí tự đặc biệt đã bị HTML encoded, khiến chúng ta không thể exploit XSS.

Trong file `chat.js` có đoạn code sau:

