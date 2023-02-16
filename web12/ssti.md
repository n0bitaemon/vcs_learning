# 1. Basic server-side template injection
Khi xem product với id=1, nhận thấy message "Unfortunately this product is out of stock" được hiển thị, và url có dụng `/?message=....`. Thử với `/?message=<%=7*7%>` thì phần message hiển thị 49. Như vậy website có lỗi SSTI.

Lab description cho ta biết website sử dụng ERB template, như vậy ta chuyển đến URL `/?message=<%=system("rm /home/carlos/morale.txt")` để xóa file morale.txt. Kết quả thành công.

# 2. 

