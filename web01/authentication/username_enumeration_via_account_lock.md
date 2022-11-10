# Username enumeration via account lock
Đầu tiên ta bắt request tới /login bằng Burpsuite

Chuyển request vào intruder, đặt username và password trở thành payload rồi thực hiện bruteforce với wordlist của username là wordlist đã cho, còn wordlist cho password thì dùng 1 danh sách gồm khoảng 5 chuỗi bất kỳ (Lưu ý đặt password phía trước username để thực hiện các requests login liên tiếp tới cùng một username)

![image](https://user-images.githubusercontent.com/103978452/201057998-9f29ae0a-de68-406e-8d4c-9aa26d99800b.png)

Vào tab Options, tới phần Grep-Extract rồi chọn chuỗi "Invalid username or password" làm dấu hiệu. Thực hiện cluster bomb bruteforce attack, ta thấy chỉ có username=guest mới xuất hiện dòng "You have made too many incorrect login attemps...". Như vậy ta biết được username=guest

Thực hiện bruteforce attack kiểu sniper, với payload là password (wordlist cho trước bởi challenge) và đặt username=guest, ta thấy chỉ có dòng password=daniel thì không có thông báo lỗi. Như vậy có thể đây là password.

![image](https://user-images.githubusercontent.com/103978452/201059313-3064ccbe-eef0-43f8-80c3-36f6a35ea19d.png)


Thực hiện đăng nhập với username=guest và password=daniel, ta thu được kết quả thành công.
