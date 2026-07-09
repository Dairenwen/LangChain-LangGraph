# LangSmith 环境变量必须在所有 LangChain import 之前设置
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_PROJECT"] = "LangChain-Learning"


# 这里来学习流式传输
from typing import AsyncIterator
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key="YOUR_PACKYAPI_API_KEY",
    base_url="https://www.packyapi.com/v1",
)

# 返回一个迭代器，产生的消息块
# for chunk in model.stream("写一个小作文"):
#     # 每一个chunk都是AIMessageChunk类型，消息块可以相加
#     print(chunk.content,end="",flush=True)

# 异步传输
import asyncio
# 定义协程
async def boil_water_async():
    print("开始煮水...")
    await asyncio.sleep(5) # 关键！await 表示等待这个操作完成，但期间让事件循环去做别的事
    print("水开了！")

async def send_message_async():
    print("开始发短信...")
    await asyncio.sleep(2) # 同样，等待2秒，但让出控制权
    print("短信发送成功！")

# 主程序（也是一个协程）
async def main():
    # 创建两个任务，并交给事件循环去调度
    task1 = asyncio.create_task(boil_water_async())
    task2 = asyncio.create_task(send_message_async())

    # 等待两个任务都完成
    await task1
    await task2

# 它负责创建事件循环，并将第一个协程（主程序）放入其中运行。
asyncio.run(main())

# 自定义生成器
async def split_into_list(input_text: AsyncIterator[str]) -> AsyncIterator[List[str]]:
    buffer = ""
    async for chunk in input_text:
        buffer += chunk
        while "。" in buffer:
            # 找到。的位置
            stop_index = buffer.index("。")
            yield [buffer[:stop_index].strip()] #yield 产生一个列表，里面只有一个元素
            buffer = buffer[stop_index + 1:]
    # 所有 chunk 处理完后，输出 buffer 里剩余的内容
    yield [buffer.strip()] #yield代表生成器的返回值，返回一个列表，里面只有一个元素

# 使用 chain.astream() 异步流式输出
parser = StrOutputParser()
chain = model | parser | split_into_list
# 需要等待的for才需要加上async，对于while不需要等待的就不需要加
async def stream_joke():
    async for chunk in chain.astream("讲一个50字的笑话"):
        print(chunk, end="|", flush=True)

asyncio.run(stream_joke())

# 消息内置方法演示
from langchain_core.messages import HumanMessage, SystemMessage

msg = HumanMessage(content="你好，今天天气怎么样？")
sys_msg = SystemMessage(content="你是一个有帮助的助手。")

# 1. pretty_print() → 终端里带颜色、格式化打印消息，方便调试
msg.pretty_print()
sys_msg.pretty_print()

# 2. pretty_repr() → 返回格式化的字符串（不直接打印），html=True 可生成 HTML
print(msg.pretty_repr())         # 普通文本格式的漂亮表示
print(msg.pretty_repr(html=True))# HTML 格式的漂亮表示

# 3. text() → 直接取消息的纯文本内容（等同于 .content，但更语义化）
print(msg.text())                # 输出: 你好，今天天气怎么样？

