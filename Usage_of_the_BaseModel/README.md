# Usage_of_the_BaseModel

本章介绍FastAPI中`BaseModel`的使用，`BaseModel` 是一个重要的类，用于定义数据模型。它来自于Pydantic库，主要用于数据验证和解析。下面是`BaseModel`的主要使用方法和示例：<br>

- [Usage\_of\_the\_BaseModel](#usage_of_the_basemodel)
    - [1. 基本使用](#1-基本使用)
    - [2. 数据验证](#2-数据验证)
    - [3. 预设默认值](#3-预设默认值)
    - [4. 嵌套模型](#4-嵌套模型)
    - [5. 数据解析和转换](#5-数据解析和转换)
  - [使用`BaseModel`的重要作用:](#使用basemodel的重要作用)
  - [使用Postman测试:](#使用postman测试)
    - [前提条件](#前提条件)
    - [在Postman中测试POST请求](#在postman中测试post请求)
    - [错误处理](#错误处理)
    - [item默认以JSON(字典)方式返回数据:](#item默认以json字典方式返回数据)
  - [注意事项:](#注意事项)
    - [在FastAPI中，使用`BaseModel`定义的数据模型时，字段必须指定类型。](#在fastapi中使用basemodel定义的数据模型时字段必须指定类型)
    - [使用`BaseModel`定义的数据模型时，数据传输只能使用json格式:](#使用basemodel定义的数据模型时数据传输只能使用json格式)


### 1. 基本使用

`BaseModel`用于定义请求和响应的数据结构。它的字段类型和验证规则会自动应用到传入的数据上。<br>

```python
# basemodel_usage.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)
```

在上面的例子中，我们定义了一个`Item`类继承自`BaseModel`，并在POST请求中使用这个数据模型。传入的数据会根据`Item`类的定义进行验证和解析。<br>

### 2. 数据验证

`BaseModel`可以自动进行数据验证，如果数据不符合定义的类型或规则，会返回一个验证错误。<br>

```python
@app.post("/validate/")
async def validate_item(item: Item):
    return {"message": "Item is valid", "item": item}
```

如果请求数据中`price`不是一个浮点数，FastAPI会自动返回一个400错误，提示数据格式错误。<br>

### 3. 预设默认值

可以为模型中的字段设置默认值，如果请求中没有提供这些字段，Pydantic会使用默认值。<br>

```python
class Item(BaseModel):
    name: str
    description: str = "This is a default description"
    price: float
    tax: float = 0.1
```

### 4. 嵌套模型

`BaseModel`可以嵌套使用，即一个模型的字段可以是另一个模型的实例。<br>

```python
class User(BaseModel):
    username: str
    full_name: str = None

class Item(BaseModel):
    name: str
    price: float
    owner: User

@app.post("/items/")
async def create_item(item: Item):
    return item
```

在这个例子中，`Item`模型包含了一个`User`模型作为字段。<br>

### 5. 数据解析和转换

`BaseModel`可以自动解析和转换传入的数据类型，例如将字符串转换为浮点数。<br>

```python
item = Item(name="example", price="5.5")
print(item.price)  # 输出: 5.5
```

## 使用`BaseModel`的重要作用:

通过使用`BaseModel`，可以提高代码的可靠性和可维护性，减少手动编写数据验证逻辑的工作量。<br>


## 使用Postman测试:

使用Postman测试FastAPI应用的POST请求非常简单。下面是使用Postman测试一个包含`BaseModel`的FastAPI应用的详细步骤：<br>

### 前提条件

确保已经安装并运行了FastAPI应用。例如，我们将使用前面的例子：<br>

```python
# basemodel_usage.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)
```

启动应用：<br>

```bash
python basemodel_usage.py
```

应用运行在的`http://0.0.0.0:8848`。<br>

### 在Postman中测试POST请求

1. **打开Postman**

打开Postman应用。

2. **创建一个新的请求**

- 点击左上角的“New”按钮，然后选择“Request”。

- 给请求命名，例如`Create Item`，并选择一个保存的集合（或者创建一个新的集合）。

3. **设置请求方法和URL**

- 将请求方法设置为`POST`。
- 在URL栏中输入`http://0.0.0.0:8848/items/`。

4. **设置请求头**

- 点击“Headers”标签。

- 添加一个新的Header，键为`Content-Type`，值为`application/json`。

5. **设置请求体**

- 点击“Body”标签。
- 选择“raw”。
- 在右侧下拉菜单中选择`JSON`。
- 在文本框中输入JSON数据，例如：

```json
{
"name": "Sample Item",
"description": "This is a sample item",
"price": 10.5,
"tax": 1.5
}
```

针对 `float` 类型，如果你的 `json` 文件对应内容填写的是整数，传入后端后`BaseModel`会自动转换为`float`类型，例如 `"tax": 2` --> `"tax": 2.0`。<br>

1. **发送请求**

- 点击“Send”按钮发送请求。

7. **查看响应**

- 在下方的响应区域查看服务器返回的结果。应该会看到与发送的JSON数据相同的响应：

```json
{
"name": "Sample Item",
"description": "This is a sample item",
"price": 10.5,
"tax": 1.5
}
```

### 错误处理

如果发送的数据格式不正确，FastAPI会返回一个 `422 Unprocessable Entity` 错误。你可以通过修改请求体的数据格式来测试不同的验证情况，例如：<br>

```json
{
"name": "Sample Item",
"description": "This is a sample item",
"price": 10.5,
"tax": "tom"
}
```

后端提示:<br>

```log
INFO:     Started server process [217483]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8848 (Press CTRL+C to quit)
INFO:     221.216.117.27:10081 - "POST /items/ HTTP/1.1" 422 Unprocessable Entity
```

Postman返回内容为:<br>

```log
{
    "detail": [
        {
            "type": "float_parsing",
            "loc": [
                "body",
                "tax"
            ],
            "msg": "Input should be a valid number, unable to parse string as a number",
            "input": "tom"
        }
    ]
}
```

这个错误表明在请求体中的 `tax` 字段期望是一个数字，但输入提供的是字符串 `"tom"`。以下是详细的说明：<br>

- **错误类型 (`float_parsing`)**：这表示系统尝试将输入解析为浮点数但失败了。

- **位置 (`body`, `tax`)**：这说明错误发生在请求体中的 `tax` 字段。

- **消息 (`msg`)**：错误消息指出输入应该是一个有效的数字，但无法将字符串解析为数字。

- **输入 (`input`)**：提供的输入是 `"tom"`，这不是一个有效的数字。

要解决这个问题，请确保请求体中的 `tax` 字段提供的是一个有效的数字。例如：<br>

```json
{
    "tax": 15.5
}
```


### item默认以JSON(字典)方式返回数据:

上述例子中 `return item` 返回的是一个继承`BaseModel`的类，可以通过修改代码查看效果:<br>

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    print(item, type(item))
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)
```

正常传输数据后，可以看到后端显示如下:<br>

```log
INFO:     Started server process [221504]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8848 (Press CTRL+C to quit)
name='Sample Item' description='This is a sample item' price=10.5 tax=2.0 <class '__main__.Item'>
INFO:     221.216.117.27:10083 - "POST /items/ HTTP/1.1" 200 OK
```

在 FastAPI 中，Pydantic 模型（如 Item）可以自动转换为 JSON(其实就是字典)。这是因为 FastAPI 使用 Pydantic 来处理请求和响应数据的验证和序列化。虽然在代码中打印时看到的是 `__main__.Item` 类型，但 FastAPI 会在返回响应时将 Pydantic 模型自动转换为 JSON 格式。<br>

可以使用以下代码进行测试:<br>

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8848/items/"
        payload = {
            "name": "Sample Item",
            "description": "This is a sample item",
            "price": 25.5,
            "tax": 1.5
        }
        async with session.post(url, json=payload) as response:
            print("Status:", response.status)
            print("Content-Type:", response.headers['content-type'])
            json_response = await response.json()
            print("Response JSON:", json_response)
            print("type:", type(json_response))
            print(json_response["price"])
            
if __name__ == "__main__":
    asyncio.run(main())
```

终端输出:<br>

```log
Status: 200
Content-Type: application/json
Response JSON: {'name': 'Sample Item', 'description': 'This is a sample item', 'price': 25.5, 'tax': 1.5}
type: <class 'dict'>
25.5
```

如果想要直接返回 `dict` 形式:<br>

```python
@app.post("/items/")
async def create_item(item: Item):
    rtn = item.model_dump()
    print(rtn, type(rtn))
    return rtn
```

如果想要将内容以 `str` 形式返回:<br>

```python
@app.post("/items/")
async def create_item(item: Item):
    rtn = item.model_dump_json()
    print(rtn, type(rtn))
    return rtn
```

## 注意事项:

### 在FastAPI中，使用`BaseModel`定义的数据模型时，字段必须指定类型。

Pydantic（`BaseModel`的基础库）要求每个字段都要有明确的数据类型，以便在数据验证和解析时能够正确地进行处理。<br>

如果只定义变量名称而不指定数据类型，Pydantic会报错。因此，至少需要指定字段的类型，即使不提供默认值。：<br>

如果试图只定义变量名称而不指定类型，Pydantic会抛出错误。例如：<br>

```python
from pydantic import BaseModel

class Item(BaseModel):
    name  # 缺少类型定义
```

这个代码会导致错误：<br>

```log
NameError: name 'name' is not defined
```

### 使用`BaseModel`定义的数据模型时，数据传输只能使用json格式:

🚨如果使用Postman测试，需要添加一个新的Header，键为`Content-Type`，值为`application/json`<br>

🔥如果想要使用 `x-www-form-urlencoded` 传输数据，需要将 FastAPI 端点的参数从 JSON 修改为表单数据。可以使用 `Form` 类来实现这一点。<br>

以下是修改后的代码：<br>

```python
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    tax: float = Form(None)
):
    item = Item(name=name, description=description, price=price, tax=tax)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)
```

在 Postman 中进行测试时，请按照以下步骤操作：<br>

1. 打开 Postman，选择 `POST` 请求类型。
2. 输入 URL，例如 `http://127.0.0.1:8848/items/`。
3. 选择 `Body` 选项卡，然后选择 `x-www-form-urlencoded`。
4. 在键值对中输入以下内容：
   - `name`，值为您希望的商品名称。
   - `description`，值为商品描述（可选）。
   - `price`，值为商品价格。
   - `tax`，值为税率（可选）。
5. 点击 `Send` 按钮发送请求。

例如，您可以输入以下键值对：<br>

- `name`：Example Item
- `description`：This is an example item.
- `price`：19.99
- `tax`：1.99

这样设置后，点击 `Send` 即可看到返回的数据。<br>