"""
Description: 解决跨域问题的示例代码。
Notes: 
1. 重点观察跨域问题的解决方案，代码逻辑是从笔者其他项目选取的。
2. 返回状态码 0 表示操作成功。例如，在 Unix 系统中，程序返回状态码 0 通常表示程序成功执行完毕，没有错误。
"""
import re
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 设置允许前端跨域连接
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许所有的源
    allow_credentials=True,
    allow_methods=["*"],    # 允许所有的HTTP方法
    allow_headers=["*"],    # 允许所有的HTTP头
)

class DataForm(BaseModel):
    """数据表单模型，包含用户提交的数据字段."""
    content: str = Field(..., title="内容")
    session_id: str = Field(default='0', title="会话id")
    interface_step: int = Field(default=0, title="会话阶段")
    times: int = Field(default=0, title="次数统计")
    intent_label: int = Field(default=0, title="归类")
    user_id: int = Field(..., title="用户id")
    name: str = Field(..., title="用户名")
    phone: str = Field(..., title="手机号")

def validate_chinese_phone_number(phone_number):
    """验证中国手机号码是否合法.

    Args:
        phone_number (str): 手机号码字符串.

    Returns:
        bool: 如果手机号码合法则返回True，否则返回False.
    """
    pattern = re.compile(r"^(?:\+86)?1[3-9]\d{9}$")
    return pattern.match(phone_number) is not None

async def send_verification_code():
    """模拟发送验证码.

    Returns:
        str: 包含验证码的字符串消息.
    """
    return '验证码(123456)已发送至您的手机，如果收到验证码，请告诉我验证码。\n如需验证码重发，请输入 "R"。'

async def send_verification(req: DataForm):
    """初始步骤，发送验证码.

    Args:
        req (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    req.intent_label = 1
    req.interface_step = 1
    req.content = await send_verification_code()
    return {"code": 0, "msg": "发送验证码", "data": req.model_dump()}

async def resend_verification(req: DataForm):
    """处理验证码重发请求.

    Args:
        req (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    req.content = await send_verification_code()
    return {"code": 0, "msg": "发送验证码", "data": req.model_dump()}

async def handle_verification(req: DataForm):
    """处理验证码验证.

    Args:
        req (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    if req.content == '123456':
        req.interface_step = 2
        req.times = 0
        req.content = '请输入您要预留的新手机号'
        return {"code": 0, "msg": "校验验证码", "data": req.model_dump()}
    else:
        req.times += 1
        if req.times >= 2:
            req.content = '校验验证码失败'
            req.intent_label = 0
            req.times = 0
            req.interface_step = 0
            return {"code": 0, "msg": "校验验证码失败", "data": req.model_dump()}
        req.content = '验证码输入错误，请重新输入'
        return {"code": 0, "msg": "校验验证码", "data": req.model_dump()}

async def handle_phone_number_update(req: DataForm):
    """处理手机号更新请求.

    Args:
        req (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    if validate_chinese_phone_number(req.content):
        req.intent_label = 0
        req.times = 0
        req.interface_step = 0
        req.content = '好的，已为您修改好新的预留手机号，您可登录 "我的"--> "个人主页" --> "预留手机号" 进行查看。'
        return {"code": 0, "msg": "手机号修改成功!!", "data": req.model_dump()}
    else:
        req.times += 1
        if req.times >= 2:
            req.content = '手机号校验失败'
            req.intent_label = 0
            req.times = 0
            req.interface_step = 0
            return {"code": 0, "msg": "手机号校验失败", "data": req.model_dump()}
        req.content = '手机号校验失败'
        return {"code": 0, "msg": "手机号校验失败", "data": req.model_dump()}

async def phone_number_modify(req: DataForm):
    """根据会话阶段处理手机号修改请求.

    Args:
        req (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    if req.interface_step == 0:
        # 初始步骤，发送验证码.
        return await send_verification(req)
    if req.interface_step == 1:
        if 'R' in req.content:
            # 处理验证码重发请求
            return await resend_verification(req)
        # 处理验证码验证.
        return await handle_verification(req)
    if req.interface_step == 2:
        # 处理手机号更新请求.
        return await handle_phone_number_update(req)

@app.post("/chat")
async def create_chat(item: DataForm):
    """处理创建请求，修改手机号.

    Args:
        item (DataForm): 用户提交的数据表单.

    Returns:
        dict: 包含返回码、消息和更新后的数据的字典.
    """
    return await phone_number_modify(item)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8848)