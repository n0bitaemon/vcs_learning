# 1. Basic server-side template injection
Khi xem product với id=1, nhận thấy message "Unfortunately this product is out of stock" được hiển thị, và url có dụng `/?message=....`. Thử với `/?message=<%=7*7%>` thì phần message hiển thị 49. Như vậy website có lỗi SSTI.

Lab description cho ta biết website sử dụng ERB template, như vậy ta chuyển đến URL `/?message=<%=system("rm /home/carlos/morale.txt")` để xóa file morale.txt. Kết quả thành công.

# 2. Basic server-side template injection (code context)

# 3. Server-side template injection using documentation
Đăng nhập với credentails "content-manager:C0nt3ntM4n4g3r", ta thấy có chức năng "Edit Template" và có thể Preview sau khi edit. Thử chèn payload `${7*7}` thì trong response có số 49, như vậy website có lỗ hổng SSTI.

Thử chèn `${abc}` thì xuất hiện thông báo lỗi cho ta biết website sử dụng template "freemaker" với ngôn ngữ Java.

![image](https://user-images.githubusercontent.com/103978452/219274969-c5098403-5979-4a8a-aafe-46d20f57f3ba.png)

Sau khi research trên internet, ta tìm được một số payload. Thử chèn `${"freemarker.template.utility.Execute"?new()("id")}` thì kết quả của lệnh id được trả về trong response. Như vậy, để xóa file "morale.txt", ta chèn vào payload `${"freemarker.template.utility.Execute"?new()("rm /home/carlos/morale.txt")}`. Sau khi click Review, bài lab được giải thành công.

# 4. Server-side template injection in an unknown language with a documented exploit

# 5. Server-side template injection with information disclosure via user-supplied objects

# 6. Server-side template injection in a sandboxed environment

# 7. Server-side template injection with a custom exploit
