# 1. OS command injection, simple case
Trong chức năng check stock, ta thấy body có dạng `productId=2&storeId=1`

Thử thay đổi body thành `productId=2&storeId=1'` thì thấy hiển thị lỗi `sh: 1: Syntax error:Unterminated quoted string`. Như vậy, server sử dụng hai biến productId và storeId để truyền vào một lệnh command, thực thi rồi trả về kết quả tương ứng.

Thay đổi body để thực thi câu lệnh whoami: `productId=2&storeId=1;whoami`, ta thu được kết quả mong muốn

![image](https://user-images.githubusercontent.com/103978452/202739993-e5acd98b-fd43-4d42-a90e-abde76bffc9d.png)

# 2. Blind OS command injection with time delays
Trong chức năng feedback, ta thấy response trả về chỉ là một object rỗng. Như vậy đây là blind OS command injection.

Body của request tới /feedback/submit có dạng `csrf=...&name=my_name&email=my_mail@gmail.com&subject=my_subject&mesage=my_message`. Lần lượt thử thêm `%22%3Bsleep+10%3Becho+%22` (ứng với `";sleep 10;echo "` sau khi URL decode) vào sau các trường name, email, subject và message. 

Ta thấy với body `csrf=Mfd0vSTsKCnatqeVnSeJaohf5YXVKSCV&name=triet%22%3Bsleep+10%3Becho+%2& email=trang%40gmail.com2&subject=trung&message=helloooo` thì response bị delay 10 giây. Như vậy, kết quả thành công.

# 3. Blind OS command injection with output redirection
