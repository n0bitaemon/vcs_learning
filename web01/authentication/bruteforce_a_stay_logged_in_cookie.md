# Brute-forcing a stay-logged-in cookie

Đăng nhập với tài khoản wiener:peter rồi bắt request tới /my-account?id=wiener

![image](https://user-images.githubusercontent.com/103978452/201253535-b4e10ed8-4649-4c68-8bb4-85d9e9bde1fc.png)

Sau khi phân tích stay-logged-in cookie, ta thấy cookie có dạng base64(username:md5(password)). Như vậy để bruteforce, ta cần tạo một danh sách phù hợp. Ta viết một đoạn code python để sinh ra danh sách các stay-logged-in cookie với format base64(carlos:md5(password)):

![image](https://user-images.githubusercontent.com/103978452/201253834-a0f4db46-f41c-4876-9d08-5ae018576bfd.png)

Vào phần Intruder, tiến hành bruteforce tới đường dẫn /my-account?id=carlos và đặt stay-logged-in cookie làm payload, sử dụng output của chương trình python trên.

Sau một thời gian, ta thấy duy chỉ có một request trả về HTTP status code 200

![image](https://user-images.githubusercontent.com/103978452/201254167-723b905a-0290-4767-a0cf-fe642288c92e.png)

Tiến hành decode base64 và decrypt md5, ta thu được username=carlos và password=soccer. Sử dụng thông tin thu được để đăng nhập, kết quả thành công.
