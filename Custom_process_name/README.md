# 自定义进程名称

通过 `setproctitle` 在代码中动态设置进程名称。
- [自定义进程名称](#自定义进程名称)
  - [前景提要：](#前景提要)
  - [使用setproctitle:](#使用setproctitle)
  - [查看进程名：](#查看进程名)
    - [通过netstat查看：](#通过netstat查看)
    - [通过 `lsof` 查看指定端口的信息：](#通过-lsof-查看指定端口的信息)
    - [使用 `grep` 结合 `ps` 查看对应的服务:](#使用-grep-结合-ps-查看对应的服务)


## 前景提要：

我们都知道，在ubuntu系统，如果使用 `python main.py` 的方式启动服务，默认的进程名为 `python`。例如:

```log
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# netstat -tulnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8531            0.0.0.0:*               LISTEN      1390722/python      
tcp        0      0 0.0.0.0:8333            0.0.0.0:*               LISTEN      1090662/python      
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      321421/nginx: worke 
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      321421/nginx: worke 
tcp        0      0 0.0.0.0:8306            0.0.0.0:*               LISTEN      3277170/python       
```

这样的方式很不方便我们查看对应的程序，有没有合适的方式能帮我们更快速定位自己的程序呢？

常见方式有：

- 通过 setproctitle 在代码中动态设置进程名称。
- 通过 shell 脚本包装你的 Python 脚本，并在脚本中设置自定义名称。


## 使用setproctitle:

终端通过 `python main.py` 运行下列代码:

```python
"""
File Name: main.py
Description: 通过 setproctitle 在代码中动态设置进程名称。
Notes: 
Requirements: pip install setproctitle
"""
from fastapi import FastAPI
from setproctitle import setproctitle
import uvicorn

# 设置自定义进程名称
setproctitle("my_fastapi_service")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with custom process name!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8333)
```

服务正常启动，终端将显示:

```log
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# python main.py 
INFO:     Started server process [1740560]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8333 (Press CTRL+C to quit)
```

## 查看进程名：

新开一个终端查看所有端口的信息：

### 通过netstat查看：

```log
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# netstat -tulnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8531            0.0.0.0:*               LISTEN      1390722/python      
tcp        0      0 0.0.0.0:8333            0.0.0.0:*               LISTEN      1740560/my_fastapi_   
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      321421/nginx: worke 
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      321421/nginx: worke 
tcp        0      0 0.0.0.0:8306            0.0.0.0:*               LISTEN      3277170/python    
```

我们注意到 **8333** 端口的进程，**Program name** 已经改变了。（显示不完全是因为 netstat 和 lsof 等工具对进程名称显示长度有限制）

### 通过 `lsof` 查看指定端口的信息：

```log
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# lsof -i :8333
COMMAND       PID USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
my_fastap 1740560 root    6u  IPv4 73837540      0t0  TCP *:8333 (LISTEN)
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# 
```

### 使用 `grep` 结合 `ps` 查看对应的服务:

```log
(base) root@iZ2ze50qtwycx9cbbvesvxZ:/data# ps aux | grep my_fastapi_service
USER       PID     %CPU  %MEM   VSZ    RSS    TTY     STAT  START    TIME COMMAND
root    1740560    0.4   0.3   58256  49068  pts/69   S+    13:12    0:00 my_fastapi_service
root    1740938    0.0   0.0   6620   2380   pts/72   S+    13:14    0:00 grep --color=auto my_fastapi_service
```

🚨注意：只要有 grep 关键字在 COMMAND 列中，这一行就是 grep 自己。