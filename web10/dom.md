# 1. DOM XSS using web messages
Nhận thấy trong source code có đoạn mã sau:

![image](https://user-images.githubusercontent.com/103978452/211499636-60830aeb-fd4d-4bcd-bae7-fbaf3f1a149a.png)
Đoạn code trên sẽ nhận web message và inject vào tag có id là 'ads'. Như vậy ta có thể cấu hình XSS sử dụng thẻ `<iframe>`

Vào exploit server, cấu hình đoạn code sau:

```
<iframe style="width: 500px; height: 500px;" src="https://0a1e00080340c863c0b7a49200dd0016.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>', '*')"></iframe>
```

Sau khi đoạn code trên được chạy, sẽ tạo 1 tag iframe. Tag iframe này sau đó sẽ gửi message đến target website, với nội dung `<img src=1 onerror=print()>`. Sau khi được inject vào thẻ có id=ads, lệnh print() sẽ được gọi.

Click "Deliver to victim", kết quả thành công.

# 2. DOM XSS using web messages and a JavaScript URL
Nhận thấy trong source code có đoạn script sau:

![image](https://user-images.githubusercontent.com/103978452/211507542-82ddefb4-5d22-42c8-abc7-f3769e961b4e.png)
Đoạn script trên sẽ bắt sự kiện message được gửi đến, kiểm tra xem trong data(url) nếu có chuỗi 'http:' hoặc 'https:' trong message content thì sẽ thiết lập `location.href=url`

Vào exploit, cấu hình đoạn code sau:
```
<iframe src="https://0a6100cd040bb11ec08677ae0042000b.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print(%22https:%22)', '*')"></iframe>
```

Đoạn code trên tạo một iframe, gửi message `javascript:print(%22https:%22)` tới target website. Như vậy khi target website bắt event 'message', lệnh `print('https')` sẽ được gọi

Sau khi click "Deliver to victim", bài lab được giải.

# 3. DOM XSS using web messages and JSON.parse

# 4. DOM-based open redirection

# 5. DOM-based cookie manipulation

# 6. Exploiting DOM clobbering to enable XSS

# 7. Clobbering DOM attributes to bypass HTML filters

# 8. 
