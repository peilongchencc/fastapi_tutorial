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
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
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
    print(encoded_data, type(encoded_data))
