from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI()

# 定义请求体的数据模型
class UserInput(BaseModel):
    text: str

# 定义处理函数
async def process_text(input_text: str):
    result1 = input_text.upper()        # 转换为大写
    await asyncio.sleep(1)              # 模拟耗时操作
    yield f"data: Uppercase: {result1}\n\n"

    result2 = input_text.lower()        # 转换为小写
    await asyncio.sleep(1)              # 模拟耗时操作
    yield f"data: Lowercase: {result2}\n\n"

    result3 = input_text[::-1]          # 反转字符串
    await asyncio.sleep(1)              # 模拟耗时操作
    yield f"data: Reversed: {result3}\n\n"

    result4 = len(input_text)           # 计算字符串长度
    await asyncio.sleep(1)              # 模拟耗时操作
    yield f"data: Length: {result4}\n\n"

# 定义端点
@app.post("/process")
async def process_input(user_input: UserInput):
    return StreamingResponse(process_text(user_input.text), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)