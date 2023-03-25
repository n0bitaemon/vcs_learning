# 1. JWT authentication bypass via unverified signature
Đăng nhập với credentials wiener:peter, sau đó dùng BurpRepeater bắt request và vào tab JSON Web Token, ta thấy payload có dạng:
```
{
    "iss": "portswigger",
    "sub": "administrator",
    "exp": 1679620905
}
```
Thay đổi giá trị `"sub": "administrator"`, rồi submit request `GET /admin`, kết quả access admin panel thành công. Thay đổi path thành `/admin/delete?username=carlos`, bài lab được giải.

# 2. JWT authentication bypass via flawed signature verification
Đăng nhập với credentials wiener:peter. Dùng JSON Editor thay đổi `"alg": "none"` và `"sub": "administrator"`, sau đó xóa đi phần signature trong JWT token. Gửi request `GET /admin` với token sau khi đã chỉnh sửa, kết quả access thành công.

Thay đổi path thành `/admin/delete?username=carlos`, bài lab được giải.

# 3. JWT authentication bypass via weak signing key
Sử dụng hashcat với wordlist cho sẵn, ta thu được secretkey=secret1
```
hashcat -a 0 -m 16500 eyJraWQiOiIzNmMzZTQ4OS1mNTNjLTRjNDItYmM0Mi03OWEzNzBmZDJmZDciLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY3OTYyMTgwMX0.mZGr5au5sw-h_MS0wVreSB9ajiZfnrb54h-4WGrIwV0 wordlist.txt
```
Dùng secret key này để thay đổi `"sig": "administrator"`, sau đó gửi request đến `/admin/delete?username=carlos`, kết quả thành công.

# 4. JWT authentication bypass via jwk header injection
Đăng nhập với credentials wiener: peter. Sử dụng JWT Editor Keys để tạo một RSA Keys mới, sau đó dùng Burp Repeater bắt request tới `/admin`, vào tab "JSON Web Token" để thay đổi giá trị `"sub": "administrator"`. 

Click "Attack" > Click "Embedded JWK" > Chọn RSA key đã tạo rồi click "OK". Sau khi gửi request, ta thấy access trang admin thành công.

Sở dĩ chúng ta có thể exploit như vậy vì server đã mặc định lấy object `jwk` trong JWT làm public key, trong khi trường đó có thể bị thay đổi. Như vậy, nếu ta thêm một trường `jwk` để server dùng làm public key, và sử dụng private key tương ứng để sign JWT, thì kết quả verify sẽ trả về hợp lệ.

Thay đổi path thành `/admin/delete?username=carlos`, kết quả bài lab được giải.

# 5. JWT authentication bypass via jku header injection

# 6. JWT authentication bypass via kid header path traversal

# 7. JWT authentication bypass via algorithm confusion

# 8. JWT authentication bypass via algorithm confusion with no exposed key
