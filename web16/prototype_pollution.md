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
Từ đoạn code trên, ta thấy nếu có thể thiết lập giá trị `config.transport_url=data:,alert(1)//` thì sẽ tạo được thẻ script và execute lệnh alert. Đây có thể trở thành prototype pollution sink.

Gửi request `/?search=x&__proto__[abc]=hello`, sau đó vào tab console nhập `Object.prototype.abc`, ta được giá trị `hello`. Như vậy, query string trong home page chính là một prototype pollution source. Ta thay đổi request thành `/?search=x&__proto__[transport_url]=data:,alert(1)//` rồi submit, kết quả bài lab được giải.

Nguyên nhân lệnh alert được execute là vì `config.transport_url` trong trường hợp này có giá trị `undefined`, do đó javascript sẽ tiếp tục tìm lên prototype của nó, đến khi gặp `Object.prototype.transport_url` có giá trị là `data:,alert(1)//` thì nó sẽ dừng lại. Kết quả, một thẻ script có thể thực thi lệnh alert được inject vào website.

# 2. DOM XSS via an alternative prototype pollution vector
Sử dụng DOM Invader, ta tìm được một source trong home page:

![image](https://user-images.githubusercontent.com/103978452/228148651-65df9309-3148-48a3-be19-5018cab74ac5.png)

Sau khi click "Test", ta thấy với request `GET /?__proto__.testproperty=DOM_INVADER_PP_POC` thì `Object.prototype.testproperty` sẽ trả về giá trị `DOM_INVADER_PP_POC`. Như vậy, đây là một prototype pollution source.

Tiếp tục sử dụng DOM Invader, ta tìm được một sink:

![image](https://user-images.githubusercontent.com/103978452/228149105-bbd2dbbf-0bfb-46b9-b2e9-7af34c790bfb.png)

```
eval('if(manager && manager.sequence){ manager.macro('+manager.sequence+') }');
```
Trong hàm eval có phép nối chuỗi bằng toán từ `+`, như vậy ta hoàn toàn có thể exploit XSS bằng cách cấu hình `manager.sequence=)};alert(1)//`. 

Dùng browser gửi request `GET /?__proto__.sequence=)};alert(1);//`. Khi đó, `Object.prototype.sequence` sẽ có giá trị là `)};alert(1)//` và nếu object `manager` không có property `sequence`, nó sẽ tìm ngược lên prototype và lấy giá trị của `Object.prototype.sequence`. Như vậy, lệnh alert được thực thi và bài lab được giải.

# 3. Client-side prototype pollution via flawed sanitization
Nhận thấy trong file `searchLoggerFiltered.js` có đoạn code sau:
```
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

function sanitizeKey(key) {
    let badProperties = ['constructor','__proto__','prototype'];
    for(let badProperty of badProperties) {
        key = key.replaceAll(badProperty, '');
    }
    return key;
}
```
Khối lệnh `if(config.transport_url){ ... }` sẽ kiểm tra `config.transport_url`, nếu tìm thấy sẽ tạo thẻ script với thuộc tính src có giá trị là giá trị của `config.transport_url`.

Như vậy, ta thấy query string là một source và đoạn code tạo tag script chính là sink. Tuy nhiên, website đã chặn prototype pollution attack bằng cách thay thế tất cả từ khóa "constructor", "__proto__", "prototype" bằng chuỗi rỗng. Tuy nhiên, ta có thể dễ dàng bypass bằng cách chèn payload "__pro__proto__to__". Dùng browser truy cập đường dẫn `/?__pro__proto__to__[transport_url]=data:,alert(1)//`, kết quả lệnh alert được thực thi và bài lab được giải.

# 4. Client-side prototype pollution in third-party libraries

# 5. Client-side prototype pollution via browser APIs

# 6. Privilege escalation via server-side prototype pollution

# 7. Detecting server-side prototype pollution without polluted property reflection

# 8. Bypassing flawed input filters for server-side prototype pollution

# 9. Remote code execution via server-side prototype pollution

# 10. Exfiltrating sensitive data via server-side prototype pollution

