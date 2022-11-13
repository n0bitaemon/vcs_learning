# Username enumeration via response timing
Login sử dụng tài khoản wiener:peter và dùng BurpSuite để bắt request. Chỉnh sửa password có độ dài thật lớn, chẳng hạn length=1056, sau đó thử với các trường hợp username đúng và sai. Ta thấy nếu username đúng thì thời gian nhận được response lên đến gần 5 giây, trong khi với trường hợp username sai thì response trả về sau chỉ 244ms.

Chức năng login sẽ bị khóa nếu đăng nhập sai nhiều lần. Tuy nhiên ta thấy có thể bypass bằng cách đặt X-Forwarded-For HTTP header.
Chuyển request /login tới Intruder, đặt X-Forwarded-For header và username là payload1 và payload2. 

![image](https://user-images.githubusercontent.com/103978452/201521614-72fadc79-0959-4419-9848-a90fc828a348.png)

Thực hiện bruteforce với payload1 gồm các địa chỉ IP từ 1.1.1.1 đến 1.1.1.255, còn payload2 thì sử dụng wordlist cho username có sẵn. Ta thấy chỉ có với username=activestat thì có thời gian phản hồi lên đến 4923 giây. Như vậy có khả năng đây là một username hợp lệ.

![image](https://user-images.githubusercontent.com/103978452/201521542-ba0337e2-2036-4b61-b76a-18b00fda1760.png)

Thay đổi request, đặt username=activestat và payload thứ 2 là password rồi thực hiện bruteforce với wordlist cho sẵn của password. Sau một thời gian, ta thấy chỉ với password=harley thì response trả về có status code 302. Sử dụng username=activestat và password=harley để đăng nhập, ta thu được kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201522030-81ba90a5-a7cf-415a-bcbd-558c78133c42.png)
