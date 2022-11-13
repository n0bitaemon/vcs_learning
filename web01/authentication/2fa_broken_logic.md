# 2FA broken logic
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
