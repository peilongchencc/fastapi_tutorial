# FastAPI FAQ

记录FastAPI常见问题解答(Frequently Asked Questions)。<br>

- [FastAPI FAQ](#fastapi-faq)
  - [FastAPI流式返回为什么一定要 `yield f"data:{i}\n\n"` 这种写法？](#fastapi流式返回为什么一定要-yield-fdatainn-这种写法)


## FastAPI流式返回为什么一定要 `yield f"data:{i}\n\n"` 这种写法？

在使用 FastAPI 进行流式返回（streaming response）时，`yield f"data:{i}\n\n"` 这种写法主要是为了符合服务器发送事件（Server-Sent Events, SSE）的格式规范。SSE 是一种允许服务器在建立连接后，持续向客户端发送事件的技术。具体原因如下：<br>

1. **SSE 规范要求**：

SSE 是一种单向的持久连接，服务器可以不断地向客户端发送数据，而客户端不需要不断地请求数据。SSE 使用 HTTP 协议，通过 `text/event-stream` 的内容类型传输数据。根据 SSE 的规范，每条消息必须以 `data:` 开头，并以一个空行结尾。例如：<br>

```log
data: message 1

data: message 2
```

这样，客户端才能正确地解析和显示消息。<br>

2. **数据格式**：

`yield f"data:{i}\n\n"` 是为了确保每条消息符合 SSE 的格式。`data:` 表示这是一条数据消息，`{i}` 是具体的数据内容，`\n\n` 是为了表示消息的结束。<br>

3. **自动换行和分隔**：

SSE 规范要求每条消息之间用空行分隔，`yield f"data:{i}\n\n"` 通过两个换行符来实现这个分隔，以确保客户端能够正确解析每条消息。<br>

具体示例代码如下：<br>

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

@app.get("/stream")
async def stream():
    async def event_generator():
        for i in range(1, 6):
            yield f"data:{i}\n\n"
            time.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

在这个例子中，`event_generator` 是一个异步生成器函数，它生成符合 SSE 规范的消息，FastAPI 使用 `StreamingResponse` 将这些消息流式返回给客户端。这样客户端就可以持续接收服务器发送的事件，而不需要不断地发起新的请求。<br>

总结来说，`yield f"data:{i}\n\n"` 这种写法是为了确保每条消息符合 SSE 的格式规范，以便客户端能够正确解析和显示流式返回的数据。<br>

