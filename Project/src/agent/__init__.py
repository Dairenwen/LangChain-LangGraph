"""LangGraph 应用包。

不要在包初始化时导入各个图。LangGraph 会按照 ``langgraph.json`` 中的
路径分别加载图；提前导入会让 ``agent`` 与 ``src.agent`` 的加载顺序互相
嵌套，容易形成循环导入。
"""
