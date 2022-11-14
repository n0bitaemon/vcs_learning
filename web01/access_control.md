# 1. Unprotected admin functionality
Truy cập /robots.txt, ta thấy đường dẫn đến trang admin là /administrator-panel

Truy cập /administrator-panel rồi xóa user carlos, kết quả thành công

# 2. Unprotected admin functionality with unpredictable URL
Vào trang chủ của website rồi sử dụng chức năng "View page source", ta có thể thấy đường dẫn đến trang admin:

![image](https://user-images.githubusercontent.com/103978452/201265800-1caa36af-8fbd-4a4a-b5d1-8cac20b8dea4.png)

Truy cập đường dẫn tìm được rồi xóa user carlos, kết quả trả về thành công

# 3. User role controlled by request parameter
Sau khi đăng nhập với tài khoản wiener:peter, ta không truy cập được /admin vì không có quyền.
Nhận thấy trong cookie có Admin=false, như vậy trang web sử dụng cookie này để kiểm tra người dùng có quyền hay không. Ta thử thay đổi Admin=true rồi tải lại trang, truy cập được vào trang admin.

![image](https://user-images.githubusercontent.com/103978452/201270837-187dcdde-59b1-4035-ae50-a049069f6bb4.png)

Từ trang admin ta xóa user carlos, kết quả thành công.

# 4. User role can be modified in user profile
Đăng nhập với tài khoản wiener:peter ta thấy không truy cập được tới /admin.
Bắt request /change-email rồi thêm trường "roleid":2 vào chuỗi json được gửi đi, ta thấy kết quả trả về thành công.

![image](https://user-images.githubusercontent.com/103978452/201271770-d50a7a7e-e264-475f-8827-6ad440d10b2b.png)

Thử truy cập lại vào trang /admin, truy cập thành công và xóa người dùng carlos.

# 5. User ID controlled by request parameter
Đăng nhập bằng tài khoản wiener:peter rồi vào trang my-account, ta thấy URL là /my-account?id=wiener

Thay tham số id, truy cập /my-account?id=carlos, ta thu được API của user carlos

# 6. User ID controlled by request parameter, with unpredictable user IDs
Đăng nhập tài khoản wiener:peter rồi click vào "My account", ta thấy trang chuyển hướng tới /my-account?id=43b37354-3032-4fea-ac2a-33adb2af46bd. Như vậy id của users là một chuỗi các kĩ tự và không thể đoán được.

Truy cập vào trang chủ và vào xem chi tiết một bài viết bất kỳ, rồi dùng dev tool để inspect tên tác giả, ta thấy một đường dẫn chứa ID của người đó.

![image](https://user-images.githubusercontent.com/103978452/201379128-da76ce74-5d2d-4015-b736-3e81480afc42.png)

Như vậy, ta có thể lấy thông tin ID của bất kỳ ai nếu họ là tác giả của một bài viết nào đó. Tìm trong danh sách ta thấy có bài "Football for dummies" được viết bởi carlos. Dùng dev tools ta lấy được id của user carlós là 4ded5e75-ca32-4644-9841-7651d6b52fb3

![image](https://user-images.githubusercontent.com/103978452/201380351-7d568e15-365b-445a-93f1-c45afb958c29.png)

Truy cập /my-account?id=4ded5e75-ca32-4644-9841-7651d6b52fb3, ta lấy được API key của carlos.

# 7. User ID controlled by request parameter with data leakage in redirect
Đăng nhập với tài khoản wiener:peter rồi truy cập /my-account?id=wiener, ta thấy bị chuyển hướng đến trang login. Như vậy không thể xem thông tin của user khác.

Tuy vậy, khi ta dùng BurpSuite bắt request này sẽ thấy response trả về có status code là 302, nhưng phần body của trang web (chứa thông tin của carlos) vẫn bị lộ ra.

![image](https://user-images.githubusercontent.com/103978452/201445219-fe38b500-ed48-43fd-9c73-2787d237466e.png)

Như vậy, ta có thể lấy được API key của user carlos.

# 8. User ID controlled by request parameter with password disclosure
Đăng nhập với tài khoản wiener:peter rồi vào "My Account", ta thấy:
+ URL có một tham số là id=wiener, thử thay đổi thành id=carlos thì ta thấy có thể truy cập vào profile của user carlos.
+ Phần đổi mật khẩu có một input với value là mật khẩu hiện tại, như vậy nếu vào được /my-account với id của admin, ta có thể có được mật khẩu của admin.

Như vậy, để xóa user carlos thì ta cần biết id của admin là gì.

Sau một vài lần thử, ta đoán được id=administrator trỏ đến profile của admin. Dùng dev tool để lấy mật khẩu của administrator rồi đăng nhập, xóa user carlos, ta được kết quả thành công

![image](https://user-images.githubusercontent.com/103978452/201451962-16c2f92f-5b14-4118-a1de-2cad197793c7.png)

# 9. Insecure direct object references
Đăng nhập với tài khoản wiener:peter, thử chức năng live chat rồi nhấn nút "View transcript". Ta thấy browser gửi request tới /download-transcript/2.txt và một file chứa đoạn hội thoại được tải về.

Bắt request với BurpSuite rồi sửa 2.txt thành 1.txt, ta thấy có những tin nhắn của một user khác. Trong đó có thông tin "my pasword is pnohengv1xfel7p674gt".

![image](https://user-images.githubusercontent.com/103978452/201459004-5a9fbd0b-dadd-416e-9ce2-43bb177b497c.png)

Thử đăng nhập với username=carlos và password=pnohengv1xfel7p674gt, kết quả thành công.

# 10. URL-based access control can be circumvented
Đầu tiên ta đăng nhập với tài khoản wiener:peter rồi bắt request tới /admin, kết quả trả về "Access Denied"

Ta thử dùng HTTP header "X-Original-URL: /admin" để ghi đè lên URL gốc, kết quả trả về trang admin thành công.

Tiếp theo, config request sao cho có query parameter là username=carlos, cùng với header "X-Original-URL: /admin/delete" để xóa user carlos. Kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/201358056-3c7e0c09-5e68-4605-b291-25e6dc4c050c.png)

# 11. Method-based access control can be circumvented
Đăng nhập với tài khoản administrator:admin rồi vào Admin panel, ta thấy có chức năng cho phép thăng cấp/hạ cấp một user bất kỳ. Dùng BurpSuite để bắt request, ta thấy khi thăng cấp 1 user thì browser sẽ gửi một POST request tới /admin-roles, body chứa hai tham số username=carlos&action=upgrade

Thử thay method POST thành GET, server trả về lỗi "Missing parameter 'username'". Ta thay đổi URL thành /admin-roles?username=carlos&action=upgrade, kết quả trả về nâng cấp thành công user carlos.

Ta hạ cấp user carlos rồi đăng nhập tài khoản wiener:peter thì thấy với request POST /admin-roles sẽ hiện lỗi "Unauthorized", như vậy ta thử dùng GET /admin-roles&username=wiener&action=upgrade. Kết quả trả về thành công

![image](https://user-images.githubusercontent.com/103978452/201468010-c16c5818-f047-459f-999f-aa27cc2b7269.png)

# 12. Multi-step process with no access control on one step
Thử đăng nhập với tài khoản administrator:admin, ta thấy trong Admin panel có chức năng upgrade/downgrade một user bất kỳ. Dùng BurpSuite để bắt request, ta thấy chỉ khi có biến confirmed=true trong request body (sau khi nhấn nút xác nhận) thì hành động mới được thực hiện.

Đăng nhập với tài khoản wiener:peter rồi thực hiện request tới /admin-roles, với các tham số action=upgrade&confirmed=true&username=wiener, kết quả upgrade thành công.

![image](https://user-images.githubusercontent.com/103978452/201459489-4197b6b9-461b-45f9-8eb0-3893c6759736.png)

# 13. Referer-based access control
Đăng nhập với tài khoản administrator:admin, ta thấy trong Admin panel có chức năng thăng cấp/hạ cấp một user bất kỳ. Dùng BurpSuite để bắt request khi thăng cấp user carlos, request GET /admin-roles?username=carlos&action=upgrade được gửi đi.

Trong HTTP header có Referer, ta thử xóa đi thì thấy lỗi "Unauthorized" xuất hiện. Như vậy việc phân quyền dựa vào HTTP header Referer.

Đăng nhập với tài khoản wiener:peter rồi gửi request đến /admin-roles?username=wiener&action=upgrade, cùng với HTTP header "Referer: https://0a7f003003e9668ac082149a0088002f.web-security-academy.net/admin". Sau khi submit, ta thu được kết quả thành công.

![image](https://user-images.githubusercontent.com/103978452/201468890-7b7eb020-6804-4e05-bee4-2bb3e1f73088.png)
