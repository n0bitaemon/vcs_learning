# 1. Username enumeration via different responses
Đầu tiên, ta dùng Burpsuite để bắt request /login.

![image](https://user-images.githubusercontent.com/103978452/200995668-dec26a4f-0275-421c-abb0-783efcf5c4fb.png)

Sau đó, sử dụng Intruder để thực hiện bruteforce username với wordlist cho trước. Sau một thời gian, ta thấy chỉ với payload username=am thì lỗi "Incorrect password" xuất hiện. Từ đó suy ra username=am

Tiếp tục thực hiện bruteforce password với wordlist có sẵn, ta thấy chỉ với payload password=monitor thì response có status=302 , khác với các response khác (status=200) 
![image](https://user-images.githubusercontent.com/103978452/200998008-5aa01d30-dd4c-40da-b8c4-6ebd3cb70fb6.png)


Sử dụng username=am và password=monitor để đăng nhập, kết quả thành công

# 2. 2FA simple bypass
Đăng nhập với username=carlos và password=montoya, ta được chuyển hướng đến trang nhập 2FA verification code

Bỏ qua việc nhập verification code, ta truy cập /my-account và thấy vẫn thành công. Như vậy, server không kiểm tra khi verification không được nhập

# 3. Password reset broken logic
Test thử chức năng reset password với user wiener, ta thấy sau khi nhập username và submit, một URL chứa token tương ứng sẽ được gửi đến email của user wiener. Khi truy cập URL thì hiện ra form yêu cầu nhập password mới. Sau khi đổi mật khẩu, request POST /forgot-password sẽ được gửi đi với các tham số gồm temp-forget-password-token, username, new-password-1 và new-password-2

Dùng BurpSuite để bắt request đổi mật khẩu mới. Ta sẽ kiểm tra xem liệu server có chấp nhận trường hợp không có temp-forgot-password-token hay không. Thử xóa trường này trong body đi thì thấy hiện thông báo "Please check your email for a reset password link => thất bại. Thử đặt temp-forgot-password-token là chuỗi rỗng, kết quả là đổi mật khẩu thành công.

![image](https://user-images.githubusercontent.com/103978452/201511116-6b775f31-ccf5-4ff8-8129-ca28f694444a.png)

Vậy ta thay temp-forgot-password-token thành empty string và đổi username=carlos, sau khi nhấn Send thì mật khẩu của carlos sẽ bị đổi. Dùng thông tin có được để đăng nhập, kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201511103-20deff01-8493-4564-aeb0-e804cbe04dc4.png)

# 4. Username enumeration via subtly different responses
Đầu tiên ta dùng Burpsuite bắt request tới /login

![image](https://user-images.githubusercontent.com/103978452/201005030-410fd4ed-e3ee-4298-8a77-b274476ec19c.png)

Khi nhập sai username hoặc password, lỗi "Incorrect username or password" sẽ xuất hiện. Thử bruteforce với các payload khác nhau, ta thấy length của responses không cố định và status code cũng không đổi. Như vậy không thể đoán username dựa trên length và status code.

Ta sẽ thử so sánh các response để xem có response nào trả về kết quả khác biệt hay không. Chuyển request sang Intruder, đặt username làm payload rồi vào Options, đến phần Grep-Extract, chọn phần "Invalid username or password" trong responses làm dấu hiệu rồi tiến hành bruteforce. Ta tìm được với username=albuquerque thì response khác với responses của các request khác. Như vậy có khả năng username là "albuquerque"

Đặt username=albuquerque và chuyển payload sang password, thực hiện bruteforce với wordlist có sẵn, ta thấy chỉ với password=klaster thì mới cho ra status code là 302.

![image](https://user-images.githubusercontent.com/103978452/201006100-8f3fe7a9-7c64-42a0-8f97-6fe7b72ffb18.png)


Thử đăng nhập với username=albuquerque và password=klaster, kết quả trả về đăng nhập thành công. 

# 5. Username enumeration via response timing
Login sử dụng tài khoản wiener:peter và dùng BurpSuite để bắt request. Chỉnh sửa password có độ dài thật lớn, chẳng hạn length=1056, sau đó thử với các trường hợp username đúng và sai. Ta thấy nếu username đúng thì thời gian nhận được response lên đến gần 5 giây, trong khi với trường hợp username sai thì response trả về sau chỉ 244ms.

Chức năng login sẽ bị khóa nếu đăng nhập sai nhiều lần. Tuy nhiên ta thấy có thể bypass bằng cách đặt X-Forwarded-For HTTP header.
Chuyển request /login tới Intruder, đặt X-Forwarded-For header và username là payload1 và payload2. 

![image](https://user-images.githubusercontent.com/103978452/201521614-72fadc79-0959-4419-9848-a90fc828a348.png)

Thực hiện bruteforce với payload1 gồm các địa chỉ IP từ 1.1.1.1 đến 1.1.1.255, còn payload2 thì sử dụng wordlist cho username có sẵn. Ta thấy chỉ có với username=activestat thì có thời gian phản hồi lên đến 4923 giây. Như vậy có khả năng đây là một username hợp lệ.

![image](https://user-images.githubusercontent.com/103978452/201521542-ba0337e2-2036-4b61-b76a-18b00fda1760.png)

Thay đổi request, đặt username=activestat và payload thứ 2 là password rồi thực hiện bruteforce với wordlist cho sẵn của password. Sau một thời gian, ta thấy chỉ với password=harley thì response trả về có status code 302. Sử dụng username=activestat và password=harley để đăng nhập, ta thu được kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201522030-81ba90a5-a7cf-415a-bcbd-558c78133c42.png)

# 6. Broken brute-force protection, IP block
Đầu tiên bắt request /login với Burpsuite

Sau một vài lần test, ta thấy cứ đăng nhập sai 3 lần thì sẽ IP sẽ bị khóa trong vòng 1 phút, và không thể dùng X-Forwarded-For để đánh lừa server. Do đó ta sẽ config bruteforce attack với Intruder bằng cách:
+ Tạo 1 list username và password tương ứng, sao cho cứ cách 2 hàng sẽ xuất hiện username=wiener và password=peter
+ Cấu hình Resource Pool sao cho chỉ gửi 1 request mỗi lần
+ Bruteforce username và password với wordlist đã tạo, sử dụng chế độ Pitchfork

![image](https://user-images.githubusercontent.com/103978452/201044762-f1da5de3-3dda-47d0-b853-95e21c6ff66c.png)
![image](https://user-images.githubusercontent.com/103978452/201044909-6234f0f0-8441-48c2-b8d6-7d570e804cd8.png)

Sau một thời gian ta thấy request chứa payload username=carlos và password=love trả HTTP status code là 302

![image](https://user-images.githubusercontent.com/103978452/201044436-f6c9448d-5419-403a-b9da-2afb9d387882.png)

Sử dụng tài khoản trên để đăng nhập, kết quả thành công.

# 7. Username enumeration via account lock
Đầu tiên ta bắt request tới /login bằng Burpsuite

Chuyển request vào intruder, đặt username và password trở thành payload rồi thực hiện bruteforce với wordlist của username là wordlist đã cho, còn wordlist cho password thì dùng 1 danh sách gồm khoảng 5 chuỗi bất kỳ (Lưu ý đặt password phía trước username để thực hiện các requests login liên tiếp tới cùng một username)

![image](https://user-images.githubusercontent.com/103978452/201057998-9f29ae0a-de68-406e-8d4c-9aa26d99800b.png)

Vào tab Options, tới phần Grep-Extract rồi chọn chuỗi "Invalid username or password" làm dấu hiệu. Thực hiện cluster bomb bruteforce attack, ta thấy chỉ có username=guest mới xuất hiện dòng "You have made too many incorrect login attemps...". Như vậy ta biết được username=guest

Thực hiện bruteforce attack kiểu sniper, với payload là password (wordlist cho trước bởi challenge) và đặt username=guest, ta thấy chỉ có dòng password=daniel thì không có thông báo lỗi. Như vậy có thể đây là password.

![image](https://user-images.githubusercontent.com/103978452/201059313-3064ccbe-eef0-43f8-80c3-36f6a35ea19d.png)


Thực hiện đăng nhập với username=guest và password=daniel, ta thu được kết quả thành công.

# 8. 2FA broken logic
Dùng BurpSuite để bắt request đăng nhập với tài khoản wiener:peter, ta thấy quá trình Authentication diễn ra như sau:
+ POST /login sẽ xác thực username và password
+ GET /login2 sẽ gửi 2FA code về email và thiết lập cookie verify=wiener
+ POST /login2 sẽ xác thực 2FA code

Ta thấy chỉ cần nhập đúng 2FA code thì sẽ đăng nhập thành công, như vậy ta có thể bỏ qua username và password mà vẫn có thể đăng nhập được. Trong khi đó, 2FA code là một số gồm 4 chữ số, và ta hoàn toàn có thể sử dụng bruteforce để tìm ra.

Thực hiện GET /login2 với Cookie verify=carlos để 2FA code được gửi về email của user carlos.
Gửi request POST /login2 vào Intruder, rồi thực hiện bruteforce với payload là mfa-code, chọn danh sách các số từ 0000 đến 9999.

![image](https://user-images.githubusercontent.com/103978452/201523528-7bcaf2d0-b488-4ed2-9efc-1656932356d2.png)

Sau một thời gian, ta thấy với mfa-code=0101 thì response trả về status code 302.

![image](https://user-images.githubusercontent.com/103978452/201523541-313244bc-2674-4f9a-bdbb-8bfc1ed1e70a.png)

Trên trình duyệt, truy cập /login2 rồi thay đổi cookie verify=carlos, nhập 2FA code là 0101, kết quả đăng nhập thành công. 

# 9. Brute-forcing a stay-logged-in cookie
Đăng nhập với tài khoản wiener:peter rồi bắt request tới /my-account?id=wiener

![image](https://user-images.githubusercontent.com/103978452/201253535-b4e10ed8-4649-4c68-8bb4-85d9e9bde1fc.png)

Sau khi phân tích stay-logged-in cookie, ta thấy cookie có dạng base64(username:md5(password)). Như vậy để bruteforce, ta cần tạo một danh sách phù hợp. Ta viết một đoạn code python để sinh ra danh sách các stay-logged-in cookie với format base64(carlos:md5(password)):

![image](https://user-images.githubusercontent.com/103978452/201253834-a0f4db46-f41c-4876-9d08-5ae018576bfd.png)

Vào phần Intruder, tiến hành bruteforce tới đường dẫn /my-account?id=carlos và đặt stay-logged-in cookie làm payload, sử dụng output của chương trình python trên.

Sau một thời gian, ta thấy duy chỉ có một request trả về HTTP status code 200

![image](https://user-images.githubusercontent.com/103978452/201254167-723b905a-0290-4767-a0cf-fe642288c92e.png)

Tiến hành decode base64 và search chuỗi md5 trên md5online.org, ta thu được username=carlos và password=soccer. Sử dụng thông tin thu được để đăng nhập, kết quả thành công.

# 10. Offline password cracking
Chèn đoạn mã xss sau vào trong input "Comment" của chức năng bình luận:

![image](https://user-images.githubusercontent.com/103978452/201256776-0246500b-0e6d-4a94-8552-b43dcf248197.png)

Sau khi submit, ta vào exploit server, truy cập access log thì thấy có request gửi đến với parameter cookie. Ta thu được chuỗi "Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz" chính là stay-logged-in cookie.

![image](https://user-images.githubusercontent.com/103978452/201257292-5f880aef-7718-4c56-b311-3a6a5f12d94e.png)

Tiến hành decode base64, ta được carlos:26323c16d5f4dabff3bb136f2460a943. Sau khi search chuỗi md5 trên md5online.org, ta thu được username=carlos và password=onceuponatime.

Sử dụng thông tin có được để đăng nhập và xóa tài khoản carlos, kết quả thành công.

# 11. Password reset poisoning via middleware
Thử chức năng đăng nhập với tài khoản wiener và dùng BurpSuite để intercept request GET /forgot-password. Ta thấy khi thay đổi Host header thì server sẽ trả về lỗi "Client Error".

Thử dùng header "X-Forwarded-Host: test.com", nhấn "Send" thì thấy trong Email client xuất hiện một email với URL có domain là test.com

![image](https://user-images.githubusercontent.com/103978452/201553696-0bdbf2bd-4ba7-4a75-a774-7d7179633311.png)

Ta thay đổi username=carlos, thiết lập X-Forwarded-Host thành domain của exploit-server. Sau khi gửi, ta vào access log của exploit-server thì thấy một request chứa reset password token.

![image](https://user-images.githubusercontent.com/103978452/201553805-6d2ee2c6-5824-4c73-9e89-90822b202e39.png)

Sử dụng token để truy cập GET /forgot-password?temp-forgot-password-token=<token_lay_duoc> rồi đổi mật khẩu của user carlos. Sử dụng thông tin có được để đăng nhập, kết quả thành công.


# 12. Password brute-force via password change
Đăng nhập với tài khoản wiener:peter rồi test thử chức năng đổi mật khẩu. Ta thấy:
+ Khi current-password đúng và new-password-1 = new-password-2 thì đổi mật khẩu thành công
+ Khi current-password đúng và new-password-1 != new-password-2 thì hiện lỗi "New passwords do not match"
+ Khi current-password sai và new-password-1 = new-password-2 thì bị logout và tính là 1 lần đăng nhập sai
+ Khi current-password sai và new-password-1 != new-password-2 thì hiện lỗi "Current password is incorrect"

Như vậy ta có thể dùng trường hợp cuối để tấn công bruteforce. Dùng BurpSuite bắt request đổi mật khẩu trong trường hợp cuối, thay đổi username=carlos và gửi đến Intruder để thực hiện tấn công bruteforce password. Ta thấy chỉ có password=biteme thì lỗi "New password do not match" mới xuất hiện.

![image](https://user-images.githubusercontent.com/103978452/201498712-0705e1b6-22fb-4877-9cff-2896e82beeca.png)

Như vậy ta thu được username=carlos và password=biteme. Sử dụng thông tin này để đăng nhập, kết quả thành công

# 13. Broken brute-force protection, multiple credentials per request

# 14. 2FA bypass using a brute-force attack

