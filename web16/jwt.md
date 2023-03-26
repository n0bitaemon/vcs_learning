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
Đăng nhập với credentials wiener:peter. Sử dụng JWT Editor Keys để tạo một RSA Keys mới, sau đó dùng Burp Repeater bắt request tới `/admin`, vào tab "JSON Web Token" để thay đổi giá trị từ `"sub": "administrator"`, đồng thời trong phần header thêm thuộc tính `"jku": "https://exploit-0af300b9039deb6dc005a86501c800cc.exploit-server.net/exploit"`.

Tiếp đó, vào exploit server, cấu hình đoạn body chính là một mảng các keys, trong đó có keys đã được tạo trước đó sau:
```
{
  "keys": [
    {
      "p": "9Y6EfMdtHPVajG3js4ca64X7ipp5NnyAfXWK9CLB_YpmNhJ0z1u23hroywrcjPfeDCc7m-NK1Eel89qI0peBFBkElvD1YUIHhP4UO1ZqtEZlHwAAqGTzKyPUWqX0SI9HHoa2B7EPtW8dcNfOcDDZtVCNdh30OVJspcmPJ9rIjnE",
      "kty": "RSA",
      "q": "vvpH4KZH1LljcsWW3zldZ1BQRYpuAfDV3Ab8JTy7EAr4pbsFDCXZbZzbCPeR6rVXabeio7b4p84rxRIRxXT982Wr7rzQ1EmPTA8nGWYg8syU-zw9en8VTiLCaAN2VtDTBZcomd7n_9403eaVFXOoS0G_K5cjNYam3AQ_K6JtEIc",
      "d": "T7LYSHgF2D8RJThM_V873rFd11QoFZaZ4lsxHvIhHUt1SNnT1Y4clDuzK_qYVnHWhEK08-q6Q37csUNXXxg3XT6uLzYe8nijHr85tNiEH8iLBlXC4MyOz8ufFuQGcwS3k0ebAUiHudo9jtQCdWoNP-f62kByWil4nU5B8dyWmUP3jR5Buyj6Ny0jFxRpXwFnKFVuRYTExnvaP9bs9JKr9Pb9gDtdwadbVHe606Vxpc80gNbDgu5Yiib9fOWFi0xhbDhRwxTa9eTfkMCu7DwnVadWd9p34MfadelAeVOFeg1yJxT7x41TTtBxSjwaVNoyBVxv_Isw8_Cy6tK2nF1qoQ",
      "e": "AQAB",
      "kid": "54518cf4-7917-471d-bd3e-552093192bd8",
      "qi": "mfyjGJN6D1dMfmovTfzhSAutaHl0LSHgHhB9KkVtEvKc6q5-8fozb60_0M6gd809lffRLhui0eDuJZH1IglTUUmbFwq850okqmyFyn5Yyc2v0R22ffiiqqqtVCPIrvqE-K4lNfAhB_7Kd9Ocb9IiRxrIJrDR_TyI6JaOmdGLr8Q",
      "dp": "g1tTwDQmSGFvqMN4FSdm3Sr1HnX39Y-wZGymgma9g1Wvy6kf13TmY_XdJhCPXtGRdMrf9komU1xoiAQVQSJOqGOhsuT_PqHFx_zq8bsOpZUqruSfdXVbJ26pQDyaat5KWygQ5BhxoMrp4t1uz1EyhO2sXs0zQh63hBBIhjdhJeE",
      "dq": "Mc3NXt2eT_CE6dJzlQU9wYqlVG1UYPcwnm_H4-Ihmn5x9659E3zvZfGJAZ6mlAH0qOI17OHzmLdgnMUok0j-TTJPkzP0ddg1IY22EZ6bqxYFKDu-gKqRoM3ZywxUGTHeRk_0S6Rg9k45lUDj0jNWSUH9G94PVY8nBquo2bVDIhM",
      "n": "ty_YdADPlQWkVWEVu9IBiyqtzzGQc1eY3XzkrhoFE5ra4JOldOggs8kC3Hh03yZWVjig4T8J57b0KJ5P6UyLbdnD2BEmbHkK5za-wUCSdSxw8A1xSPZKeD36Ac5BA0Bs0VUExoZ8qLP-LZH9n-HbS8whPW7A5YVvNDeNJl6L2H0u1p76XXQPkquFlQh_jQWgYX4yMkW4Zd95QhI5193zyQ75LEAZe-GhbsMvMnWN1mQo4av7VBHLMGZiAPLtUI977oD0ZQKbYnLjq2D7u7hetz364Cj7GdQ7FulGZcFqI40lkSKT_e0xe6XKEUxoaJ4vJbE12_FHiGujKck0EMctlw"
    }
  ]
}
```
Trở lại tab JSON Web Token, click "Sign" để tiến hành signing với RSA key đã tạo. Click "Send", ta thấy access trang admin thành công.

Thay đổi path thành `/admin/delete?username=carlos`, bài lab được giải.

# 6. JWT authentication bypass via kid header path traversal
Đăng nhập với credentials wiener:peter, sau đó dùng BurpRepeater để bắt request tới `/admin`. Trong tab JSON Web Token, ta sửa tham số kia trong phần header thành `"kid": "../../../../dev/null"`. Tiếp đó, tiến hành thay đổi `"sub": "administrator"` và sign lại JWT với key là một empty string. Sau khi submit, ta access trang admin thành công.

Sở dĩ có thể exploit là vì website dùng tham số "kid" để trỏ tới một static file, và dùng nó để làm key. Khi thay đổi thành `../../../../dev/null`, key sẽ tương ứng một chuỗi rỗng. Như vậy, ta có thể thay đổi JWT theo ý muốn do key đã biết trước.

Đổi path thành `/admin/delete?username=carlos`, bài lab được giải thành công.

# 7. JWT authentication bypass via algorithm confusion

# 8. JWT authentication bypass via algorithm confusion with no exposed key
