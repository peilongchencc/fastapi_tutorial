# 跨域问题:

跨域问题（CORS，Cross-Origin Resource Sharing）是指浏览器出于安全考虑，限制了从一个域（Origin）加载的网页对另一个域的资源进行请求的行为。<br>
- [跨域问题:](#跨域问题)
  - [跨域问题出现的场景:](#跨域问题出现的场景)
  - [同源策略解释:](#同源策略解释)
    - [举例说明:](#举例说明)
  - [跨域问题解决方案:](#跨域问题解决方案)


## 跨域问题出现的场景:

跨域问题常出现在前端与后端联调时，例如，当你的前端应用在 `http://localhost:3000` 上运行，而后端 API 服务在 `http://localhost:8848` 上运行时，这两个服务就属于不同的域。当前端试图访问后端的 API 时，浏览器会阻止这种请求，因为它违反了同源策略。<br>

💦可以从后端的后台看到，当浏览器发起一个跨域请求时，它会首先发出一个 "预检" 请求（ **OPTIONS 请求** ），以检查目标服务器是否允许该跨域请求。如果目标服务器没有适当的 **CORS** 设置:<br>

- 浏览器将阻止前端从后端获取数据，并在控制台显示跨域错误。
- 后端将提示"405 Method Not Allowed"。


## 同源策略解释:

同源策略中的“源”是指协议、域名和端口的组合。如果两个 URL 的协议、域名和端口都相同，则它们被认为是同源的。**(路径可以不同)** <br>

### 举例说明:

假设你有两个 URL:<br>

- http://example.com:8080/api/data

- http://example.com:8080/ui/page

这两个 URL 的协议（http）、域名（example.com）和端口（8080）都是相同的，只是路径不同（ `/api/data` 和 `/ui/page` ）。根据同源策略，它们被认为是同源的，因此浏览器允许它们之间进行通信。<br>

🚨非同源的例子非常多，两个 URL 的协议（http）、域名（example.com）和端口只要有一个不同都属于非同源。<br>


## 跨域问题解决方案:

为了允许前端访问后端 API，需要通过 CORS 机制来告知浏览器该请求是安全的。FastAPI 提供了一个简单的方式来处理这个问题，就是使用 `CORSMiddleware` 中间件来配置允许的跨域请求。例如：<br>

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 设置允许前端跨域连接
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有的源
    # allow_origins=["http://localhost:8081"],  # (可选)只允许从 http://localhost:8081 这个源的请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有的HTTP方法
    allow_headers=["*"],  # 允许所有的HTTP头
)

# 你的其他代码
# ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)
```

这段代码的含义是:<br>

- `allow_origins=["*"]`：允许所有源发起的请求。你也可以指定具体的域名，如 `allow_origins=["http://localhost:8081"]`。
- `allow_credentials=True`：允许包含认证信息（如 cookies）的请求。
- `allow_methods=["*"]`：允许所有 HTTP 方法（如 GET、POST、PUT、DELETE）。
- `allow_headers=["*"]`：允许所有 HTTP 头，例如 `Content-Type`。

没有这段设置时，浏览器会因跨域问题阻止前端对后端的访问，导致前端无法获取后端的数据或服务。通过正确配置 CORS，可以使得前端安全地访问后端的资源。<br>

总之，跨域问题是一个安全机制，但可以通过适当的配置来允许受信任的跨域请求，从而使得前后端能够正常通信。<br>