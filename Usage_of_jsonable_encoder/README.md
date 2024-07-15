# Usage_of_jsonable_encoder

在 FastAPI 中，`jsonable_encoder` 函数的主要作用是将复杂的对象转换为可以用 JSON 序列化的基本数据类型。具体来说，它可以处理以下类型的数据：<br>

1. **Pydantic 模型**：将 Pydantic 模型转换为字典。
2. **数据库模型**：将 ORM 模型实例转换为字典。
3. **日期时间对象**：将 `datetime` 对象转换为字符串（默认 ISO 格式，也可以自定义）。
4. **其他 Python 对象**：例如 `set` 转换为 `list`，自定义类可以通过定义 `__jsonable_encoder__` 方法来自定义转换逻辑。

简单来说，`jsonable_encoder` 的作用是确保数据在传输前转换为 JSON 兼容的格式，这对于通过 API 发送响应数据尤其重要。<br>

`custom_encoder` 是 `jsonable_encoder` 中的参数，可以对 `data` 中的所有内容进行遍历操作，并对特定类型的对象应用自定义的编码逻辑。`jsonable_encoder` 函数在遍历输入数据时，会检查每个元素的类型，并根据定义的 `custom_encoder` 执行相应的编码转换。<br>

以下是一个示例，展示了 `custom_encoder` 如何遍历数据并对特定类型的对象进行编码：<br>

```python
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    name: str
    price: float
    available: bool

class User(BaseModel):
    username: str
    joined_at: datetime

def encode_json(data: dict):
    return jsonable_encoder(
        data,
        custom_encoder={
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
            Item: lambda x: {"item_name": x.name, "item_price": x.price, "item_available": x.available}
        }
    )

if __name__ == "__main__":
    # 示例数据
    item = Item(name="Laptop", price=999.99, available=True)
    user = User(username="johndoe", joined_at=datetime(2024, 6, 30, 10, 0, 0))
    
    sample_data = {
        "item": item,
        "user": user,
        "timestamp": datetime(2023, 7, 3, 14, 30, 45),
        "numbers_set": {1, 2, 3}
    }

    # 使用 encode_json 函数编码数据
    encoded_data = encode_json(sample_data)
    
    # 输出编码后的数据
    print(encoded_data)
```

在这个示例中，`custom_encoder` 包含两个自定义编码器：<br>
1. 对 `datetime` 对象使用自定义的日期时间格式。
2. 对 `Item` 对象进行自定义编码，将其转换为包含自定义字段名的字典。

输出结果将会如下（格式可能会有所不同）：<br>

```json
{
    "item": {
        "item_name": "Laptop",
        "item_price": 999.99,
        "item_available": true
    },
    "user": {
        "username": "johndoe",
        "joined_at": "2024-06-30 10:00:00"
    },
    "timestamp": "2023-07-03 14:30:45",
    "numbers_set": [1, 2, 3]
}
```

可以看到：<br>

- `datetime` 对象被转换为了自定义的日期时间格式字符串。
- `Item` 对象被转换为包含自定义字段名的字典。

`jsonable_encoder` 会递归地遍历数据结构，并在遇到特定类型的对象时，使用 `custom_encoder` 中定义的函数进行编码转换。这种机制允许我们对复杂数据结构中的特定类型对象进行自定义处理。<br>


## 注意事项:

### `datetime`的使用:

`datetime` 对象本身不会在未传入具体时间的情况下自动使用当前时间。不过，你可以在创建 `datetime` 对象时显式地指定使用当前时间。<br>

例如，如果你想在创建 `User` 对象时默认使用当前时间，可以这样做：<br>

```python
from datetime import datetime
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    name: str
    price: float
    available: bool

class User(BaseModel):
    username: str
    joined_at: datetime = datetime.now()  # 使用当前时间作为默认值
```