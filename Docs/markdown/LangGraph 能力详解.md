LangGraph 能力详解
版权说明
本“ LangGraph ”课程（以下简称“本课程”）的所有内容，包括但不限于文字、图片、音频、视
频、软件、程序、数据库、设计、布局、界面等，均由本课程的开发者或授权方拥有版权。 我们鼓励
个人学习者使用本课程进行学习和研究。在遵守相关法律法规的前提下，个人学习者可以下载、浏
览、学习本课程的内容，并为了个人学习、研究或教学目的而使用其中的材料。 但请注意， 未经我们
明确授权，个人学习者不得将本课程的内容用于任何商业目的 ，包括但不限于销售、转让、许可或以
其他方式从中获利。此外，个人学习者也不得擅自修改、复制、传播、展示、表演或制作本课程内容
的衍生作品。 任何未经授权的使用均属侵权行为，我们将依法追究法律责任。如果您希望以其他方式
使用本课程的内容，包括但不限于引用、转载、摘录、改编等，请事先与我们取得联系，获取书面授
权。 感谢您对“比特就业课”课程的关注与支持，我们将持续努力，为您提供更好的学习体验。 特此
说明。 比特就业课版权所有方。
代码 & 板书链接
课堂代码：https://gitee.com/zhibite-edu/langchain-
course/tree/master/%E8%AF%BE%E5%A0%82%E4%BB%A3%E7%A0%81/PythonProject
课堂板书：https://gitee.com/zhibite-edu/langchain-
course/tree/master/%E8%AF%BE%E5%A0%82%E6%9D%BF%E4%B9%A6

综合案例用到的表：https://gitee.com/zhibite-edu/langchain-
course/tree/master/%E5%85%B6%E5%AE%83
一、LangGraph 介绍
1. LangGraph 是什么？
1.1 认识智能服务（Agent Server）
学习过 LangChain，我们已经知道 AI 世界是如何初步搭建的。实际我们已经用过：
• ChatGPT 原生模型：对话式 AI，一问一答
• DeepSeek 客戶端：类似的对话助手
• 一些 AI 工具：比如 AI 画画、AI 写文章等
在 LangChain 篇章中，我们接入 LLM 构建的 AI 系统有以下特点：
• 单次对话，“记不住”太多上下文
• 主要是问答模式
• 相对简单的任务
什么是 Agent Server？它是更聪明的 AI 助手
想象一个虚拟的“小助手”，它不仅能回答问题，还能：
• 记住和你聊过的所有事情
• 执行一连串任务（比如：查天气 → 推荐穿搭 → 提醒带伞）
• 中途可以等你给出反馈
• 运行很长时间不会“忘记”
Agent Server 例子：
分镜 1：我说 “帮我规划周末旅行”，Agent  分镜 2：Agent Server 第一步 “查天气”，屏幕
Server 界面显示回应。  显示天气预报界面。

分镜 3：Agent Server 第二步 “找景点”，屏幕 分镜 4：Agent Server 第三步 “订酒店”，屏幕
展示景点列表和图片。 显示酒店预订页面。
分镜 5：Agent Server 第四步 “规划路线”，屏 分镜 6：Agent Server 第五步 “打包建议”，屏
幕呈现地图路线图。 幕列出物品清单。
1.2 构建 Agent Server 时遇到的四大难题
难题  描述  就像...
状态丢失  AI 处理长任务时容易“忘记”前面步骤  写长文章时电脑突然关机
难以调试  不知道 AI 为什么做出某个决定  黑盒子，看不到内部
无法干预  不能中途给 AI 指导  自动驾驶不能接管

部署困难  复杂 Agent Server 难以上线运行  手工制作 vs 工厂生产
思考一下：
如果你要造一个能连续工作 24 小时的 AI 客服，上述哪个问题最头疼？
1.3 解决方案：LangGraph -- Agent Server 的“操作系统”
LangGraph 是一个强大且灵活的“Agent Server 操作系统内核”。它不关心我们具体用什么模型或
提示词，而是为我们解决构建复杂、可靠、可交互的 Agent Server 时所面临的状态管理、流程编排、
持久化和人工监督等底层工程难题。如果我们需要构建超越简单问答的、具备复杂逻辑和长期记忆的
AI 应用，LangGraph 就是为此设计的工具。
如果把 Agent Server 比作一个公司，那么：
• AI 模型 = 员工（干活的人）
• 工具 = 办公设备（电脑、电话）
• LangGraph = 项目经理 + 流程系统
简单来说，LangGraph 是一个专门用于构建和管理 Agent Server 的底层框架。

1.3.1 LangGraph 的三大超能力
1.3.1.1 记忆大师
代码块
1 # 传统AI：每次对话都是新的开始
2 AI回答("你好") → "你好！"
3 AI回答("我叫小明") → "很高兴认识你！"
4 AI回答("我叫什么？") → "我不知道你的名字"
5
6 # LangGraph Agent Server：记住一切
7 Agent Server("你好") → "你好！"
8 Agent Server("我叫小明") → "你好小明！"
9 Agent Server("我叫什么？") → "你叫小明！"
无论过了多久，会话了多少次，LangGraph 都可以记住！
1.3.1.2 流程指挥官
把复杂任务分解成小步骤：

视图
开始 理解需求 执行步骤1 检查结果 执行步骤2 等待反馈 继续执行 结束
1.3.1.3 容错卫士
LangGraph 还提供了以下关键基础设施，保障 Agent Server 的执行过程：
• 持久执行：构建能从故障中恢复、长时间运行的 Agent Server。
• 人工介入：允许在流程中随时检查和修改 Agent Server 状态。
• 强大的调试能力：与 LangSmith 集成，提供可视化追踪和深度洞察。
• 生产就绪的部署：为有状态、长时工作流提供可扩展的部署方案。
1.3.2 LangGraph 在现实中的应用
LangGraph 为生产级代理提供支持，受到 LinkedIn、Uber、Klarna、GitLab 等公司的信赖。
公司  相关产品/服务  主要功能/定位  核心技术/备注
LinkedIn  LinkedIn AI 代理（如  提供个性化工作推荐、人脉拓 目前主要在探索和测试阶段，
LinkedIn Coach）  展、职业发展建议等。  旨在提升平台互动体验。
Uber  Uber AI Solutions（智能 为企业提供构建自主、目标驱 强调其智能体 AI 可协调处理
体解决方案）  动的多智能体 AI 系统的框 复杂任务，是其主要技术方
架、工具和数据服务。  向。
Klarna  1. AI 支付与购物助手  1. 处理支付、退款等客服任 其AI助手明确由 LangGraph
务，已进行数百万次对 构建，是智能体技术在生产环
2. Agentic Product
话。  境中的典型应用案例。
Protocol
2. 一个让 AI 智能体能发现和
比较线上产品的开放数据
协议。

GitLab  1. GitLab Duo  一套覆盖软件开发生命周期 其中 CodeRider 是一款深度
（需求、编码、测试、部署 集成 GitLab 的 AI 编程工具，
2. CodeRider
等）的 AI 助手套件。  基于 LangGraph 开发。
....
除了表格中的概述，各公司的智能体产品在设计和应用上各有侧重：
• Klarna 是瑞典的一家金融公司，他的 AI 助手是将 LangGraph 应用于生产级业务的典范。它已
经处理了超过 250 万次对话，自动化了约 70% 的重复性客服任务，将平均问题解决时间缩短了
80%。该助手是一个多智能体系统，能自主路由请求、处理不同任务（如支付、退款等），并显
著提升了服务效率。
• GitLab 的 AI 产品线非常丰富，其 CodeRider 产品特别值得关注。它基于 LangGraph 构建，不
仅提供代码补全、解释等基础功能，更能胜任复杂任务的全流程智能开发，例如自动分解任务、
跨文件编辑代码、执行终端指令等。而 GitLab Duo 则是一个更广泛的 AI 功能套件，包含代码建
议、漏洞解释、合并请求摘要等数十种功能，旨在扮演虚拟开发团队的角色。
思考一下，我们可以构建什么？
• 个人学习助手（记住你的学习进度）
• 智能客服（处理复杂咨询）
• 数据分析助手（多步骤分析）
• 游戏 NPC（有记忆的虚拟角色）
2. LangGraph 生态系统
LangGraph 是 LangChain 产品家族的一部分。可以与 LangSmith（用于追踪、评估、监控）、
LangGraph 部署平台（用于轻松部署和扩展Agent Server）以及 LangChain（提供大量集成和组件）
结合使用，形成完整的开发、调试、部署工作流。
LangGraph 与 LangChain 顺利集成，但也可以在没有 LangChain 的情况下使用。
3. LangGraph 的核心概念
3.1 常见概念区分
3.1.1 Agent
An agent is AI-powered software that accomplishes a goal. Period." — Dharmesh Shah,
HubSpot CTO and Agents.ai co-founder
Agent是实现目标的人工智能软件— Dharmesh Shah, HubSpot 首席技术官兼 Agents.ai 联合创始人

Agent (智能体)  是一个能够感知环境输入、自主决策、规划行动路径, 并可调用工具或执行操作以达成
目标的自主性软件实体.
其核心在于：由大语言模型 (LLM) 动态控制流程走向
想象你有一个超级聪明的程序员助手, 你只需要说一句："把这个项目的单元测试覆盖率提升到 80%.
"
然后他就自己去看代码、写测试、运行构建、检查结果……直到达标为止⸺中间不需要你插手.
这个"能独立完成任务"的程序, 就是我们说的 Agent (智能体) .
想象一个私人助理机器人：
• 你说："帮我安排下周去上海的差旅. "
• 它不会傻傻地只回复"好的", 而是会：
a. 查天气 → 决定带什么衣服
b. 查航班/高铁时间 → 比较价格
c. 预订酒店 → 发送日程到你的手机
d. 提醒你带身份证
整个过程没有固定的流程图, 它自己"想"出来的步骤 ⸺ 这就是典型的 Agent 行为
3.1.2 工作流
Workflow (工作流)  是一个将复杂过程分解为定义明确、顺序执行的任务流程, 并在其中自动化传递数
据与任务的状态, 用戶完成特定目标. 如果说 Agent 是聪明的执行者，那 工作流就是它的行动蓝图 ⸺
它定义了“先做什么、后做什么、在什么条件下跳转或终止”。
其核心在于：预设的、可重复的流程路径.
比如公司的报销流程
• 提交发票 → 领导审批 → 财务审核 → 财务结算 → 归档完成
或者一个自动化客服工单系统
• 用戶提交问题 → 系统自动分类 → 分配给对应客服 → 客服处理 → 用戶评价 → 工单关闭
这个固定路径, 整个过程沿着预设的流程运行, 就是典型的工作流行为.
LangGraph 是实现的就是工作流！
3.1.3 工作流和 Agent 区别
从概念上来讲, 工作流的流程固定, 步骤预设, 适合明确流程的任务. Agent 是由大模型 (LLM) 动态控制
流程走向, 灵活度高.

类型  英文名  特点  适用场景
工作流  Workflow  流程固定, 代码驱动, 步骤预设  明确流程的任务, 如客服工单处理
智能体  Agent  动态决策, LLM 控制流程走向  开放问题求解, 如科研推理
Workflow 像是"炒菜机器人"⸺按步骤进行炒菜. 比如放油 → 炒蛋 → 加盐 → 出锅, 即使鸡蛋坏了,
也不会停下来.
Agent 像是"米其林主厨"⸺他会思考："今天食材新鲜吗? 客人忌口吗? 要不要换做法? "
◦ 自主决定菜单
◦ 调整火候和配料
◦ 品尝后返工改进
但无论是 Workflow 还是 Agent ，对于他们做出来的 AI 应用，在 LangChain 中，可以统称为 Agent
Server！
3.2 工作流
3.2.1 工作流介绍
工作流具有预先确定的代码路径，并设计为按特定顺序运行。当需要设计更高复杂性的 AI 应用时，工
作流为定义明确的任务提供可预测性和一致性。
例如，现在需要研发一款主打城市通勤的 智能电动自行车 ，具有导航、社交、防盗等功能。在开始研
发前，需要进行多维度分析，如：
• 市场分析：用戶关注续航里程、车身重量、防盗能力，并对“骑行社交”（组队、分享路线）有新
兴兴趣。
• 竞品分析：传统品牌车型智能化不足；互联网品牌车型续航和线下售后服务是其短板。
• 技术分析：评估更轻量化的电池材料与车身设计以提升续航和便携性，并开发基于 GPS 和移动网络
的智能防盗系统与社交功能 App 的集成。
• 最终汇总分析结果。
则我们可以将多维度分析设定为具体的流程（工作流），从而达到先分析再汇总的特定运行顺序。如
下图所示：

视图
市场分析
START 竞品分析 汇总报告 END
技术分析
在 LangGraph 中，工作流基于 LLM ，以及添加到其中的各种增强功能（如工具调用、结构化输出和
短期记忆）而实现：
再次强调：LangGraph 是一个强大且灵活的“Agent Server 操作系统内核”。它不关心我们具体用
什么模型或提示词，而是为我们解决构建复杂、可靠、可交互的 Agent Server 时所面临的状态管理、
流程编排、持久化和人工监督等底层工程难题。
3.2.2 理解图计算
如何实现工作流逻辑？图计算是一种用节点和边来表示复杂系统的方法。在 AI 领域，它特别适合构建
多步骤、有状态的智能工作流。
想象一个快递配送系统，下图展示了包裹从输入（揽收站）到输出（配送站）的过程：

• 配送站、揽收站、分拣中心 = 节点（Node）
• 运输路线 = 边（Edge）
• 包裹信息 = 状态（State）
• 完整配送网 = 图（Graph）
3.3 实现工作流的核心概念
3.3.1 State（状态） - 快递的"包裹信息"
State 就像快递包裹上的标签，记录着包裹的当前位置、目的地、配送状态等信息。在整个配送过程
中，所有站点都能查看和更新这个信息。
状态特性：
• 共享性：所有节点（快递站点）都能读取和修改
• 持久性：在整个工作流（快递运输）执行期间持续存在

• 结构化：有明确的字段定义
代码示例：
代码块
1 from typing import TypedDict
2
3 class PackageState(TypedDict):
4 # 包裹基本信息
5 package_id: str # 包裹id
6 origin: str # 始发站
7 destination: str # 目的地
8
9 # 配送状态
10 status: str # "待揽收", "运输中", "派送中", "已签收"
11 history: list[str] # 流转历史
12 total_distance: int # 总里程
13
14 # 配送详情
15 priority: str # "普通", "加急"
所有配送站点共享的包裹信息卡就是 LangGraph 中的 State！
3.3.2 Nodes（节点） - 快递站点
节点就像快递配送网络中的各个站点，每个站点负责特定的处理步骤。例如：
揽收站：接收包裹，初始化信息 分拣中心：根据目的地分类包裹
派送站：最终配送至收件人

节点特征：
• 单一职责：每个节点只做一件事
• 输入输出：接收状态，返回状态更新
• 独立性：节点间不直接通信，通过 State 交互
代码示例（节点只不过是函数）：
代码块
1 def receive_package(state: PackageState):
2 """揽收站"""
3 return {
4 "status": "已揽收",
5 "history": [f"在{state['origin']}揽收"]
6 }
7
8 def sort_package(state: PackageState):
9 """分拣中心：根据目的地分拣"""
10 destination = state["destination"]
11
12 if "北京" in destination:
13 next_station = "北京分拣中心"
14 elif "上海" in destination:
15 next_station = "上海分拣中心"
16 else:
17 next_station = "其他地区分拣中心"
18
19 return {
20 "status": "已分拣",
21 "history": [f"分拣至{next_station}"]
22 }
23
24 def final_delivery(state: PackageState):
25 """派送站"""

26 return {
27 "status": "已签收",
28 "history": [f"已送达{state['destination']}"]
29 }
3.3.3 Edges（边） - 快递运输路线
边定义了包裹在站点之间的流动路径，就像快递公司的运输路线图。对于路线，一般类型有：
• 开始/结束路线：流程的开始和结束点（包裹的开始站，与结束站）
• 固定路线：包裹可以从揽收站→分拣中心（所有包裹都走这条路），而不能从配送站→揽收站，而
是配送站→家。

• 条件路线：根据目的地选择不同的分拣中心
实际上在 LangGraph 中，边就定义了节点之间的连接关系，决定了工作流的执行顺序。边的类型有：
• 固定边：总是从 A 到 B
• 条件边：根据状态决定下一步

• 以及图的开始和结束点，标志了工作流的入口和出口。
因此，LangGraph 通过节点（每个处理步骤）、边（步骤之间的连接）和状态（保存执行过程），就
可以构建出一个任务工作流（图）。
二、LangGraph 入门教程：构建 AI 工作流
1. 编码前的版本说明
LangGraph 放弃了对 Python 3.9 的支持，所有 LangChain 包现在都需要 Python 3.10 或更高版本。.
使用 查看 Python 版本。如低于3.9，需要重装。
python --version
2. 【案例一】智能快递配送系统
2.1 Graph API 编码思路
构建 Graph 图，首先需要【定义状态】，然后【定义并添加节点和边】，最后【编译】它。编译提供
了对图形结构的一些基本检查（没有孤立节点等）
LangGraph 所谓的“编译” 与 传统意义上的语言编译完全不同，LangGraph 编译本质是在运行时动
态构建和验证一个复杂的图，而非翻译代码。
C++的编译是“完整编译”或“静态编译”的典范。 它追求在程序运行之前，就将所有代码“解
决”完毕，生成一个独立、高效、可直接被操作系统调用的“成品”。它比 Java 的编译更彻底（直接
到机器码，而非中间码），也更底层（紧密绑定操作系统和CPU架构）。
“编译”对比表格：
特性  LangGraph 的编译  Java 的编译  C++ 的编译
配置组装与验证  语言翻译与转换（到中间码）  语言翻译与转换（到本地机器
本质
码）
应用程序运行时（初始化 应用程序开发时（构建阶段）  应用程序开发时（构建阶段）
发生阶段
阶段）
1. 构建可执行的工作流 1. 将高级语言转为低级语言 1. 将高级语言转为特定平台的
对象  （字节码）  本地机器码
2. 进行结构验证  2. 进行语法和深度语义检查  2. 进行彻底的语法、语义检查
主要目的
与优化
3. 链接所有模块，生成完整的
可执行文件

2.2 代码实现
2.2.1 步骤1：定义 State，设置快递的"包裹信息"
定义图时要做的第一件事是定义图的 状态 。 状态 将是图中所有 节点 和 边 的输入，可以是
 或   模型（ 的性能不如 ）。如下所示：
TypedDict Pydantic Pydantic TypedDict
代码块
1 from typing import TypedDict, Annotated
2 from operator import add
3
4 # 1. 定义包裹状态
5 class PackageState(TypedDict):
6 # 包裹基本信息
7 package_id: str # 包裹id
8 origin: str # 始发站
9 destination: str # 目的地
10
11 # 配送状态
12 status: str # "待揽收", "运输中", "派送中", "已签收"
13 history: Annotated[list[str], add] # 流转历史
14 total_distance: Annotated[int, add] # 总里程
15
16 # 配送详情
17 priority: str # "普通", "加急"
2.2.1.1 【知识点】State 更新机制：Reducers
状态 支持更新的关键是 Reducers。在示例中，我们使用   类型为 和
Annotated history
指定了一个 reducer 函数 （ ）。这定义了如何更新包裹信
total_distance operator.add
息，特别是当多个站点都要记录信息时。当状态更新时，新的值会追加到现有值中，而不是替换。如
下所示：
代码块
1 # 覆盖更新：每次新状态替换旧状态
2 status: str
3
4 # 追加更新：新的流转记录添加到历史列表
5 history: Annotated[list[str], add]
6
7 # 数值累加：里程数累加
8 total_distance: Annotated[int, add]

2.2.2 步骤2：定义 StateGraph 图，成立快递公司
StateGraph 是一个有状态图计算框架，它基于有向图（Directed Graph） 模型构建，专门设计用于处
理多步骤、有状态的工作流程。
StateGraph 用来将复杂的工作流程可视化、模块化，让开发者能够像设计快递配送网络一样设计软件
系统。通过这种思维方式，即使是复杂的多步骤 AI 应用也变得清晰可控。
我们需要使用 来定义。  仅是一个构建
langgraph.graph.state.StateGraph StateGraph
器类，可以使用 来构建。如下所示：
State
代码块
1 from langgraph.graph import StateGraph
2
3 # 2. 成立快递公司
4 delivery = StateGraph(PackageState)
注意，这里仅是构建出 ，还无法直接用于执行。
StateGraph
2.2.3 步骤3：定义 Nodes，创建配送站点
接着我们可以定义各个配送站点（节点）。在 LangGraph 中， 节点 就是一个 Python 函数（同步或
异步）。注意
• 节点 接收 状态 作为参数。
• 节点 不需要返回整个 状态 模式，只需一个更新。
如下所示：
代码块
1 # 3. 定义各个配送站点
2 def receive_package(state: PackageState):
3 """揽收站"""
4 return {
5 "status": "已揽收",
6 "history": [f"在{state['origin']}揽收"]
7 }
8
9 def sort_package(state: PackageState):
10 """分拣中心：根据目的地分拣"""
11 destination = state["destination"]
12
13 if "北京" in destination:

14 next_station = "北京分拣中心"
15 elif "上海" in destination:
16 next_station = "上海分拣中心"
17 else:
18 next_station = "其他地区分拣中心"
19
20 return {
21 "status": "已分拣",
22 "history": [f"分拣至{next_station}"]
23 }
24
25 def final_delivery(state: PackageState):
26 """派送站"""
27 return {
28 "status": "已签收",
29 "history": [f"已送达{state['destination']}"]
30 }
2.2.4 步骤4：添加 Nodes，建设配送站点
接下来，我们需要将各节点，组织进图中，即添加节点到 中。可以使用
StateGraph
将新节点添加到 。 方法常用参数说明：
add_node() StateGraph add_node()
参数名  类型  描述
node  字符串 或 StateNode 对象  作用：指定节点要运行的函数或可执行对象
使用方式：
• 如果传入字符串，该字符串将作为节点名称，此时
会使用  action  参数作为实际的执行函数
• 如果传入 StateNode 对象，则直接使用该对象定义
节点
action  StateNode 对象或 None（默认 作用：定义与节点关联的动作（执行逻辑）
值）
使用方式：
• 当  node  参数是字符串时， action  会作为该节
点的实际执行函数
• 当  node  参数已经是 StateNode 对象时，
action  通常为 None
......

代码如下所示：
代码块
1 # 4. 添加配送站点
2 delivery.add_node("揽收站", receive_package)
3 delivery.add_node("分拣中心", sort_package)
4 delivery.add_node("派送站", final_delivery)
2.2.5 步骤5：添加 Edges，规划运输路线
各节点（站点）准备好后，则需要为快递运输规划路线。如：

视图
✨ START
初始化信息
📦 揽收站
⚙ 主分拣中心
默认中转
🔄 分支分拣中心A  🔄 分支分拣中心B  🔄 分支分拣中心C
目的地：东部 目的地：西部 目的地：南部
🚚 派送站
最终配送
✅ END 派送结束
实际上，这就是为 图 定义 边 。边有几种关键类型：
• 普通边/固定边（Normal Edges）：直接从一个节点转到下一个节点。
• 条件边（Conditional Edges）：调用函数来确定下一步要转到哪个节点。
例如，设置最简单运输路线：快递由揽收站接收，下一站固定为分拣中心，最后到派送中进行派送。
这就是固定边，如下图所示：

视图
✨ START
初始化信息
📦 揽收站
⚙ 分拣中心
🚚 派送站
最终配送
✅ END 派送结束
再例如，我们可以根据以下条件，判断快递如何运输：
• 包裹是加急件 → 走空运线路
• 包裹不是加急件 → 走标准线路
这就是条件边，如下图所示：

视图
✨ START
初始化信息
📦 揽收站
⚙ 分拣中心
🔄 加急配送 🔄 标准配送
🚚 派送站
最终配送
✅ END 派送结束
要说明的是，在 LangGraph 中：
• 节点：是一个特殊节点，表示将用戶输入发送到图形的节点。引用此节点的主要目的是确
START
定应该首先调用哪些节点。
• 节点：是一个表示终端节点的特殊节点。当想要指示哪些边在完成后没有后续动作时，将引
END
用此节点。
• 条件入口点（Conditional Entry Point）：调用一个函数来确定在用戶输入到达时首先调用哪个节
点。
代码实现

1）使用 向图中添加从开始节点（或起始节点列表）到结束节点的固定边。
add_edge()
方法常用参数说明：
add_edge()
参数名  类型  描述
start_key  字符串 或 字符串列表  边的起始节点的键。
end_key  字符串  边的结束节点的键。
2）使用 向图中添加 从起始节点到任意数量的目标节点 的条件边。
add_conditional_edges()
方法常用参数说明：
add_conditional_edges()
参数名  类型  描述
source  字符串  起始节点。退出此节点时，将运行此条件边。
path  Callable 或 Runnable  决定下一个节点或多个节点的方法。
如果没有指定  path_map  应返回一个或多个节点。
如果返回  “END” ，图将停止执行。
path_map  字典 或 字符串列表 或 None  【可选】将路径映射到节点名。
如省略，path 返回的路径应为节点名。
接下来实现下图对应的代码：

视图
✨ START
初始化信息
📦 揽收站
⚙ 分拣中心
🔄 加急配送 🔄 标准配送
🚚 派送站
最终配送
✅ END 派送结束
对应代码如下：
代码块
1 # 新增节点
2 def standard_delivery(state: PackageState):
3 """标准配送"""
4 return {
5 "status": "运输中",
6 "history": ["标准陆运"],
7 "total_distance": 500
8 }
9
10 def express_delivery(state: PackageState):

11 """加急配送"""
12 return {
13 "status": "加急运输",
14 "history": ["空运加急"],
15 "total_distance": 800
16 }
17
18
19 # 4. 添加配送站点
20 delivery.add_node("揽收站", receive_package)
21 delivery.add_node("分拣中心", sort_package)
22 delivery.add_node("标准配送", standard_delivery)
23 delivery.add_node("加急配送", express_delivery)
24 delivery.add_node("派送站", final_delivery)
25
26 # 5. 设计配送路线
27 delivery.add_edge(START, "揽收站")
28 delivery.add_edge("揽收站", "分拣中心")
29
30 # 智能路由：根据优先级选择配送方式
31 def select_delivery(state: PackageState):
32 """智能路由决策 - 根据包裹特性选择路线"""
33
34 if state["priority"] == "加急":
35 return "加急配送"
36 else:
37 return "标准配送"
38
39 delivery.add_conditional_edges(
40 "分拣中心", # source：起始节点。退出此节点时，将运行此条件边。
41 select_delivery, # path：确定下一个或多个节点的可调用对象。
42 ["加急配送", "标准配送"] # path_map
43 )
44 delivery.add_edge("标准配送", "派送站")
45 delivery.add_edge("加急配送", "派送站")
46 delivery.add_edge("派送站", END)
也可以将决策返回映射到路由，如下所示：
代码块
1 # 智能路由：根据优先级选择配送方式
2 def select_delivery(state: PackageState):
3 """智能路由决策 - 根据包裹特性选择路线"""
4
5 if state["priority"] == "加急":

6 return "备注加急"
7 else:
8 return "无备注"
9
10 delivery.add_conditional_edges(
11 "分拣中心", # source：起始节点。退出此节点时，将运行此条件边。
12 select_delivery, # path：确定下一个或多个节点的可调用对象。
13 {
14 "备注加急": "加急配送",
15 "无备注": "标准配送"
16 }
17 )
2.2.6 步骤6：StateGraph 图编译，从公司创建到运行
在步骤2中，我们仅是构建出 ，还无法直接用于执行。LangGraph 要求：必须先编译
StateGraph
图，然后才能使用它。编译提供了对图结构的一些基本检查，这会验证：
• 从 START 到所有节点的可达性
• 从所有节点到 END 的可达性
• 没有孤立节点或死循环
使用 方法即可编译图。该方法将   编译为   对
compile() StateGraph CompiledStateGraph
象。编译后的图实现了   接口，可以异步调用、流式传输、批处理和运行。
Runnable
代码如下：
代码块
1 # 7. 编译系统
2 delivery_system = delivery.compile()
到这里，核心代码已编写完成。接下来进行测试，代码如下：
代码块
1 # 8. 测试配送
2 test_packages = [
3 {
4 "package_id": "P001",
5 "origin": "北京",
6 "destination": "上海",
7 "priority": "普通",
8 "history": [],

9 "total_distance": 0
10 },
11 {
12 "package_id": "P002",
13 "origin": "广州",
14 "destination": "乌鲁木齐",
15 "priority": "加急",
16 "history": [],
17 "total_distance": 0
18 }
19 ]
20
21 for package in test_packages:
22 print(f"\n配送包裹: {package['package_id']}")
23 result = delivery_system.invoke(package)
24 print("最终状态:", result["status"])
25 print("配送历史:", result["history"])
26 print("总里程:", result["total_distance"])
注意，默认情况下，图将具有相同的输入和输出结构。对于 方法，支持单个输入，它的输
invoke()
入可以是字典或任何其他类型，默认返回最新的 State。打印结果如下：
代码块
1 配送包裹: P001
2 最终状态: 已签收
3 配送历史: ['在北京揽收', '分拣至上海分拣中心', '标准陆运', '已送达上海']
4 总里程: 500
5
6 配送包裹: P002
7 最终状态: 已签收
8 配送历史: ['在广州揽收', '分拣至其他地区分拣中心', '空运加急', '已送达乌鲁木齐']
9 总里程: 800
到此，我们已经构建出了一个图式的智能快递配送系统，来理解 LangGraph 图的基本能力与用法！核
心概念回顾：
1. State = 包裹信息卡（记录所有状态）
2. Nodes = 配送站点（执行具体操作）
3. Edges = 运输路线（控制流转顺序）
4. Reducers = 信息更新规则（如何记录变更）
5. 编译 = 从路线图到运营系统的转换

3. 【案例二】支持搜索的智能代理系统
3.1 案例介绍
案例一只是为了演示什么是 Graph。对于 LangGraph，实际上是要调用 LLM 来完成智能应用系统。因
此该案例会将使用 Graph API，来完成一个支持搜索、支持调用 LLM 的智能代理系统。核心功能如
下：
• 智能对话与工具调用：基于聊天模型，能够理解用戶问题并决定是否需要调用搜索工具
• 自动搜索整合：通过 Tavily 搜索工具获取实时信息，并将搜索结果整合到回答中
• 循环决策机制：能够多次调用工具和模型，直到获得满意答案
流程设置如下：
视图
不需要 返回最终答案
用戶提问 LLM判断是否需要搜索 需要 执行搜索
整合结果
例如我们可以用它来：
• 实时信息查询：查询最新新闻、股价、天气等
今天特斯拉的最新股价是多少？还有哪些重要的科技新闻？
• 事实核查：验证信息的准确性
有人说阿波罗登月是伪造的，请提供证据来验证登月的真实性
• 深度研究：多轮搜索获取全面信息
我需要关于'人工智能在医疗诊断中的应用'的最新研究论文、临床试验结果和专家观点，请提供
全面的综述
• 知识扩展：补充模型知识库之外的信息
GPT-4o-mini 的训练数据截止到什么时候？之后有哪些重要的AI发展事件？
3.2  编码思路

构建 Graph 图，首先需要定义状态，然后定义并添加节点和边，最后编译它。编译提供了对图形结构
的一些基本检查（没有孤立节点等）
3.2.1 设置 Nodes
根据节点的单一职责特性，即每个节点只做一件事，我们可以设置：
• 节点1（ ）：专门负责搜索，获取搜索结果。
tool_node
• 节点2（ ）：专门负责调用 LLM，获取最终结果。
llm_call
根据节点的独立性特性，即每个节点间不直接通信，而是通过 State 交互。它们接收 State，返回
State 的更新。
3.2.2 设置 State
根据状态的共享性特性，即所有节点都能读取和修改状态。LangGraph 在许多情况下，将以前的对话
历史记录存储为 State 中的消息列表会很有帮助，这样就能通过 State 中的消息列表来跟踪整个对话的
完整历史，这是构建对话系统的关键。
为此，我们可以在图状态中添加一个 键，如下所示：
messages
代码块
1 from langchain.messages import AnyMessage
2 from typing_extensions import TypedDict, Annotated
3 import operator
4
5 class MessagesState(TypedDict):
6 # 类型: list[AnyMessage] - 任意消息对象的列表
7 # 合并策略: operator.add - 使用加法操作符进行状态合并
8 # 效果: 当状态更新时，新的消息会追加到现有列表中，而不是替换
9 messages: Annotated[list[AnyMessage], operator.add]
10 # 类型: int - 整数值
11 # 用途: 跟踪LLM（大语言模型）的调用次数
12 llm_calls: int
注意  这个注解特别重要：
Annotated[list[AnyMessage], operator.add]
•  表示新消息会追加到列表中，而不是替换；
operator.add
• 这确保了对话历史的连续性。
 的具体作用：
messages
1. 对话记忆

代1 码块#  存储完整的对话流程
2 messages = [
3 HumanMessage(content="你好"),
4 AIMessage(content="你好！我是AI助手"),
5 HumanMessage(content="什么是机器学习？"),
6 AIMessage(content="机器学习是...")
7 ]
2. 上下文维护
当专门负责调用 LLM 的节点（ 节点）需要调用 LLM 时，可以通过 State 将整个
llm_call
 历史作为上下文：
messages
代码块
1 # LLM 基于完整的对话历史生成回复
2 response = llm.invoke(state["messages"])
3. 状态持久化
State 中的   字段确保在图的各个节点之间传递时，对话状态不会丢失：
messages
代码块
1 def node(state: MessagesState):
2 # 可以访问完整的对话历史
3 all_messages = state["messages"]
4 latest_message = state["messages"][-1]
5 # 处理并添加新消息
6 return {"messages": [new_ai_message]}
因此，没有这个字段，系统就无法记住之前的对话内容，每次都会像第一次对话一样。
3.2.3 设置 Edges
对于流程设置如下所示：

视图
不需要 返回最终答案
用戶提问 LLM判断是否需要搜索 需要 执行搜索
整合结果
且已经定义了两个节点：
• 节点1（ ）：专门负责搜索，获取搜索结果。
tool_node
• 节点2（ ）：专门负责调用 LLM，获取最终结果。
llm_call
因此，可以定义以下逻辑：
• 对于开始逻辑：是当用戶进行输入后，直接让 LLM 进行处理。是否需要搜索工具调用，也是通过
LLM 进行判断。因此图的入口点则是 节点。
llm_call
• 对于结束逻辑：可以根据 LLM 返回的结构判断是否调用工具，来决定我们是应该继续循环还是停止
循环：
◦ 如果 LLM 要调用工具，则进入tool_node节点进行处理；
◦ 如果 LLM 不要调用工具，则结束。
最终 Graph 效果如下图所示：
视图
__start__
llm_call
__end__ tool_node

3.3 代码实现
3.3.1 步骤1：准备工作，定义聊天模型和搜索工具
代码块
1 # 步骤 1: 定义工具和模型
2 from langchain.chat_models import init_chat_model
3 from langchain_tavily import TavilySearch
4
5 search = TavilySearch(max_results=4)
6 tools = [search]
7 # 绑定工具
8 model = init_chat_model("gpt-4o-mini", temperature=0)
9 model_with_tools = model.bind_tools(tools)
3.3.2 步骤2：定义状态
代码块
1 # 步骤 2: 定义状态
2
3 from langchain.messages import AnyMessage
4 from typing_extensions import TypedDict, Annotated
5 import operator
6
7 class MessagesState(TypedDict):
8 # 类型: list[AnyMessage] - 任意消息对象的列表
9 # 合并策略: operator.add - 使用加法操作符进行状态合并
10 # 效果: 当状态更新时，新的消息会追加到现有列表中，而不是替换
11 messages: Annotated[list[AnyMessage], operator.add]
12 # 类型: int - 整数值
13 # 用途: 跟踪LLM（大语言模型）的调用次数
14 llm_calls: int
3.3.3 步骤3：定义模型节点
由于 节点 不需要返回整个 状态 模式，只需一个更新。且 表示新消息会追加到列表
operator.add
中，而不是替换。因此模型节点代码如下：
代码块

1 # 步骤 3: 定义模型节点
2 from langchain.messages import SystemMessage
3
4 def llm_call(state: dict):
5 """LLM决定是否调用工具"""
6
7 return {
8 "messages": [
9 model_with_tools.invoke(
10 [
11 SystemMessage(
12 content="你是一个乐于助人的助手，支持调用工具进行搜索。"
13 )
14 ]
15 + state["messages"]
16 )
17 ],
18 "llm_calls": state.get('llm_calls', 0) + 1
19 }
3.3.4 步骤4：定义工具节点
3.3.4.1 要点1：回顾 AIMessage 消息结构
在学习 LangChain 篇章时，我们便知道当 LLM 需要调用工具时，LLM 输出结果  的结构
AIMessage
如下所示：
代码块
1 AIMessage(
2 content='',
3 additional_kwargs={'refusal': None},
4 response_metadata={
5 ...
6 },
7 id='lc_run--30b6a3d7-1bd0-4093-8a36-9b43bea458fc-0',
8 tool_calls=[
9 {
10 'name': 'tavily_search',
11 'args': {
12 'query': '西安天气',
13 'search_depth': 'basic'
14 },
15 'id': 'call_XAa0MF8j9YQp6KFk28tqIvpB',
16 'type': 'tool_call'

17 }
18 ],
19 usage_metadata={
20 ...
21 }
22 )
其中包含一个 属性。此属性包括执行工具所需的一切，包括工具名称和输入参数。有
tool_calls
了这些内容，便可以进行工具调用。
3.3.4.2 要点2：构造
ToolMessage
仅仅成功调用工具还不行，我们需要将工具的返回构造成 ，再传输给聊天模型。才能
ToolMessage
给我们返回真正需要的答案：
1. 将工具输出传递给聊天模型，包括 、 (工具调用)、
HumanMessage AIMessage
ToolMessage
2. 聊天模型根据以上消息列表的输入，将最终结果 返回。
AIMessage
可以使用下面这种方式定义 ：
ToolMessage
代码块
1 ToolMessage(content=${工具的返回}, tool_call_id=tool_calls[n]["id"])
3.3.4.3 要点3：在 State 中访问 messages
由于 LangChain 允许传输下面这种格式的消息：
代码块
1 {
2 "messages": [
3 {
4 "type": "human",
5 "content": "message"
6 }
7 ]
8 }
但 State 中对于 message 的更新，总是会反序列化为 LangChain Message 格式！如将上述格式反序
列化为下面这种格式：

代1 码块{
2 "messages": [
3 HumanMessage(content="message")
4 ]
5 }
因此，应该使用 点表示法 来访问消息属性，例如要访问 AIMessage 中的 属性时，应
tool_calls
使用   来获取。
state["messages"][-1].tool_calls
因此，定义工具节点完整代码如下：
代码块
1 # 步骤 4: 定义工具节点
2 from langchain.messages import ToolMessage
3
4 tools_by_name = {tool.name: tool for tool in tools}
5 def tool_node(state: dict):
6 """执行工具调用"""
7
8 result = []
9 for tool_call in state["messages"][-1].tool_calls:
10 tool = tools_by_name[tool_call["name"]]
11 observation = tool.invoke(tool_call["args"])
12 result.append(ToolMessage(content=observation,
tool_call_id=tool_call["id"]))
13 return {"messages": result}
3.3.5 步骤5：构建图，设置节点与边
对于开始逻辑：是当用戶进行输入后，直接让 LLM 进行处理。是否需要搜索工具调用，也是通过 LLM
进行判断。因此图的入口点则是 节点。
llm_call
对于结束逻辑：可以根据 LLM 返回的结构判断是否调用工具，来决定我们是应该继续循环还是停止循
环：
• 如果 LLM 要调用工具，则进入tool_node节点进行处理；
• 如果 LLM 不要调用工具，则结束。
代码块
1 # 步骤 5: 构件图
2
3 from langgraph.graph import StateGraph, START, END

4
5 # 定义结束逻辑
6 def should_continue(state: MessagesState):
7 """根据LLM是否调用工具来决定是应该继续循环（路由到工具节点）还是停止循环（END）"""
8
9 messages = state["messages"]
10 last_message = messages[-1]
11
12 # 如果LLM调用工具，则执行操作
13 if last_message.tool_calls:
14 return "tool_node"
15 return END
16
17 agent_builder = StateGraph(MessagesState)
18 agent_builder.add_node("llm_call", llm_call)
19 agent_builder.add_node("tool_node", tool_node)
20
21 agent_builder.add_edge(START, "llm_call")
22 agent_builder.add_conditional_edges(
23 "llm_call", # source：起始节点。退出此节点时，将运行此条件边。
24 should_continue, # path：确定下一个或多个节点的可调用对象。
25 ["tool_node", END] # path_map：可选，将路径映射到节点名称
26 )
27 agent_builder.add_edge("tool_node", "llm_call")
28
29 # 编译图
30 agent = agent_builder.compile()
3.3.6 步骤6：可视化图
我们可以通过 Mermaid 图表，来展示出 Graph 效果。
Mermaid 是一种使用文本生成流程图、饼状图、甘特图等图表的描述语言，它可以帮助用戶以简
单、直观的方式创建各种类型的图表，包括流程图、时序图、甘特图等。
Mermaid 在线绘图工具：https://www.jyshare.com/front-end/9729/
使用姿势：
1. LangGraph 中，编译后的图提供了获取 Graph 可绘制表示的方法： ，其参数
get_graph()
 或  ，表示显示详细视图。
xray=True xray=1
2. 再通过 ，将图形转换为 Mermaid 格式并生成 PNG 图片的二进制数据。
draw_mermaid_png()
3. 最后需要导入 库用于图像显示。
matplotlib

代码如下：
代码块
1 import matplotlib.pyplot as plt
2 import matplotlib.image as mpimg
3 try:
4 # 生成 Mermaid 图表并保存为图片
5 mermaid_code = agent.get_graph(xray=True).draw_mermaid_png()
6 # 保存文件
7 with open("../jpg/graph1.jpg", "wb") as f:
8 f.write(mermaid_code)
9
10 #使用 matplotlib 显示图像
11 img = mpimg.imread("../jpg/graph1.jpg")
12 plt.imshow(img) # 显示图片
13 plt.axis('off') # 关闭坐标轴
14 plt.show() # 弹出窗口显示图片
15 except Exception as e:
16 print(f"An error occurred: {e}")
效果如下：
3.3.7 步骤7：执行（非流式与流式）

• 使用 方法进行非流式执行：
invoke()
代码块
1 from langchain.messages import HumanMessage
2 messages = agent.invoke({
3 "messages": [
4 HumanMessage(content="今天西安的天气如何？")
5 ]
6 })
7 print(f"调用 LLM 总次数：{messages["llm_calls"]}次")
8 for m in messages["messages"]:
9 m.pretty_print()
运行结果：
代码块
1 调用 LLM 总次数：2次
2 ================================ Human Message
=================================
3
4 今天西安的天气如何？
5 ================================== Ai Message
==================================
6 Tool Calls:
7 tavily_search (call_6LQafbVZn9qCzWix4Ob3auPI)
8 Call ID: call_6LQafbVZn9qCzWix4Ob3auPI
9 Args:
10 query: 西安天气
11 time_range: day
12 ================================= Tool Message
=================================
13
14 {'query': '西安天气', 'follow_up_questions': None, 'answer': None, 'images':
[], 'results': [{'url': 'https://feeds-
drcn.cloud.huawei.com.cn/landingpage/latest?
docid=10512921993454170538700817&to_app=hwbrowser&dy_scenario=relate&tn=8f7efc3
6ddc74442b888d848e6ae3f3b32b722a839fa5de71583e48ad5dc75fb&channel=HW_JINGXUAN_Z
H&ctype=news&cpid=666&r=CN&emuiVer=27', 'title': '陕西省西安市今日天气(11月26
日)', 'content': '今晨6时，西安晴，气温0℃，东北风3-4级，相对湿度88%。 预计，今天白天多
云，最高气温13.7℃，微风，今天夜间晴，最低气温-1.1℃，微风。', 'score': 0.826278,
'raw_content': None}, {'url': 'https://weather.cma.cn/web/weather/V8870.html',
'title': '西安 - 中国气象局-天气预报-城市预报', 'content': '13℃ 2℃ 12℃ 12℃ 12℃
2℃ 1℃ | 气温 | 13℃ | 5.3℃ | 4℃ | 2.6℃ | 3.5℃ | 10.5℃ | 10.5℃ | 12.2℃ |
| 气温 | 10.5℃ | 10.5℃ | 12.2℃ | 10.4℃ | 7.6℃ | 5.5℃ | 4.4℃ | 3.3℃ | | 气
温 | 2℃ | 10.2℃ | 11℃ | 11.8℃ | 5.4℃ | 5.2℃ | 4.9℃ | 4.3℃ | | 气温 |

8.3℃ | 16.6℃ | 16.8℃ | 12.8℃ | 8.6℃ | 7.4℃ | 4℃ | 4.3℃ | | 气温 | 4.5℃ |
11℃ | 12℃ | 11.2℃ | 5.9℃ | 5℃ | 3.4℃ | 3.1℃ | | 气温 | 2.2℃ | 7.6℃ |
10.6℃ | 9.6℃ | 8.5℃ | 5.3℃ | 2.1℃ | 1.6℃ |', 'score': 0.82492816,
'raw_content': None}, {'url':
'https://shaanxi.weather.com.cn/xian/index.shtml', 'title': '西安天气预报 - 陕
西', 'content': '城市预报列表(11-26 07:30发布). 西安: 17℃/2℃. 长安: 14℃/0℃. 临
潼: 15℃/', 'score': 0.7265231, 'raw_content': None}, {'url':
'https://weather.yahoo.co.jp/weather/world/CN/57036/', 'title': '西安(シーアン)
（中国）の天気 - Yahoo!天気・災害', 'content': '西安(シーアン)（中国）の今日・明日・週
間天気予報が確認できます。天気、最低気温、最高気温はもちろん、現地時刻、日の出、日の入り時
刻までわかります。', 'score': 0.7060491, 'raw_content': None}], 'response_time':
0.86, 'request_id': '4d571ab8-52b8-4628-94d9-e37c5ae9727f'}
15 ================================== Ai Message
==================================
16
17 今天西安的天气情况如下：
18
19 - **今晨6时**：晴，气温0℃，东北风3-4级，相对湿度88%。
20 - **白天气温**：预计最高气温13.7℃，天气多云，微风。
21 - **夜间气温**：预计最低气温-1.1℃，天气晴，微风。
22
23 如果需要更详细的信息，可以查看以下链接：
24 - [陕西省西安市今日天气](https://feeds-
drcn.cloud.huawei.com.cn/landingpage/latest?
docid=10512921993454170538700817&to_app=hwbrowser&dy_scenario=relate&tn=8f7efc3
6ddc74442b888d848e6ae3f3b32b722a839fa5de71583e48ad5dc75fb&channel=HW_JINGXUAN_Z
H&ctype=news&cpid=666&r=CN&emuiVer=27)
25 - [中国气象局 - 西安天气预报](https://weather.cma.cn/web/weather/V8870.html)
26 - [西安天气预报 - 陕西](https://shaanxi.weather.com.cn/xian/index.shtml)
• 使用 进行流式输出：
stream()
代码块
1 from langchain.messages import HumanMessage
2 for chunk in agent.stream({
3 "messages": [HumanMessage(content="今天西安的天气如何？")]
4 }):
5 print(chunk)
注意，这里的流式，指的是 Graph 执行步骤的流式输出，即途径节点的过程。每个节点对 Graph
State 的更新值（注：并非是更新后的值），都可以通过这种方式追踪。由此， 类型为
chunk
：key 代表节点名称；value 代表将更新的 State 值。
dict

4. 【案例三】基于 LangGraph 实现的代理式 RAG（检索增强生成）系统
4.1 案例介绍
还记得我们在 LangChain 篇章中，编写过 LCEL 链式的 RAG 系统。整个系统就是一条直线：
视图
输入问题 检索文档 组合提示词 生成答案 输出结果
它适合初学者，因为：
• 概念少：只需要理解 Runnable, StrOutputParser 等基础概念
• 逻辑简单：线性流程，易于理解和调试
• 代码直观：一眼就能看懂数据流动
• 快速上手：几分钟就能跑通整个流程
而在 LangGraph 篇章中，我们将会构建一个智能的文档问答系统（复杂版），它能够根据检索结果的
质量动态调整查询策略。逻辑如下图所示：
视图
否 直接回答
合格 生成答案
用戶问题 AI决策是否需要检索? 是 检索文档 质量检查
不合格
重写问题
举个例子：这里我们提供了“比特就业课”相关的几篇课程宣传文档，作为知识库。

可以支持我们询问：
• "比特提供了哪些课程"
• "Java开发方向的课程安排"
• "测试开发方向的主线课程有哪些"
• "C++开发方向的项目列表"
• "Redis课程内容是什么"
• ......
当用戶询问 比特提供了哪些课程 时，根据要求，会经历：
" "
1. 模型决定调用检索工具，搜索"比特课程"
2. 检索到相关文档后进行评估
3. 如果文档相关，直接生成答案
4. 如果文档不相关，重写问题后重新检索

视图
开始：“比特提供了哪些课
程”
AI思考：我知道答案吗？
不知道，需要查资料
搜索：“比特课程”
知道答案
资料相关吗
不相关
相关
基于资料生成答案 重写问题 直接回答
结束

这个设计确保了即使初次检索不成功，系统也能通过重写查询来改进结果质量，比传统 RAG 系统更加
鲁棒。
鲁棒性：是指系统在面对各种内外部干扰时，仍能保持其性能稳定的能力。具体来说：
• 它描述了系统在不确定性、噪声、误差或其他不利因素下的表现。
• 鲁棒性与稳定性不同，稳定性关注系统在扰动消失后的恢复，而鲁棒性关注在持续扰动下的表
现。
• 在模型中，鲁棒性指的是模型在陌生环境或噪声干扰下依旧能够完成预期任务的能力。
• 在控制系统中，鲁棒性是指系统在一定参数摄动下维持性能的特性，是现代控制系统设计的重要
指标。
因此，相较于 LangChain 篇章中链式的 RAG： 怎么让 跑起来 ，该案例将学习 怎么让 跑
" RAG " " RAG
得更好、更智能 ！
"
4.2 编码思路
构建一个智能文档问答系统，我们要将复杂流程分解为离散步骤，且通过共享状态连接各个节点，核
心设计思路如下：
• 模块化设计：每个节点只做一件事，职责清晰
• 质量闭环：检索 → 检查 → 优化 → 再检索，确保答案质量
• 智能路由：AI 自主决定下一步行动，无需人工干预
因此，我们需要：
• 第一步：准备"知识库"（数据加载与处理）
• 第二步：创建"检索工具"
• 第三步：设计"工作流程节点"
◦ 节点1：决策节点
generate_query_or_respond
◦ 节点2：检索器工具节点
retrieve
◦ 节点3：问题优化节点
rewrite_question
◦ 节点4：答案生成节点
generate_answer
•  第四步：组装"工作流水线"
◦ 条件边1：LLM 决策是否需要进行知识库检索
◦ 条件边2：检测【检索到的文档】是否与【问题】相关
最终 Graph 示意图：

视图
__start__
generate_query_or_respond
tools
retrieve
generate_answer rewrite_question
__end__
4.3 代码实现
4.3.1 步骤一：准备"知识库"并创建"检索工具"
代码块
1 from langchain.chat_models import init_chat_model
2 from langchain_openai import OpenAIEmbeddings
3 from langchain_core.messages import HumanMessage
4 from langchain_community.document_loaders import UnstructuredMarkdownLoader
5 from langchain_text_splitters import RecursiveCharacterTextSplitter
6 from langchain_core.vectorstores import InMemoryVectorStore
7 from langchain_classic.tools.retriever import create_retriever_tool
8
9 # 聊天模型与嵌入模型
10 model = init_chat_model("gpt-4o-mini")
11 embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
12
13 # 加载文档列表
14 paths = [

15 "../bit/企业介绍.md",
16 "../bit/C++开发方向.md",
17 "../bit/Java开发方向.md",
18 "../bit/测试开发方向.md"
19 ]
20 docs = [UnstructuredMarkdownLoader(path).load() for path in paths]
21 docs_list = [item for sublist in docs for item in sublist]
22 # from_tiktoken_encoder：使用 tiktoken 编码器来计算长度的文本分割器。
23 text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
24 encoding_name="cl100k_base",
25 chunk_size=1000,
26 chunk_overlap=50
27 )
28 doc_splits = text_splitter.split_documents(docs_list)
29
30 # 使用内存中向量存储和 OpenAI 嵌入
31 vectorstore = InMemoryVectorStore.from_documents(
32 documents=doc_splits,
33 embedding=embeddings
34 )
35
36 # 使用 LangChain 的预构建 create_retriever_tool 创建检索器工具：
37 retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
38 retriever_tool = create_retriever_tool(
39 retriever,
40 "retrieve_bit",
41 "搜索并返回有关比特就业课的信息。",
42 )
其中， 用于创建一个基于文档检索的工具，参数说明：
create_retriever_tool()
•  - 检索器实例，负责实际的文档检索
retriever: BaseRetriever
•  - 工具名称，传递给语言模型，需要唯一且具有描述性
name: str
•  - 工具描述，帮助语言模型理解何时使用该工具
description: str
该方法返回 对象，其继承了 。 是所有 LangChain 工具的基础类。执
Tool BaseTool BaseTool
行工具时可使用 方法，而执行参数则是检索器执行参数。
invoke()
代码块
1 return Tool(
2 name=name,
3 description=description,
4 func=func,
5 coroutine=afunc,
6 args_schema=RetrieverInput,

7 response_format=response_format,
8 )
测试：
代码块
1 # 测试
2 test_queries = [
3 "比特提供了哪些课程",
4 "Java开发方向的课程安排",
5 "测试开发方向的主线课程有哪些",
6 "C++开发方向的项目列表",
7 "Redis课程内容是什么"
8 ]
9 for query in test_queries:
10 print("-" * 50)
11 print(f"查询: {query}\n")
12 result = retriever_tool.invoke({"query": query})
13 # 只显示前100个字符，避免输出过长
14 content_preview = result[:100] + "..." if len(result) > 100 else result
15 print(f"结果预览: {content_preview}")
16 print(f"结果长度: {len(result)} 字符")
4.3.2 步骤二：设计"工作流程节点"
根据 Graph 示意图，设计出以下四个节点：
• 节点1：决策节点
generate_query_or_respond
• 节点2：检索器工具节点
retrieve
• 节点3：问题优化节点
rewrite_question
• 节点4：答案生成节点
generate_answer

视图
__start__
generate_query_or_respond
tools
retrieve
generate_answer rewrite_question
__end__
4.3.2.1 节点1：决策节点
generate_query_or_respond
该节点核心设计：
• 决定是直接回答还是检索文档
• 可以使用   让模型能够调用检索工具
model.bind_tools([retriever_tool])
代码如下：
代码块
1 from langgraph.graph import MessagesState
2 def generate_query_or_respond(state: MessagesState):
3 """调用模型以基于当前状态生成响应。
4 给定问题，它将决定使用检索工具检索，或者简单地响应用戶。"""
5 response = (
6 model.bind_tools([retriever_tool]).invoke(state["messages"])
7 )
8 return {"messages": [response]}
其中 是 LangGraph 中给我们写好只包含 的 State，可以直接使用。其
MessagesState messages
源码如下：

代码块
1 class MessagesState(TypedDict):
2 messages: Annotated[list[AnyMessage], add_messages]
测试 方法返回值：
generate_query_or_respond
代码块
1 # 测试generate_query_or_respond方法返回值
2 input_messages = {
3 "messages": [
4 {
5 "role": "user",
6 "content": "比特提供了哪些课程?",
7 }
8 ]
9 }
10 generate_query_or_respond(input_messages)["messages"][-1].pretty_print()
11
12 # 打印：
13 # ================================== Ai Message
==================================
14 # Tool Calls:
15 # retrieve_bit (call_hNvMsOUD3MFKEXwX1Tzqahw1)
16 # Call ID: call_hNvMsOUD3MFKEXwX1Tzqahw1
17 # Args:
18 # query: 比特课程
从结果看来，根据我们的输入： 比特提供了哪些课程 ，LLM 决定继续检索文档，且设置好了初次的
?
查询字符串！
4.3.2.2 节点2：检索器工具节点
retrieve
前面已经创建好了检索器工具。对于节点，可以使用 类来定义：
ToolNode
代码块
1 from langgraph.prebuilt import ToolNode
2 retrieve_node = ToolNode([retriever_tool])
 用于创建 LangGraph 工作流程中执行工具的节点。
ToolNode

4.3.2.3 节点3：问题优化节点
rewrite_question
该节点主要负责当文档不相关时，重写问题以改进检索效果。代码如下：
代码块
1 REWRITE_PROMPT = (
2 "查看输入并尝试推断潜在的语义意图/含义。\n"
3 "这是最初的问题："
4 "\n ------- \n"
5 "{question}"
6 "\n ------- \n"
7 "提出一个改进后的问题："
8 )
9 def rewrite_question(state: MessagesState):
10 """重写原始用戶问题"""
11
12 messages = state["messages"]
13 question = messages[0].content
14 prompt = REWRITE_PROMPT.format(question=question)
15 response = model.invoke([HumanMessage(content=prompt)])
16
17 return {"messages": [{"role": "user", "content": response.content}]}
模拟【检索内容与原本问题不相关】的情况，测试一下：
代码块
1 from langchain_core.messages import convert_to_messages
2 input_messages = {
3 "messages": convert_to_messages(
4 [
5 {
6 "role": "user",
7 "content": "比特提供了哪些课程?",
8 },
9 {
10 "role": "assistant",
11 "content": "",
12 "tool_calls": [
13 {
14 "id": "1",
15 "name": "retrieve_bit",
16 "args": {"query": "比特课程"},
17 }
18 ],
19 },

20 {"role": "tool", "content": "你好", "tool_call_id": "1"},
21 ]
22 )
23 }
24 response = rewrite_question(input_messages)
25 print(response["messages"][-1]["content"])
26 # 打印结果如下：
27 # 改进后的问题可以是：“我想了解比特所提供的课程有哪些，包括课程内容、目标和学习时长。”
4.3.2.4 节点4：答案生成节点
generate_answer
该节点将基于相关文档生成最终答案，代码如下：
代码块
1 # 生成答案
2 GENERATE_PROMPT = (
3 "你是负责回答问题的助手。 "
4 "使用以下检索到的上下文片段来回答问题。 "
5 "如果你不知道答案，就说你不知道。 "
6 "最多只用三句话，回答要简明扼要。\n"
7 "Question: {question} \n"
8 "Context: {context}"
9 )
10
11 def generate_answer(state: MessagesState):
12 """生成答案"""
13
14 # 最原始问题
15 question = state["messages"][0].content
16 # 最新问题的检索结果（保证参考答案准确）
17 context = state["messages"][-1].content
18 prompt = GENERATE_PROMPT.format(question=question, context=context)
19 response = model.invoke([HumanMessage(content=prompt)])
20 return {"messages": [response]}
4.3.3 步骤三：组装"工作流水线"
根据下图，开始组装"工作流水线"。

视图
__start__
generate_query_or_respond
tools
retrieve
generate_answer rewrite_question
__end__
4.3.3.1 添加节点与入口点
代码块
1 # 组装Graph
2 from langgraph.graph import StateGraph, START, END
3 from langgraph.prebuilt import ToolNode, tools_condition
4
5 workflow = StateGraph(MessagesState)
6 workflow.add_node(generate_query_or_respond)
7 workflow.add_node("retrieve", ToolNode([retriever_tool]))
8 workflow.add_node(rewrite_question)
9 workflow.add_node(generate_answer)
10
11 workflow.add_edge(START, "generate_query_or_respond")
4.3.3.2 条件边1：LLM 决策是否需要进行知识库检索

第一条分支用来判断是否需要调用工具，如下图所示：
“是否需要调用工具”的判断，可以使用   方法来决定工作流的路由（等价于
tools_condition()
手动写的 方法），规则如下：
should_continue
• 如果最后一条 AI 消息包含工具调用，则路由到工具执行节点；
• 否则，请结束工作流。
该方法返回类型为 ，表示：
Literal["tools", "__end__"]
• 当最后一条 AI 消息包含工具调用，则返回
"tools"
• 否则返回
"__end__"
因此，代码如下所示：
代码块
1 workflow.add_conditional_edges(
2 "generate_query_or_respond",
3 # 评估 LLM 决策
4 tools_condition,
5 {
6 "tools": "retrieve", # 将条件输出转换为图中的节点
7 "__end__": END,
8 },
9 )

4.3.3.3 条件边2：检测【检索到的文档】是否与【问题】相关
该条件边核心在于：
• 评估检索到的文档与问题的相关性
• 可以使用【结构化输出】模型返回二元评分
◦ ：表示检索到的文档与问题相关
yes
◦ ：表示检索到的文档与问题不相关
no
• 返回下一步路由决策：  或
"generate_answer" "rewrite_question"
代码如下：
代码块
1 # 对文档进行评估
2 from pydantic import BaseModel, Field
3 from typing import Literal
4
5 GRADE_PROMPT = (
6 "你是一个评分员，评估检索到的文档与用戶问题的相关性。 \n "
7 "以下是检索到的文档： \n\n {context} \n\n"
8 "以下是用戶的问题： {question} \n"
9 "如果文档包含与用戶问题相关的关键字或语义，则将其评为相关。 \n"
10 "给出一个二元分数“yes”或“no”，以表明该文档是否与问题相关。"
11 )
12

13 class GradeDocuments(BaseModel):
14 """使用二值评分进行相关性检查"""
15 score: str = Field(
16 description="相关性评分：如果相关则为“yes”，如果不相关则为“no”"
17 )
18
19 def grade_documents(state: MessagesState) -> Literal["generate_answer",
"rewrite_question"]:
20 """确定检索到的文档是否与问题相关"""
21 question = state["messages"][0].content
22 context = state["messages"][-1].content
23
24 prompt = GRADE_PROMPT.format(question=question, context=context)
25 response = (
26 model.with_structured_output(GradeDocuments).invoke(
27 [{"role": "user", "content": prompt}]
28 )
29 )
30 score = response.score
31
32 if score == "yes":
33 return "generate_answer"
34 else:
35 return "rewrite_question"
36
37 workflow.add_conditional_edges(
38 "retrieve",
39 # 评估代理决策
40 grade_documents,
41 ["generate_answer", "rewrite_question"],
42 )
4.3.3.4 添加结束点并编译
代码块
1 workflow.add_edge("generate_answer", END)
2 workflow.add_edge("rewrite_question", "generate_query_or_respond")
3
4 graph = workflow.compile()
4.3.3.5 运行 RAG
代码块
1 # 运行 RAG

2 for chunk in graph.stream(
3 {
4 "messages": [HumanMessage(content="C++开发方向的项目列表")]
5 }
6 ):
7 for node, update in chunk.items():
8 print(f"由节点 {node} 更新消息:")
9 if node != "rewrite_question":
10 update["messages"][-1].pretty_print()
11 print("\n\n")
结果如下：
代码块
1 由节点 generate_query_or_respond 更新消息:
2 ================================== Ai Message
==================================
3 Tool Calls:
4 retrieve_bit (call_kKhk5pvL33lGneckV1YvMKKt)
5 Call ID: call_kKhk5pvL33lGneckV1YvMKKt
6 Args:
7 query: C++开发方向的项目列表
8
9
10 由节点 retrieve 更新消息:
11 ================================= Tool Message
=================================
12 Name: retrieve_bit
13
14 ....(检索结果较长，省略显示)
15
16
17 由节点 generate_answer 更新消息:
18 ================================== Ai Message
==================================
19
20 C++开发方向的项目包括多个层次的挑战项目、标准项目和极简项目。挑战项目如微服务的即时通讯系
统和视频点播系统，涵盖复杂功能和技术组件；标准项目包括仿QQ音乐的音乐播放客戶端等，适合快速
掌握；极简项目则如贪吃蛇游戏，适合基础薄弱的同学。总共有15个不同规格的项目可供选择。
5. LangGraph 的其他特性

5.1 使用 Overwrite 绕过 reducer
在 LangGraph 中，reducers 用于控制状态更新的处理方式。默认情况下，每个状态键都有其独立的
reducer 函数，用于决定如何合并节点返回的更新。但有时我们需要完全覆盖状态值而不是合并，这时
就需要使用  。
Overwrite
为什么需要 Overwrite？想象一下开发一个聊天应用时：
• 正常情况下，新消息会追加到消息列表中。
• 但有时需要清空聊天记录并重新开始，这时候就需要绕过追加逻辑，直接覆盖整个消息列表。
代码示例：
代码块
1 from langgraph.graph import StateGraph, START, END
2 from langgraph.types import Overwrite
3 from typing_extensions import Annotated, TypedDict
4 import operator
5
6 class State(TypedDict):
7 messages: Annotated[list, operator.add]
8
9 def add_message(state: State):
10 return {"messages": ["first message"]}
11
12 def replace_messages(state: State):
13 # 绕过reducer并替换整个消息列表
14 return {"messages": Overwrite(["replacement message"])}
15
16 builder = StateGraph(State)
17 builder.add_node("add_message", add_message)
18 builder.add_node("replace_messages", replace_messages)
19 builder.add_edge(START, "add_message")
20 builder.add_edge("add_message", "replace_messages")
21 builder.add_edge("replace_messages", END)
22 graph = builder.compile()
23
24 result = graph.invoke({"messages": ["initial"]})
25 print(result["messages"])
输出:  ，而不是
['replacement message'] ['initial message', 'first
。
message', 'replacement message']
使用 Overwrite 的应用场景如下：
• 重置对话：清空聊天历史，开始新对话

• 状态重置：在错误恢复后重置应用状态
• 数据清理：替换损坏或过时的数据
5.2 定义输入输出模式
默认情况下，LangGraph 使用单一的状态模式。但我们可以定义独立的输入和输出模式，解释如下：
• 独立的输入模式：验证输入数据的结构
• 独立的输出模式：过滤输出数据，只返回需要的信息
• 内部模式：节点间通信使用的完整状态
为什么需要独立的内部模式？考虑一个问答系统：
• 输入：用戶的问题（字符串）
• 输出：AI 的答案（字符串）
• 内部：可能需要存储中间结果、上下文等信息
我们不想把内部状态都暴露给用戶！
在 LangGraph 中，如果想要定义独立的输入和输出模式，可以使用 StateGraph 的初始化参数：
参数名  类型  描述
input_schema  type[InputT] 或 None  定义 StateGraph 输入的 State 类
output_schema  type[OutputT] 或 None  定义 StateGraph 输出的 State 类
state_schema  type[StateT]   定义 StateGraph 的 State 类
代码示例如下：
代码块
1 from langgraph.graph import StateGraph, START, END
2 from typing_extensions import TypedDict
3
4 # 1. 定义输入模式 - 只包含用戶问题
5 class InputState(TypedDict):
6 question: str
7
8 # 2. 定义输出模式 - 只包含AI答案
9 class OutputState(TypedDict):

10 answer: str
11
12 # 3. 定义完整状态模式（内部使用）
13 class OverallState(InputState, OutputState):
14 pass
15
16 def answer_node(state: InputState):
17 """处理输入并生成答案"""
18 # 这里可以访问 question，生成 answer
19 return {
20 "answer": f"Answer to: {state['question']}",
21 "question": state["question"]
22 }
23
24 # 构建图时指定输入输出模式
25 builder = StateGraph(
26 OverallState,
27 input_schema=InputState, # 输入验证
28 output_schema=OutputState # 输出过滤
29 )
30
31 builder.add_node("answer_node", answer_node)
32 builder.add_edge(START, "answer_node")
33 builder.add_edge("answer_node", END)
34 graph = builder.compile()
35
36 # 测试
37 result = graph.invoke({"question": "What is LangGraph?"})
38 print(result) # 输出: {'answer': 'Answer to: What is LangGraph?'}
39 # 注意：question 字段被过滤掉了，不在输出中
独立的输入和输出实际应用场景如下：
• API 开发：定义清晰的请求/响应格式
• 微服务：服务间明确的数据契约
• 数据管道：明确的输入输出规范
5.3 在节点间传递私有状态
有时节点间需要传递临时数据，这些数据对中间逻辑很重要，但不应该出现在最终输出中，只在特定
节点间共享，这就是私有状态的概念。
举个例子，现在我们需要根据数据库中的信息，生成相关数据报告，因此可以设置三个节点：
• 节点 ：从数据库获取原始数据（包含敏感信息）
1

• 节点 ：处理数据，过滤掉敏感信息
2
• 节点 ：生成最终报告
3
此时， 节点 和 节点 需要共享原始数据，但 节点 不应该看到敏感信息。代码如下：
1 2 3
代码块
1 from langgraph.graph import StateGraph, START, END
2 from typing_extensions import TypedDict
3
4 # 公共状态（最终输出中可见）
5 class OverallState(TypedDict):
6 final_result: str
7
8 # 节点1的私有输出
9 class Node1Output(TypedDict):
10 sensitive_data: str # 这个字段不会出现在最终状态中
11
12 # 节点2需要的输入（包含私有数据）
13 class Node2Input(TypedDict):
14 sensitive_data: str
15
16 def node_1(state: OverallState) -> Node1Output:
17 """第一步：获取包含敏感信息的原始数据"""
18 private_data = "这是敏感信息"
19 print(f"Node1: 获取到敏感数据，但不会暴露给最终输出")
20 return {"sensitive_data": private_data}
21
22 def node_2(state: Node2Input) -> OverallState:
23 """第二步：处理数据，移除敏感信息"""
24 print(f"Node2: 处理敏感数据: {state['sensitive_data']}")
25 # 处理数据，返回清理后的结果
26 return {"final_result": "清理后的处理结果"}
27
28 def node_3(state: OverallState) -> OverallState:
29 """第三步：只看到清理后的数据"""
30 print(f"Node3: 只能看到最终结果: {state['final_result']}")
31 return {"final_result": state["final_result"] + " - 完成"}
32
33 # 构建图
34 builder = StateGraph(OverallState)
35 # add_sequence：支持添加一系列节点，按所给的顺序执行。
36 # 注意：我们使用 add_sequence 但类型系统会处理私有状态
37 builder.add_sequence([node_1, node_2, node_3])
38 builder.add_edge(START, "node_1")
39 graph = builder.compile()
40

41 # 测试
42 response = graph.invoke({"final_result": "initial"})
43 print(f"\n最终输出: {response}")
运行上述代码，会看到：
代码块
1 Node1: 获取到敏感数据，但不会暴露给最终输出
2 Node2: 处理敏感数据: 这是敏感信息
3 Node3: 只能看到最终结果: 清理后的处理结果
4
5 最终输出: {'final_result': '清理后的处理结果 - 完成'}
节点间传递私有状态实际应用场景如下：
• 数据处理：中间处理步骤的临时数据
• 认证流程：令牌等敏感信息的传递
• 复杂计算：中间计算结果
• 错误处理：错误详情在内部传递，但对外提供友好消息
以上三个特性让 LangGraph 能够处理复杂的企业级应用场景，同时保持代码的清晰和安全性。
三、工作流的常见模式
工作流模式是预先定义好的执行路径，就像工厂的流水线一样，每个步骤都有明确的输入输出和顺
序。根据不同的需求场景，从而定制出工作流常见的用法选项。
1. 提示链模式（Prompt Chaining）
1.1 概念
提示链就像流水线一样，前一个步骤的输出作为下一个步骤的输入。这就跟进行内容创作时，需要 大
纲 → 初稿 → 润色 → 最终稿 ，且每个步骤的输出需要传输给下一个步骤，才能确保内容质量逐
步提升。

视图
START 输入主题 大纲生成 大纲 初稿生成 初稿 润色文章 润色版 最终稿生成 终稿 END
1.2 模式实践
我们可以创建一个内容创作场景的工作流，包含 大纲 → 初稿 → 润色 → 最终稿 。节点即可设计
为：
• 节点: 只负责大纲生成
generate_outline
• 节点: 只负责初稿写作
generate_draft
• 节点: 只负责内容润色
polish_content
• 节点: 只负责最终整合
finalize_content
且可以使用定义输入输出的方式，如下所示：
代码块
1 # 1. 定义输入模式 - 只包含用戶输入
2 class InputState(TypedDict):
3 topic: str # 用戶输入的主题
4
5
6 # 2. 定义输出模式 - 只包含最终结果
7 class OutputState(TypedDict):
8 final_content: str # 最终的内容
9
10
11 # 3. 定义完整状态模式（内部使用）
12 class OverallState(InputState, OutputState):
13 outline: str # 第一步：生成的大纲
14 draft: str # 第二步：生成的初稿
15 polished_draft: str # 第三步：润色后的稿件
完整代码示例如下：

代1 码块fr om langchain.chat_models import init_chat_model
2 from langchain_core.messages import HumanMessage
3 from typing_extensions import TypedDict
4 from langgraph.graph import StateGraph, START, END
5
6 model = init_chat_model("gpt-4o-mini")
7
8 # 1. 定义输入模式 - 只包含用戶输入
9 class InputState(TypedDict):
10 topic: str # 用戶输入的主题
11
12
13 # 2. 定义输出模式 - 只包含最终结果
14 class OutputState(TypedDict):
15 final_content: str # 最终的内容
16
17
18 # 3. 定义完整状态模式（内部使用）
19 class OverallState(InputState, OutputState):
20 outline: str # 第一步：生成的大纲
21 draft: str # 第二步：生成的初稿
22 polished_draft: str # 第三步：润色后的稿件
23
24
25 # 第一步：生成大纲
26 PROMPT_1 = (
27 "根据主题生成文章大纲。\n"
28 "主题：{topic}\n"
29 "要求："
30 "1.只需两个最核心标题"
31 "2.不用进行说明，只返回最终大纲"
32 )
33 def generate_outline(state: InputState):
34 """根据主题生成内容大纲"""
35 print("*" * 50)
36 print(f"内容大纲生成中...\n")
37 prompt = PROMPT_1.format(topic=state['topic'])
38 outline = model.invoke([HumanMessage(content=prompt)]).content
39 print(f"大纲已生成：\n{outline}\n")
40 return {
41 "outline": outline,
42 "topic": state["topic"]
43 }
44
45
46 # 第二步：基于大纲生成初稿
47 PROMPT_2 = (

48 "根据以下内容生成文章完整初稿。\n"
49 "主题：{topic}\n"
50 "大纲: "
51 "{outline}\n"
52 "要求："
53 "1.每个标题下，最多使用三句话的内容即可"
54 "2.不用进行说明，只返回最终结果"
55 )
56 def generate_draft(state: OverallState):
57 """根据大纲生成完整初稿"""
58 print("*" * 50)
59 print(f"生成初稿中...\n")
60 prompt = PROMPT_2.format(topic=state['topic'],outline=state['outline'])
61 draft = model.invoke([HumanMessage(content=prompt)]).content
62 print(f"初稿已生成：\n{draft}\n")
63 return {"draft": draft}
64
65
66 # 第三步：润色稿件
67 PROMPT_3 = (
68 "根据文章初稿进行润色。\n"
69 "主题：{topic}\n"
70 "初稿: "
71 "{draft}\n"
72 "要求："
73 "1.润色后，文章不能太长"
74 )
75 def polish_content(state: OverallState):
76 """对初稿进行润色优化"""
77 print("*" * 50)
78 print(f"文章润色中...\n")
79 prompt = PROMPT_3.format(topic=state['topic'],draft=state['draft'])
80 polished = model.invoke([HumanMessage(content=prompt)]).content
81 print(f"润色完成，内容如下：\n{polished}\n")
82 return {"polished_draft": polished}
83
84
85 # 第四步：生成最终稿
86 PROMPT_4 = (
87 "根据润色版文章，生成文章终稿。\n"
88 "主题：{topic}\n"
89 "大纲: "
90 "{outline}\n"
91 "润色版文章: "
92 "{polished_draft}\n"
93 )
94 def finalize_content(state: OverallState):

95 """生成最终版本的内容"""
96 prompt =
PROMPT_4.format(topic=state['topic'],outline=state['outline'],polished_draft=st
ate['polished_draft'])
97 final_content = model.invoke([HumanMessage(content=prompt)]).content
98 return {"final_content": final_content}
99
100
101 # 构建工作流
102 builder = StateGraph(
103 OverallState,
104 input_schema=InputState,
105 output_schema=OutputState
106 )
107
108 # 添加节点
109 builder.add_node(generate_outline) # 节点1：生成大纲
110 builder.add_node(generate_draft) # 节点2：生成初稿
111 builder.add_node(polish_content) # 节点3：润色稿件
112 builder.add_node(finalize_content) # 节点4：生成最终稿
113
114 # 连接节点（直线流程）
115 builder.add_edge(START, "generate_outline") # 开始 → 生成大纲
116 builder.add_edge("generate_outline", "generate_draft") # 大纲 → 生成初稿
117 builder.add_edge("generate_draft", "polish_content") # 初稿 → 润色
118 builder.add_edge("polish_content", "finalize_content") # 润色 → 最终稿
119 builder.add_edge("finalize_content", END) # 最终稿 → 结束
120
121 # 编译工作流
122 chain = builder.compile()
123
124 # 使用工作流
125 result = chain.invoke({"topic": "人工智能的未来发展"})
126 print("=" * 50)
127 print("最终创作结果:")
128 print("=" * 50)
129 print(result["final_content"])
130 print("=" * 50)
运行后，每个节点都有详细的日志输出（调试）：
代码块
1 **************************************************
2 内容大纲生成中...
3

4 大纲已生成：
5 # 人工智能的未来发展
6
7 ## 1. 技术趋势与创新方向
8 ### 1.1 自然语言处理的进步
9 ### 1.2 机器学习与深度学习的演变
10 ### 1.3 强人工智能的可能性
11
12 ## 2. 应用领域与社会影响
13 ### 2.1 医疗行业的变革
14 ### 2.2 自动化与就业市场的关系
15 ### 2.3伦理与监管的挑战
16
17 **************************************************
18 生成初稿中...
19
20 初稿已生成：
21 （内容较多，已省略）
22
23 **************************************************
24 文章润色中...
25
26 润色完成，内容如下：
27 （内容较多，已省略）
28
29 ==================================================
30 最终创作结果:
31
32 （内容较多，已省略）
33 ==================================================
2. 并行化模式（Parallelization）
2.1 概念
并行化是指多个任务同时进行，提高效率，最终汇总结果。在多角度处理同一问题时，常用该模式。
例如，现在需要研发一款主打城市通勤的 智能电动自行车 ，具有导航、社交、防盗等功能。在开始研
发前，需要进行多维度分析，如：
• 市场分析：用戶关注续航里程、车身重量、防盗能力，并对“骑行社交”（组队、分享路线）有新
兴兴趣。
• 竞品分析：传统品牌车型智能化不足；互联网品牌车型续航和线下售后服务是其短板。

• 技术分析：评估更轻量化的电池材料与车身设计以提升续航和便携性，并开发基于GPS和移动网络
的智能防盗系统与社交功能App的集成。
最终汇总分析结果。而并行分析不仅省时，还能提升决策质量。
视图
市场分析
STRAT 竞品分析 汇总报告 END
技术分析
2.2 模式实践
实现一个工作流，可以并行执行三个维度的分析，最后整合成全面的产品研发建议，为智能电动自行
车项目提供决策支持。完整代码示例：
代码块
1 from typing import TypedDict
2
3 from langgraph.constants import START, END
4 from langgraph.graph import StateGraph
5
6
7 class AnalysisState(TypedDict):
8 concept: str # 概念
9 market: str # 市场分析
10 competitor: str # 竞品分析
11 tech: str # 技术分析
12 report: str # 汇总报告
13
14
15 # 三个并行分析任务
16 def market_task(state: AnalysisState):
17 """市场分析"""

18 return {"market": "用戶关注续航、重量、防盗，对骑行社交有兴趣..."}
19
20
21 def competitor_task(state: AnalysisState):
22 """竞品分析"""
23 return {"competitor": "传统品牌智能化不足，互联网品牌续航和售后差..."}
24
25
26 def tech_task(state: AnalysisState):
27 """技术分析"""
28 return {"tech": "轻量化电池车身、GPS防盗、社交App集成..."}
29
30
31 # 汇总结果
32 def combine_results(state: AnalysisState):
33 """生成最终报告"""
34 report = f"产品分析报告\n\n"
35 report += f"市场分析：\n{state['market']}\n\n"
36 report += f"竞品分析：\n{state['competitor']}\n\n"
37 report += f"技术分析：\n{state['tech']}\n\n"
38 report += "建议：聚焦续航、防盗、社交功能的平衡发展"
39 return {"report": report}
40
41
42 # 构建工作流
43 builder = StateGraph(AnalysisState)
44 builder.add_node("market", market_task)
45 builder.add_node("competitor", competitor_task)
46 builder.add_node("tech", tech_task)
47 builder.add_node("combine", combine_results)
48 # 并行执行三个分析
49 builder.add_edge(START, "market")
50 builder.add_edge(START, "competitor")
51 builder.add_edge(START, "tech")
52 # 汇总结果
53 builder.add_edge("market", "combine")
54 builder.add_edge("competitor", "combine")
55 builder.add_edge("tech", "combine")
56 builder.add_edge("combine", END)
57 workflow = builder.compile()
58
59 # 使用
60 result = workflow.invoke({"concept": "城市通勤智能电动自行车"})
61 print(result["report"])

3. 路由模式（Routing）
3.1 概念
路由模式也被称为"智能分流"，根据输入内容决定执行哪个分支。最典型案例就是智能客服系统，可
以用戶问题自动分类处理，如下所示：
视图
售前咨询 售前处理 END
STRAT 分析问题类型 售后问题 售后处理 END
技术问题 技术处理 END
3.2 模式实践
实现一个智能客服系统，根据用戶问题自动分类，达到精准匹配处理能力。核心设计在于条件路由机
制：
• 动态路径选择：可以基于 LLM 分析结果动态决定执行路径（结构化返回）
• 分支隔离：不同类型的问题由专用处理器处理
关键代码如下：
代码块
1 # 定义路由决策的数据结构
2 class Route(BaseModel):
3 step: Literal["pre_sale", "after_sale", "technical"] = Field(
4 description="根据用戶问题类型决定路由到售前、售后还是技术处理"
5 )
6
7 # 路由决策节点
8 def model_call_router(state: State):
9 """分析用戶输入，决定问题类型"""
10 model = init_chat_model("gpt-4o-mini")

11 decision = model.with_structured_output(Route).invoke(state["input"])
12 return {"decision": decision.step}
节点即可设计为：
• 节点: 路由决策节点，根据用戶问题，由 LLM 通过结构化返回进行智能决
model_call_router
策。
• 节点: 处理售前咨询
pre_sale_handler
• 节点: 处理售后问题
after_sale_handler
• 节点: 处理技术问题
technical_handler
完整代码如下所示：
代码块
1 from langchain.chat_models import init_chat_model
2 from langgraph.constants import START, END
3 from langgraph.graph import StateGraph
4 from typing_extensions import Literal, TypedDict
5 from pydantic import BaseModel, Field
6
7
8 class State(TypedDict):
9 input: str # 用戶输入
10 decision: str # 路由决策
11 output: str # 最终输出
12
13
14 # 定义路由决策的数据结构
15 class Route(BaseModel):
16 step: Literal["pre_sale", "after_sale", "technical"] = Field(
17 description="根据用戶问题类型决定路由到售前、售后还是技术处理"
18 )
19
20 # 路由决策节点
21 def model_call_router(state: State):
22 """分析用戶输入，决定问题类型"""
23 model = init_chat_model("gpt-4o-mini")
24 decision = model.with_structured_output(Route).invoke(state["input"])
25 return {"decision": decision.step}
26
27
28 # 三个不同的处理节点
29 def pre_sale_handler(state: State):
30 """处理售前咨询"""

31 return {"output": "售前咨询已处理，处理内容....."}
32
33 def after_sale_handler(state: State):
34 """处理售后问题"""
35 return {"output": "售后问题已处理，处理内容....."}
36
37 def technical_handler(state: State):
38 """处理技术问题"""
39 return {"output": "技术问题已处理，处理内容....."}
40
41
42 # 路由函数 - 根据决策返回下一个节点
43 def route_decision(state: State):
44 if state["decision"] == "pre_sale":
45 return "pre_sale_handler" # 去售前处理节点
46 elif state["decision"] == "after_sale":
47 return "after_sale_handler" # 去售后处理节点
48 elif state["decision"] == "technical":
49 return "technical_handler" # 去技术处理节点
50
51 # 构建路由工作流
52 router_builder = StateGraph(State)
53
54 # 添加处理节点
55 router_builder.add_node(pre_sale_handler)
56 router_builder.add_node(after_sale_handler)
57 router_builder.add_node(technical_handler)
58 router_builder.add_node(model_call_router)
59
60 # 先经过路由决策
61 router_builder.add_edge(START, "model_call_router")
62
63 # 条件边：根据路由结果选择分支
64 router_builder.add_conditional_edges(
65 "model_call_router",
66 route_decision,
67 ["pre_sale_handler", "after_sale_handler", "technical_handler"]
68 )
69 # 所有分支最终都结束
70 router_builder.add_edge("pre_sale_handler", END)
71 router_builder.add_edge("after_sale_handler", END)
72 router_builder.add_edge("technical_handler", END)
73 router_workflow = router_builder.compile()
74
75 # 测试
76 test_cases = [
77 "我想了解一下你们产品的价格和功能", # 售前咨询

78 "我购买的产品有质量问题，需要退货", # 售后问题
79 "这个软件安装后无法正常运行，报错代码0x80070005", # 技术问题
80 "请问你们的售后服务政策是什么", # 售前咨询
81 "我的订单已经发货但还没收到", # 售后问题
82 "如何配置数据库连接参数" # 技术问题
83 ]
84 for test_case in test_cases:
85 print("*" * 50)
86 result = router_workflow.invoke({"input": test_case})
87 print(f"用戶问题：{test_case}\n{result['output']}")
运行结果：
代码块
1 **************************************************
2 用戶问题：我想了解一下你们产品的价格和功能
3 售前咨询已处理，处理内容.....
4 **************************************************
5 用戶问题：我购买的产品有质量问题，需要退货
6 售前咨询已处理，处理内容.....
7 **************************************************
8 用戶问题：这个软件安装后无法正常运行，报错代码0x80070005
9 技术问题已处理，处理内容.....
10 **************************************************
11 用戶问题：请问你们的售后服务政策是什么
12 售后问题已处理，处理内容.....
13 **************************************************
14 用戶问题：我的订单已经发货但还没收到
15 售前咨询已处理，处理内容.....
16 **************************************************
17 用戶问题：如何配置数据库连接参数
18 技术问题已处理，处理内容.....
4. 协调者-工作者模式（Orchestrator-Workers）
4.1 概念
协调者-工作者模式可以理解为一个大脑（协调者）分配任务，多个工人（工作者）执行，最后合成最
终结果。例如，当我们要处理几百页的技术文档，可以让协调者拆分文档，接着安排多个工作者并行
处理不同章节，最终汇总结果。如下图所示：

视图
工作者
（章节1处理）
协调者  工作者  合成器
开始 结束
（拆分并分配任务） （章节2处理） （最终汇总）
工作者
（章节3处理）
协调者 工作者 模式和 并行化 模式都涉及同时执行多个任务，但它们的核心区别在于任务分配方
-
式：
• 并行化 ：任务在设计时就确定，所有任务同时开始。
• 协调者 工作者 ：任务在运行时由协调者动态分配。
-
举个例子：
【案例：文档翻译】
• 并行化 ：已知要翻译3个固定章节，同时翻译
• 协调者 工作者 ：先分析文档结构，发现需要翻译5个章节，动态分配
-
【案例：数据分析】
• 并行化 ：同时计算平均值、最大值、最小值（固定指标）
• 协调者 工作者 ：先分析数据特征，决定需要计算哪些统计指标
-
4.2 模式实践
接下来，我们实现：
• 协调者：负责根据{topic}生成报告大纲。并根据生成的大纲，将生成内容的子任务指派给工作者。
• 工作者：生成大纲对应的内容。
◦ 注意：协调者生成3个标题，就需要3个工作者生成对应内容；生成10个标题，就需要10个工作
者生成对应内容。
• 合成器：汇总所有工作者的成果。
因此，关键在于任务指派，协调者在运行时需动态分配工作者，即边的数量在运行时才能确定。

为了支持这种设计模式，LangGraph 支持从条件边返回 对象。 有两个参数：第一个是节
Send Send
点的名称，第二个是要传递给该节点的状态。
代码块
1 # 任务分配函数 - 关键部分！
2 def assign_workers(state: State):
3 """为每个任务创建工作者"""
4 # 为每个部分创建一个工作者任务
5 return [Send("llm_call", {"section": section}) for section in
state["sections"]]
6
7 graph.add_conditional_edges("node", assign_workers)
这样，任务分配函数会根据任务的数量，运行时动态生成n条数量的、指向 节点的边
llm_call
因此，对于我们要实现的案例，其完整代码如下：
代码块
1 from langchain.chat_models import init_chat_model
2 from langgraph.constants import START, END
3 from langgraph.graph import StateGraph
4 from langgraph.types import Send
5 from typing import Annotated, TypedDict, List
6 import operator
7
8 from pydantic import BaseModel
9
10
11 class State(TypedDict):
12 topic: str
13 sections: list # 协调者生成的计划
14 completed_sections: Annotated[list, operator.add] # 工作者完成的结果
15 final_report: str
16
17
18 # 定义数据结构-结构化输出
19 class Section(BaseModel):
20 name: str
21 description: str
22
23 class Sections(BaseModel):
24 sections: List[Section]
25
26 # 创建规划器
27 model = init_chat_model("gpt-4o-mini")

28 planner = model.with_structured_output(Sections)
29
30 # 协调者节点 - 制定计划
31 def orchestrator(state: State):
32 """协调者：分析任务并制定执行计划"""
33 report_sections = planner.invoke(
34 f"为主题'{state['topic']}'制定报告大纲，包含3个章节"
35 )
36 return {"sections": report_sections.sections}
37
38 # 工作者节点 - 执行具体任务
39 def llm_call(state: State):
40 """工作者：根据分配的任务生成内容"""
41 section = state["section"] # 从协调者接收的任务
42 result = model.invoke(
43 f"编写报告章节：{section.name}，内容要求：{section.description}"
44 )
45 return {"completed_sections": [result.content]} # 结果会自动合并
46
47 # 汇总节点
48 def synthesizer(state: State):
49 """汇总所有工作者的成果"""
50 completed_sections = state["completed_sections"]
51 final_report = "\n\n---\n\n".join(completed_sections)
52 return {"final_report": final_report}
53
54 # 任务分配函数 - 关键部分！
55 def assign_workers(state: State):
56 """为每个任务创建工作者"""
57 # 为每个章节创建一个工作者任务
58 worker_tasks = []
59 for section in state["sections"]:
60 worker_tasks.append(
61 Send("llm_call", {"section": section}) # 发送任务给工作者
62 )
63 return worker_tasks
64
65 # 构建工作流
66 builder = StateGraph(State)
67
68 builder.add_node("orchestrator", orchestrator)
69 builder.add_node("llm_call", llm_call)
70 builder.add_node("synthesizer", synthesizer)
71
72 builder.add_edge(START, "orchestrator")
73
74 # 关键：协调者后创建多个工作者

75 builder.add_conditional_edges(
76 "orchestrator",
77 assign_workers,
78 ["llm_call"] # 创建的工作者都指向llm_call节点
79 )
80
81 # 所有工作者完成后汇总
82 builder.add_edge("llm_call", "synthesizer")
83 builder.add_edge("synthesizer", END)
84
85 worker = builder.compile()
86
87 response =worker.invoke({"topic": "中国近代史"})
88 print(response)
运行结果：
代码块
1 {
2 'topic': '中国近代史',
3 'sections': [
4 Section(
5 name='第一章：近代史概述',
6 description='介绍中国近代史的背景与重要性，涵盖社会、经济、文化等多个方面的
变化。'
7 ),
8 Section(
9 name='第二章：鸦片战争与列强侵华',
10 description='探讨鸦片战争对中国的影响，以及随后的列强侵华与民族觉醒进程。'
11 ),
12 Section(
13 name='第三章：辛亥革命与新文化运动',
14 description='分析辛亥革命及其后果，以及新文化运动对中国现代化的推动作用。'
15 )
16 ],
17 'completed_sections': [
18 '# 第一章：...',
19 '# 第二章：...',
20 '# 第三章：...'
21 ],
22 'final_report': '# 第一章：...# 第二章：...# 第三章：...'
23 }

5. 评估器-优化器模式（Evaluator-optimizer）
5.1 概念
评估器-优化器模式的流程是：
• 先进行生成内容
• 再进行评估质量
• 如果需要改进就重新生成，不断改进直到满足质量标准
经典的场景就是 内容质量优化 、 代码生成和改进 等。评估器-优化器流程图如下所示：
视图
开始 生成内容 评估质量 通过 结束
不通过：带着反馈重新生成
5.2 模式实践
对于 评估器 优化器 模式，快速上手篇章的【案例3-智能的文档问答系统】中，实际上已经实现过
-
了，该案例能够根据检索结果的质量动态调整查询策略。逻辑如下图所示：
视图
否 直接回答
合格 生成答案
用戶问题 AI决策是否需要检索? 是 检索文档 质量检查
不合格
重写问题
评估器 优化器 的核心在于 质量检测 ，相关代码如下：
-

代码块
1 def grade_documents(state: MessagesState):
2 """评估检索结果质量"""
3 # 评估逻辑...
4 if score == "yes":
5 return "generate_answer" # 质量达标，生成答案
6 else:
7 return "rewrite_question" # 质量不够，优化问题重新检索
值得再说的是，除了可以让 LLM 当作 评估器 ，在 LangGraph 中，还支持 人机交互 式的评估，即将
质量评估由人工来完成。这部分能力敬请期待！
四、LangGraph 持久化（Persistence）
1. 什么是持久化能力？
简单来说，在 LangGraph 中持久化能力指的是将 AI 应用的状态（如对话历史、中间结果、用戶信息
等）保存下来，即使程序重启或系统宕机，也能恢复之前的状态，让 AI "记住"之前发生的一切。
想象一下这个场景：你今天在和智能助手聊天，说了很多重要信息。然后你关闭了应用，明天重新打
开并重新与它对话时，希望它还记得你说过的话吗？当然希望！这就是 AI 应用需要持久化的第一个原
因。
再看第二个场景：假设有一个助手，它可以搜索网络。流程如下所示【快速上手-案例二】。

视图
不需要 返回最终答案
用戶提问 LLM判断是否需要搜索 需要 执行搜索
整合结果
没有持久化：
• 用戶问：“今天的天气怎么样？”
• 助手调用搜索工具，得到答案：“今天晴天，25度。”
• 程序崩溃重启。
• 用戶再问：“那我需要带伞吗？”
• 助手没有之前的上下文，它可能又会去调用搜索工具，而不是基于“今天晴天”这个上下文来回
答“不需要”。
有持久化：
• 用戶问：“今天的天气怎么样？”
• 助手调用搜索工具，得到答案：“今天晴天，25度。” （这个状态，包括对话历史和工具调用结
果，被自动保存）
• 程序崩溃重启。
• 用戶再问：“那我需要带伞吗？”（与之前在同一会话下）
• LangGraph 加载之前保存的状态，状态里记录了“今天晴天”。
• 助手看到上下文是晴天，于是直接回答：“今天是晴天，您不需要带伞。” （无需再次调用搜索
工具）
实际上在 LangGraph 中，持久化能力具体包含两部分能力：
1. 【线程级】持久化：能够【自动保存】工作流执行过程中的【状态快照】，维持单次会话的完整上
下文。
对应上述场景二；
解释1：这里的【线程持久化】和【操作系统线程】概念完全独立区分。操作系统线程是进程内
的执行单元，是操作系统能够进行调度的最小单位。而线程级持久化表示聊天过程中的单次会话

的持久化信息，用来隔离不同的聊天会话。
解释2：这里的【状态快照】并非是之前学习过的 State 的快照。这个状态包含了所有必要的上下
文信息，比如：已经调用过哪些工具、用戶的输入、聊天历史、下一步要执行的节点等等。
2. 【跨会话】持久化：通过存储（Store）保存用戶信息、偏好设置等长期数据，实现不同对话间信
息的持久化共享。
对应上述场景一；
例如，可以将用戶基本情况（有高血压病史）存储，后续无论在何时何地，或无论新开几个会话
窗口，都可以基于用戶基本信息（有高血压病史）生成结果。
2. 线程级持久化
2.1 线程级持久化是怎么工作的？
当我们开始执行工作流，过程中可能会发生 崩溃或重启导致的中断 等异常情况。
根据 LangGraph 的持久化机制，线程级持久化表示能够【自动保存】工作流执行过程中的【状态快
照】，维持单次会话的完整上下文。当工作流执行到某一步时，它会自动保存当前步骤的状态快照。
这个状态包含了所有必要的上下文信息，比如：已经调用过哪些工具、用戶的输入、聊天历史、下一
步要执行的节点等等。
因此，工作流在执行过程中会发生如下图所示的流程：
• 正常执行：紫色/蓝色节点和实线箭头
• 异常恢复：红色/绿色节点和虚线箭头
• 检查点回滚：橙色节点和虚线箭头

视图
初始状态
工作流启动
初始化上下文：用戶输入、
加载当前线程内的历史状态
执行步骤1
状态1：+工具调用记录1、
中间结果1、下一步要执行
的节点
异常中断（崩溃/重启）
Persistence 自动保存
状态丢失风险
状态1快照到存储
执行步骤2
状态2：+工具调用记录2、 从持久化存储
中间结果2、更新聊天历 恢复状态1快照
史、下一步要执行的节点
异常中断（崩溃/重启）
Persistence 自动保存
状态丢失风险 回滚到状态1
状态2快照到存储
执行步骤3
状态3：+最终计算结果、完 从持久化存储
回滚到状态2
整聊天历史、下一步要执行 恢复状态2快照
的节点
Persistence 自动保存
状态3快照到存储
需要回滚
从持久化存储
工作流终止
选择状态1/2快照回滚
持久化存储
状态3快照 状态2快照 状态1快照
线程级持久化机制确保了：
1. 状态不丢失：即使应用程序崩溃、重启，或者一个长时间的流程被中断，当它恢复时，可以从上次
停止的地方继续执行，而不是从头开始。

2. 支持长时间运行的任务：对于需要与用戶进行多轮交互（如多步对话助手）或处理耗时极长的流程
（如等待外部 API 回调），持久化是必不可少的。
3. 检查点和回滚：我们可以将状态保存到某个时间点（检查点），并在需要时回滚到该状态。
2.2 核心概念
LangGraph 的持久化机制⸺ 线程级持久化 是其核心功能，它通过【线程】和【检查点】这两个核心
部分来实现。具体如下：
2.2.1 Threads（线程）
在 LangGraph 中，Thread 代表一个独立的工作流执行会话。可以把它想象成【与某个用戶的一次完
整对话历史】或【处理某个特定任务的一次完整执行过程】。例如在 DS 中的一次完整对话：

Thread 的关键特性如下：
• 隔离性：每个 Thread 都是完全独立的，它们的状态互不干扰
• 持久化单元：Thread 是状态持久化的基本单位
• 标识符：通过唯一的   来识别
thread_id
2.2.2 Checkpoints（检查点）
Checkpoint 是 Thread 在特定时刻的【状态快照】。它记录了工作流执行到某个节点时的完整状态。
例如在刚才的会话中，每一次用戶输入和对话结束后，都可以保存一个最新的【状态快照】：

Checkpoint 的关键特性：
• 状态快照（StateSnapshot）：保存了工作流在某个时间点的完整状态。包含【状态值】、【下一
步要执行的节点】、【与此检查点关联的配置】和【与此检查点关联的元数据】等信息。
StateSnapshot 结构如下：
代码块
1 StateSnapshot(
2 # 当前状态值（如：对话消息列表）
3 values={'messages': [用戶消息, AI回复, 用戶消息...]},
4
5 # 接下来要执行的节点
6 next=('generate_response',),
7
8 # 配置信息
9 config={'configurable': {'thread_id': '123', 'checkpoint_id': 'abc'}},
10
11 # 元数据（步骤号、来源、写入信息等）
12 metadata={'step': 2, 'source': 'loop', 'writes': {...}},
13
14 # 父检查点（形成链表）
15 parent_config={'configurable': {'thread_id': '123', 'checkpoint_id':
'def...'}},
16
17 # 创建时间
18 created_at=''
19 )

具体示例：
代码块
1 [
2 StateSnapshot(values={'messages': [HumanMessage(content='你好',
additional_kwargs={}, response_metadata={}), AIMessage(content='你好！有什么我
可以帮助你的吗？', additional_kwargs={'refusal': None}, response_metadata=
{'token_usage': {'completion_tokens': 11, 'prompt_tokens': 130,
'total_tokens': 141, 'completion_tokens_details':
{'accepted_prediction_tokens': None, 'audio_tokens': None,
'reasoning_tokens': None, 'rejected_prediction_tokens': None},
'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}},
'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-
CiGUUZCWPLKOuRv6sdzolSVAzwtMW', 'finish_reason': 'stop', 'logprobs': None},
id='lc_run--7d1e5db6-e8b2-42c1-9fd8-ba21c42705ac-0', usage_metadata=
{'input_tokens': 130, 'output_tokens': 11, 'total_tokens': 141,
'input_token_details': {'cache_read': 0}, 'output_token_details': {}})],
'llm_calls': 1}, next=(), config={'configurable': {'thread_id': '1',
'checkpoint_ns': '', 'checkpoint_id': '1f0cf5cf-48e3-6bbb-8001-
c351576393a6'}}, metadata={'source': 'loop', 'step': 1, 'parents': {}},
created_at='2025-12-02T08:57:39.538826+00:00', parent_config=
{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id':
'1f0cf5cf-38d7-61a8-8000-2dacafb54f11'}}, tasks=(), interrupts=()),
3 StateSnapshot(values={'messages': [HumanMessage(content='你好',
additional_kwargs={}, response_metadata={})]}, next=('llm_call',), config=
{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id':
'1f0cf5cf-38d7-61a8-8000-2dacafb54f11'}}, metadata={'source': 'loop',
'step': 0, 'parents': {}}, created_at='2025-12-02T08:57:37.855930+00:00',
parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf5cf-38d4-6e0c-bfff-6ce6b2a2dd01'}}, tasks=
(PregelTask(id='44c184e5-8661-3f3c-eeee-7a2f569f7e88', name='llm_call', path=
('__pregel_pull', 'llm_call'), error=None, interrupts=(), state=None, result=
{'messages': [AIMessage(content='你好！有什么我可以帮助你的吗？',
additional_kwargs={'refusal': None}, response_metadata={'token_usage':
{'completion_tokens': 11, 'prompt_tokens': 130, 'total_tokens': 141,
'completion_tokens_details': {'accepted_prediction_tokens': None,
'audio_tokens': None, 'reasoning_tokens': None,
'rejected_prediction_tokens': None}, 'prompt_tokens_details':
{'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai',
'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint':
'fp_efad92c60b', 'id': 'chatcmpl-CiGUUZCWPLKOuRv6sdzolSVAzwtMW',
'finish_reason': 'stop', 'logprobs': None}, id='lc_run--7d1e5db6-e8b2-42c1-
9fd8-ba21c42705ac-0', usage_metadata={'input_tokens': 130, 'output_tokens':
11, 'total_tokens': 141, 'input_token_details': {'cache_read': 0},
'output_token_details': {}})], 'llm_calls': 1}),), interrupts=()),

4 StateSnapshot(values={'messages': []}, next=('__start__',), config=
{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id':
'1f0cf5cf-38d4-6e0c-bfff-6ce6b2a2dd01'}}, metadata={'source': 'input',
'step': -1, 'parents': {}}, created_at='2025-12-02T08:57:37.855022+00:00',
parent_config=None, tasks=(PregelTask(id='56c07f44-a6a6-a8b8-899a-
d5c24b2ff671', name='__start__', path=('__pregel_pull', '__start__'),
error=None, interrupts=(), state=None, result={'messages':
[HumanMessage(content='你好', additional_kwargs={}, response_metadata=
{})]}),), interrupts=())
5 ]
• 版本历史与可恢复点：一个 Thread 可以有多个 Checkpoints，形成执行历史，使得同一个会话的
历史状态可以从任意 Checkpoint 追溯和访问。
Threads 与 Checkpoints 关系如下：
2.3 线程级持久化使用姿势
2.3.1 步骤一：配置 持久化存储
checkpointer

在定义图时，我们需要指定 。LangGraph 支持多种 的定义方式：
checkpointer checkpointer
2.3.1.1 方式1：内存存储
最简单的方式，状态保存在程序内存中。适用于开发和测试，程序重启后状态会丢失。用法如下所
示：
这里使用快速上手⸺案例2的代码，在编译图时，直接添加编译参数
checkpointer
视图
__start__
llm_call
__end__ tool_node
代码块
1 from langgraph.checkpoint.memory import InMemorySaver
2 # 定义存储方式
3 checkpointer = InMemorySaver()
4 # 用 checkpointer 编译图
5 agent = agent_builder.compile(checkpointer=checkpointer)
2.3.1.2 方式2：使用 Postgres 存储库
LangGraph 提供了几个检查点存储实现，所有这些都通过独立的、可安装的库实现。适用于生产环境
或需要状态持久化的场景。
• SQLite 存储（ ）：使用 SQLite 数据库（
langgraph-checkpoint-sqlite SqliteSaver
/  ）的 LangGraph 检查点的实现。非常适合实验和本地工作流程。需要单
AsyncSqliteSaver
独安装。
• Postgres 存储（ ）：使用 Postgres 数据库
langgraph-checkpoint-postgres
（  /  ）的 LangGraph 检查点的实现。非常适合在生
PostgresSaver AsyncPostgresSaver
产中使用。需要单独安装。
为什么选择 PostgreSQL 作为存储库？

在众多持久化存储方案中，PostgreSQL 作为关系型数据库的佼佼者（PostgreSQL 和 MySQL 一
样，都是最流行的开源关系型数据库），具备以下显著优势，使其成为持久化的理想选择：
• LangGraph 原生支持： LangGraph 提供了  ，简化了与 PostgreSQL 的集成
PostgresSaver
过程。
• 数据结构化与一致性： 关系型数据库天生适合存储结构化数据。Graph 的状态，尤其是消息历
史、用戶档案、工具使用记录等，都可以很好地映射到表格结构中，确保数据的一致性和完整
性。
• 可靠性与持久性： PostgreSQL 提供了事务支持、ACID 特性、数据备份与恢复机制，确保数据的
持久性和高可用性，即使系统崩溃也能保证数据不丢失。
• 强大的查询能力： SQL 语言提供了灵活且强大的数据查询能力，方便我们对历史行为、用戶数据
进行分析、统计和审计。结合 等扩展，甚至可以直接在数据库中进行向量相似度搜
pgvector
索，实现更高级的知识管理。
• 可扩展性： 通过读写分离、分区、集群等技术，PostgreSQL 可以支持大规模的并发访问和数据
存储，满足 Agent 在生产环境中的性能需求。
• 成熟的生态系统： 拥有庞大的社区支持、丰富的工具和成熟的运维经验，降低了开发和维护成
本。
使用 Docker 快速安装并启动 postgres：
代码块
1 # 1. 拉取 PostgreSQL 镜像
2 docker pull postgres:latest
3
4 # 2. 运行 PostgreSQL 容器
5 # -p 5432:5432: 将容器的5432端口映射到宿主机的5432端口
6 # -e POSTGRES_PASSWORD=bit: 设置PostgreSQL的postgres用戶密码
7 # --name postgres-sql: 给容器命名
8 # -d: 后台运行
9 docker run --name postgres-sql -e POSTGRES_PASSWORD=bit -p 5432:5432 -d
postgres
可以使用 Navicat 测试链接：注意默认连接 postgres 初始数据库，如果有其他数据库可以配置连
接。

1. 安装 包
langgraph-checkpoint-postgres
代码块
1 pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres
2. 设置 PostgreSQL 连接字符串 (URI)
PostgreSQL URI 通常遵循以下格式：
postgresql://<user>:<password>@<host>:
<port>/<database_name>
3. 使用 Postgre 存储库作为检查点
使用 方法从连接字符串创建一个新的 PostgresSaver 实
PostgresSaver.from_conn_string()
例。
注意：第一次使用 Postgres 检查点时需要调用
checkpointer.setup()
代码块
1 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
2 with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
3
4 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
5 checkpointer.setup()
6
7 # 编译图
8 agent = agent_builder.compile(checkpointer=checkpointer)
9
10 # ...后续调用...

2.3.2 步骤二：使用 Thread 进行执行
当我们编译好图并准备运行时，我们需要通过一个 Thread ID 来标识这次执行。
• 如果 Thread ID 不存在：LangGraph 会创建一个新的 Thread，并从初始状态开始执行。
• 如果 Thread ID 已存在：LangGraph 会从 Checkpointer 中加载该 Thread 的最后一次保存的状
态，并从这个状态继续执行。
这里依旧使用postgres存储，进行第一次执行：创建一个新的 Thread (thread_id="1")
代码块
1 from langchain.messages import HumanMessage
2
3 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
4 with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
5
6 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
7 checkpointer.setup()
8
9 # 编译图
10 agent = agent_builder.compile(checkpointer=checkpointer)
11
12 # 第一次执行，创建一个新的 Thread (thread_id="1")
13 config = {"configurable": {"thread_id": "1"}}
14 result1 = agent.invoke(
15 {"messages": [HumanMessage(content="今天西安的天气如何？")]},
16 config
17 )
18 print(f"调用 LLM 总次数：{result1["llm_calls"]}次")
19 for m in result1["messages"]:
20 m.pretty_print()
运行后，可以看到postgres库中，已经存储了检查点信息：
一段时间后，再次使用相同的 thread_id 调用：
代码块

1 from langchain.messages import HumanMessage
2
3 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
4 with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
5
6 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
7 # checkpointer.setup()
8
9 # 编译图
10 agent = agent_builder.compile(checkpointer=checkpointer)
11
12 # ............... 一段时间后，程序可能重启了（使用postgres存储） ...............
13
14 # 再次使用相同的 thread_id 调用
15 # LangGraph 会从上次的状态继续，而不是重新开始
16 # 此时，result2 的上下文会包含之前的对话历史
17 config = {"configurable": {"thread_id": "1"}}
18 result2 = agent.invoke(
19 {"messages": [HumanMessage(content="我们刚才聊到哪了？")]},
20 config
21 )
22 print(f"调用 LLM 总次数：{result2["llm_calls"]}次")
23 for m in result2["messages"]:
24 m.pretty_print()
第二次调用结果如下：
代码块
1 调用 LLM 总次数：3次
2 ================================ Human Message
=================================
3
4 今天西安的天气如何？
5 ================================== Ai Message
==================================
6 Tool Calls:
7 tavily_search (call_8ALCCwF3xudzjavTFNI6rA0m)
8 Call ID: call_8ALCCwF3xudzjavTFNI6rA0m
9 Args:
10 query: 西安天气
11 ================================= Tool Message
=================================
12
13 (省略...)

14 ================================== Ai Message
==================================
15
16 今天西安的天气情况如下：
17
18 - **气温**：最高温度约为18°C，最低温度约为7°C。
19 - **天气状况**：多云，空气质量较好。
20
21 如果你想查看更详细的天气预报，可以访问以下链接：
22 - [中国气象局 - 西安天气预报](https://weather.cma.cn/web/weather/V8870.html)
23 - [天气网 - 西安天气](https://www.weather.com.cn/weather40d/101110101.shtml)
24
25 请根据天气情况合理安排你的出行！
26 ================================ Human Message
=================================
27
28 我们刚才聊到哪了？
29 ================================== Ai Message
==================================
30
31 我们刚才聊到西安的天气情况，包括今天的气温和天气状况。如果你有其他问题或者想讨论的内容，请
告诉我！
从结果看来，result2 的上下文会包含之前的对话历史。LangGraph 会从上次的状态继续，而不是重新
开始
2.3.3 其他基本用法
2.3.3.1 获取状态快照
当使用 编译图时，执行时就会在每个步骤处保存状态快照。在 LangGraph 中状态快
checkpointer
照就是   对象，其具有以下关键属性：
StateSnapshot
代码块
1 StateSnapshot(
2 # 当前状态值（如：对话消息列表）
3 values={'messages': [用戶消息, AI回复, 用戶消息...]},
4
5 # 接下来要执行的节点
6 next=('generate_response',),
7
8 # 配置信息
9 config={'configurable': {'thread_id': '123', 'checkpoint_id': 'abc'}},
10

11 # 元数据（步骤号、来源、写入信息等）
12 metadata={'step': 2, 'source': 'loop', 'writes': {...}},
13
14 # 父检查点（形成链表）
15 parent_config={'configurable': {'thread_id': '123', 'checkpoint_id':
'def...'}},
16
17 # 创建时间
18 created_at=''
19 )
我们可以使用 方法，获取编译后的图的最新状态快照。让我们分别获取一下
get_state(config)
执行前与执行后的最新状态快照：
代码块
1 from langchain.messages import HumanMessage
2 config = {"configurable": {"thread_id": "1"}}
3
4 # 调用前的状态快照
5 snapshot = agent.get_state(config)
6 print(snapshot)
7
8 result1 = agent.invoke(
9 {"messages": [HumanMessage(content="你好")]},
10 config
11 )
12
13 # 调用后的状态快照
14 snapshot = agent.get_state(config)
15 print(snapshot)
打印结果：
代码块
1 StateSnapshot(
2 values={},
3 next=(),
4 config={'configurable': {'thread_id': '1'}},
5 metadata=None,
6 created_at=None,
7 parent_config=None,
8 tasks=(),
9 interrupts=()
10 )

11 StateSnapshot(
12 values={'messages': [HumanMessage(content='你好', additional_kwargs={},
response_metadata={}), AIMessage(content='你好！有什么我可以帮助你的吗？',
additional_kwargs={'refusal': None}, response_metadata={'token_usage':
{'completion_tokens': 11, 'prompt_tokens': 130, 'total_tokens': 141,
'completion_tokens_details': {'accepted_prediction_tokens': None,
'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens':
None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}},
'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-
CiGBdkNSGgkZ3ccpa6NEAyUHrzqls', 'finish_reason': 'stop', 'logprobs': None},
id='lc_run--f76d30e4-0e06-4f18-ab44-0e43e8ff70b8-0', usage_metadata=
{'input_tokens': 130, 'output_tokens': 11, 'total_tokens': 141,
'input_token_details': {'cache_read': 0}, 'output_token_details': {}})],
'llm_calls': 1},
13 next=(),
14 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf5a3-b6ff-6b2e-8001-dc5cd083ad82'}},
15 metadata={'source': 'loop', 'step': 1, 'parents': {}},
16 created_at='2025-12-02T08:38:09.968610+00:00',
17 parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf5a3-a7a5-6cf8-8000-ec666fd226fe'}},
18 tasks=(),
19 interrupts=()
20 )
2.3.3.2 获取状态历史记录
我们可以通过调用   来获取给定线程的图执行的完整历史记录。这
get_state_history(config)
将返回与配置中提供的线程 ID 关联的   对象列表。
StateSnapshot
代码块
1 from langchain.messages import HumanMessage
2 config = {"configurable": {"thread_id": "1"}}
3 result1 = agent.invoke(
4 {"messages": [HumanMessage(content="你好")]},
5 config
6 )
7 # 查看状态历史记录
8 history = list(agent.get_state_history(config))
9 print(history)
返回结果将按时间顺序排序，列表中的第一个检查点（ ）是最新的。结果如下：
StateSnapshot

代码块
1 [
2 StateSnapshot(values={'messages': [HumanMessage(content='你好',
additional_kwargs={}, response_metadata={}), AIMessage(content='你好！有什么我可
以帮助你的吗？', additional_kwargs={'refusal': None}, response_metadata=
{'token_usage': {'completion_tokens': 11, 'prompt_tokens': 130,
'total_tokens': 141, 'completion_tokens_details':
{'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens':
None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details':
{'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai',
'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_efad92c60b',
'id': 'chatcmpl-CiGUUZCWPLKOuRv6sdzolSVAzwtMW', 'finish_reason': 'stop',
'logprobs': None}, id='lc_run--7d1e5db6-e8b2-42c1-9fd8-ba21c42705ac-0',
usage_metadata={'input_tokens': 130, 'output_tokens': 11, 'total_tokens': 141,
'input_token_details': {'cache_read': 0}, 'output_token_details': {}})],
'llm_calls': 1}, next=(), config={'configurable': {'thread_id': '1',
'checkpoint_ns': '', 'checkpoint_id': '1f0cf5cf-48e3-6bbb-8001-
c351576393a6'}}, metadata={'source': 'loop', 'step': 1, 'parents': {}},
created_at='2025-12-02T08:57:39.538826+00:00', parent_config={'configurable':
{'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0cf5cf-38d7-61a8-
8000-2dacafb54f11'}}, tasks=(), interrupts=()),
3 StateSnapshot(values={'messages': [HumanMessage(content='你好',
additional_kwargs={}, response_metadata={})]}, next=('llm_call',), config=
{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id':
'1f0cf5cf-38d7-61a8-8000-2dacafb54f11'}}, metadata={'source': 'loop', 'step':
0, 'parents': {}}, created_at='2025-12-02T08:57:37.855930+00:00',
parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf5cf-38d4-6e0c-bfff-6ce6b2a2dd01'}}, tasks=
(PregelTask(id='44c184e5-8661-3f3c-eeee-7a2f569f7e88', name='llm_call', path=
('__pregel_pull', 'llm_call'), error=None, interrupts=(), state=None, result=
{'messages': [AIMessage(content='你好！有什么我可以帮助你的吗？',
additional_kwargs={'refusal': None}, response_metadata={'token_usage':
{'completion_tokens': 11, 'prompt_tokens': 130, 'total_tokens': 141,
'completion_tokens_details': {'accepted_prediction_tokens': None,
'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens':
None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}},
'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-
CiGUUZCWPLKOuRv6sdzolSVAzwtMW', 'finish_reason': 'stop', 'logprobs': None},
id='lc_run--7d1e5db6-e8b2-42c1-9fd8-ba21c42705ac-0', usage_metadata=
{'input_tokens': 130, 'output_tokens': 11, 'total_tokens': 141,
'input_token_details': {'cache_read': 0}, 'output_token_details': {}})],
'llm_calls': 1}),), interrupts=()),
4 StateSnapshot(values={'messages': []}, next=('__start__',), config=
{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id':
'1f0cf5cf-38d4-6e0c-bfff-6ce6b2a2dd01'}}, metadata={'source': 'input', 'step':

-1, 'parents': {}}, created_at='2025-12-02T08:57:37.855022+00:00',
parent_config=None, tasks=(PregelTask(id='56c07f44-a6a6-a8b8-899a-
d5c24b2ff671', name='__start__', path=('__pregel_pull', '__start__'),
error=None, interrupts=(), state=None, result={'messages':
[HumanMessage(content='你好', additional_kwargs={}, response_metadata={})]}),),
interrupts=())
5 ]
2.3.3.3 重放
如果我们用一个 和一个 （表示检查点标识符，用于指代线程内的特
thread_id checkpoint_id
定检查点）来调用一个图，那么我们将重新执行对应于 之后的步骤。如下所示：
checkpoint_id
• 先执行一次完整的流程，获取一次完整历史记录；
• 保存中间过程某一次快照，并重新执行快照后的步骤；
• 获取第二次调用后的完整历史记录，验证是否重放成功；
代码块
1 from langchain.messages import HumanMessage
2 config = {"configurable": {"thread_id": "1"}}
3 # 第一次执行
4 result1 = agent.invoke(
5 {"messages": [HumanMessage(content="今天西安的天气如何？")]},
6 config
7 )
8
9 # 保存调用工具前的状态
10 print("-" * 80)
11 print(f"第一次执行历史：")
12 to_replay = None
13 for state in agent.get_state_history(config):
14 print("checkpoint_id: ", state.config["configurable"]["checkpoint_id"],
15 "消息数: ", len(state.values["messages"]),
16 "下一节点: ", state.next)
17 if len(state.values["messages"]) == 2: # 保存调用工具前的状态
18 to_replay = state
19
20 print("-" * 80)
21 print(f"从{to_replay.next}节点开始重新执行, 重放配置：{to_replay.config}")
22
23 # 第二次执行：重放
24 result2 = agent.invoke(None, config=to_replay.config)
25 print("-" * 80)

26 print(f"第二次执行历史：重放后")
27 # 查看新的历史记录
28 for state in agent.get_state_history(config):
29 print("checkpoint_id: ", state.config["configurable"]["checkpoint_id"],
30 "消息数: ", len(state.values["messages"]),
31 "下一节点: ", state.next)
32
33 result2['messages'][-1].pretty_print()
执行结果如下所示。可以看到历史记录中帮我们记录所有的执行过程，包括重放前和重放后的步骤！
这同时也证明了重放成功。
代码块
1 -------------------------------------------------------------------------------
-
2 第一次执行历史：
3 checkpoint_id: 1f0cf6bc-cb09-61e3-8003-1a74660e9324 消息数: 4 下一节点: ()
4 checkpoint_id: 1f0cf6bc-b148-624e-8002-f696045e95a8 消息数: 3 下一节点:
('llm_call',)
5 checkpoint_id: 1f0cf6bc-8a86-62a5-8001-38aa0c3d8d80 消息数: 2 下一节点:
('tool_node',)
6 checkpoint_id: 1f0cf6bc-7abe-6d9a-8000-ef816c492e36 消息数: 1 下一节点:
('llm_call',)
7 checkpoint_id: 1f0cf6bc-7abc-6ce5-bfff-5241076b5574 消息数: 0 下一节点:
('__start__',)
8 -------------------------------------------------------------------------------
-
9 从('tool_node',)节点开始重新执行, 重放配置：{'configurable': {'thread_id': '1',
'checkpoint_ns': '', 'checkpoint_id': '1f0cf6bc-8a86-62a5-8001-38aa0c3d8d80'}}
10 -------------------------------------------------------------------------------
-
11 第二次执行历史：重放后
12 checkpoint_id: 1f0cf6bd-0e30-6cf9-8003-f22545cde7b2 消息数: 4 下一节点: ()
13 checkpoint_id: 1f0cf6bc-e376-6e52-8002-9c66bdb5577a 消息数: 3 下一节点:
('llm_call',)
14 checkpoint_id: 1f0cf6bc-cb09-61e3-8003-1a74660e9324 消息数: 4 下一节点: ()
15 checkpoint_id: 1f0cf6bc-b148-624e-8002-f696045e95a8 消息数: 3 下一节点:
('llm_call',)
16 checkpoint_id: 1f0cf6bc-8a86-62a5-8001-38aa0c3d8d80 消息数: 2 下一节点:
('tool_node',)
17 checkpoint_id: 1f0cf6bc-7abe-6d9a-8000-ef816c492e36 消息数: 1 下一节点:
('llm_call',)
18 checkpoint_id: 1f0cf6bc-7abc-6ce5-bfff-5241076b5574 消息数: 0 下一节点:
('__start__',)

19 ================================== Ai Message
==================================
20
21 今天西安的天气情况如下：
22
23 - **天气**：晴
24 - **气温**：最高温度约为 13°C，最低温度约为 2°C
25 - **风速**：东北风，约 6 英里/小时
26 - **空气质量**：不健康
重放功能实际应用为时间旅行，详见下文【时间旅行（Time Travel）】篇章。
2.3.3.4 更新状态
我们还可以编辑图状态。我们使用 方法来做到这一点。
update_state()
让我们更新用戶的输入，换成其他搜索内容：
• 先执行一次完整的流程，获取一次完整历史记录；
• 保存第一次调用LLM前的步骤快照，修改用戶输入来更新快照，并重新执行更新后快照步骤；
代码如下：
代码块
1 from langchain.messages import HumanMessage
2 from langgraph.types import Overwrite
3
4 config = {"configurable": {"thread_id": "1"}}
5 # 第一次执行
6 result1 = agent.invoke(
7 {"messages": [HumanMessage(content="今天西安的天气如何？")]},
8 config
9 )
10
11 # 找到调用LLM前的步骤
12 print("-" * 80)
13 print(f"第一次执行历史：")
14 selected_state = None
15 for state in agent.get_state_history(config):
16 print("checkpoint_id: ", state.config["configurable"]["checkpoint_id"],
17 "消息数: ", len(state.values["messages"]),
18 "下一节点: ", state.next)
19 if len(state.values["messages"]) == 1: # 此时消息数为1；下一节点是'llm_call'
20 selected_state = state
21

22 print("-" * 80)
23 print(f"更新前配置：{selected_state.config}")
24
25 # 根据指定的config，更新对于步骤的值
26 # 更新用戶输入
27 new_config = agent.update_state(
28 selected_state.config,
29 {"messages": Overwrite([HumanMessage(content="今天北京的天气如何？")])} # 清
空消息，重新写入
30 )
31 print("-" * 80)
32 print(f"更新后配置：{new_config}")
33
34 # 第二次执行：重放更新后的配置
35 result2 = agent.invoke(None, config=new_config)
36 for message in result2['messages']:
37 message.pretty_print()
执行结果如下：
代码块
1 -------------------------------------------------------------------------------
-
2 第一次执行历史：
3 checkpoint_id: 1f0cf6c8-743c-6b8d-8003-d8a1130c15e0 消息数: 4 下一节点: ()
4 checkpoint_id: 1f0cf6c8-4244-682c-8002-bdc8b86d460d 消息数: 3 下一节点:
('llm_call',)
5 checkpoint_id: 1f0cf6c8-3304-6782-8001-7ebc967b7bb1 消息数: 2 下一节点:
('tool_node',)
6 checkpoint_id: 1f0cf6c8-1b1c-62a0-8000-42b9d34bb01d 消息数: 1 下一节点:
('llm_call',)
7 checkpoint_id: 1f0cf6c8-1b19-6adb-bfff-915f44142490 消息数: 0 下一节点:
('__start__',)
8 -------------------------------------------------------------------------------
-
9 更新前配置：{'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf6c8-1b1c-62a0-8000-42b9d34bb01d'}}
10 -------------------------------------------------------------------------------
-
11 更新后配置：{'configurable': {'thread_id': '1', 'checkpoint_ns': '',
'checkpoint_id': '1f0cf6c8-7444-61e3-8001-d9eb91c95052'}}
12 ================================ Human Message
=================================
13
14 今天北京的天气如何？

15 ================================== Ai Message
==================================
16 Tool Calls:
17 tavily_search (call_FfUFDwThpNTBHoijgvNmwtMr)
18 Call ID: call_FfUFDwThpNTBHoijgvNmwtMr
19 Args:
20 query: 北京天气
21 ================================= Tool Message
=================================
22
23 （省略...）
24 ================================== Ai Message
==================================
25
26 今天北京的天气情况如下：
27 - 当前气温：-4°C
28 - 湿度：23%
29 - 风速：25.2 km/h
30 - 天气状况：晴朗
31 - 最高气温：预计为16°C
3. 跨会话持久化
3.1  的局限性
Checkpoint
3.1.1 问题场景：跨会话信息丢失
LangGraph 的 Checkpoint 机制提供了强大的短期记忆能力，它能够：
• 自动保存工作流每个步骤的状态快照
• 维持单次对话的完整上下文
• 隔离不同线程（Thread）的执行状态
简单示例（仅调用了下 LLM）：
代码块
1 import operator
2 from typing import TypedDict, Annotated
3
4 from langchain.chat_models import init_chat_model
5 from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
6 from langgraph.checkpoint.memory import InMemorySaver
7 from langgraph.constants import START, END

8 from langgraph.graph import StateGraph
9
10
11 # 定义状态
12 class MessagesState(TypedDict):
13 messages: Annotated[list[AnyMessage], operator.add]
14
15 # 定义模型节点
16 model = init_chat_model("gpt-4o-mini", temperature=0)
17 def llm_call(state: dict):
18 """LLM调用"""
19 return {
20 "messages": [
21 model.invoke([SystemMessage(content="你是一个乐于助人的助手。")]
22 + state["messages"])
23 ]
24 }
25
26 # 构件图
27 builder = StateGraph(MessagesState)
28 builder.add_node("llm_call", llm_call)
29 builder.add_edge(START, "llm_call")
30 builder.add_edge("llm_call", END)
31 graph = builder.compile(checkpointer=InMemorySaver())
检查点可以完美处理会话内记忆，如下所示：
代码块
1 config1 = {"configurable": {"thread_id": "1"}}
2 # 第一次对话
3 result1 = graph.invoke({"messages": [HumanMessage(content="我爱吃汉堡，推荐一家餐
厅")]}, config1)
4
5 # AI记得：你爱吃汉堡
6 result2 = graph.invoke({"messages": [HumanMessage(content="我爱吃什么？")]},
config1)
7 result2["messages"][-1].pretty_print()
8 # 输出：你提到你爱吃汉堡，所以可以推测你喜欢美味的快餐和丰富的口味组合。如果你有其他喜欢的
食物或菜系，也可以告诉我，我可以为你推荐更多相关的美食或餐厅！
想象一个多会话的 AI 助手场景：
• 星期一，用戶首次对话
• 星期二，用戶开启一个新对话

如下所示：
代码块
1 # 星期一，用戶首次对话
2 config1 = {"configurable": {"thread_id": "day_1"}}
3 result1 = graph.invoke({"messages": [HumanMessage(content="我爱吃汉堡，推荐一家餐
厅")]}, config1)
4
5 # 星期二，用戶开启一个新对话
6 config2 = {"configurable": {"thread_id": "day_2"}}
7 result2 = graph.invoke({"messages": [HumanMessage(content="我爱吃什么？")]},
config2)
8 result2["messages"][-1].pretty_print()
9 # 输出：我不知道你具体喜欢吃什么，但可以根据一些常见的食物类型来猜测。比如，有些人喜欢甜
食，如蛋糕和冰淇淋；有些人喜欢咸食，如薯条和披萨；还有些人喜欢健康的食物，如沙拉和水果。你
可以告诉我你喜欢的食物类型，我可以给你一些推荐！
问题出现：AI不记得用戶喜欢汉堡！每次对话都要"重新认识"。
3.1.2 现实世界的需求：从"单次对话"到"终身服务"
例如一个智能客服系统，具有以下实际业务需求：
• 识别 VIP 客戶，优先服务
• 避免重复询问相同问题
• 基于历史投诉优化服务

仅是检查点无法满足这些需求：
代码块
1 graph = builder.compile(checkpointer=InMemorySaver())
2
3 config1 = {"configurable": {"thread_id": "query_1"}}
4 result1 = graph.invoke({"messages": [HumanMessage(content="我的账戶被冻结了")]},
config1)
5 # 用戶第一次投诉账戶问题，已解决。智能客服了如下过程：
6 # - 搜集用戶信息
7 # - 了解用戶问题与需求
8 # - 处理问题
9
10 config2 = {"configurable": {"thread_id": "query_2"}}
11 result2 = graph.invoke({"messages": [HumanMessage(content="我的账戶又被冻结
了")]}, config2)
12 # 10天后，用戶第二次投诉账戶问题。
13 # 由于智能客服不知道用戶历史，无法准确解决问题。还需再次了解前因后果
如何做到【共享状态】的需求模型，如精准识别客戶、保留VIP客戶关键历史记录，是智能客服系统的
关键。如下图所示：

3.2 解决方案：引入 Store
Store 像是一个长期记忆仓库，支持在我们在执行过程中保存用戶信息、偏好设置等长期数据，以实现
不同对话间信息的持久化共享。
3.2.1 存储 vs 检查点
• 检查点：保存状态变化历史（时间线）
• 存储：保存结构化知识（数据库）

实际上，使用 模式才能够真正实现：
Checkpoint + Store

3.2.2 引入 Store 后，AI 应用架构的范式转变
Store 的引入，不是简单的功能增加，而是 AI 应用架构的范式转变：
第1阶段：无状态AI（石器时 第2阶段：检查点（工业革 第3阶段：检查点+Store（智能时
代） 命）  代）
  每次对话都是陌生人   单次对话有记忆   终身记忆，持续学习
  "你好！" "你好！"（无限循   "我叫小明" "你好小   "一年前你喜欢披萨，现在还喜
环） 明！"  欢吗？"
  但明天就忘记    "根据你的阅读历史，推荐这本
书..."

Store 的引入，真正能做到：
• 从关注单次交互 → 到关注用戶生命周期
• 从处理当前请求 → 到利用历史数据
• 从通用回复 → 到深度个性化
这种转变让 AI 从"工具"进化为"伙伴"，真正实现智能服务的核心理念：在正确的时间，以正确的方
式，为正确的人提供正确的价值。
题外话：使用 AI 不要随意泄露自己的隐私信息，很容易被保存下来！
3.3 跨会话持久化使用姿势
要想使用 store，我们需要创建一个存储实例，其也有【内存级存储】与相关【存储库存储】两种方
式。例如内存级存储：
代码块
1 from langgraph.store.memory import InMemoryStore
2 store = InMemoryStore()
接着只需像以前一样使用 Checkpoints 和 Store 变量编译图表即可。如下所示：
代码块
1 graph = builder.compile(checkpointer=checkpointer, store=store)

3.3.1 方式1：内存存储
3.3.1.1 Store 基本用法
本身是通过 Namespace 区分不同数据，如下所示：
Store
在 LangGraph 中，其提供了一个简单的内存实现  。想要进行存储，需要：
InMemoryStore
• 先定义命名空间：为了区分不同用戶的记忆，需要一个“命名空间”。这就像在数据库里为每个用
戶创建一个独立的文件夹。命名空间用于组织记忆，通常按业务逻辑划分。一般用元组来定义命名
空间。如：
代码块
1 # 使用元组 - 层次清晰，易于扩展
2 namespace1 = ("user_123", "preferences", "food") # 用戶食物偏好
3 namespace2 = ("user_123", "preferences", "music") # 用戶音乐偏好
4 namespace3 = ("user_123", "conversations", "2025-05") # 用戶某天的对话历史
5
6 # 使用字符串 - 扁平且易混淆
7 namespace4 = "user_123_preferences_food" # 需要解析，容易出错
8 namespace5 = "user_123_preferences_music"
9 namespace6 = "user_123_conversations_2024"
• 当在对话中获取到用戶的重要信息时，使用 方法将内存保存到存储中的命名空
store.put()
间。该方法参数包含：
◦ ：决定这个记忆属于谁以及是什么类型。
namespace
◦ ：是这个记忆条目的唯一键。
memory_id
◦ ：是记忆的具体内容，一个字典。
memory_content
代码块

1 from langgraph.store.memory import InMemoryStore
2 store = InMemoryStore()
3 store.put(namespace, memory_id, memory_content)
完整代码如下：
代码块
1 # 1. 导入并创建存储
2 from langgraph.store.memory import InMemoryStore
3 import uuid # 用于生成唯一ID
4
5 store = InMemoryStore()
6
7 # 2. 定义命名空间 (Namespace)
8 # 命名空间用于组织记忆，通常按业务逻辑划分，例如按用戶。
9 # 这里我们用一个元组 (用戶ID, 记忆类型)
10 user_id = "user_123"
11 namespace = (user_id, "preferences") # 用戶 user_123 的偏好记忆
12
13 # 3. 存入一条记忆 (Memory)
14 # 每条记忆需要一个唯一的 memory_id 和 一个 value (通常是字典)
15 memory_id = str(uuid.uuid4()) # 生成唯一ID，如 "abc-123-def-456"
16 memory_value = {"favorite_food": "汉堡", "allergy": "花粉"}
17 store.put(namespace, memory_id, memory_value)
18 print("记忆已存入！")
19
20 # 4. 读取记忆
21 # 可以搜索某个命名空间下的所有记忆
22 all_memories = store.search(namespace)
23 for mem in all_memories:
24 print(mem.dict()) # 记忆对象转成字典查看
25
运行结果：
代码块
1 记忆已存入！
2 {
3 'namespace': [
4 'user_123', 'preferences'
5 ],
6 'key': 'db826e33-c68c-4669-a79a-3579bff02ff1',
7 'value': {
8 'favorite_food': '汉堡',

9 'allergy': '花粉'
10 },
11 'created_at': '2025-12-03T08:16:14.134568+00:00',
12 'updated_at': '2025-12-03T08:16:14.134576+00:00',
13 'score': None
14 }
因使用元组作为命名空间，故同样支持下面的搜索方式：
代码块
1 all_memories = store.search((user_id, ))
3.3.1.2 在 LangGraph 中使用 Store
内存存储适用于开发和测试，程序重启后存储的数据会丢失。这里依旧使用 快速上手 案例 的代码
—— 2
进行演示。
由于要加入 Store，需要在合适的地方加入与存储关键信息相关的代码。如我们可以在每次调用 LLM
前先进行信息收集，然后带着收集到的共享信息进行 LLM 调用。因此，流程变成了：
视图
__start__
get_person_by_llm
llm_call
__end__ tool_node
这样，两部分信息将会被收集：一是用戶发的消息；二是通过工具调用返回的结果信息也会被采集。
代码如下：

• 在编译图时，直接添加编译参数 ，如下所示：
store
代码块
1 from langgraph.store.memory import InMemoryStore
2 store = InMemoryStore()
3 # 用 checkpointer + store 编译图
4 agent = agent_builder.compile(checkpointer=checkpointer, store=store)
现在，在任何一个节点的函数中，都可以通过注入   参数来访问这个全局存储。
store
• 新增提取用戶信息节点
在这个节点中，我们需要根据【用戶发的消息】和【工具调用返回的结果】来采集需要收集的信息。
收集的信息需要使用 Store 进行存储。关键设计如下：
1. 任何节点函数，如果需要访问 Store，可以通过在参数中声明   和
store: BaseStore
 来获取。
config: RunnableConfig
2. 在这里可以通过 LLM 提取用戶信息，因此定义结构化返回是很有必要的。
代码块
1 # 定义结构化输出
2 class Person(BaseModel):
3 """一个人的信息。"""
4
5 # 注意:
6 # 1. 每个字段都是 Optional “可选的” —— 允许 LLM 在不知道答案时输出 None。
7 # 2. 每个字段都有一个 description “描述” —— LLM使用这个描述。
8 name: Optional[str] = Field(default=None, description="这个人的名字")
9 height_in_meters: Optional[str] = Field(default=None, description="以米为单
位的高度")
10 favourite_food: Optional[list[str]] = Field(default=None, description="最喜
欢的食物列表")
11
12 model_with_structured = model.with_structured_output(Person)
13
14 # 提取用戶信息节点
15 def get_person_by_llm(state: MessagesState, config: RunnableConfig, *, store:
BaseStore):
16 """通过 LLM 提取用戶信息"""
17
18 # 1. 先提取
19 people_info = model_with_structured.invoke(
20 [
21 SystemMessage(

22 content="你是一个提取信息的专家，只从文本中提取我的相关信息，不能提取别
人的信息。如果你不知道要提取的属性的值，属性值返回null。"
23 )
24 ]
25 + state["messages"][-3:] # 只查看最近3条消息
26 )
27
28 # 2. 再保存
29 user_id = config["configurable"]["user_id"]
30
31 # 保存用戶基本信息
32 namespace1 = (user_id, "info")
33 # 每次put前应判断是否存在，再更新。否则会有多条记录被记录。这里简写
34 store.put(
35 namespace1,
36 str(uuid.uuid4()),
37 {
38 "name": people_info.name,
39 "height": people_info.height_in_meters
40 }
41 )
42
43 # 保存用戶偏好
44 namespace2 = (user_id, "preferences")
45 store.put(
46 namespace2,
47 str(uuid.uuid4()),
48 {"favourite_food": people_info.favourite_food} # 省略追加逻辑：先搜再更新
49 )
50 return {
51 "llm_calls": state.get('llm_calls', 0) + 1
52 }
• 更新模型调用节点：添加共享信息到提示词
调用 LLM 之前，我们便可以通过查询 Store 获取共享信息，然后将其加入到提示词中，完成调用。
代码块
1 def llm_call(state: MessagesState, config: RunnableConfig, *, store:
BaseStore):
2 """LLM决定是否调用工具"""
3
4 # 搜索用戶信息
5 user_id = config["configurable"]["user_id"]
6 namespace1 = (user_id, "info")
7 namespace2 = (user_id, "preferences")

8 info_result = store.search(namespace1)
9 pref_result = store.search(namespace2)
10 return {
11 "messages": [
12 model_with_tools.invoke(
13 [
14 SystemMessage(
15 content=f"你是一个乐于助人的助手，支持调用工具进行搜索。"
16 f"查询 LLM 前可参考以下信息："
17 f"1. 用戶基本情况：{info_result[0].value} "
18 f"2. 用戶偏好情况：{pref_result[0].value}"
19 )
20 ]
21 + state["messages"]
22 )
23 ],
24 "llm_calls": state.get('llm_calls', 0) + 1
25 }
• 构件图时，加入新节点与调整边
根据下图完成调整：
视图
__start__
get_person_by_llm
llm_call
__end__ tool_node
代码块
1 agent_builder = StateGraph(MessagesState)
2 agent_builder.add_node(llm_call)

3 agent_builder.add_node(tool_node)
4 # 新增节点
5 agent_builder.add_node(get_person_by_llm)
6
7 # 调整边
8 agent_builder.add_edge(START, "get_person_by_llm")
9 agent_builder.add_edge("get_person_by_llm", "llm_call")
10 agent_builder.add_conditional_edges(
11 "llm_call",
12 should_continue,
13 ["tool_node", END]
14 )
15 agent_builder.add_edge("tool_node", "get_person_by_llm")
到此，代码已经改造完成，完整代码如下：
代码块
1 import uuid
2 from typing import Optional
3
4 from langchain.chat_models import init_chat_model
5 from langchain_core.messages import HumanMessage
6 from langchain_core.runnables import RunnableConfig
7 from langchain_tavily import TavilySearch
8 from langgraph.checkpoint.memory import InMemorySaver
9 from langgraph.store.base import BaseStore
10 from langgraph.store.memory import InMemoryStore
11 from pydantic import BaseModel, Field
12
13 # 步骤 1: 定义工具和模型
14 search = TavilySearch(max_results=4)
15 tools = [search]
16 # 绑定工具
17 model = init_chat_model("gpt-4o-mini", temperature=0)
18 model_with_tools = model.bind_tools(tools)
19
20 # 步骤 2: 定义状态
21 from langchain.messages import AnyMessage
22 from typing_extensions import TypedDict, Annotated
23 import operator
24
25 class MessagesState(TypedDict):
26 # 类型: list[AnyMessage] - 任意消息对象的列表
27 # 合并策略: operator.add - 使用加法操作符进行状态合并
28 # 效果: 当状态更新时，新的消息会追加到现有列表中，而不是替换

29 messages: Annotated[list[AnyMessage], operator.add]
30 # 类型: int - 整数值
31 # 用途: 跟踪LLM（大语言模型）的调用次数
32 llm_calls: int
33
34
35 # 步骤 3：新增提取信息节点
36 # 定义结构化输出
37 class Person(BaseModel):
38 """一个人的信息。"""
39
40 # 注意:
41 # 1. 每个字段都是 Optional “可选的” —— 允许 LLM 在不知道答案时输出 None。
42 # 2. 每个字段都有一个 description “描述” —— LLM使用这个描述。
43 name: Optional[str] = Field(default=None, description="这个人的名字")
44 height_in_meters: Optional[str] = Field(default=None, description="以米为单
位的高度")
45 favourite_food: Optional[list[str]] = Field(default=None, description="最喜
欢的食物列表")
46
47 model_with_structured = model.with_structured_output(Person)
48
49 def get_person_by_llm(state: MessagesState, config: RunnableConfig, *, store:
BaseStore):
50 """通过 LLM 提取用戶信息"""
51
52 # 1. 先提取
53 people_info = model_with_structured.invoke(
54 [
55 SystemMessage(
56 content="你是一个提取信息的专家，只从文本中提取我的相关信息，不能提取别
人的信息。如果你不知道要提取的属性的值，属性值返回null。"
57 )
58 ]
59 + state["messages"][-3:] # 只查看最近3条消息
60 )
61
62 # 2. 再保存
63 user_id = config["configurable"]["user_id"]
64
65 # 保存用戶基本信息
66 namespace1 = (user_id, "info")
67 # 每次put前应判断是否存在，再更新。否则会有多条记录被记录。这里简写
68 store.put(
69 namespace1,
70 str(uuid.uuid4()),
71 {

72 "name": people_info.name,
73 "height": people_info.height_in_meters
74 }
75 )
76
77 # 保存用戶偏好
78 namespace2 = (user_id, "preferences")
79 store.put(
80 namespace2,
81 str(uuid.uuid4()),
82 {"favourite_food": people_info.favourite_food} # 省略追加逻辑：先搜再更新
83 )
84 return {
85 "llm_calls": state.get('llm_calls', 0) + 1
86 }
87
88
89
90 # 步骤 4: 更新模型调用节点：添加共享用戶信息到提示词
91 from langchain.messages import SystemMessage
92
93 def llm_call(state: MessagesState, config: RunnableConfig, *, store:
BaseStore):
94 """LLM决定是否调用工具"""
95
96 # 搜索用戶信息
97 user_id = config["configurable"]["user_id"]
98 namespace1 = (user_id, "info")
99 namespace2 = (user_id, "preferences")
100 info_result = store.search(namespace1)
101 pref_result = store.search(namespace2)
102 return {
103 "messages": [
104 model_with_tools.invoke(
105 [
106 SystemMessage(
107 content=f"你是一个乐于助人的助手，支持调用工具进行搜索。"
108 f"查询 LLM 前可参考以下信息："
109 f"1. 用戶基本情况：{info_result[0].value} "
110 f"2. 用戶偏好情况：{pref_result[0].value}"
111 )
112 ]
113 + state["messages"]
114 )
115 ],
116 "llm_calls": state.get('llm_calls', 0) + 1
117 }

118
119
120 # 步骤 5: 定义工具节点
121 from langchain.messages import ToolMessage
122
123 tools_by_name = {tool.name: tool for tool in tools}
124 def tool_node(state: dict):
125 """执行工具调用"""
126
127 result = []
128 for tool_call in state["messages"][-1].tool_calls:
129 tool = tools_by_name[tool_call["name"]]
130 observation = tool.invoke(tool_call["args"])
131 result.append(ToolMessage(content=observation,
tool_call_id=tool_call["id"]))
132 return {"messages": result}
133
134
135 # 步骤 6: 构件图
136 from langgraph.graph import StateGraph, START, END
137
138 # 定义结束逻辑
139 def should_continue(state: MessagesState):
140 """根据LLM是否调用工具来决定是应该继续循环（路由到工具节点）还是停止循环（END）"""
141
142 messages = state["messages"]
143 last_message = messages[-1]
144
145 # 如果LLM调用工具，则执行操作
146 if last_message.tool_calls:
147 return "tool_node"
148 return END
149
150 # 加入新节点并修改边
151 agent_builder = StateGraph(MessagesState)
152 agent_builder.add_node(llm_call)
153 agent_builder.add_node(tool_node)
154 agent_builder.add_node(get_person_by_llm)
155
156 agent_builder.add_edge(START, "get_person_by_llm")
157 agent_builder.add_edge("get_person_by_llm", "llm_call")
158 agent_builder.add_conditional_edges(
159 "llm_call",
160 should_continue,
161 ["tool_node", END]
162 )
163 agent_builder.add_edge("tool_node", "get_person_by_llm")

164
165 checkpointer = InMemorySaver()
166 store = InMemoryStore()
167 # 编译图
168 agent = agent_builder.compile(checkpointer=checkpointer, store=store)
• 运行与验证：同一用戶但不同会话的请求
代码块
1 # 第一次聊天
2 config1 = {"configurable": {"thread_id": "1", "user_id": "1"}}
3 result1 = agent.invoke(
4 {"messages": [HumanMessage(content="我叫李华，我最爱吃汉堡。我的朋友叫小明，他爱
吃披萨")]},
5 config1
6 )
7 print(f"\n调用 LLM 总次数：{result1["llm_calls"]}次")
8 for m in result1["messages"]:
9 m.pretty_print()
10
11 # ---------- 过了几天 ---------------
12
13 # 同一个人，再次进行对话
14 config2 = {"configurable": {"thread_id": "2", "user_id": "1"}}
15 result2 = agent.invoke(
16 {"messages": [HumanMessage(content="给我推荐下餐厅")]},
17 config2
18 )
19 print(f"\n调用 LLM 总次数：{result2["llm_calls"]}次")
20 for m in result2["messages"]:
21 m.pretty_print()
执行结果如下：
代码块
1 调用 LLM 总次数：2次
2 ================================ Human Message
=================================
3
4 我叫李华，我最爱吃汉堡。我的朋友叫小明，他爱吃披萨
5 ================================== Ai Message
==================================
6

7 你好，李华！很高兴认识你。汉堡和披萨都是很受欢迎的美食。你和小明有没有一起去过什么好吃的地
方呢？或者你们有没有想尝试的新餐厅？
8
9 调用 LLM 总次数：4次
10 ================================ Human Message
=================================
11
12 给我推荐下餐厅
13 ================================== Ai Message
==================================
14 Tool Calls:
15 tavily_search (call_btsV05aeqldqjaZNvgdlYRe9)
16 Call ID: call_btsV05aeqldqjaZNvgdlYRe9
17 Args:
18 query: 推荐汉堡餐厅
19 ================================= Tool Message
=================================
20
21 {省略.....}
22 ================================== Ai Message
==================================
23
24 以下是一些推荐的汉堡餐厅：
25
26 1. **[Burger She Wrote](https://www.novacircle.com/zh-CN/spots/north-
america/united-states/california/los-angeles-county/los-angeles/burger-she-
wrote-9ea267)** - 位于洛杉矶，这是一家小而温馨的餐厅，以其美味的和牛汉堡而闻名。
27
28 2. **[Tripadvisor 上洛杉矶的最佳汉堡](https://cn.tripadvisor.com/Restaurants-
g32655-zfd10907-zfn7231034-Los_Angeles_California-Hamburger.html)** - 包含多家受
欢迎的汉堡餐厅，如Bottega Louie和Eggslut，后者以其鸡蛋汉堡而著称。
29
30 希望这些推荐能帮助你找到美味的汉堡！
扩展：尝试修改上面的例子，让你的 AI 助手能记住用戶的更多信息（比如不喜欢的东西、上次聊到
的话题记录等），并在新的对话中聪明地利用这些信息。
3.3.1.3 语义搜索
Store 的强大之处在于它支持语义搜索，而不仅仅是精确匹配。这意味着我们可以用自然语言问题来查
找相关记忆。
首先，我们需要配置带嵌入模型的 Store，如下所示：
代码块

1 store = InMemoryStore(
2 index={
3 "embed": init_embeddings("openai:text-embedding-3-small"), # 使用OpenAI
嵌入模型
4 "dims": 1536, # 嵌入向量的维度
5 "fields": ["$"] # 对value中的所有字段进行嵌入
6 }
7 )
在节点中，可以这样搜索：
代码块
1 user_id = config["configurable"]["user_id"]
2 namespace = (user_id, )
3 # 在Store中进行语义搜索，找出最相关的2个记忆
4 # 这里直接在user_id维度下通过语义去找
5 info_result = store.search(namespace, query="用戶基本信息", limit=2)
6 pref_result = store.search(namespace, query="用戶偏好信息", limit=2)
扩展：如果我们让 AI 助手能记住用戶的更多信息（比如不喜欢的东西、上次聊到的话题记录等）。
在新的对话，语义搜索可以把历史记录中的相关记忆找出来，帮助 AI 助手进行更加准确的回复。
3.3.2 方式2：Postgres 存储库
Postgres 存储库适用于生产环境或需要状态持久化的场景。由于之前已经启动过 PostgresSQL，这里
可以直接连接到数据库，作为 使用。只需在编译时设置 即可。
PostgresStore store
修改【内存存储】部分的代码：将内存存储方式修改为 Postgres 存储库。
注意：第一次使用 Postgres store 时需要调用
store.setup()
代码块
1 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
2 with (
3 PostgresSaver.from_conn_string(DB_URI) as checkpointer,
4 PostgresStore.from_conn_string(DB_URI) as store,
5 ):
6
7 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
8 checkpointer.setup()
9 # 第一次使用 Postgres store 时需要调用 store.setup()
10 store.setup()
11

12 # 编译图
13 agent = agent_builder.compile(checkpointer=checkpointer, store=store)
14
15 # ...后续调用...
模拟第一次聊天：
代码块
1 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
2 with (
3 PostgresSaver.from_conn_string(DB_URI) as checkpointer,
4 PostgresStore.from_conn_string(DB_URI) as store,
5 ):
6
7 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
8 checkpointer.setup()
9 # 第一次使用 Postgres store 时需要调用 store.setup()
10 store.setup()
11
12 # 编译图
13 agent = agent_builder.compile(checkpointer=checkpointer, store=store)
14
15 # 第一次聊天
16 config1 = {"configurable": {"thread_id": "1", "user_id": "1"}}
17 result1 = agent.invoke(
18 {"messages": [HumanMessage(content="我叫李华，我最爱吃汉堡。我的朋友叫小明，
他爱吃披萨")]},
19 config1
20 )
21 print(f"\n调用 LLM 总次数：{result1["llm_calls"]}次")
22 for m in result1["messages"]:
23 m.pretty_print()
运行系统后可以看到，postgres 中新增 store 相关表，其中存放了用戶基本的信息：
再次验证：同一用戶但不同会话的请求
代码块

1 DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
2 with (
3 PostgresSaver.from_conn_string(DB_URI) as checkpointer,
4 PostgresStore.from_conn_string(DB_URI) as store,
5 ):
6
7 # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
8 # checkpointer.setup()
9 # 第一次使用 Postgres store 时需要调用 store.setup()
10 # store.setup()
11
12 # 编译图
13 agent = agent_builder.compile(checkpointer=checkpointer, store=store)
14
15 # ---------- 过了几天 ---------------
16
17 # 同一个人，再次进行对话
18 config2 = {"configurable": {"thread_id": "2", "user_id": "1"}}
19 result2 = agent.invoke(
20 {"messages": [HumanMessage(content="给我推荐下餐厅")]},
21 config2
22 )
23 print(f"\n调用 LLM 总次数：{result2["llm_calls"]}次")
24 for m in result2["messages"]:
25 m.pretty_print()
注意执行前，将以下代码注掉，因为：在存入store前，并没有编写 不存在存入，存在更新 的代码逻
辑（只是演示），因此会将空的用戶信息误存，导致LLM调用前查出来空的。
代码块
1 def get_person_by_llm(state: MessagesState, config: RunnableConfig, *, store:
BaseStore):
2
3 ...
4
5 # 每次put前应判断是否存在，再更新。否则会有多条记录被记录。这里简写
6 # store.put(
7 # namespace1,
8 # str(uuid.uuid4()),
9 # {
10 # "name": people_info.name,
11 # "height": people_info.height_in_meters
12 # }
13 # )
14

15 # 保存用戶偏好
16 # store.put(
17 # namespace2,
18 # str(uuid.uuid4()),
19 # {"favourite_food": people_info.favourite_food} # 省略追加逻辑：先搜再更
新
20 # )
21
22 ...
最终执行结果如下：
代码块
1 调用 LLM 总次数：3次
2 ================================ Human Message
=================================
3
4 给我推荐下餐厅
5 ================================== Ai Message
==================================
6 Tool Calls:
7 tavily_search (call_PkIzsQRuCS6KZM15g3noHgBU)
8 Call ID: call_PkIzsQRuCS6KZM15g3noHgBU
9 Args:
10 query: 推荐汉堡餐厅
11 ================================= Tool Message
=================================
12
13 {'query': '推荐汉堡餐厅', 'follow_up_questions': None, 'answer': None, 'images':
[], 'results': [{'url':
'https://www.reddit.com/r/AskNYC/comments/1470o9z/best_burger_spot_in_nyc/?
tl=zh-hans', 'title': '纽约最好吃的汉堡店是哪家？ : r/AskNYC', 'content': 'The
Thompson 的Burger Joint 和Minetta Tavern 等被推荐。汉堡餐厅推荐 ，来自1 个月前。
Smashed 和Korzo 等被推荐。纽约/布鲁克林最好的汉堡？ 以及 ...Read more', 'score':
0.7336813, 'raw_content': None}, {'url':
'https://www.cosmopolitan.com/tw/lifestyle/food-and-drink/g44382807/hamburger-
20230629/', 'title': '美國旅遊必吃7大人氣漢堡店！IN-N-OUT最強勁敵', 'content':
'1.The Habit Burger Grill · 2.Cheeseburger in Paradise · 3.Five Guys · 4.IN-N-
OUT · 5.Shake Shack · 6.SmashburgerRead more', 'score': 0.61972505,
'raw_content': None}, {'url': 'https://cn.tripadvisor.com/Restaurants-g60763-
zfd10907-zfn7102345-New_York_City_New_York-Hamburger.html', 'title': '纽约市最佳
汉堡', 'content': "Ellen's Stardust Diner · (23,569 条点评). 美式烹饪, 晚餐 ;
Virgil's Real BBQ - NYC · (4,968 条点评). 美式烹饪, 烧烤 ; 1. S'MAC · (488 条点
评). 快餐小吃, 美式烹饪 ; 2.Read more", 'score': 0.56719416, 'raw_content':
None}, {'url':

'https://mliesl.edu/contents/ch/%E7%BE%8E%E5%9B%BD%E6%9C%80%E4%BD%B3%E6%B1%89%E
5%A0%A1%E8%BF%9E%E9%94%81%E6%8E%92%E5%90%8D/', 'title': '美国最佳汉堡连锁排名',
'content': '最受好评的汉堡连锁店之一– Five Guys – 被康涅狄格州、乔治亚州、蒙大拿州、内
布拉斯加州、俄勒冈州、南卡罗来纳州、佛蒙特州和西弗吉尼亚州评为第一名。 那是8 个州同意，
...Read more', 'score': 0.56690645, 'raw_content': None}], 'response_time':
0.92, 'request_id': '0ee8ee23-bbd3-48e2-b4c2-ca6d1c1dfe7a'}
14 ================================== Ai Message
==================================
15
16 以下是一些推荐的汉堡餐厅：
17
18 1. **[纽约最好吃的汉堡店]
(https://www.reddit.com/r/AskNYC/comments/1470o9z/best_burger_spot_in_nyc/?
tl=zh-hans)** - 推荐的汉堡店包括 The Thompson 的 Burger Joint 和 Minetta Tavern
等。
19
20 2. **[美国旅游必吃7大人氣漢堡店](https://www.cosmopolitan.com/tw/lifestyle/food-
and-drink/g44382807/hamburger-20230629/)** - 包括 The Habit Burger Grill、
Cheeseburger in Paradise、Five Guys、IN-N-OUT、Shake Shack 和 Smashburger。
21
22 3. **[纽约市最佳汉堡](https://cn.tripadvisor.com/Restaurants-g60763-zfd10907-
zfn7102345-New_York_City_New_York-Hamburger.html)** - 推荐的餐厅有 Ellen's
Stardust Diner 和 Virgil's Real BBQ - NYC。
23
24 4. **[美国最佳汉堡连锁排名]
(https://mliesl.edu/contents/ch/%E7%BE%8E%E5%9B%BD%E6%9C%80%E4%BD%B3%E6%B1%89%E
5%A0%A1%E8%BF%9E%E9%94%81%E6%8E%92%E5%90%8D/)** - Five Guys 是最受好评的汉堡连锁店
之一。
25
26 希望这些推荐能帮助到您！如果您有特定的城市或地区需求，请告诉我。
4. 持久化实现的三大应用能力
4.1 记忆（Memory）
4.1.1 记忆概念
记忆，是一种能够记住之前互动信息的系统。对于人工智能代理来说，记忆至关重要，因为它使他们
能够记住之前的互动，从反馈中学习，并根据用戶偏好进行调整。随着代理处理涉及大量用戶交互的
更复杂任务，这一能力对效率和用戶满意度都变得至关重要。
注意要区分记忆和持久化的概念：
• 持久化为 LangGraph 底层能力，包含【线程级】持久化和【跨会话】持久化

• 记忆为 LangGraph 能实现的应用层能力，包含【短期记忆】和【长期记忆】
在应用层，短期记忆就由线程级持久化实现，长期记忆由跨会话持久化实现。
• 短期记忆：单次会话中保持的上下文信息
• 长期记忆：跨会话保存的用戶或应用数据
4.1.2 管理短期记忆
对应短期记忆和长期记忆是如何添加的就不过多演示了（就是持久化部分的内容）。但在应用层，我
们还需要掌握在应用系统中，出现一些具体场景时，如何对记忆进行管理。例如当消息记录过多，我
们需要进行消息裁剪、总结消息、消息删除等操作。
要再说明一点，既然是应用层能力，我们应该对记忆的存储方式有所选择。如下所示：
代码块
1 # 开发阶段：内存存储
2 from langgraph.checkpoint.memory import InMemorySaver
3 from langgraph.store.memory import InMemoryStore
4
5 # 生产阶段：数据库
6 from langgraph.checkpoint.postgres import PostgresSaver
7 from langgraph.store.postgres import PostgresStore
4.1.2.1 修剪消息
大多数 LLM 都有一个最大支持的上下文窗口。决定何时截断消息的一种方法是对消息历史记录中的令
牌进行计数，并在接近该限制时截断。
消息裁剪方法可以参考 LangChain 篇章部分的内容。

代码块
1 from langchain_core.messages.utils import trim_messages
2 from langchain.chat_models import init_chat_model
3 from langgraph.checkpoint.memory import InMemorySaver
4 from langgraph.graph import StateGraph, START, MessagesState
5
6 model = init_chat_model("gpt-4o-mini", temperature=0)
7
8 def call_model(state: MessagesState):
9 # 只保留最近的128个token的消息
10 messages = trim_messages(
11 state["messages"],
12 strategy="last", # 策略：保留最后的部分
13 token_counter=model, # 计算token数量
14 max_tokens=128, # 最大token数
15 start_on="human", # 从用戶消息开始
16 end_on=("human", "tool"), # 结束于用戶或工具消息
17 )
18 response = model.invoke(messages)
19 return {"messages": [response]}
20
21 checkpointer = InMemorySaver()
22 builder = StateGraph(MessagesState)
23 builder.add_node(call_model)
24 builder.add_edge(START, "call_model")
25 graph = builder.compile(checkpointer=checkpointer)
26
27 config = {"configurable": {"thread_id": "1"}}
28 graph.invoke({"messages": "hi, my name is bob"}, config)
29 graph.invoke({"messages": "write a short poem about cats"}, config)
30 graph.invoke({"messages": "now do the same but for dogs"}, config)
31 final_response = graph.invoke({"messages": "what's my name?"}, config)
32
33 final_response["messages"][-1].pretty_print()
4.1.2.2 删除消息
可以从图状态中删除消息以管理消息历史记录。当想要删除特定消息或清除整个消息历史记录时，这
非常有用。
代码块
1 def call_model(state: MessagesState):
2 messages = state["messages"]

3 if len(messages) > 6:
4 # 删除最早的6条消息
5 return {
6 "messages": [RemoveMessage(id=m.id) for m in messages[:6]]
7 }
8
9 response = model.invoke(messages)
10 return {"messages": [response]}
11
12 # ....
13
14 # 测试：可以发现只剩最后一条消息了
15 for message in final_response["messages"]:
16 message.pretty_print()
删除所有消息：
代码块
1 from langgraph.graph.message import REMOVE_ALL_MESSAGES
2
3 def call_model(state: MessagesState):
4 return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}
注意：删除后消息无法恢复，要确保删除后的对话仍然是有效的。
4.1.2.3 总结消息
实际上，修剪或删除消息也会存在问题：可能会因剔除消息而丢失信息。因此，某些应用更希望将消
息历史记录进行总结，把旧的对话内容总结成简短摘要，保留关键信息，以代替冗长的历史记录。
我们可以先将 State 进行扩展，除了对话记录，还包含一个总结摘要字段：

1 from langgraph.graph import MessagesState
2
3 class State(MessagesState):
4 summary: str
现在要求：
• 对话记录：记录新的对话与结果
• 摘要：每次对话完成，需要进行总结。
• 完成总结摘要后，可以删除历史对话。
那么，在每次调用 LLM 时，便可以根据【新的请求】与【总结摘要信息】共同构建提示词来完成请
求。
完整代码如下所示：
代码块
1 from langchain.chat_models import init_chat_model
2 from langchain_core.messages import HumanMessage, RemoveMessage
3 from langgraph.checkpoint.memory import InMemorySaver
4 from langgraph.graph import StateGraph, START, MessagesState
5
6 model = init_chat_model("gpt-4o-mini", temperature=0)
7
8 class State(MessagesState):
9 summary: str
10
11 def call_model(state: State):
12 # 使用历史总结+最新消息发起调用
13 summary = state.get("summary", "")
14 messages = model.invoke([HumanMessage(content=summary)] +
state["messages"])
15 return {"messages": messages}
16
17
18 def summarize_conversation(state: State):
19 """ 生成历史总结 """
20
21 # 1. 创建总结提示词
22 summary = state.get("summary", "")
23 if summary: # 有摘要，扩展
24 summary_message = (
25 f"这是到目前为止的对话摘要：{summary}\n\n"
26 "基于上面的新消息扩展摘要："
27 )
28 else: # 无摘要，新增

29 summary_message = "创建上面对话的摘要："
30
31 # 2. 生成新总结：【消息列表】+【历史总结】调用模型
32 messages = state["messages"] + [HumanMessage(content=summary_message)]
33 response = model.invoke(messages)
34
35 # 3. 删除历史对话：除了最新的AI消息,都可以删除
36 return {
37 "summary": response.content, # 历史总结
38 "messages": [RemoveMessage(id=m.id) for m in state["messages"][:-1]] #
保留最后的消息是为了打印结果
39 }
40
41 checkpointer = InMemorySaver()
42 builder = StateGraph(State)
43 builder.add_node(call_model)
44 builder.add_node("summarize", summarize_conversation)
45
46 builder.add_edge(START, "call_model")
47 builder.add_edge("call_model", "summarize") # 每次对话完，进行总结
48 graph = builder.compile(checkpointer=checkpointer)
49
50 config = {"configurable": {"thread_id": "1"}}
51 graph.invoke({"messages": "hi, my name is bob"}, config)
52 graph.invoke({"messages": "write a short poem about cats"}, config)
53 graph.invoke({"messages": "now do the same but for dogs"}, config)
54 final_response = graph.invoke({"messages": "what's my name?"}, config)
55
56 final_response["messages"][-1].pretty_print()
57 print("\nSummary:", final_response["summary"])
58
59 # 打印结果如下：
60 # ================================== Ai Message
==================================
61
62 # Your name is Bob.
63
64 # Summary: 对话摘要：用戶自我介绍为Bob，并询问如何获得帮助。随后，用戶请求写一首关于猫的
短诗。接着，用戶又请求写一首关于狗的短诗。用戶对动物的诗歌表现出兴趣，可能希望进一步探讨与
宠物相关的主题或创作。
实际上，无需每次调用后都进行总结，可设置阈值进行总结。只需判断 消息数量 阈值 ，再进行总
>
结与删除即可。
扩展：LangMem 是一个由 LangChain 维护的库。它提供了可与任何存储系统一起使用的功能原
语，也提供了与 LangGraph 存储层的本机集成。例如上述我们手动完成的汇总消息功能，在

LangMem中专门提供了记忆管理库（如：SummarizationNode），简化了总结消息的过程。有兴
趣的同学可以自行了解。
4.2 人机交互（Human-in-the-loop）
什么是人机交互？想象有以下场景：
• AI 自动发送邮件前，你想亲自最后确认一遍内容
• AI 生成文章后，你想亲自手动修改几个段落
• ...
在 AI 系统中，我们希望可以在 AI 自动流程中插入一个“暂停键”，等待人类输入后再继续，这就是人
机交互功能。
4.2.1 核心概念：中断（Interrupts）
想要完成 人机交互 能力，需要用到 LangGraph 基于持久化实现的【中断】能力！中断就像打游戏一
样，当玩家无法通关某关卡时，希望暂停游戏（中断），攻略一下后再继续游戏：

• 用戶可以在游戏过程中主动按下“存档键”；
• 此时会将游戏当前状态等信息进行存档，保存下来；（实现游戏过程的中断）
• 当我们攻略后想继续游戏时，就可以读取存档继续玩。（恢复游戏继续）
在 LangGraph 中，中断允许工作流执行时在特定点暂停，等待外部输入后再继续执行。
4.2.2 中断如何实现？
在工作流中，想要实现暂停与恢复很简单，只需要：
• 通过调用 方法中断执行流程，依靠持久化能力，保存当前状态。
interrupt()
• 外部用戶通过发送 对象，使得工作流恢复执行流程。
Command
交互流程如下图所示：

视图
LangGraph系统 外部/人类
运行节点
执行 interrupt()
暂停并保存状态
状态快照已保存
__interrupt__返回
控制权移交
人类决策/审批
系统处理/输入
Command(resume="结果")
收到外部指令
恢复保存的状态
继续执行节点
LangGraph系统 外部/人类

直接看代码：
代码块
1 from typing import TypedDict
2
3 from langgraph.checkpoint.memory import InMemorySaver
4 from langgraph.constants import START
5 from langgraph.graph import StateGraph
6 from langgraph.types import interrupt, Command
7
8 class State(TypedDict):
9 input: str
10 output: str
11
12 def hello_node(state: State):
13 # 主动喊“停！”，并传递提示信息
14 human = interrupt("暂停，是否继续？") # 第一次运行会停在这里
15 if human == "yes":
16 return {"output": "你好，我是你的贴心助手！"}
17 else:
18 return {"output": "拜拜"}
19
20 builder = StateGraph(State)
21 builder.add_node(hello_node)
22 builder.add_edge(START, "hello_node")
23 # 必须指定checkpointer，以在每个步骤后保存图状态。
24 graph = builder.compile(checkpointer=InMemorySaver())
25
26 # 必须使用thread_id运行 Graph，相当于告诉系统读哪个存档。
27 config = {"configurable": {"thread_id": "human_1"}}
28
29 # 步骤1：启动，触发暂停
30 first = graph.invoke({"input": "hi"}, config=config)
31 print(first) # 看到提问:__interrupt__
32
33 # 步骤2：恢复，把答案交回去
34 second = graph.invoke(Command(resume="no"), config=config)
35 print(second["output"])
代码关键点：
• 编译图时：必须指定 ，以在每个步骤后保存图状态。
checkpointer
• 调用 时：表示主动喊“停！”，并传递提示信息。
interrupt()
• 使用 恢复执行，需使用 语法。
invoke/stream Command(resume=...)

◦ 表示传回 AI 的响应值
resume
◦ 必须使用 运行 Graph，相当于告诉系统读哪个存档。
thread_id
因此实现了中断，便是实现了人机交互模式。
4.2.3 中断的黄金法则（规则和限制）
4.2.3.1 只传能序列化的简单数据
复杂值无法进行传递，例如不要传函数、类实例、数据库连接等。只传能序列化的简单数据，如字符
串、数字、布尔、简单字典/列表。
正面示例✔：
代码块  代码块
1 def node_a(state: State): 1 def node_a(state: State):
2 # ✅ 正确：传递可序列化的简单类 2 # ✅ 正确：传递带有简单值的字典
型 3 response = interrupt({
3 name = interrupt("What's 4 "question": "Enter user
your name?") details",
4 count = interrupt(42) 5 "fields": ["name",
5 approved = interrupt(True) "email", "age"],
6 6 "current_values":
7 return {"name": name, state.get("user", {})
"count": count, "approved": 7 })
approved} 8
9 return {"user": response}
反面示例❌：
代码块  代码块
1 def validate_input(value): 1 class DataProcessor:
2 return len(value) > 0 2 def __init__(self, config):
3 3 self.config = config
4 def node_a(state: State): 4
5 # ❌错误：传递一个函数来实现中断 5 def node_a(state: State):
6 # 函数不能被序列化 6 processor =
7 response = interrupt({ DataProcessor({"mode": "strict"})
8 "question": "What's your 7
name?", 8 # ❌ 错误：传递一个类实例来实现
9 "validator": 中断
validate_input 9 # 实例不能被序列化
10 }) 10 response = interrupt({
11 return {"name": response}

11 "question": "Enter data
to process",
12 "processor": processor
# This will fail
13 })
14 return {"result": response}
4.2.3.2 不应该将   调用包裹在   代码块中
interrupt() try/except
错误做法是：如果将   调用包裹在通用的   或
interrupt() try/except Exception
（空）代码块中，你编写的代码会提前捕获这个特殊异常。这会导致运行时系统无法
try/except
感知到中断，从而使   功能失效。
interrupt()
反面示例❌：
代码块
1 def node_a(state: State):
2 # ❌ 错误：在try/except中包装中断
3 try:
4 interrupt("What's your name?")
5 except Exception as e:
6 print(e)
7 return state
根本原因是  函数内部通过抛出一个特殊的异常来实现暂停执行。这个异常需要被
interrupt()
LangGraph 的运行时系统捕获，以触发状态的保存和等待。
正确做法：
• 分离逻辑：将   调用与可能引发其他异常的代码分开。先调用  ，
interrupt() interrupt()
然后再处理可能出错的操作。
• 精确捕获：在   块中只捕获你预期会发生的、非常具体的异常类型（例如
try/except
）。这样，  抛出的特殊异常就不会被你的代码捕获，而
NetworkException interrupt()
能顺利传递给运行时系统。
正面示例✔：
代码块  代码块
1 def node_a(state: State): 1 def node_a(state: State):
2 # ✅ 正确：先中断，再处理 2 # ✅ 正确：捕捉特定的异常类型
3 interrupt("What's your 3 try:
name?")

4 try: 4 name = interrupt("What's
5 # 将中断调用与易出错代码分开 your name?")
6 fetch_data() 5 fetch_data()
7 except Exception as e: 6 except NetworkException as e:
8 print(e) 7 print(e)
9 return state 8 return state
这部分是一个重要的警告，旨在避免开发者因使用常规的错误处理模式而导致   机制
interrupt()
失效。其核心是必须让   抛出的特殊异常能够“逃逸”出你编写的节点函数，以便被
interrupt()
LangGraph 运行时正确处理。
4.2.3.3 中断前的动作要“幂等”
非常重要的是：当节点恢复执行时，发起中断的节点会从头再跑一遍。因此，对于中断前的代码，会
多重复执行！
如果这些代码包含非幂等的副作用操作（如创建记录、发送消息、扣款等），每次恢复都会重复这些
操作。这可能导致数据重复、不一致或意外行为。
幂等性：一个操作无论执行一次还是多次，产生的效果都相同。
正面示例✔：
代码块  代码块

1 # 使用幂等操作 1 # 将副作用放在中断之后
2 def node_a(state: State): 2 def node_a(state: State):
3 # ✅ 正确：使用 upsert（更新或 3 # ✅ 正确：先中断，获得批准后再
插入）操作，多次执行结果一致 执行副作用
4 db.upsert_user( 4 approved =
5 user_id=state["user_id"], interrupt("Approve this change?")
6 status="pending_approval" 5 if approved:
7 ) 6 db.create_audit_log(
8 7
9 approved = user_id=state["user_id"],
interrupt("Approve this change?") 8 action="approved"
10 9 )
11 return {"approved": approved} 10 return {"approved": approved}
代码块
1 # 将副作用分离到独立节点
2 def approval_node(state: State):
3 # 只处理中断
4 approved = interrupt("Approve this change?")
5 return {"approved": approved}
6
7 def notification_node(state: State):
8 # ✅ 正确：副作用在独立节点中，仅在获得批准后执行一次
9 if state["approved"]:
10 send_notification(user_id=state["user_id"], status="approved")
11 return state
反面示例❌：
代码块  代码块
1 # 在中断前创建新记录 1 # 在中断前追加到列表
2 def node_a(state: State): 2 def node_a(state: State):
3 # ❌ 错误：每次恢复都会创建新的 3 # ❌ 错误：每次恢复都会重复追加
审计记录 相同条目
4 audit_id = 4 db.append_to_history(
db.create_audit_log({ 5 state["user_id"],
5 "user_id": 6 "approval_requested"
state["user_id"], 7 )
6 "action": 8 approved =
"pending_approval", interrupt("Approve this change?")
7 "timestamp": 9 return {"approved": approved}
datetime.now()
8 })
9

10 approved =
interrupt("Approve this change?")
11 return {"approved":
approved, "audit_id": audit_id}
这一规则的核心是：确保在   调用之前执行的所有操作都是幂等的，或者将非幂等操
interrupt()
作移到   调用之后。这是为了避免因节点重新执行而导致的重复副作用，确保系统的
interrupt()
数据一致性和预期行为。
4.2.3.4 中断顺序固定
在同一个节点中使用多个   调用时需要注意的顺序和索引匹配规则。LangGraph 使用
interrupt()
严格的索引顺序来匹配恢复值：
• 恢复执行从头开始：节点恢复时会从开头重新运行，而不是从中断的精确行继续。
• 索引匹配：LangGraph 为每个执行任务维护一个恢复值列表。遇到   时，按顺序
interrupt()
从这个列表中取对应的值。
• 顺序必须一致：中断调用的顺序在每次执行中必须完全相同。
正面示例✔：
代码块
1 def node_a(state: State):
2 # ✅ 正确：中断调用顺序固定
3 name = interrupt("What's your name?") # 索引0
4 age = interrupt("What's your age?") # 索引1
5 city = interrupt("What's your city?") # 索引2
6
7 return {"name": name, "age": age, "city": city}
反面示例❌：
代码块  代码块
1 # 条件性跳过中断 1 # 基于非确定性数据的循环中断
2 def node_a(state: State): 2 def node_a(state: State):
3 name = interrupt("What's 3 # ❌ 错误：中断数量随动态列表变
your name?") # 索引0 化
4 4 results = []
5 # ❌ 错误：第一次可能跳过，恢复 5 for item in
时可能不跳过，导致索引错乱 state.get("dynamic_list", []):
6 if state.get("needs_age"): # 列表可能在不同执行中变化

7 age = interrupt("What's 6 result =
your age?") # 索引1（有时存在） interrupt(f"Approve {item}?") #
8 中断数量不确定
9 city = interrupt("What's 7 results.append(result)
your city?") # 索引1或2（不确
定）
4.2.4 人机交互的应用场景
使用中断来实现需要人工介入的交互式工作流有四种常见模式：
1. 审批或拒绝：在执行关键操作（如 API 调用、数据库更改）之前暂停流程，等待人工批准或拒
绝。根据返回的指令，流程图会路由到不同的分支。
2. 审查和编辑状态：暂停流程，让人工可以审查并修改流程图当前的状态（例如，LLM 生成的文本
内容），然后将编辑后的内容传回，更新状态并继续执行。
3. 在工具中中断：将中断直接置于工具函数内部。当 LLM 调用该工具时，流程会自动暂停，允许人
工在工具实际执行前审查、编辑其调用参数或直接取消调用。
4. 验证人工输入：通过循环使用中断，反复要求人工输入，直到输入内容通过验证（例如，确保输
入一个有效的正数年龄）。这适用于需要收集和验证数据的场景。
这部分的核心思想是：中断功能解锁了“暂停执行并等待外部输入”的能力，从而使得构建 人机交互
（human-in-the-loop） 的应用成为可能。每个模式都附带了简明的代码示例，展示了如何在中途暂
停、如何将信息传递给外部系统，以及如何在获得响应后恢复执行。
4.2.4.1 批准或拒绝（Approve or reject）
这是中断功能最常见的一种用途。在执行关键性操作（例如调用 API、修改数据库、进行金融交易等）
之前，暂停图（graph）的执行，等待人工（如管理员、用戶）的批准或拒绝。

视图
__start__
批准此操作？
interrupt
人工拒绝 人工批准
拒绝后操作 批准后操作
__end__
实现方式：
• 在节点中使用   函数暂停执行。传入一个包含审批问题、操作详情等信息的JSON
interrupt()
可序列化对象，该对象会显示在调用结果   中。
result["interrupt"]
• 当图被暂停后，外部系统（如 UI 界面）可以根据   中的信息向用戶展示审批请求。
interrupt
• 人工做出决定（批准或拒绝）后，通过再次调用图并传入   来恢复执
Command(resume=...)
行。
• 恢复时，传入   表示批准，传入   表示
Command(resume=True) Command(resume=False)
拒绝。
• 节点代码会接收这个   值作为   函数的返回值，然后根据该值，使用
resume interrupt()
 将流程路由到不同的后续节点（例如“proceed”节点或“cancel”节
Command(goto=...)
点）。
• 表示要导航到的下一个节点的名称
Command(goto=...)
【练习】AI 转账前进行人工审批
代码块
1 from typing import Literal, Optional, TypedDict
2
3 from langgraph.checkpoint.memory import MemorySaver
4 from langgraph.graph import StateGraph, START, END
5 from langgraph.types import Command, interrupt

6
7
8 class ApprovalState(TypedDict):
9 action_details: str # 操作详情（如"转账30000元"）
10 status: Optional[Literal["等待", "批准", "拒绝"]] # 审批状态
11
12
13 def approval_node(state: ApprovalState) -> Command[Literal["proceed",
"cancel"]]:
14 # 中断执行，将审批请求传递给调用者
15 decision = interrupt({
16 "question": "批准此操作？",
17 "details": state["action_details"],
18 })
19
20 # 恢复后路由到适当的节点
21 return Command(goto="proceed" if decision else "cancel")
22
23
24 def proceed_node(state: ApprovalState):
25 return {"status": "批准"}
26
27
28 def cancel_node(state: ApprovalState):
29 return {"status": "拒绝"}
30
31
32 # 构建图
33 builder = StateGraph(ApprovalState)
34 builder.add_node("approval", approval_node)
35 builder.add_node("proceed", proceed_node)
36 builder.add_node("cancel", cancel_node)
37 builder.add_edge(START, "approval")
38 builder.add_edge("proceed", END)
39 builder.add_edge("cancel", END)
40
41 graph = builder.compile(checkpointer=MemorySaver())
42
43 # 运行图（首次调用会触发中断）
44 config = {"configurable": {"thread_id": "123"}}
45 initial = graph.invoke(
46 {"action_details": "转账30000元", "status": "等待"},
47 config=config,
48 )
49 print(initial["__interrupt__"]) # -> [Interrupt(value={'question': ...,
'details': ...})]
50

51 # 用决策恢复执行：True路由到proceed，False路由到cancel
52 resumed = graph.invoke(Command(resume=True), config=config)
53 print(resumed["status"]) # -> "批准"
4.2.4.2 查看和编辑状态（Review and edit state）
该场景表示在流程执行过程，使用中断功能让人进行审查和编辑状态内容。
视图
初始状态 中断触发 更新状态
传入编辑内容
UI展示内容 人工编辑
恢复流程
【练习】人工审核 AI 文档内容，并进行编辑
示例如下：
代码块
1 from typing import TypedDict
2
3 from langgraph.checkpoint.memory import InMemorySaver
4 from langgraph.graph import StateGraph, START, END
5 from langgraph.types import Command, interrupt
6
7
8 class ReviewState(TypedDict):
9 generated_text: str
10
11
12 def review_node(state: ReviewState):
13 # 请求审阅者编辑生成的内容
14 updated = interrupt({
15 "instruction": "查看并编辑此内容",
16 "content": state["generated_text"],
17 })
18 return {"generated_text": updated}

19
20
21 # 构建图
22 builder = StateGraph(ReviewState)
23 builder.add_node("review", review_node)
24 builder.add_edge(START, "review")
25 builder.add_edge("review", END)
26
27 graph = builder.compile(checkpointer=InMemorySaver())
28
29 config = {"configurable": {"thread_id": "42"}}
30 initial = graph.invoke({"generated_text": "初稿"}, config=config)
31 print(initial["__interrupt__"]) # -> [Interrupt(value={'instruction': ...,
'content': ...})]
32
33 # 用审阅者编辑后的文本恢复执行
34 final_state = graph.invoke(
35 Command(resume="审稿后的改进稿"),
36 config=config,
37 )
38 print(final_state["generated_text"]) # -> "审稿后的改进稿"
除此之外，还允许：
• 人工审查和修改LLM生成的内容（如文本、数据）
代码块
1 # 生成营销文案后让营销专家审核
2 interrupt({
3 "instruction": "为社交媒体优化营销文案",
4 "content": "...", # 待审核文案
5 "platform": "douyin"
6 })
• 在继续执行前纠正错误、添加信息或进行微调
代码块
1 # 提取结构化数据后让专家验证
2 interrupt({
3 "instruction": "验证和纠正提取的产品规格",
4 "content": "...", # 提取的规格
5 "required_fields": ["尺寸", "重量", "材料"]
6 })

• 适用于需要质量控制或专业审核的自动化流程
代码块
1 # 生成代码后让开发人员审查
2 interrupt({
3 "instruction": "查看生成的Python函数的效率和最佳实践",
4 "content": "...", # 待审核代码
5 "language": "Python"
6 })
注意恢复时传入的内容会完全替换原始内容。如果需要部分编辑，可以在中断载荷中标记可编辑部
分。
4.2.4.3 在工具中中断（Interrupts in tools）
还支持将中断功能直接嵌入到工具（tool）函数内部，从而实现在工具调用前进行人工审查和干预的能
力。

视图
初始状态
调用模型
需要调用工具
工具执行前
先执行中断
人工决定执行工具
人工决定不执行工具 执行工具
更新状态
关键特点如下：
• 中断逻辑内置于工具，而非图的节点中。
• 工具变得“智能”，知道何时需要人工批准。
• 工具可以在任何图中使用，自动具备中断能力
【练习】AI 发送邮件前，人工审查邮件内容
代码如下：
代码块
1 import operator
2 from typing import TypedDict, Annotated
3
4 from langchain.chat_models import init_chat_model
5 from langchain.tools import tool

6 from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage,
HumanMessage
7 from langgraph.checkpoint.memory import InMemorySaver
8 from langgraph.constants import START, END
9 from langgraph.graph import StateGraph
10 from langgraph.types import interrupt, Command
11
12
13 class MessagesState(TypedDict):
14 messages: Annotated[list[AnyMessage], operator.add]
15
16
17 @tool
18 def send_email(to: str, subject: str, body: str):
19 """发送电子邮件给收件人"""
20
21 # 在发送前暂停
22 response = interrupt({
23 "action": "发送邮件",
24 "to": to,
25 "subject": subject,
26 "body": body,
27 "message": "同意发送这封邮件吗？",
28 })
29
30 if response.get("action") == "同意":
31 final_to = response.get("to", to)
32 final_subject = response.get("subject", subject)
33 final_body = response.get("body", body)
34 # 实际发送邮件（此处为示例，仅打印）
35 email_info = f"收件人：{final_to} 主题：{final_subject} 正文：
{final_body}"
36 print(f"[发送邮件] {email_info}")
37 return email_info
38
39 return "用戶取消邮件"
40
41
42 # 使用绑定工具的模型
43 model_with_tools = init_chat_model("gpt-4o-mini",
temperature=0).bind_tools([send_email])
44 def llm_call(state: dict):
45 """LLM决定是否调用工具"""
46
47 messages = model_with_tools.invoke(
48 [SystemMessage(content="你支持调用工具进行邮件发送。")]
49 + state["messages"]

50 )
51
52 # 直接调用工具（为了演示效果）
53 if messages.tool_calls:
54 tool_call = messages.tool_calls[0]
55 tool_result = send_email.invoke(tool_call["args"])
56 return {"messages": [ToolMessage(content=tool_result,
tool_call_id=tool_call["id"])]}
57
58 return {"messages": [messages]}
59
60
61 builder = StateGraph(MessagesState)
62 builder.add_node("llm_call", llm_call)
63 builder.add_edge(START, "llm_call")
64 builder.add_edge("llm_call", END)
65
66 graph = builder.compile(checkpointer=InMemorySaver())
67
68
69 config = {"configurable": {"thread_id": "email-workflow"}}
70 initial = graph.invoke(
71 {"messages": [HumanMessage(content="发送电子邮件至alice@example.com，主题是：
请假，内容是：理由如下...")]},
72 config=config
73 )
74 print(initial["__interrupt__"]) # -> [Interrupt(value={'action': '...', ...})]
75
76 # 用批准和可选编辑的参数恢复
77 resumed = graph.invoke(
78 # Command(resume={"action": "同意", "subject": "病假"}),
79 Command(resume={"action": "不同意"}),
80 config=config,
81 )
82 print(resumed["messages"][-1]) # -> 工具调用结果
4.2.4.4 验证人工输入（Validating human input）
该场景使用中断功能在循环中验证人类输入，直到输入有效为止。

视图
用戶输入
开始 中断 验证输入 有效 更新状态 结束
无效，错误反馈
【练习】用戶注册流程中的年龄验证
代码块
1 from typing import TypedDict
2
3 from langgraph.checkpoint.memory import InMemorySaver
4 from langgraph.graph import StateGraph, START, END
5 from langgraph.types import Command, interrupt
6
7 class FormState(TypedDict):
8 age: int | None
9
10 def get_age_node(state: FormState):
11 prompt = "你多大了？"
12
13 while True:
14 answer = interrupt(prompt) # 有效载荷出现在 result["__interrupt__"] 中
15
16 if isinstance(answer, int) and answer > 0:
17 return {"age": answer}
18 # 每次验证失败后，提示信息会更新
19 prompt = f"'{answer}' 不是一个有效的年龄。请输入正数。"
20
21 # 构建图
22 builder = StateGraph(FormState)
23 builder.add_node(get_age_node)
24 builder.add_edge(START, "get_age_node")
25 builder.add_edge("get_age_node", END)
26 graph = builder.compile(checkpointer=InMemorySaver())
27
28 config = {"configurable": {"thread_id": "form-1"}}
29 # 首次调用：显示初始提示
30 first = graph.invoke({"age": None}, config=config)

31 print(first["__interrupt__"]) # -> [Interrupt(value='你多大了？', ...)]
32
33 # 提供无效数据：节点重新提示
34 retry = graph.invoke(Command(resume="三十"), config=config)
35 print(retry["__interrupt__"]) # -> [Interrupt(value="'三十' 不是一个有效的年
龄...", ...)]
36
37 # 提供有效数据：循环退出，状态更新
38 final = graph.invoke(Command(resume=30), config=config)
39 print(final["age"]) # -> 30
4.3 时间旅行（Time Travel）
4.3.1 时间旅行是什么？
AI 工作流具有非确定性：大语言模型每次运行可能产生不同结果。且复杂任务需要多个 AI 调用协同完
成时，错误可能出现在任何步骤，难以定位。
LangGraph 的工作方式：每个节点执行后都会自动“存档”。时间旅行允许用戶重放先前的执行以查
看或调试特定的步骤。
视图
开始 可读取/更新、可恢复执行
节点1（检查点） 可读取/更新、可恢复执行
节点2（检查点）
结束
这个能力会很有用：

1. 分析推理过程：理解 AI 如何得出最终结果，学习成功的决策路径。（看看AI是怎么“想”出好答案
的）
2. 定位和修复错误：精确找到错误发生的节点，测试修复方案而不影响原始流程。（找出AI在哪一
步“想歪了”）
3. 探索替代方案：尝试不同的输入或中间状态，比较不同路径的效果。（试试不同的选择会不会更
好）
4.3.2 时间旅行四步法
4.3.2.1 第一步：初始执行工作流
伪代码：
代码块
1 # 编译需要checkpointer
2 graph = workflow.compile(checkpointer=InMemorySaver())
3
4 # 创建执行线程
5 import uuid
6 config = {
7 "configurable": {
8 "thread_id": uuid.uuid4(), # 唯一线程标识
9 }
10 }
11
12 # 执行工作流
13 state = graph.invoke({}, config)
4.3.2.2 第二步：查看历史检查点
伪代码：
代码块
1 # 获取所有历史状态（按时间倒序）
2 states = list(graph.get_state_history(config))
3
4 for state in states:
5 print(f"检查点ID: {state.config['configurable']['checkpoint_id']}")
6 print(f"下一步节点: {state.next}")
7 print(f"当前状态: {state.values}")
8 print("-" * 50)
9
10 # 输出示例：

11 # 检查点ID: 1f0d4d2b-bdc2-6f06-8002-9b67bb1d3867
12 # 下一步节点: ()
13 # 当前状态: {'...': '...'}
14
15 # 检查点ID: 1f0d4d2b-9506-6bf8-8001-6af0cdc2fea0
16 # 下一步节点: ('write_joke',)
17 # 当前状态: {'...': '...'}
18
19 # 检查点ID: 1f0d4d2b-7a6e-6dd7-8000-5cc1931477df
20 # 下一步节点: ('generate_topic',)
21 # 当前状态: {}
22
23 # 检查点ID: 1f0d4d2b-7a6c-643e-bfff-77054fa568c8
24 # 下一步节点: ('__start__',)
25 # 当前状态: {}
4.3.2.3 第三步：修改状态（可选）
•  更新状态（会创建新的检查点分支）
update_state
• 原始检查点保持不变
• 新分支可以独立发展
伪代码：
代码块
1 # 选择特定检查点
2 selected_state = states[1] # 写笑话之前的检查点
3
4 # 修改状态数据
5 new_config = graph.update_state(
6 selected_state.config, # 原始配置
7 values={"topic": "程序员"} # 修改主题
8 )
4.3.2.4 第四步：从检查点恢复执行
• 输入为  ，因为状态已在检查点中
None
• 配置必须包含有效的  ：通过指定   和   来调
checkpoint_id thread_id checkpoint_id
用图，可以从历史某个检查点开始重放执行，用于调试或探索不同路径。
• 执行从指定检查点继续，生成新的历史分支
伪代码：

1 # 从修改后的检查点继续执行
2 result = graph.invoke(None, new_config) # 输入为None，因为状态已存在
3 print(result["joke"]) # 输出关于程序员的新笑话
4.3.3 【完整示例】AI 笑话生成器
我们要创建一个生成笑话的系统：
1. 第一步：想一个主题
2. 第二步：根据主题写笑话
4.3.3.1 状态类型定义
代码块
1 from typing_extensions import TypedDict, NotRequired
2
3 class State(TypedDict):
4 topic: NotRequired[str] # 笑话主题，可选字段
5 joke: NotRequired[str] # 笑话内容，可选字段
4.3.3.2 节点函数实现
代码块
1 model = init_chat_model("gpt-4o-mini")
2 def generate_topic(state: State):
3 """第一个AI调用：生成主题"""
4 response = model.invoke("给我一个搞笑的笑话主题")
5 return {"topic": response.content} # 更新状态
6
7 def write_joke(state: State):
8 """第二个AI调用：编写笑话"""
9 response = model.invoke(f"写一个关于{state['topic']}的笑话")
10 return {"joke": response.content} # 更新状态
4.3.3.3 工作流构建
代码块
1 # 创建状态图
2 workflow = StateGraph(State)
3
4 # 添加节点

5 workflow.add_node("generate_topic", generate_topic)
6 workflow.add_node("write_joke", write_joke)
7
8 # 连接节点
9 workflow.add_edge(START, "generate_topic")
10 workflow.add_edge("generate_topic", "write_joke")
11 workflow.add_edge("write_joke", END)
12
13 # 编译并启用检查点
14 graph = workflow.compile(checkpointer=InMemorySaver())
执行工作流：
代码块
1 config = {"configurable": {"thread_id": "1"}}
2 result = graph.invoke({}, config)
3 print(result["joke"])
4.3.3.4 时间旅行调试过程
• 发现问题：最终笑话主题太宽泛
• 回溯分析：
代码块
1 # 查看所有检查点
2 states = list(graph.get_state_history(config))
3
4 # 检查主题生成节点后的状态
5 topic_state = states[1] # generate_topic之后的检查点
6 print("AI生成的主题：", topic_state.values["topic"])
• 修改测试：
代码块
1 # 修改为更具体的主题
2 new_config = graph.update_state(
3 topic_state.config,
4 values={"topic": "程序员调试代码时的趣事"}
5 )
6

7 # 重新执行
8 new_result = graph.invoke(None, new_config)
9 print("改进后的笑话：", new_result["joke"])
5. 持久化小结
在 LangGraph 中，持久化能力提供了：
• 自动化：在使用 LangGraph 时，持久化基础设施（检查点和存储）是自动处理的，无需手动配
置。
• 多种存储后端：提供了多种检查点存储后端，包括内存（ 用于开发测试）、
InMemorySaver
Postgres（ 用于生产）。
PostgresSaver
基于上述技术，LangGraph 支持以下强大功能：
功能  说明
状态查询  • graph.get_state(config) ：获取线程的最新状态。
• graph.get_state_history(config) ：获取线程的完整状态历史（所有检查
点），按时间倒序排列。
时间旅行与重放  通过指定  thread_id  和  checkpoint_id  来调用图，可以从历史某个检查点开始
重放执行，用于调试或探索不同路径。
状态编辑  graph.update_state(config, values) ：允许直接修改线程的当前状态。修改
会遵循状态模式中定义的规则（例如，对列表是追加而非覆盖）。
人机交互  允许在执行的特定步骤暂停，让人工审查和修改状态后再继续。
记忆  线程自动记录完整的交互历史，实现多轮对话的记忆。
• 短期记忆：单次会话中保持的上下文信息
• 长期记忆：跨会话保存的用戶或应用数据
掌握了这些能力，我们就能构建出复杂、可靠、且包含记忆能力的 AI 系统。
五、LangGraph 其他核心能力
1. 运行时上下文（Runtime context）

1.1 什么是运行上下文？
1.1.1 上下文定义与分类
上下文（Context） 是程序运行时可访问的数据和环境信息。在 LangGraph 中，上下文用于传递：
• 用戶身份、配置参数
• 数据库连接、API 密钥
• 会话状态、历史记录等
上下文可按两个维度分类：
维度  类型  描述  示例
静态上下文  运行中不变的数据  用戶ID、数据库连接
可变性
动态上下文  运行中会变化的数据  对话记录、中间结果
运行时上下文  单次运行/线程有效  当前请求的临时数据
生命周期
跨会话上下文  多次会话持久化  用戶偏好、历史记录
因此，在 LangGraph 中，包含三种上下文：
类型  可变性  生命周期  访问方式
静态运行时上下文  静态  单次运行/线程  context  参数传入
动态运行时上下文  动态  单次运行  图状态对象
动态跨会话上下文  动态  跨会话  存储（Store）
关于我们之前学习过的 和 ，则分别代表 动态运行时上下文 和 动态跨会话上
checkpoints store
下文 。接下来一起来看下 静态运行时上下文 的使用方式。
1.1.2 场景练习
做个小练习：根据具体场景，分析各种数据如何保存。例如我们需要开发一个 智能旅行规划助手 ，该
助手需要：
1. 根据用戶的母语提供个性化回答
2. 根据用戶的会员等级提供不同服务

3. 连接到旅游数据库查询信息
4. 根据季节推荐不同的活动
5. 记住用戶的历史查询，提供更精准的建议
这些信息如何保存？
数据类型  上下文类型  为什么
数据库连接  静态运行时上下文  每次查询都需要，单次运行中不变
用戶语言偏好  静态运行时上下文  个性化回答，单次运行中不变
用戶会员等级  静态运行时上下文  服务分级，单次运行中不变
当前季节  静态运行时上下文  推荐季节性活动，单次运行中不变
对话历史  动态运行时上下文  了解上下文，单次运行中变化
用戶旅行偏好  跨会话上下文  长期记忆，跨会话
通过以上练习，应该能够理解 LangGraph 中运行上下文的概念，并在实际项目中正确使用不同类型的
上下文来构建更智能、更个性化的 AI 应用。
记住：良好的上下文管理是构建复杂、可维护 AI 应用的关键！正确的上下文设计能让我们的AI应用：
• ✅ 更高效：避免重复传递不变数据
• ✅ 更智能：基于上下文提供个性化服务
• ✅ 更可维护：清晰的数据边界和职责分离
• ✅ 更易扩展：支持多用戶、多场景、长期记忆
1.2 配置运行时上下文
1.2.1 定义上下文模式
首先需要定义一个上下文的数据结构（通常用   或  ）。下面我们演示一个
dataclass TypedDict
实际示例，在该参数中我们配置了三个参数：用戶ID、LLM 和系统消息，以便在运行时使用。
代码块
1 from dataclasses import dataclass
2
3 @dataclass
4 class ContextSchema:
5 user_id: str

6 model_provider: str = "openai" # 默认值
7 system_message: str = "你是一个乐于助人的助手。"
1.2.2 在图中使用上下文模式
创建图时传入   参数。
context_schema
代码块
1 from langgraph.graph import StateGraph
2
3 builder = StateGraph(
4 State, # 状态模式
5 context_schema=ContextSchema # 添加上下文模式
6 )
1.2.3 在节点中访问上下文
节点函数可通过   参数访问上下文。
runtime
代码块
1 from langgraph.runtime import Runtime
2
3 def my_node(state: State, runtime: Runtime[ContextSchema]):
4 user_id = runtime.context.user_id
5 model_provider = runtime.context.model_provider
6
7 if model_provider == "openai":
8 # 使用 OpenAI 模型
9 pass
10 elif model_provider == "anthropic":
11 # 使用 Anthropic 模型
12 pass
13
14 return {"result": f"用戶{user_id}处理完成"}
1.2.1 运行图时传入上下文

1 graph.invoke(
2 {"input": "Hello"},
3 context={
4 "user_id": "user123",
5 "model_provider": "anthropic",
6 "system_message": "请用中文回答"
7 }
8 )
1.2.2 【完整示例】
代码块
1 from dataclasses import dataclass
2
3 from langgraph.runtime import Runtime
4 from langgraph.graph import StateGraph, START, END
5 from typing_extensions import TypedDict
6 from langchain.messages import AnyMessage
7
8 @dataclass
9 class AppContext:
10 user_id: str
11 language: str = "en"
12
13 class AppState(TypedDict):
14 messages: list[AnyMessage]
15 user_name: str = ""
16
17
18 def greet_user(state: AppState, runtime: Runtime[AppContext]):
19 greeting = "Hello" if runtime.context.language == "en" else "你好"
20 user_name = state.get("user_name", "Guest")
21
22 return {"messages": [f"{greeting}, {user_name}!"]}
23
24 builder = StateGraph(AppState, context_schema=AppContext)
25 builder.add_node("greet", greet_user)
26 builder.add_edge(START, "greet")
27 builder.add_edge("greet", END)
28
29 graph = builder.compile()
30
31 # 英文用戶

32 result_en = graph.invoke(
33 {"user_name": "Alice"},
34 context={"user_id": "123", "language": "en"}
35 )
36 # 输出: Hello, Alice!
37
38 # 中文用戶
39 result_zh = graph.invoke(
40 {"user_name": "张三"},
41 context={"user_id": "456", "language": "zh"}
42 )
43 # 输出: 你好, 张三!
1.3 在工具中访问上下文
工具是调用外部系统、API、数据库交互或执行计算的功能。因此，对于用戶身份、配置参数、数据库
连接、API 密钥等这类调用 API 的参数信息和配置信息，则需要传递给工具。上下文对工具的重要性：
• 个性化响应：根据用戶上下文提供定制化回答
• 权限控制：基于用戶身份限制工具访问
• 状态感知：工具可以根据当前状态决定行为
• 依赖注入：避免硬编码配置，提高可测试性
1.3.1 基本用法
工具可以通过   参数访问运行时信息。这个参数，为工具提供包括：
ToolRuntime
• ：图状态数据
State
• ：静态上下文
Context
• ：持久化存储等
Store
使用   时，只需在工具签名中添加 ，它会自动注入。调
ToolRuntime runtime: ToolRuntime
用时，无需手动传输。
定义一个带有运行时信息的工具如下所示：
代码块
1 from langchain.tools import tool, ToolRuntime
2
3 @tool
4 def get_user_info(runtime: ToolRuntime) -> str:

5 """获取当前用戶的信息"""
6 user_id = runtime.context.user_id # 访问上下文
7 user_state = runtime.state["user_name"] # 访问状态
8
9 return f"User {user_id}, state: {user_state}"
1.3.2 【完整示例】
构建一个支持搜索的 AI 系统，假设调用搜索 API 需要用戶数据作为参数，则需要向工具中传入相关信
息。关键步骤如下：
1. 定义状态、上下文结构
2. 定义工具节点（ToolNode）、定义 LLM 节点
3. 构建并编译图，需加入状态和上下文参数
4. 执行并验证结果
代码块
1 from dataclasses import dataclass
2 from langchain.chat_models import init_chat_model
3 from langchain.messages import SystemMessage, HumanMessage
4 from langchain.tools import tool, ToolRuntime
5 from langchain.messages import AnyMessage
6 from langgraph.prebuilt import ToolNode, tools_condition
7 from langgraph.graph import StateGraph, START, END
8 from typing_extensions import TypedDict, Annotated
9 import operator
10
11 class MessagesState(TypedDict):
12 messages: Annotated[list[AnyMessage], operator.add]
13 user_name: str = ""
14
15 @dataclass
16 class Context:
17 user_id: str
18
19 @tool
20 def search(runtime: ToolRuntime[Context]) -> str:
21 """调用搜索工具"""
22 user_id = runtime.context.user_id # 访问上下文
23 user_name = runtime.state["user_name"] # 访问状态
24 print(f"日志记录：user_id: {user_id}, user_name: {user_name} 调用查询工具")
25 return f"查询天气：晴天，15-20度" # 模拟调用
26

27 # 绑定工具
28 model_with_tools = init_chat_model("gpt-4o-mini",
temperature=0).bind_tools([search])
29 def llm_call(state: dict):
30 """LLM决定是否调用工具"""
31 return {
32 "messages": [
33 model_with_tools.invoke(
34 [SystemMessage(content="你是一个乐于助人的助手，支持调用工具进行搜
索。")]
35 + state["messages"]
36 )
37 ]
38 }
39
40 # 定义并编译图
41 builder = StateGraph(MessagesState, context_schema=Context)
42 builder.add_node("llm_call", llm_call)
43 builder.add_node("tool_node", ToolNode([search]))
44
45 builder.add_edge(START, "llm_call")
46 builder.add_conditional_edges(
47 "llm_call",
48 tools_condition,
49 {
50 "tools": "tool_node", # 将条件输出转换为图中的节点
51 "__end__": END,
52 },)
53 builder.add_edge("tool_node", "llm_call")
54 graph = builder.compile()
55
56 for chunk in graph.stream(
57 {
58 "messages": [HumanMessage(content="今天西安的天气如何？")],
59 "user_name": "小明"
60 },
61 context={"user_id": "123"}
62 ):
63 for node, update in chunk.items():
64 update["messages"][-1].pretty_print()
65
66
67 # 打印结果如下：
68 # ================================== Ai Message
==================================
69 # Tool Calls:
70 # search (call_YU9O02F9JBdiz3J7CMmUYLNE)

71 # Call ID: call_YU9O02F9JBdiz3J7CMmUYLNE
72 # Args:
73 # 日志记录：user_id: 123, user_name: 小明 调用查询工具
74 # ================================= Tool Message
=================================
75 # Name: search
76 #
77 # 查询天气：晴天，15-20度
78 # ================================== Ai Message
==================================
79 #
80 # 今天西安的天气是晴天，气温在15到20度之间。
2. 流（Streaming）
2.1 概念
在 LangChain 篇章中，我们已经知道了流式传输用来逐步输出数据，无需等待全部处理完成。这可以
提升用戶体验，减少等待感，尤其适用于大语言模型（LLM）这类延迟较高的任务。就像看电影时，
画面一帧帧播放，而不是等全部下载完再看。
在 LangGraph 篇章中，流式处理可将图运行的实时数据反馈显示到应用程序中，如：状态、LLM 生成
的文本、自定义数据等。且支持多种流模式。
2.2 五种流模式
LangGraph 支持以下五种流模式：
模式  说明  适用场景
values 流式输出完整状态  需要知道每一步的完整状态
updates 流式输出状态变化  关注每一步更新了哪些字段
messages 流式输出 LLM 生成的 token  实时展示 LLM 生成内容
custom 流式输出自定义数据  自定义进度条、日志等
debug 输出所有调试信息  开发调试阶段
将一种或多种流模式作为列表传递给 或 方法是其使用姿势。
stream astream

2.3 基础示例：流式输出状态值
代码块
1 from langgraph.graph import StateGraph, START
2
3 # 定义状态结构
4 class State(dict):
5 topic: str
6 joke: str
7
8 # 创建节点函数
9 def refine_topic(state):
10 return {"topic": state["topic"] + "和猫"}
11
12 def generate_joke(state):
13 return {"joke": f"这是一个关于{state['topic']}的笑话"}
14
15 # 构建图
16 graph = (
17 StateGraph(State)
18 .add_node(refine_topic)
19 .add_node(generate_joke)
20 .add_edge(START, "refine_topic")
21 .add_edge("refine_topic", "generate_joke")
22 .compile()
23 )
24
25 # 流式输出状态更新
26 for chunk in graph.stream(
27 {"topic": "冰激凌"},
28 stream_mode="updates" # 只看更新部分
29 ):
30 print(chunk)
31
32 for chunk in graph.stream(
33 {"topic": "冰激凌"},
34 stream_mode="values" # 每一步的完整状态
35 ):
36 print(chunk)
时输出：
stream_mode="updates"
代码块

1 {'refine_topic': {'topic': '冰激凌和猫'}}
2 {'generate_joke': {'joke': '这是一个关于冰激凌和猫的笑话'}}
时输出：
stream_mode="values"
代码块
1 {'topic': '冰激凌'}
2 {'topic': '冰激凌和猫'}
3 {'topic': '冰激凌和猫', 'joke': '这是一个关于冰激凌和猫的笑话'}
2.4 流式传输自定义数据
LangGraph 不仅支持输出状态这类的数据，还支持从节点或工具中输出用戶自定义的数据。步骤如
下：
• 使用 访问流编写器并发出自定义数据。
get_stream_writer()
• 调用  （）  或  （）  时设置   以获取流中的自
.stream .astream stream_mode="custom"
定义数据。还可以组合多种模式（如 、 ），但至少必须有一个是
["updates" "custom"]
。
"custom"
2.4.1 基本用法
2.4.1.1 从节点和工具中输出用戶自定义数据
这里改造下【运行时上下文-在工具中访问上下文】的代码：
代码块
1 from dataclasses import dataclass
2 from langchain.chat_models import init_chat_model
3 from langchain.messages import SystemMessage, HumanMessage
4 from langchain.tools import tool, ToolRuntime
5 from langchain.messages import AnyMessage
6 from langgraph.config import get_stream_writer
7 from langgraph.prebuilt import ToolNode, tools_condition
8 from langgraph.graph import StateGraph, START, END
9 from typing_extensions import TypedDict, Annotated
10 import operator
11
12 class MessagesState(TypedDict):
13 messages: Annotated[list[AnyMessage], operator.add]

14 user_name: str = ""
15
16 @dataclass
17 class Context:
18 user_id: str
19
20 @tool
21 def search(runtime: ToolRuntime[Context]) -> str:
22 """调用搜索工具"""
23 user_id = runtime.context.user_id # 访问上下文
24 user_name = runtime.state["user_name"] # 访问状态
25
26 # 获取流式写入器
27 writer = get_stream_writer()
28 # 发送开始信号
29 writer({
30 "type": "search_tool",
31 "status": "start",
32 "user_id": user_id,
33 "user_name": user_name
34 })
35
36 # 模拟搜索过程
37 writer({
38 "type": "search_tool",
39 "status": "searching",
40 "user_id": user_id,
41 "user_name": user_name
42 })
43 # 模拟处理时间
44 import time
45 time.sleep(2)
46
47 # 结束
48 writer({
49 "type": "search_tool",
50 "status": "end",
51 "user_id": user_id,
52 "user_name": user_name
53 })
54 return f"查询天气：晴天，15-20度" # 模拟调用
55
56
57 # 绑定工具
58 model_with_tools = init_chat_model("gpt-4o-mini",
temperature=0).bind_tools([search])
59 def llm_call(state: dict):

60 """LLM决定是否调用工具"""
61
62 # 获取流式写入器
63 writer = get_stream_writer()
64
65 # 发送开始处理的信号
66 writer({
67 "type": "llm_call",
68 "status": "start",
69 "message": "开始调用LLM",
70 "content": state["messages"][-1].content
71 })
72
73 result = model_with_tools.invoke(
74 [SystemMessage(content="你是一个乐于助人的助手，支持调用工具进行搜索。")]
75 + state["messages"]
76 )
77
78 # 调用结束
79 writer({
80 "type": "llm_call",
81 "status": "end",
82 "message": "调用LLM完成"
83 })
84 return {"messages": [result]}
85
86 # 定义并编译图
87 builder = StateGraph(MessagesState, context_schema=Context)
88 builder.add_node("llm_call", llm_call)
89 builder.add_node("tool_node", ToolNode([search]))
90
91 builder.add_edge(START, "llm_call")
92 builder.add_conditional_edges(
93 "llm_call",
94 tools_condition,
95 {
96 "tools": "tool_node", # 将条件输出转换为图中的节点
97 "__end__": END,
98 }, )
99 builder.add_edge("tool_node", "llm_call")
100 graph = builder.compile()
101
102 for chunk in graph.stream(
103 {
104 "messages": [HumanMessage(content="今天西安的天气如何？")],
105 "user_name": "小明"
106 },

107 context={"user_id": "123"},
108 stream_mode=["custom"]
109 ):
110 print(chunk)
打印结果：
代码块
1 ('custom', {'type': 'llm_call', 'status': 'start', 'message': '开始调用LLM',
'content': '今天西安的天气如何？'})
2 ('custom', {'type': 'llm_call', 'status': 'end', 'message': '调用LLM完成'})
3 ('custom', {'type': 'search_tool', 'status': 'start', 'user_id': '123',
'user_name': '小明'})
4 ('custom', {'type': 'search_tool', 'status': 'searching', 'user_id': '123',
'user_name': '小明'})
5 ('custom', {'type': 'search_tool', 'status': 'end', 'user_id': '123',
'user_name': '小明'})
6 ('custom', {'type': 'llm_call', 'status': 'start', 'message': '开始调用LLM',
'content': '查询天气：晴天，15-20度'})
7 ('custom', {'type': 'llm_call', 'status': 'end', 'message': '调用LLM完成'})
2.4.1.2 设置多种传输模式
还可以组合多种模式（如 、 ），但至少必须有一个是  。如下
["updates" "custom"] "custom"
所示：
代码块
1 for chunk in graph.stream(
2 {
3 "messages": [HumanMessage(content="今天西安的天气如何？")],
4 "user_name": "小明"
5 },
6 context={"user_id": "123"},
7 stream_mode=["custom", "updates"]
8 ):
9 print(chunk)
打印结果：
代码块

1 ('custom', {'type': 'llm_call', 'status': 'start', 'message': '开始调用LLM',
'content': '今天西安的天气如何？'})
2 ('custom', {'type': 'llm_call', 'status': 'end', 'message': '调用LLM完成'})
3 ('updates', {'llm_call': {'messages': [AIMessage(content='', additional_kwargs=
{'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 10,
'prompt_tokens': 57, 'total_tokens': 67, 'completion_tokens_details':
{'accepted_prediction_tokens': None, 'audio_tokens': 0, 'reasoning_tokens': 0,
'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens':
0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-
mini-2024-07-18', 'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-
ClrG4UM0QgdVL1saWDn6UY5HzMC42', 'finish_reason': 'tool_calls', 'logprobs':
None}, id='lc_run--71774886-08f2-4fe3-9511-909fcb517d8d-0', tool_calls=
[{'name': 'search', 'args': {}, 'id': 'call_C5ahwoeJCrlaHgGK2ypQgZ91', 'type':
'tool_call'}], usage_metadata={'input_tokens': 57, 'output_tokens': 10,
'total_tokens': 67, 'input_token_details': {'audio': 0, 'cache_read': 0},
'output_token_details': {'audio': 0, 'reasoning': 0}})]}})
4 ('custom', {'type': 'search_tool', 'status': 'start', 'user_id': '123',
'user_name': '小明'})
5 ('custom', {'type': 'search_tool', 'status': 'searching', 'user_id': '123',
'user_name': '小明'})
6 ('custom', {'type': 'search_tool', 'status': 'end', 'user_id': '123',
'user_name': '小明'})
7 ('updates', {'tool_node': {'messages': [ToolMessage(content='查询天气：晴天，15-
20度', name='search', tool_call_id='call_C5ahwoeJCrlaHgGK2ypQgZ91')]}})
8 ('custom', {'type': 'llm_call', 'status': 'start', 'message': '开始调用LLM',
'content': '查询天气：晴天，15-20度'})
9 ('custom', {'type': 'llm_call', 'status': 'end', 'message': '调用LLM完成'})
10 ('updates', {'llm_call': {'messages': [AIMessage(content='今天西安的天气是晴天，气
温在15到20度之间。', additional_kwargs={'refusal': None}, response_metadata=
{'token_usage': {'completion_tokens': 20, 'prompt_tokens': 83, 'total_tokens':
103, 'completion_tokens_details': {'accepted_prediction_tokens': None,
'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens':
None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}},
'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18',
'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-
ClrG7AWCON5HjNu3JOxdJupdyJvEu', 'finish_reason': 'stop', 'logprobs': None},
id='lc_run--3ae60a09-a1e6-4b1d-9c6c-499d76f17d1b-0', usage_metadata=
{'input_tokens': 83, 'output_tokens': 20, 'total_tokens': 103,
'input_token_details': {'cache_read': 0}, 'output_token_details': {}})]}})
可以看到 LangGraph 运行将一种或多种流模式作为列表传递给 或 。
stream astream
2.4.2 应用场景
2.4.2.1 创建自定义监控面板

那么自定义流式数据到底有什么用？让我们改造一下代码。
改造一：将工具调用模拟为多步骤执行
代码块
1 @tool
2 def search(runtime: ToolRuntime[Context]) -> str:
3 """调用搜索工具"""
4 user_id = runtime.context.user_id # 访问上下文
5 user_name = runtime.state["user_name"] # 访问状态
6
7 # 获取流式写入器
8 writer = get_stream_writer()
9 # 发送开始信号
10 writer({
11 "type": "search_tool",
12 "status": "start",
13 "user_id": user_id,
14 "user_name": user_name
15 })
16
17 # 模拟搜索过程
18 search_steps = [
19 {"name": "搜索1", "time": 1, "result": "晴天，"},
20 {"name": "搜索2", "time": 2, "result": "15-20度"},
21 ]
22
23 all_result = "查询天气："
24 import time
25 for i, step in enumerate(search_steps, 1):
26 writer({
27 "type": "search_tool",
28 "status": "searching",
29 "step": step['name'],
30 "all_step": len(search_steps),
31 "cur_step": i,
32 "user_id": user_id,
33 "user_name": user_name
34 })
35 # 模拟处理时间
36 time.sleep(step['time'])
37 all_result += step['result']
38
39 # 结束
40 writer({
41 "type": "search_tool",
42 "status": "end",

43 "user_id": user_id,
44 "user_name": user_name,
45 "result": all_result
46 })
47 return all_result
改造二：输出结果重定义（这里只处理了工具部分自定义数据流。其它同理自行改造）
代码块
1 # 运行并监控自定义流
2 print("图开始执行：")
3 for chunk in graph.stream(
4 {
5 "messages": [HumanMessage(content="今天西安的天气如何？")],
6 "user_name": "小明"
7 },
8 context={"user_id": "123"},
9 stream_mode=["custom", "updates"]
10 ):
11 if chunk[0] == "custom": # 自定义监控，可以输出到文件
12 info = chunk[-1]
13 if info.get("type") == "llm_call":
14 pass
15 elif info.get("type") == "search_tool":
16 status = info.get("status")
17 if status == "start":
18 print(f"用戶id:{info['user_id']}, 用戶名称:{info['user_name']}开
始调用工具...")
19 elif status == "searching":
20 print(f"[{info['cur_step']}/{info['all_step']}] 正在处理:
{info['step']}")
21 elif status == "end":
22 print(f"调用完成！结果: {info['result']}")
23 elif chunk[0] == "updates": # 正常输出到终端
24 pass
完整代码如下：
代码块
1 from dataclasses import dataclass
2 from langchain.chat_models import init_chat_model
3 from langchain.messages import SystemMessage, HumanMessage
4 from langchain.tools import tool, ToolRuntime
5 from langchain.messages import AnyMessage

6 from langgraph.config import get_stream_writer
7 from langgraph.prebuilt import ToolNode, tools_condition
8 from langgraph.graph import StateGraph, START, END
9 from typing_extensions import TypedDict, Annotated
10 import operator
11
12
13 class MessagesState(TypedDict):
14 messages: Annotated[list[AnyMessage], operator.add]
15 user_name: str = ""
16
17
18 @dataclass
19 class Context:
20 user_id: str
21
22
23 @tool
24 def search(runtime: ToolRuntime[Context]) -> str:
25 """调用搜索工具"""
26 user_id = runtime.context.user_id # 访问上下文
27 user_name = runtime.state["user_name"] # 访问状态
28
29 # 获取流式写入器
30 writer = get_stream_writer()
31 # 发送开始信号
32 writer({
33 "type": "search_tool",
34 "status": "start",
35 "user_id": user_id,
36 "user_name": user_name
37 })
38
39 # 模拟搜索过程
40 search_steps = [
41 {"name": "搜索1", "time": 1, "result": "晴天，"},
42 {"name": "搜索2", "time": 2, "result": "15-20度"},
43 ]
44
45 all_result = "查询天气："
46 import time
47 for i, step in enumerate(search_steps, 1):
48 writer({
49 "type": "search_tool",
50 "status": "searching",
51 "step": step['name'],
52 "all_step": len(search_steps),

53 "cur_step": i,
54 "user_id": user_id,
55 "user_name": user_name
56 })
57 # 模拟处理时间
58 time.sleep(step['time'])
59 all_result += step['result']
60
61 # 结束
62 writer({
63 "type": "search_tool",
64 "status": "end",
65 "user_id": user_id,
66 "user_name": user_name,
67 "result": all_result
68 })
69 return all_result
70
71
72 # 绑定工具
73 model_with_tools = init_chat_model("gpt-4o-mini",
temperature=0).bind_tools([search])
74
75
76 def llm_call(state: dict):
77 """LLM决定是否调用工具"""
78
79 # 获取流式写入器
80 writer = get_stream_writer()
81
82 # 发送开始处理的信号
83 writer({
84 "type": "llm_call",
85 "status": "start",
86 "message": "开始调用LLM",
87 "content": state["messages"][-1].content
88 })
89
90 result = model_with_tools.invoke(
91 [SystemMessage(content="你是一个乐于助人的助手，支持调用工具进行搜索。")]
92 + state["messages"]
93 )
94
95 # 调用结束
96 writer({
97 "type": "llm_call",
98 "status": "end",

99 "message": "调用LLM完成"
100 })
101 return {"messages": [result]}
102
103 # 定义并编译图
104 builder = StateGraph(MessagesState, context_schema=Context)
105 builder.add_node("llm_call", llm_call)
106 builder.add_node("tool_node", ToolNode([search]))
107
108 builder.add_edge(START, "llm_call")
109 builder.add_conditional_edges(
110 "llm_call",
111 tools_condition,
112 {
113 "tools": "tool_node", # 将条件输出转换为图中的节点
114 "__end__": END,
115 }, )
116 builder.add_edge("tool_node", "llm_call")
117 graph = builder.compile()
118
119
120 # 运行并监控自定义流
121 print("图开始执行：")
122 for chunk in graph.stream(
123 {
124 "messages": [HumanMessage(content="今天西安的天气如何？")],
125 "user_name": "小明"
126 },
127 context={"user_id": "123"},
128 stream_mode=["custom", "updates"]
129 ):
130 if chunk[0] == "custom": # 自定义监控，可以输出到文件
131 info = chunk[-1]
132 if info.get("type") == "llm_call":
133 pass
134 elif info.get("type") == "search_tool":
135 status = info.get("status")
136 if status == "start":
137 print(f"用戶id:{info['user_id']}, 用戶名称:{info['user_name']}开
始调用工具...")
138 elif status == "searching":
139 print(f"[{info['cur_step']}/{info['all_step']}] 正在处理:
{info['step']}")
140 elif status == "end":
141 print(f"调用完成！结果: {info['result']}")
142 elif chunk[0] == "updates": # 正常输出到终端
143 pass

打印结果：
代码块
1 图开始执行：
2 用戶id:123, 用戶名称:小明开始调用工具...
3 [1/2] 正在处理: 搜索1
4 [2/2] 正在处理: 搜索2
5 调用完成！结果: 查询天气：晴天，15-20度
可以看到，我们可以通过自定义数据创建自定义的监控面板！这个过程中，还可以计算中间进度
（ 、 ）。
[1/2] [2/2]
因此，自定义流式数据的用法，可以做到：
1. 实时进度反馈：在长时间处理任务中显示进度
2. 调试信息输出：输出中间计算结果
3. 多源数据整合：同时流式输出不同类型的数据
4. 自定义监控：创建自定义的监控面板
2.5 流式传输 LLM tokens
Token 是大语言模型处理文本的基本单位。因此 LangGraph 可以：
• 使用   模式可以从 graph 的任何部分（包括节点、工具等）逐
stream_mode="messages"
Token 流式传输 LLM 输出。
• 输出格式为  元组。
(message_chunk, metadata)
2.5.1 基本用法
代码块
1 from typing import TypedDict
2 from langgraph.graph import StateGraph, START
3 from langchain_openai import ChatOpenAI
4
5 # 定义状态
6 class State(TypedDict):
7 input: str
8 output: str
9

10 # 初始化模型
11 model = ChatOpenAI(model="gpt-4o-mini")
12 def llm_node(state: State):
13 """生成答案的节点"""
14 return {"output": model.invoke([
15 {"role": "system", "content": "你是一个乐于助人的助手。"},
16 {"role": "user", "content": state["input"]}
17 ])
18 }
19
20 # 构建图
21 builder = StateGraph(State)
22 builder.add_node(llm_node)
23 builder.add_edge(START, "llm_node")
24 graph = builder.compile()
25
26
27 # 流式输出 LLM Tokens
28 # 输出格式为(message_chunk, metadata) 元组。
29 for token_chunk, metadata in graph.stream(
30 {"input": "请解释什么是机器学习？"},
31 stream_mode="messages"
32 ):
33 if token_chunk.content:
34 # 逐 Token 输出
35 print(token_chunk.content, end="", flush=True)
2.5.2 高级功能
2.5.2.1 按 Tags 过滤 Tokens
我们还可以将 tags 与 LLM 调用相关联，以按 LLM 调用筛选流式令牌。
代码块
1 from typing import TypedDict
2 from langgraph.graph import StateGraph, START
3 from langchain_openai import ChatOpenAI
4
5 # 初始化带标签的模型
6 joke_model = ChatOpenAI(
7 model="gpt-4o-mini",
8 model_kwargs={"tags": ["joke"]} # 给模型添加标签
9 )
10

11 poem_model = ChatOpenAI(
12 model="gpt-4o-mini",
13 model_kwargs={"tags": ["poem"]} # 给模型添加标签
14 )
15
16 class CreativeState(TypedDict):
17 topic: str
18 joke: str
19 poem: str
20
21
22 def generate_creative_content(state: CreativeState):
23 """同时生成笑话和诗歌"""
24 topic = state["topic"]
25
26 # 生成笑话
27 print(f"\n生成关于 {topic} 的笑话：")
28 joke_response = joke_model.invoke([
29 {"role": "user", "content": f"讲一个关于 {topic} 的笑话"}
30 ])
31
32 # 生成诗歌
33 print(f"\n生成关于 {topic} 的诗歌：")
34 poem_response = poem_model.invoke([
35 {"role": "user", "content": f"写一首关于 {topic} 的短诗"}
36 ])
37
38 return {
39 "joke": joke_response.content,
40 "poem": poem_response.content
41 }
42
43
44 # 构建图
45 builder = StateGraph(CreativeState)
46 builder.add_node("creative", generate_creative_content)
47 builder.add_edge(START, "creative")
48 graph = builder.compile()
49
50 # 流式输出并过滤
51 for token_chunk, metadata in graph.stream(
52 {"topic": "猫"},
53 stream_mode="messages"
54 ):
55 # 只输出笑话相关的 Tokens
56 tags = metadata.get("tags", [])
57

58 if "joke" in tags:
59 print(token_chunk.content, end="", flush=True)
60
61 # 也可以过滤诗歌
62 # if "poem" in tags:
63 # print(token_chunk.content, end="", flush=True)
2.5.2.2 按节点名称过滤
可以指定特定节点流式传输Tokens，需按流式传输元数据中的   字段筛选输出：
langgraph_node
代码块
1 from typing import TypedDict
2 from langgraph.graph import StateGraph, START, END
3 from langchain_openai import ChatOpenAI
4
5 model = ChatOpenAI(model="gpt-4o-mini")
6
7 class State(TypedDict):
8 query: str
9 summary: str
10 translation: str
11
12 def generate_summary(state: State):
13 """生成摘要"""
14 response = model.invoke([
15 {"role": "user", "content": f"请为以下内容生成摘要：{state['query']}"}
16 ])
17 return {"summary": response.content}
18
19
20 def generate_translation(state: State):
21 """生成翻译"""
22 response = model.invoke([
23 {"role": "user", "content": f"请将以下内容翻译成英文：{state['query']}"}
24 ])
25 return {"translation": response.content}
26
27
28 # 构建并行处理图
29 builder = StateGraph(State)
30 builder.add_node("summarize", generate_summary)
31 builder.add_node("translate", generate_translation)
32

33 builder.add_edge(START, "summarize")
34 builder.add_edge(START, "translate")
35 builder.add_edge("summarize", END)
36 builder.add_edge("translate", END)
37 graph = builder.compile()
38
39 # 流式输出并只显示某个节点的 Tokens
40 target_node = "summarize" # 可以改为 "translate"
41 for token_chunk, metadata in graph.stream(
42 {"query": "人工智能是计算机科学的一个分支，致力于创造能够执行通常需要人类智能的
任务的机器。"},
43 stream_mode="messages"
44 ):
45 # 获取节点名称
46 node_name = metadata.get("langgraph_node", "")
47
48 # 只输出目标节点的 Tokens
49 if token_chunk.content and node_name == target_node:
50 # 添加节点标签
51 if node_name == "translate":
52 prefix = "🌐 [翻译] "
53 elif node_name == "summarize":
54 prefix = "📋 [摘要] "
55 else:
56 prefix = ""
57
58 print(f"{prefix}{token_chunk.content}", end="", flush=True)
3. 子图（Subgraphs）
3.1 什么是子图？
在 LangGraph 中，子图是另一个图中的一个节点，可以独立开发和测试，也可以被多个主图复用。子
图可用于：
• 模块化开发：不同团队可以独立开发不同部分
• 代码复用：相同逻辑的图只需开发一次
3.2 使用子图的两种方式
3.2.1 方式一：从节点调用子图（不同状态模式）

这种方式是从一个图（如主图）的节点内部调用另一个图（如子图）。因此其使用特点是：子图和主
图的状态结构可以完全不同。
视图
node_2节点内调用
__start__ node_1 sub_node_1 sub_node_2 __end__
代码块
1 from typing_extensions import TypedDict
2 from langgraph.graph.state import StateGraph, START
3
4 # 1. 定义子图
5 class SubState(TypedDict):
6 # 注意，这些键都不与父图状态共享
7 sub_1: str
8 sub_2: str
9
10 def sub_node_1(state: SubState):
11 return {"sub_1": "sub_1"}
12
13 def sub_node_2(state: SubState):
14 return {"sub_2": state["sub_2"] + state["sub_1"]}
15
16 sub_builder = StateGraph(SubState)
17 sub_builder.add_node(sub_node_1)
18 sub_builder.add_node(sub_node_2)
19 sub_builder.add_edge(START, "sub_node_1")
20 sub_builder.add_edge("sub_node_1", "sub_node_2")
21 subgraph = sub_builder.compile()
22
23 # 2. 定义主图
24 class ParentState(TypedDict):
25 parent: str
26
27 def node_1(state: ParentState):
28 return {"parent": "hi! " + state["parent"]}
29

30 def node_2(state: ParentState):
31 # 将状态转换为子图状态
32 response = subgraph.invoke({"sub_2": state["parent"]})
33 # 将响应转换回父状态
34 return {"parent": response["sub_2"]}
35
36 builder = StateGraph(ParentState)
37 builder.add_node("node_1", node_1)
38 builder.add_node("node_2", node_2)
39 builder.add_edge(START, "node_1")
40 builder.add_edge("node_1", "node_2")
41 graph = builder.compile()
42
43 # 要在流式输出中包含子图的输出，可以在父图的 .stream（） 方法中设置 subgraphs=True。
44 # subgraphs默认为False
45 for chunk in graph.stream({"parent": "parent"}, subgraphs=True):
46 print(chunk)
输出结果：
代码块
1 ((), {'node_1': {'parent': 'hi! parent'}})
2 (('node_2:60e75a5e-41d7-8ec4-915d-afb8f8f62c1c',), {'sub_node_1': {'sub_1':
'sub_1'}})
3 (('node_2:60e75a5e-41d7-8ec4-915d-afb8f8f62c1c',), {'sub_node_2': {'sub_2':
'hi! parentsub_1'}})
4 ((), {'node_2': {'parent': 'hi! parentsub_1'}})
扩展：定义主图、子图、孙子图进行调用。
上述代码中，要在流式输出中包含子图的输出，可以在父图的 方法中设置
.stream()
。这将从父图和任何子图流式传输输出。
subgraphs=True
3.2.2 方式二：将子图作为节点（共享状态模式）
这种方式可以将图添加为另一个图中的节点，如下所示：
代码块
1 # 子图和主图使用相同的状态结构
2 子图 = 创建子图()
3
4 # 直接把子图作为节点加入主图
5 主图.add_node("子图节点", 子图)

其特点是：子图和主图共享部分状态。
代码块
1 from typing_extensions import TypedDict
2 from langgraph.graph.state import StateGraph, START
3
4 # 1. 定义子图
5 class SubState(TypedDict):
6 parent: str # 共享父图状态
7 sub: str # Sub私有
8
9 def sub_node_1(state: SubState):
10 return {"sub": "sub"}
11
12 def sub_node_2(state: SubState):
13 return {"parent": state["parent"] + state["sub"]}
14
15 sub_builder = StateGraph(SubState)
16 sub_builder.add_node(sub_node_1)
17 sub_builder.add_node(sub_node_2)
18 sub_builder.add_edge(START, "sub_node_1")
19 sub_builder.add_edge("sub_node_1", "sub_node_2")
20 subgraph = sub_builder.compile()
21
22
23 # 2. 定义主图

24 class ParentState(TypedDict):
25 parent: str
26
27 def node_1(state: ParentState):
28 return {"parent": "hi! " + state["parent"]}
29
30 builder = StateGraph(ParentState)
31 builder.add_node("node_1", node_1)
32 builder.add_node("node_2", subgraph)
33 builder.add_edge(START, "node_1")
34 builder.add_edge("node_1", "node_2")
35 graph = builder.compile()
36
37 for chunk in graph.stream({"parent": "parent"}):
38 print(chunk)
输出结果：
代码块
1 {'node_1': {'parent': 'hi! parent'}}
2 {'node_2': {'parent': 'hi! parentsub'}}
3.3 为子图添加短期记忆
如果图包含子图 ，则只需在编译父图时提供 。LangGraph 会自动将 传
checkpoint checkpoint
播到子图。
代码块
1 from langgraph.graph import START, StateGraph
2 from langgraph.checkpoint.memory import InMemorySaver
3 from typing import TypedDict
4
5 class State(TypedDict):
6 foo: str
7
8 # 子图
9 def subgraph_node_1(state: State):
10 return {"foo": state["foo"] + "bar"}
11
12 subgraph_builder = StateGraph(State)
13 subgraph_builder.add_node(subgraph_node_1)
14 subgraph_builder.add_edge(START, "subgraph_node_1")

15 subgraph = subgraph_builder.compile()
16
17 # 主图
18 builder = StateGraph(State)
19 builder.add_node("node_1", subgraph)
20 builder.add_edge(START, "node_1")
21
22 checkpointer = InMemorySaver()
23 graph = builder.compile(checkpointer=checkpointer)
3.4 在子图中使用中断
3.4.1 基本用法
在子图中，同样可以使用中断。且添加短期记忆后，可以检查图状态 （检查点）。但要注意，只有当
子图中断时，才能查看子图状态；恢复后，将无法访问子图形状态。例如：
代码块
1 from langgraph.graph import START, StateGraph
2 from langgraph.checkpoint.memory import InMemorySaver
3 from langgraph.types import interrupt, Command
4 from typing_extensions import TypedDict
5
6 class State(TypedDict):
7 foo: str
8
9 # 子图
10 def subgraph_node_1(state: State):
11 print("sub_node_1")
12 return {}
13
14 def subgraph_node_2(state: State):
15 print("sub_node_2")
16 value = interrupt("输入值:")
17 return {"foo": state["foo"] + value}
18
19 subgraph_builder = StateGraph(State)
20 subgraph_builder.add_node(subgraph_node_1)
21 subgraph_builder.add_node(subgraph_node_2)
22 subgraph_builder.add_edge(START, "subgraph_node_1")
23 subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
24 subgraph = subgraph_builder.compile()
25
26 # 主图

27 builder = StateGraph(State)
28 builder.add_node("node_1", subgraph)
29 builder.add_edge(START, "node_1")
30
31 graph = builder.compile(checkpointer=InMemorySaver())
32
33 config = {"configurable": {"thread_id": "1"}}
34
35 graph.invoke({"foo": ""}, config)
36 parent_state = graph.get_state(config)
37
38 # 访问子图状态只能在子图被中断时才可用。
39 # 一旦恢复了图，将无法访问子图状态。
40 subgraph_state = graph.get_state(config, subgraphs=True).tasks[0].state
41 print(subgraph_state)
42
43 print(graph.invoke(Command(resume="bar"), config))
结果如下：
代码块
1 sub_node_1
2 sub_node_2
3 StateSnapshot(
4 values={'foo': ''},
5 next=('subgraph_node_2',),
6 config={...},
7 metadata={...},
8 parent_config={...},
9 tasks=(
10 PregelTask(
11 id='4afcaec2-1fd1-7bfc-cab9-dcd3f1b6980d',
12 name='subgraph_node_2',
13 path=('__pregel_pull', 'subgraph_node_2'),
14 error=None,
15 interrupts=(
16 Interrupt(
17 value='输入值:',
18 id='f62f6bce645a53af213c432eee562e49'
19 ),
20 ),
21 state=None,
22 result=None
23 ),
24 ),

25 interrupts=(Interrupt(value='输入值:',
id='f62f6bce645a53af213c432eee562e49'),)
26 )
27 sub_node_2
28 {'foo': 'bar'}
3.4.2 恢复时的注意事项
之前讲过，当节点恢复执行时，发起中断的节点会从头再跑一遍。因此，对于中断前的代码，会多重
复执行！
而在子图场景下，子图的不同调用方式有不同的执行结果。
3.4.2.1 将子图作为节点时
上面的例子就是将子图作为节点的示例，去掉状态看看调用结果：
代码块
1 sub_node_1
2 sub_node_2
3 sub_node_2
4 {'foo': 'bar'}

由于是 节点发起中断调用，我们可以看到 节点被调用两
subgraph_node_2 subgraph_node_2
次，符合预期。
3.4.2.2 节点内调用子图时
但当是节点内调用子图时：
• 父图将从调用子图并触发中断的节点的开头恢复执行。
• 同样，子图也将从调用中断的节点的开头恢复。
修改下代码：
代码块
1 from langgraph.graph import START, StateGraph
2 from langgraph.checkpoint.memory import InMemorySaver
3 from langgraph.types import interrupt, Command
4 from typing_extensions import TypedDict
5
6 class State(TypedDict):
7 foo: str
8
9 # 子图
10 def subgraph_node_1(state: State):
11 print("sub_node_1")
12 return {}
13
14 def subgraph_node_2(state: State):
15 print("sub_node_2")
16 value = interrupt("输入值:")
17 return {"foo": state["foo"] + value}
18
19 subgraph_builder = StateGraph(State)
20 subgraph_builder.add_node(subgraph_node_1)
21 subgraph_builder.add_node(subgraph_node_2)
22 subgraph_builder.add_edge(START, "subgraph_node_1")
23 subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
24 subgraph = subgraph_builder.compile()
25
26 # 主图
27 def node_1(state: State):
28 print("node_1")
29 response = subgraph.invoke({"foo": state["foo"]})
30 return {"foo": response["foo"]}
31
32 builder = StateGraph(State)
33 builder.add_node("node_1", node_1)

34 builder.add_edge(START, "node_1")
35
36 graph = builder.compile(checkpointer=InMemorySaver())
37
38 config = {"configurable": {"thread_id": "1"}}
39 graph.invoke({"foo": ""}, config)
40 print(graph.invoke(Command(resume="bar"), config))
打印结果:
代码块
1 node_1
2 sub_node_1
3 sub_node_2
4 node_1 # 主图节点重新执行
5 sub_node_2 # 子图节点重新执行
6 {'foo': 'bar'}
可以看到不仅是调用中断的子图节点重新执行，就连调用子图的主图节点也会被重新调用！
六、综合案例--AI智能租房助手
1. 案例需求说明
1.1 案例演示

1.2 项目能力说明
1.2.1 房源推荐
• 通过对话分析用戶需求（预算、地段、通勤、戶型偏好等），实时筛选并推荐房源。
• 展示思考过程，如调用了哪些工具、工具调用结果，体现对话结果准确性。
• 若用戶需求模糊（如“给我推荐房子”），智能体会追问具体需求（“为了给您推荐合适的房源，
请提供以下信息....”）。

1.2.2 房源预定
• 支持直接预定，也可以通过房源推荐引导预定。
• 引导合同签署，自动生成代办清单（如“下一步需上传身份证号码”）。
1.2.3 查询我的
• 支持跨会话查询用戶历史预算、已租房源信息

1.2.4 常规问答
• 支持进行常规问答
1.3 涉及知识点
• 对话式交互
• LangGraph 图，包括状态、节点、边和条件边
• 子图与子图中断

• 线程级持久化与跨会话持久化
• 内存存储与 Postgres 存储
• 路由模式
• 读取 SQL 数据库的工具
• 人机交互（中断）
• 运行时上下文
• 多种流模式混合输出
• LangGraph 项目结构
• LangGraph 生态部署
2. 搭建一个 LangGraph 项目
我们可以自行搭建 Python 服务，基于 LangGraph 图调用（自己制定协议）提供对外服务。也可以使
用 LangChain 生态中 LangSmith Deployment 部署应用程序，这需要我们准备一个结构化的项目。
这里我们选择后者。
LangSmith Deployment 构建在开源的 LangGraph 框架上，用于开发有状态的应用程序。
LangGraph 提供核心抽象和执行模型，而 LangSmith 支持从开发到生产的整个生命周期，
LangSmith 增加了托管基础设施、可观察性、部署选项、助手和并发控制等能力。
2.1 搭建项目
2.1.1 步骤1：安装 LangGraph CLI
使用 pip 安装  （需 Python 3.11 或更高版本）。
langgraph-cli[inmem]
代码块
1 pip install -U "langgraph-cli[inmem]"
2
3 # 验证安装情况
4 langgraph --help
LangGraph CLI 是用于构建和运行 LangGraph 应用程序的命令行工具。LangGraph CLI 提供了如下
指令：
指令  解释

langgraph dev 启动一个轻量级本地开发服务器（无需 Docker），非常适合快速测试。
langgraph build 构建你的 LangGraph API 服务器的 Docker 镜像以便部署。
langgraph 它会根据你的配置导出一个 Docker 文件，用于自定义构建。
dockerfile
langgraph up 在本地 Docker 启动 LangGraph API 服务器。需要运行 Docker; 本地开发用
LangSmith API 密钥。
由此产生的服务器公开了：
• 助手（Assistants）：是图的配置实例
• 线程（Threads）：线程包含一组运行的累积输出。实际表示为一组会话。
• 线程执行（Thread Runs）：运行是对线程上的图形/助手的调用。它更新线程的状态。
公开的所有 API 端点见这里。可以看到也包括用于检查点和存储的托管数据库。
2.1.2 步骤2：创建应用
使用   命令从指定模板创建新应用。
langgraph new
• 方式1：创建时不指定具体模板。而是通过交互式菜单，允许你从可用模板列表中选择。
可以选择的模板有：
1. 新 LangGraph 项目：一个简单、精简且具有记忆功能的聊天机器人。
2. ReAct 代理：一种简单且可灵活扩展至多种工具的代理。
3. 记忆代理：一种采用 ReAct 风格的代理，额外配备了一个工具，用于存储记忆，以便在不同对话
线程间使用。
4. 检索代理：包含基于检索的问答系统的代理。
5. 数据丰富代理：一种执行网络搜索并将搜索结果整理成结构化格式的代理。

• 方式2：用   模板创建一个新应用。这个模板展示了一个单
new-langgraph-project-python
节点应用，你可以用自己的逻辑进行扩展。
代码块
1 langgraph new path/to/your/app --template new-langgraph-project-python
【项目结构】见下文，这里先不讲解。
项目创建完成后，可以使用 PyCharm 打开项目。
2.1.3 步骤3：安装依赖
进入应用目录，以编辑模式安装依赖。
代码块
1 cd path/to/your/app
2 pip install -e .
环境准备可能遇到的问题：由于 Debian/Ubuntu 等系统从 Python 3.11 开始引入了新的保护机制，为
了保护 Python 环境不被意外破坏，默认禁止直接使用   安装包到系统 Python。
pip install
解决：
• 使用虚拟环境（推荐）
• 在   命令后添加   参数强制覆盖系统保护（不推
pip install --break-system-packages
荐，急用可临时使用）
2.1.4 步骤4：配置环境
复制   文件为  ，并填入必要的  。
.env.example .env LANGSMITH_API_KEY

代1 码块LA NGSMITH_PROJECT=new-agent
2
3 LANGSMITH_API_KEY=lsv2_....
4 LANGSMITH_TRACING=true
5
6 OPENAI_API_KEY=...
2.1.5 步骤5：查看并启动服务器
可以看到，这个模板展示了一个单节点 Graph，可以用自己的逻辑进行扩展。
除此之外，要构建和运行一个有效的应用程序，LangGraph CLI 需要遵循一个 配
langgraph.json
置文件（该配置文件下文会讲）。其中必须要配置 ：从图 ID （ ）映射到定义已
"graphs" agent
编译图（ ）路径。如下所示：
./src/agent/graph.py:graph

运行   命令启动本地开发服务器（输出中会提供 API 和 Studio UI 地址）。
langgraph dev
命令会以内存模式启动 Agent Server。该模式适合开发和测试。
langgraph dev
❗注意：如果启动过程有报错，如下所示。请检查你的 版本是否为 （该
langgraph-api 0.7.19
版本有bug）。如果是请修改为其它版本即可，如 。
0.7.18
代码块
1 报错：Traceback (most recent call last):

2 File "D:\Python313\Lib\site-packages\starlette\routing.py", line 694, in
lifespan
3 async with self.lifespan_context(app) as maybe_state:
4 ~~~~~~~~~~~~~~~~~~~~~^^^^^
5 File "D:\Python313\Lib\contextlib.py", line 214, in __aenter__
6 return await anext(self.gen)
7 ^^^^^^^^^^^^^^^^^^^^^
8 File "D:\Python313\Lib\site-packages\langgraph_api\timing\timer.py", line
227, in combined_lifespan
9 await stack.enter_async_context(ls(app))
10 File "D:\Python313\Lib\contextlib.py", line 668, in enter_async_context
11 result = await _enter(cm)
12 ^^^^^^^^^^^^^^^^
13 File "D:\Python313\Lib\contextlib.py", line 214, in __aenter__
14 return await anext(self.gen)
15 ^^^^^^^^^^^^^^^^^^^^^
16 File "D:\Python313\Lib\site-packages\langgraph_runtime_inmem\lifespan.py",
line 110, in lifespan
17 await graph.collect_graphs_from_env(True)
18 File "D:\Python313\Lib\site-packages\langgraph_api\graph.py", line 485, in
collect_graphs_from_env
19 await register_graph(
20 spec.id, graph, spec.config, description=spec.description
21 )
22 File "D:\Python313\Lib\site-packages\langgraph_api\graph.py", line 97, in
register_graph
23 await register_graph_db()
24 File "D:\Python313\Lib\site-packages\langgraph_runtime_inmem\retry.py", line
27, in wrapper
25 return await func(*args, **kwargs)
26 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
27 File "D:\Python313\Lib\site-packages\langgraph_api\graph.py", line 83, in
register_graph_db
28 await Assistants.put(
29 ~~~~~~~~~~~~~~^
30 conn,
31 ^^^^^
32 ...<8 lines>...
33 system=True,
34 ^^^^^^^^^^^^
35 )
36 ^
37 TypeError: Assistants.put() got an unexpected keyword argument 'system'
38 [uvicorn.error] api_variant=local_dev langgraph_api_version=0.7.19
thread_name=MainThread

39 2026-02-05T03:15:42.073224Z [error ] Application startup failed. Exiting.
[uvicorn.error] api_variant=local_dev langgraph_api_version=0.7.19
thread_name=MainThread
2.1.6 步骤6：在 Studio 中测试
通过输出的 URL 在 LangGraph Studio 中可视化并调试你的应用。Studio 是一个图形界面，用于与你
的 Agent Server 交互。它不会持久化任何私有数据（你发送到服务器的数据不会发送到
LangSmith）。虽然 Studio 接口在 smith.langchain.com 提供，但它运行在浏览器中，并直接连接到
本地 Agent Server。
2.1.7 步骤7：测试 API
可以通过 Python SDK（异步/同步） 或直接发送 REST API 请求来测试应用功能。
• 对于 Python SDK，使用 先进行安装，再通过其内置接口进行
pip install langgraph-sdk
访问。
• 对于 REST API，接口文档已经由 LangGraph CLI 提供好了，点击 API Docs 即可查看。

由于我们要完成一个 web 应用，案例将不采用 SDK 方式调用，而是选择 REST API 请求。它们的概
念、使用流程都一样，只是使用姿势不一样，一通百通。
接下来参考 API Docs，使用 API Docs 提供的工具或 Apifox 进行测试。如下所示：
• 创建会话线程： • 基于线程发起流式调用：
流式调用常见的 有：
stream_mode
Mode  模式  Description  描述
values 在每个超级步骤后流式传输完整的图状态。
updates 在图的每一步后，将更新状态。如果同一步进行多次更新（例如运行多个节点），这
些更新会分别流式传输。
messages  or  流式传输 LLM 令牌和元数据，用于调用 LLM 的图节点（对聊天应用非常有用）。
messages-tuple
custom 从你的图内部流式传输自定义数据
events 流式传输所有事件（包括图表状态）;主要用于迁移大型 LCEL 应用。

也可以把列表作为   参数传递，同时流放多个模式（如
stream_mode "stream_mode":
）。
["updates", "messages"]
这里还需要注意流式返回的结构，服务器会以 SSE 格式发送一系列事件：
代码块
1 event: metadata
2 data: {"run_id":"019ba0cd-d6b7-7ce0-87b9-d28d2f0c756d","attempt":1}
3 id: 1767929403693-0
4
5 event: updates
6 data: {"call_model":{"changeme":"output from call_model. Configured with
None"}}
7 id: 1767929403699-0
• ：该流部分的事件类型
event
• ：与事件相关的数据负载
data
• ：事件的ID
id
Event 与 data 的值与我们传入的 流模式有关，上面我们传了 ，换
stream_mode "update"
成 再看（用 API Docs 进行测试），如下所示：
"values"
常见返回的 event 有：
• 事件为 ，data 中会包含图节点和 LLM 调用细节及其他信息。
metadata
• 事件为 ，data 中会包含每个节点更新的状态。
updates
• 事件为 ，data 中会包含每个节点最新的状态。
values

• 事件为 ，data 中会包含来自聊天模型调用的单个 LLM 令牌。
messages
• ......
2.2 项目结构说明
要使用 LangSmith Deployment 部署应用程序，需要准备一个结构化的项目。一个可部署的
LangSmith 应用必须包含以下四个部分：
• 一个或多个图：承载应用程序的核心逻辑。
• 配置文件 ( )：定义应用的依赖项、图和环境变量。
langgraph.json
• 依赖文件：声明项目所需的包或库（如  ,  ）。
requirements.txt pyproject.toml
• 环境变量文件 (可选，  )：存放环境变量配置信息。
.env
项目文件结构示例：
代码块
1 my-app/
2 ├── .env # 环境变量
3 ├── langgraph.json # 配置文件
4 ├── pyproject.toml # 管理项目元数据，指定依赖关系
5 └── src # src 下面是包名，包下面是业务代码，所有的项目代码都在这里
6 └─agent
7 │ graph.py # 构造 graph 的代码
8 └─ __init__.py
2.3 pyproject.toml 配置文件
 配置文件是现代 Python 项目的标准配置文件，替代了传统的   和
pyproject.toml setup.py
 文件。主要用于：
requirements.txt
• 项目元数据定义（名称、版本、作者等）
• 依赖管理（生产依赖和开发依赖）
• 构建系统配置
• 代码质量工具配置（如ruff代码检查器）
下面对于  配置信息进行说明：
pyproject.toml
1. [project] - 项目基本信息
代码块

1 name = "agent" # 项目名称
2 version = "0.0.1" # 项目版本号
3 description = "Starter template for making a new agent LangGraph." # 项目描述
4 readme = "README.md" # 项目说明文档
5 license = { text = "MIT" } # 许可证类型（MIT许可证）
6 requires-python = ">=3.10" # 支持的Python版本（3.10及以上）
2. [project.dependencies] - 生产环境依赖
代码块
1 # 以下列举了本次案例中需要用到的依赖包
2 dependencies = [
3 "langchain>=1.0.5",
4 "langchain_openai>=1.0.2",
5 "langchain-community>=0.4.1",
6 "langgraph>=1.0.0",
7 "langgraph-checkpoint>=3.0.1",
8 "langgraph-checkpoint-postgres>=3.0.2",
9 "langgraph-cli>=0.4.11",
10 "python-dotenv>=1.0.1", # 环境变量管理工具
11 "PyMySQL>=1.1.2",
12 "numpy>=2.3.4",
13 "pycryptodome>=3.23.0",
14 ]
3. [project.optional-dependencies] - 可选依赖（按组）
代码块
1 dev = ["mypy>=1.11.1", "ruff>=0.6.1"] # 开发依赖：类型检查 + 代码检查工具
4. [build-system] - 构建系统配置
代码块
1 requires = ["setuptools>=73.0.0", "wheel"] # 构建所需工具
2 build-backend = "setuptools.build_meta" # 构建后端（setuptools）
5. [tool.setuptools] - 包目录结构配置
代码块
1 packages = ["langgraph.templates.agent", "agent"] # 包含的Python包

2 [tool.setuptools.package-dir] # 包目录映射
3 "langgraph.templates.agent" = "src/agent" # 将源代码映射到指定目录
4 "agent" = "src/agent"
5 [tool.setuptools.package-data]
6 "*" = ["py.typed"] # 包含类型提示文件（支持类型检查）
6. [tool.ruff] - Ruff代码检查器配置
Ruff是一个快速的Python代码检查工具，集成了多种检查器。
代码块
1 lint.select = [ # 启用的检查规则
2 "E", # pycodestyle（PEP8代码风格检查）
3 "F", # pyflakes（语法和逻辑错误检查）
4 "I", # isort（导入排序检查）
5 "D", # pydocstyle（文档字符串检查）
6 "D401", # 要求文档字符串第一行用命令式语气
7 "T201", # 打印语句检查
8 "UP", # pyupgrade（自动升级Python语法）
9 ]
10
11 lint.ignore = [ # 忽略的规则
12 "UP006", # 忽略"建议使用list[]而非typing.List"的警告
13 "UP007", # 忽略"建议使用dict[]而非typing.Dict"的警告
14 "UP035", # 允许从typing_extensions导入
15 "D417", # 不要求每个函数参数都有文档
16 "E501", # 忽略行长度限制
17 ]
18
19 [tool.ruff.lint.per-file-ignores]
20 "tests/*" = ["D", "UP"] # 测试文件中忽略文档检查和语法升级检查
21
22 [tool.ruff.lint.pydocstyle]
23 convention = "google" # 使用Google风格的文档字符串格式
7. [dependency-groups] - 依赖组（开发依赖）
代码块
1 dev = [
2 "anyio>=4.7.0", # 异步IO库
3 "langgraph-cli[inmem]>=0.4.7", # LangGraph命令行工具（带内存后端）
4 "mypy>=1.13.0", # 静态类型检查器
5 "pytest>=8.3.5", # 测试框架
6 "ruff>=0.8.2", # 代码检查器

7 ]
可以看到，这是一个 LangGraph 项目模板配置，用于快速创建基于 LangGraph 框架的 AI 应用。项目
结构主要包含：
• 源代码位于   目录
src/agent/
• 支持类型提示（包含   文件）
py.typed
• 使用了现代 Python 开发工具链（ruff、mypy、pytest等）
2.4 langgraph.json 配置文件
要使用 LangSmith Deployment 部署应用程序，核心是通过一个配置文件将各个组件整合起来。默认
情况下，CLI 会在当前目录查找名为   的文件。
langgraph.json
下表汇总了配置文件的主要字段。
配置键  是否必需  类型/选项  描述与示例
$schema 必需  字符串  指向 JSON Schema 以进行验证，例
如： "https://langgra.ph/schema.json"
dependencie 必需  数组  项目依赖。可以是：
s
1. 单个点  "." ：查找本地 Python 包。
2. 目录路径：如  "./"  或  "./local_package" ，该目录
需包含  pyproject.toml 、 setup.py  或
requirements.txt 。
3. Python 包名。
graphs 必需  对象  图定义映射。格式为  {"图ID": "文件路径:导出对象"} 。
• 示例： { "chat": "./chat.graph:graph" }
auth 可选  对象  自定义认证配置（v0.0.11+）。需指定认证处理器路径。
• 示例： { "path": "./auth.py:auth", ... }
base_image 可选  字符串  基础 Docker 镜像。默认为  langchain/langgraph-api 。
可用于固定版本，例如  "langchain/langgraph-
server:0.2" 。
image_distr 可选  枚举  基础镜像的 Linux 发行版。可选： "debian" （默
o  (>=0.2.11) 认）、 "wolfi" 、 "bookworm" 、 "bullseye" 。推荐使
用更安全的  "wolfi" 。

env 可选  字符串或对 环境变量配置。可以是  .env  文件路径，或直接是键值对映
象  射。
store 可选  对象  存储配置，用于添加语义搜索和/或设置存活时间。
• index ：语义搜索索引配置（需指定  embed  嵌入模
型、 dims  维度、 fields  字段）。
• ttl ：数据过期配置（可设置  refresh_on_read 、
default_ttl 、 sweep_interval_minutes ）。
checkpointe 可选  对象  检查点配置。
r
• ttl ：检查点过期策略（ strategy ,
sweep_interval_minutes ,  default_ttl ）。
• serde  (Agent server 0.5+)：反序列化行为控制
（ allowed_json_modules ,  pickle_fallback ）。
http 可选  对象  HTTP 服务器配置。可配置自定义应用 ( app )、CORS、中间
件顺序 ( middleware_order )、可配置头、挂载前缀
( mount_prefix ) 等。
webhooks   可选  对象  出站 Webhook 配置。包含  env_prefix 、 headers （静
(v0.5.36+)  态请求头）、 url （URL验证策略）等。
python_vers 可选  字符串  Python 版本。可选  "3.11" （默认）、 "3.12"  或
ion "3.13" 。
node_versio 可选  字符串  Node.js 版本。如需使用 LangGraph.js，可设为  "20" 。
n
pip_install 可选  枚举  Python 包安装器。可选  "auto" （默认，使用  uv
er  (v0.3+)  pip ）、 "pip"  或  "uv" 。
api_version 可选  字符串  LangGraph API 服务器语义版本（如  "0.3" ）。默认为最新
 (v0.3.7+)  版。
• 版本注意：部分配置键有最低 CLI 版本要求，已在表中标出（如   需 langgraph-
image_distro
cli >=0.2.11）。
• 示例参考：官方提供了多个完整配置示例，例如“基础配置”、“使用 Wolfi 基础镜像”、“为存
储添加语义搜索”、“配置存储项 TTL”等，是极佳的入门参考。
• 自定义嵌入：  字段除了使用预置模型名（如
store.index.embed "openai:text-
），还支持指向自定义嵌入函数的本地路径（如
embedding-3-small"
）。
"./embeddings.py:embed_texts"

3. 案例思路解析
3.1 整体思路--五步构建法
构建 LangGraph 系统的核心是将流程分解为离散的节点，通过共享的状态连接，每个节点可读取和写
入状态，并自主决定后续路径。
第一步：工作流分解
• 将流程拆分为独立步骤，每个步骤成为一个节点。如有复杂操作，可拆分为子图处理。
• 绘制节点间连接关系
第二步：节点功能识别
• LLM节点：用于理解、分析、生成文本或推理决策
• 数据节点：从外部源检索信息
• 动作节点：执行外部操作
• 用戶输入节点：需要人工干预
第三步：状态设计
• 状态是共享内存，所有节点均可访问
• 只存储原始数据，不存储格式化文本或提示模板
• 设计原则：
◦ 跨步骤需要持久化的数据才存入状态
◦ 可从其他数据推导的信息不存储
第四步：节点实现
• 每个节点是接收状态并返回更新的函数
• 使用 对象指定状态更新和下一节点
Command
• 错误处理策略：
◦ 瞬时错误（网络问题）：自动重试
◦ LLM可恢复错误：将错误存入状态，让LLM重试
◦ 用戶可修复错误：使用 暂停等待人工输入
interrupt()
◦ 意外错误：抛出供调试
第五步：连接组装
• 添加节点和必要边
• 使用检查点器（checkpointer）实现持久化，支持暂停/恢复
• 编译为可执行应用

3.2 按功能模块拆分为多图
根据案例需求（房源推荐、房源预定、查询我的、常规问答），可以将不同的能力拆分为不同的子图
完成。如：
• 推荐子图：负责进行房源推荐，包括查询数据库，根据条件推荐合适的房
recommended_graph
源。
• 预定子图：负责房源预定，生成工单。
reserve_graph
• 其它子图：负责其它问题处理，如常规问答等。
extend_graph
除此之外，我们还需要一个主图负责路由，判定用戶请求该路由到哪个子图中去执行具体逻辑处理。
3.3 主图--智能分流
节点设计如下：
• 节点：查询持久化消息，例如用戶历史偏好数据。
get_store_info
• 节点：识别用戶输入的问题，进行智能路由。
identify_question
• 子图节点：路由1，进行房源推荐
recommended_graph
• 子图节点：路由2，预定房源子图
reserve_graph
• 子图节点：路由3，其它问题处理，如常规问答等。
extend_graph
• 节点：路由4，用戶查询自己的信息
get_user_preferences
• 节点：是否需要预定房源。当推荐房源结束后，主动咨询是否需要预定房源。
need_reserve

3.4 推荐子图--构建自定义 SQL 代理
节点设计如下：
• 节点：收集用戶希望推荐的房源关键信息
collect_user_info
• 节点：调用 SQL 工具，查询表有哪些
list_tables
• 节点：LLM 绑定 工具，强制调用 工具
call_get_schema get_schema get_schema
• 节点：执行工具，获取表的详细信息，如表结构、示例数据等
get_schema
• 节点：LLM 绑定 工具，非强制工具调用。用来生成查询 SQL 或
generate_query run_query
生成最终结果
• 节点：LLM 绑定 工具，强制调用 工具。
check_query run_query run_query
• 节点：执行工具，用来运行 节点生成的 SQL，检测 SQL 是否正
run_query generate_query
确

3.5 预定子图--人工介入的预定系统
节点设计如下：
• 节点：中断获取要预定的房源标题
get_title
• 节点：中断获取预定人的电话
get_phone
• 节点：中断获取预定人的身份证
get_id
• 节点：构造并添加预定消息
add_reserve_message
• 节点：LLM 绑定生成工单的工具
call_orders
• 节点：生成工单的工具
tool_node
3.6 扩展子图--除业务外的智能问答助手

节点设计如下：
• 节点：LLM 对话助手
extend_node
4. 案例开发
4.1 通用设计
4.1.1 LLM
在案例中，无论主图还是子图，涉及到 LLM 调用统一使用 OpenAI。
llm.py
1 from langchain.chat_models import init_chat_model
2
3 model = init_chat_model("gpt-4o-mini", temperature=0)
4.1.2 持久化存储
本案例中，由于我们要收集用戶偏好信息与历史预定信息，因此要使用持久化存储。
定义存储值的结构：

s1toref.pryo m typing import Optional
2
3 from pydantic import BaseModel, Field
4
5 class ReservedInfo(BaseModel):
6 """房源的预定信息"""
7 order_id: str = Field(description="预定id")
8 title: str = Field(description="预定的房源标题")
9 phone_number: str = Field(description="预定电话")
10
11 price: Optional[float] = Field(
12 default=None,
13 description="预定的房源价格，单位为元/月"
14 )
15 intro: Optional[str] = Field(
16 default=None,
17 description="预定的房源介绍"
18 )
19 city_name: Optional[str] = Field(
20 default=None,
21 description="预定的房源所在城市名"
22 )
23 region_name: Optional[str] = Field(
24 default=None,
25 description="预定的房源所在区/县"
26 )
27
28 class UserPreferences(BaseModel):
29 """用戶偏好信息"""
30 budget_min: Optional[float] = Field(
31 default=None,
32 description="用戶的最低预算，单位为元/月"
33 )
34 budget_max: Optional[float] = Field(
35 default=None,
36 description="用戶的最高预算，单位为元/月"
37 )
38 reserved_info: Optional[list[ReservedInfo]] = Field(
39 default=None,
40 description="预定过的房源列表"
41 )
42
将来可以在节点中获取或添加持久化信息，如下所示：
代码块

1 def node(state: State, runtime: Runtime[ContextSchema], *, store: BaseStore):
2 # 1. 通过 Namespace 获取用戶偏好数据
3 namespace = (user_id, "preferences")
4
5 # 2. 查询
6 prefs_result = store.search(namespace)
7
8 # 3. 存储
9 prefs = UserPreferences(
10 budget_min=updated_state.get('budget_min'),
11 budget_max=updated_state.get('budget_max'),
12 )
13 store.put(
14 namespace,
15 str(uuid.uuid4()),
16 prefs.model_dump(exclude_none=True)
17 )
4.1.3 运行时上下文
由于获取用戶偏好数据时，构建的 Namespace 需要根据用戶id进行区分。则可以将用戶id添加进上下
文，单次运行时可根据用戶id获取用戶持久化信息。
content.py
1 from typing import TypedDict
2
3 class ContextSchema(TypedDict):
4 user_id: str
将来可以在节点中获取上下文信息，如下所示：
代码块
1 def node(state: State, runtime: Runtime[ContextSchema], *, store: BaseStore):
2 user_id = runtime.context.get("user_id")
4.2 主图--智能分流

4.2.1 状态定义
• 主状态 ：全局共享状态。状态继承自 ，自动管理对话历史。
State MessagesState
◦ ：用戶意图，表示用戶输入的问题含义（推荐 or 预定 or 查询 or 其它）
user_intent
◦ ：用戶偏好信息，实现数据共享
user_preferences
• 节点间传输私有状态 ：当推荐子图执行完成后，用戶获取用戶是否想要
NeedReserveOutput
预定房源的意向。从而决定是否执行预定子图。
state/main.py
1 from typing import TypedDict
2
3 from langgraph.graph import MessagesState
4
5 class State(MessagesState):
6 user_intent: str # 用戶意图
7 user_preferences: dict # 用戶偏好
8
9 class NeedReserveOutput(TypedDict):
10 reserve: str # 这个字段不会出现在最终状态中
4.2.2 工作流定义
注意，编译 graph 时，无需设置 checkpointer 和 store。将来进行 LangSmith 部署时，持久化可以通
过配置进行设置。

g1raphf.rpoym  typing import Literal
2
3 from langgraph.constants import START, END
4 from langgraph.graph import StateGraph
5
6 from src.agent.common.content import ContextSchema
7 from src.agent.extend import extend_graph
8 from src.agent.node.main import get_store_info, identify_question,
need_reserve, get_user_preferences
9 from src.agent.recommend import recommended_graph
10 from src.agent.reserve import reserve_graph
11 from src.agent.state.main import State, NeedReserveOutput
12
13 # 构建图
14 builder = StateGraph(State, context_schema=ContextSchema)
15 builder.add_node(get_store_info) # 查询持久化消息
16 builder.add_node(identify_question) # 识别用戶输入的问题
17 builder.add_node("recommended_graph", recommended_graph) # 推荐房源子图, 注意
需要指定名称
18 builder.add_node(need_reserve) # 是否需要预定房源
19 builder.add_node("reserve_graph", reserve_graph) # 预定房源子图
20 builder.add_node("extend_graph", extend_graph) # 待扩展子图
21 builder.add_node(get_user_preferences)
22
23 builder.add_edge(START, "get_store_info")
24 builder.add_edge("get_store_info", "identify_question") # 识别问题
25 def router_message(state: State) -> Literal["recommended_graph",
"reserve_graph", "extend_graph", "get_user_preferences"]:
26 user_intent = state["user_intent"]
27 if user_intent == "recommend_house":
28 return "recommended_graph"
29 elif user_intent == "reserve_house":
30 return "reserve_graph"
31 elif user_intent == "get_info":
32 return "get_user_preferences"
33 else:
34 return "extend_graph"
35
36 builder.add_conditional_edges(
37 "identify_question",
38 router_message, # 消息路由。
39 ["recommended_graph", "reserve_graph", "extend_graph",
"get_user_preferences"]
40 )
41
42 # 路由1：推荐房源-》（中断询问）预定房源
43 builder.add_edge("recommended_graph", "need_reserve")

44 def should_reserve(state: NeedReserveOutput) -> Literal[END, "reserve_graph"]:
45 reserve = state["reserve"]
46 if reserve == '需要':
47 return "reserve_graph"
48 else:
49 return END
50 builder.add_conditional_edges(
51 "need_reserve",
52 should_reserve, # 不需要预定就结束对话
53 [END, "reserve_graph"]
54 )
55
56 # 路由2：预定房源
57 builder.add_edge("reserve_graph", END)
58
59 # 路由3：查询我的信息
60 builder.add_edge("get_user_preferences", END)
61
62 # 路由4：其它
63 builder.add_edge("extend_graph", END)
64 graph = builder.compile()
4.2.3 节点实现
node/main.py
1 from typing import Literal
2
3 from langchain_core.messages import SystemMessage, HumanMessage,
filter_messages, AIMessage
4 from langgraph.runtime import Runtime
5 from langgraph.store.base import BaseStore
6 from langgraph.types import interrupt
7 from pydantic import BaseModel, Field
8
9 from src.agent.common.content import ContextSchema
10 from src.agent.common.llm import model
11 from src.agent.state.main import State, NeedReserveOutput
12
13 class UserMessage(BaseModel):
14 """用戶提问的消息摘要"""
15 type: Literal["recommend_house", "reserve_house", "get_info", "others"] = (
16 Field(description="根据用戶问题描述判断问题类型：推荐房源、预定房源、获取信息、
其他内容"))

17
18 # 节点：识别用戶问题：预定、推荐、我的
19 def identify_question(state: State):
20
21 def extract_info(messages) -> UserMessage:
22 system_message = SystemMessage(
23 content="""
24 你是一个根据描述提取信息提取专家。请从用戶的描述中提取用戶想要咨询的相关信息。
25 严谨根据语义推断信息，但不能猜测或编造信息。"""
26 )
27 # 创建结构化提取模型
28 return (model.with_structured_output(schema=UserMessage)
29 .invoke([system_message] + messages))
30
31 # 最新的用戶消息
32 user_question = state["messages"][-1].content
33 user_message = extract_info([HumanMessage(content=user_question)])
34 return {"user_intent": user_message.type}
35
36 # 节点：查询持久化消息
37 def get_store_info(state: State, runtime: Runtime[ContextSchema], *, store:
BaseStore):
38 # 搜索用戶信息
39 user_id = runtime.context.get("user_id")
40 namespace = (user_id, "preferences")
41 pref_result = store.search(namespace)
42 if pref_result and pref_result[0]:
43 return {"user_preferences": pref_result[0].value}
44 else:
45 return {}
46
47 # 节点：中断询问是否主要帮助预定房源
48 def need_reserve(state: State) -> NeedReserveOutput:
49 prompt = f"已经为您推荐合适的房源，是否需要帮您预订房源？\n"
50 prompt += "如果不需要，请输入'**不需要**'。\n"
51 prompt += "如果需要，请输入'**需要**'。\n(注意输入其它值无效)"
52 # 中断，等待用戶输入
53 answer = interrupt(prompt)
54 return {"reserve": str(answer).strip()}
55
56 # 节点：返回用戶偏好信息
57 def get_user_preferences(state: State):
58 prefs = state.get("user_preferences", {})
59 user_messages = filter_messages(state["messages"], include_types="human")
60
61 # 格式化已预定过的信息
62 reserved_list = prefs.get('reserved_info', [])

63 if reserved_list:
64 reserved_str = "\n"
65 for i, item in enumerate(reserved_list, 1):
66 reserved_str += f"{i}. 预定工单ID: {item.get('order_id')}, " \
67 f"房源标题: {item.get('title')}, " \
68 f"预定电话: {item.get('phone_number')}\n"
69 else:
70 reserved_str = "无"
71
72 response = model.invoke([
73 SystemMessage(content="""你是一个乐于助人的助手，可以根据用戶偏好信息进行回
复。
74 如果有的偏好数据为空，不要猜测或编造数据。
75 不要直接回复偏好数据是什么，要结合问题进行生动回复。
76 如果问题与用戶偏好数据无关，直接回复即可。"""),
77 HumanMessage(
78 content="用戶的历史偏好信息如下："
79 f"1. 最低预算：{prefs.get('budget_min')}"
80 f"2. 最高预算：{prefs.get('budget_max')}"
81 f"3. 已预定过的信息：{reserved_str}"
82 ),
83 user_messages[-1]
84 ])
85 return {"messages": [response]}
86
4.3 推荐子图--构建自定义 SQL 代理

4.3.1 状态定义
state/recommend.py
1 from langgraph.graph import MessagesState
2
3 # 推荐房源状态
4 class RecommendState(MessagesState):
5 # 用戶偏好(数据共享)
6 user_preferences: dict
7 # 以下是推荐的关键参数
8 city: str # 城市
9 budget_min: float # 最低预算
10 budget_max: float # 最高预算
11 district: str # 区域
12 room_type: str # 房屋类型
13 orientation: str # 朝向
14 room_count: int # 推荐数量
15 others: str # 其它要求
16
17 # 获取推荐信息方法

18 def get_recommend_info(state: dict) -> str:
19 info_prompt = """
20 提取用戶期望推荐的房源信息如下：
21 - 城市: {city}
22 - 区域: {district}
23 - 预算: {budget_min} - {budget_max} 元/月
24 - 房屋类型: {room_type}
25 - 朝向: {orientation}
26 - 特殊要求: {others}
27 - 推荐数量: {room_count}
28 如果某些信息未指定，请使用合适的默认值或放宽条件。"""
29 return info_prompt.format(
30 city=state.get('city', '未指定'),
31 district=state.get('district', '未指定'),
32 budget_min=state.get('budget_min', '未指定'),
33 budget_max=state.get('budget_max', '未指定'),
34 room_type=state.get('room_type', '未指定'),
35 orientation=state.get('orientation', '未指定'),
36 others=state.get('others', '无'),
37 room_count=state.get('room_count', 5)
38 )
39
4.3.2 工作流定义
1. 收集用戶信息 → 2. 列出数据库表 → 3. 获取表结构 → 4. 生成SQL查询 → 5. 检查查询 → 6. 执行查询
→ 7. 返回结果
代码块
1 from typing import Literal
2
3 from langgraph.graph import END, START, StateGraph
4
5 from src.agent.common.content import ContextSchema
6 from src.agent.node.recommend import (
7 collect_user_info,
8 list_tables,
9 call_get_schema,
10 get_schema_node,
11 generate_query,
12 check_query,
13 run_query_node
14 )
15 from src.agent.state.recommend import RecommendState

16
17 # 构建图
18 builder = StateGraph(RecommendState, context_schema=ContextSchema)
19 builder.add_node(collect_user_info) # 收集用戶信息节点
20 builder.add_node(list_tables) # 调用sql_db_list_tables工具
21 builder.add_node(call_get_schema) # LLM绑定sql_db_schema工具，强制
工具调用
22 builder.add_node("get_schema", get_schema_node) # sql_db_schema工具
23 builder.add_node(generate_query) # LLM绑定sql_db_query工具，非强
制工具调用
24 builder.add_node(check_query) # LLM绑定sql_db_query工具，强制
工具调用
25 builder.add_node("run_query", run_query_node) # sql_db_query工具
26
27 # 添加边
28 builder.add_edge(START, "collect_user_info") # 从开始节点到用戶信息收集节
点
29 builder.add_edge("collect_user_info", "list_tables") # 用戶信息收集完成后，获取所
有表
30 builder.add_edge("list_tables", "call_get_schema") # LLM：（强制调用
sql_db_schema工具），确保这些表确实存在，且过滤出需要的表
31 builder.add_edge("call_get_schema", "get_schema") # 工具：输出需要的表的模式和
示例行
32 builder.add_edge("get_schema",
33 "generate_query") # LLM：（非强制调用sql_db_query工具）给定一个输
入问题，创建一个语法正确的{dialect}查询来运行，然后查看查询的结果并返回答案。
34 def should_continue(state: RecommendState) -> Literal[END, "check_query"]:
35 messages = state["messages"]
36 last_message = messages[-1]
37 if not last_message.tool_calls:
38 return END
39 else:
40 return "check_query"
41 builder.add_conditional_edges(
42 "generate_query",
43 should_continue, # 查看最后一条消息是否是工具调用。
44 # 是：LLM：（强制调用sql_db_query工具）执行SQL，生成人工用戶消息进行检查
45 # 否：end
46 [END, "check_query"]
47 )
48 builder.add_edge("check_query", "run_query") # 工具：输入详细而正确的SQL查询，
输出是来自数据库的结果
49 builder.add_edge("run_query", "generate_query") # LLM：（非强制调用sql_db_query
工具）给定一个数据库的结果，然后查看查询的结果并返回答案。
50 recommended_graph = builder.compile()

4.3.3 节点实现
4.3.3.1 节点
collect_user_info
该节点收集用戶希望推荐的房源关键信息。交互流程：
1. 从历史偏好初始化
2. 从当前对话提取
3. 缺失信息中断询问
4. 持久化更新
代码块
1 import uuid
2 import os
3
4 from langchain_community.utilities import SQLDatabase
5 from langchain_community.agent_toolkits import SQLDatabaseToolkit
6 from typing import Optional
7 from langchain_core.messages import AIMessage, HumanMessage, SystemMessage,
filter_messages
8 from langgraph.prebuilt import ToolNode
9 from langgraph.runtime import Runtime
10 from langgraph.store.base import BaseStore
11 from langgraph.types import interrupt
12 from pydantic import BaseModel, Field
13
14 from src.agent.common.content import ContextSchema
15 from src.agent.common.llm import model
16 from src.agent.state.recommend import RecommendState, get_recommend_info
17 from src.agent.common.store import UserPreferences
18
19 # 定义用戶信息的数据模型(结构化输出)
20 class UserInfo(BaseModel):
21 """用戶的租房需求信息"""
22
23 city: Optional[str] = Field(
24 default=None,
25 description="用戶所在或想要租房的城市，例如：西安、北京、上海"
26 )
27 district: Optional[str] = Field(
28 default=None,
29 description="用戶想要租房的具体区域或行政区，例如：雁塔区、碑林区、海淀区"
30 )
31 budget_min: Optional[float] = Field(

32 default=None,
33 description="用戶的最低预算，单位为元/月"
34 )
35 budget_max: Optional[float] = Field(
36 default=None,
37 description="用戶的最高预算，单位为元/月"
38 )
39 room_type: Optional[str] = Field(
40 default=None,
41 description="房屋类型，例如：整租、合租、公寓、一室一厅、两室一厅"
42 )
43 orientation: Optional[str] = Field(
44 default=None,
45 description="房屋朝向，例如：朝南、朝北、东南、南北通透"
46 )
47 room_count: Optional[int] = Field(
48 default=None,
49 description="需要推荐的房屋数量"
50 )
51 others: Optional[str] = Field(
52 default=None,
53 description="特殊要求，例如：带阳台、独立卫生间、近地铁、可养宠物、有电梯等"
54 )
55
56 # 节点：收集用戶信息
57 def collect_user_info(state: RecommendState, runtime: Runtime[ContextSchema],
*, store: BaseStore):
58 # 1. 获取需要被解析的数据：最新的用戶消息+偏好数据
59 pref = state.get("user_preferences")
60 user_messages = filter_messages(state["messages"], include_types="human")
61 if pref and (pref['budget_min'] or pref['budget_max']):
62 extract_messages = [
63 HumanMessage(
64 content="用戶的历史偏好信息如下："
65 f"1. 最低预算：{pref['budget_min']}"
66 f"2. 最高预算：{pref['budget_max']}"
67 ),
68 user_messages[-1]
69 ]
70 else:
71 extract_messages = [user_messages[-1]]
72
73 # 2. 提取信息函数
74 def extract_info(messages) -> UserInfo:
75 system_message = SystemMessage(
76 content="""
77 你是一个租房需求信息提取专家。请从用戶的描述与历史信息中提取租房相关信息。

78 如果用戶历史偏好信息与最新用戶消息冲突，以最新的用戶消息为主。
79 只提取用戶明确提到的信息，不要猜测或推断。
80 如果某个信息用戶没有提到，就返回null。
81 注意预算的单位可能是元/月、元/天等，请统一转换为元/月。
82 如果用戶提到价格范围，请分别提取最低和最高预算。
83 如果用戶提到推荐几套房，提取room_count字段。"""
84 )
85 # 创建结构化提取模型
86 return (model.with_structured_output(schema=UserInfo)
87 .invoke([system_message] + messages))
88
89 # 3. 更新状态函数
90 def update_state(current_state: dict, info: UserInfo) -> dict:
91 if not info:
92 return current_state
93
94 # 获取所有非None的字段
95 user_info_dict = info.model_dump(exclude_none=True)
96 current_state.update(user_info_dict)
97 return current_state
98
99 # 初始化更新后的状态
100 updated_state = {}
101 # 4. 初次提取信息
102 extracted_info = extract_info(extract_messages)
103 updated_state = update_state(updated_state, extracted_info)
104
105 # 5. 检查是否缺失关键信息
106 missing_info = []
107 if not updated_state.get('city'):
108 missing_info.append("**城市**")
109 if updated_state.get('budget_min') is None or
updated_state.get('budget_max') is None:
110 missing_info.append("**预算范围**")
111
112 # 6. 处理缺失信息（中断并询问用戶）
113 if missing_info:
114 prompt = f"为了给您推荐合适的房源，请提供以下信息：{', '.join(missing_info)}
和其它信息。\n"
115 prompt += "如果您不想提供，请输入'**不提供**'，我会根据已有信息为您推荐房源。"
116 # 中断，等待用戶输入
117 answer = interrupt(prompt)
118 if str(answer).strip() == "不提供":
119 # 如果用戶选择不提供，设置默认值
120 if not updated_state.get('city'):
121 updated_state['city'] = "随机城市"
122 if not updated_state.get('budget_min'):

123 updated_state['budget_min'] = 500.0
124 if not updated_state.get('budget_max'):
125 updated_state['budget_max'] = 5000.0
126 if not updated_state.get('room_count'):
127 updated_state['room_count'] = 5
128 print(f"用戶选择不提供信息，使用默认值: 城市=
{updated_state.get('city')}, "
129 f"预算={updated_state.get('budget_min')}-
{updated_state.get('budget_max')}")
130 else:
131 # 用戶提供了更多信息，再次提取
132 user_response_msg = HumanMessage(content=str(answer))
133 extracted_info = extract_info([user_response_msg])
134 updated_state = update_state(updated_state, extracted_info)
135
136 # 7.持久化用戶信息（updated_state有值才更新）
137 if updated_state.get('budget_min') or updated_state.get('budget_max'):
138 user_id = runtime.context.get("user_id")
139 namespace = (user_id, "preferences")
140 # 这里需要重新查询，获取key用来更新
141 prefs_result = store.search(namespace)
142 if len(prefs_result) == 0:
143 # 没有持久化信息，就新增
144 prefs = UserPreferences(
145 budget_min=updated_state.get('budget_min'),
146 budget_max=updated_state.get('budget_max'),
147 )
148 store.put(
149 namespace,
150 str(uuid.uuid4()),
151 prefs.model_dump(exclude_none=True)
152 )
153 # 更新用戶偏好
154 updated_state['user_preferences'] = prefs.model_dump()
155 else:
156 # 有持久化信息，判断更新
157 prefs = prefs_result[0].value
158 store_min = prefs['budget_min']
159 store_max = prefs['budget_max']
160 cur_min = updated_state.get('budget_min')
161 cur_max = updated_state.get('budget_max')
162 update_min = False
163 update_max = False
164 if store_min and cur_min and cur_min < store_min:
165 # 都有，就比较
166 update_min = True
167 elif not store_min and cur_min:

168 # store 没有，cur 有，就更新
169 update_min = True
170
171 if store_max and cur_max and cur_max > store_max:
172 update_max = True
173 elif not store_max and cur_max:
174 update_max = True
175
176 if update_min or update_max:
177 if update_min:
178 prefs['budget_min'] = cur_min
179 print(f"更新用戶最低预算={cur_min}")
180 if update_max:
181 prefs['budget_max'] = cur_max
182 print(f"更新用戶最高预算={cur_max}")
183 store.put(
184 namespace,
185 prefs_result[0].key,
186 prefs
187 )
188 # 更新用戶偏好
189 updated_state['user_preferences'] = prefs
190
191 # 8. 准备最终消息并更新消息，确保消息列表中包含最新消息
192 updated_state['messages'] =
[HumanMessage(content=get_recommend_info(updated_state))]
193
194 # 打印日志
195 print(f"已收集用戶信息: 城市={updated_state.get('city')}, "
196 f"区域={updated_state.get('district')}, "
197 f"预算={updated_state.get('budget_min')}-
{updated_state.get('budget_max')}, "
198 f"房间数={updated_state.get('room_count')}")
199
200 return updated_state
201
4.3.3.2 节点 和 节点
get_schema run_query
工具节点：获取表的详细信息，如表结构、示例数据等。
get_schema
工具节点：用来执行 SQL。
run_query
可以看到，这两个节点由于数据库交互相关。在 langchain 中，要想与 SQL 数据库进行交互，可以用
到一个 SQL 交互工具包：SQLDatabase Toolkit。

4.3.3.2.1 SQLDatabase Toolkit 工具包
SQLDatabase Toolkit 是 langchain-community 中的一个工具包，旨在帮助系统与 SQL 数据库进行
交互。其主要应用是构建能够通过查询关系数据库来回答问题的问答系统，并支持迭代式错误恢复。
SQLDatabase Toolkit 主要功能：
• 提供专用工具：
◦ ：执行 SQL 查询并返回结果。
QuerySQLDatabaseTool
◦ ：获取指定表的 schema 和示例数据。
InfoSQLDatabaseTool
◦ ：列出数据库中的所有表。
ListSQLDatabaseTool
◦ ：在运行前检查 SQL 查询的正确性。
QuerySQLCheckerTool
• 支持智能体工作流：Graph 可以使用这些工具自主探索数据库结构、编写查询、检查并执行，最终
给出自然语言答案。
4.3.3.2.2 接入 SQL 工具包
• 安装工具包
SQLDatabase Toolkit 工具包包含在   包中：
langchain-community
代码块
1 pip install -qU langchain-community
• 准备数据表并配置SQL环境变量（.env）

.env
1 # MYSQL 配置
2 DB_USER=bitedev
3 DB_PASSWORD=bite%40123
4 DB_HOST=192.168.100.233
5 DB_PORT=3308
6 DB_NAME=bitehouse_prd
• 实例化工具
代码块
1 db_user = os.getenv('DB_USER')
2 db_password = os.getenv('DB_PASSWORD')
3 db_host = os.getenv('DB_HOST')
4 db_port = os.getenv('DB_PORT')
5 db_name = os.getenv('DB_NAME')
6 db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:
{db_port}/{db_name}")
7
8 # 获取数据库工具
9 toolkit = SQLDatabaseToolkit(db=db, llm=model)
10 tools = toolkit.get_tools()
11 # [QuerySQLDatabaseTool(description="Input to this tool is a detailed and
correct SQL query, output is a result from the database. If the query is not
correct, an error message will be returned. If an error is returned, rewrite
the query, check the query, and try again. If you encounter an issue with
Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct
table fields.", db=<langchain_community.utilities.sql_database.SQLDatabase
object at 0x103d5fa60>),
12 # InfoSQLDatabaseTool(description='Input to this tool is a comma-separated
list of tables, output is the schema and sample rows for those tables. Be sure
that the tables actually exist by calling sql_db_list_tables first! Example
Input: table1, table2, table3', db=
<langchain_community.utilities.sql_database.SQLDatabase object at
0x103d5fa60>),
13 # ListSQLDatabaseTool(db=
<langchain_community.utilities.sql_database.SQLDatabase object at
0x103d5fa60>),
14 # QuerySQLCheckerTool(description='Use this tool to double check if your query
is correct before executing it. Always use this tool before executing a query
with sql_db_query!', db=
<langchain_community.utilities.sql_database.SQLDatabase object at
0x103d5fa60>, llm=ChatOpenAI(client=
<openai.resources.chat.completions.Completions object at 0x10742d720>,
async_client=<openai.resources.chat.completions.AsyncCompletions object at

0x10742f7f0>, root_client=<openai.OpenAI object at 0x103d5fac0>,
root_async_client=<openai.AsyncOpenAI object at 0x10742d780>, temperature=0.0,
model_kwargs={}, openai_api_key=SecretStr('**********')),
llm_chain=LLMChain(verbose=False, prompt=PromptTemplate(input_variables=
['dialect', 'query'], input_types={}, partial_variables={},
template='\n{query}\nDouble check the {dialect} query above for common
mistakes, including:\n- Using NOT IN with NULL values\n- Using UNION when
UNION ALL should have been used\n- Using BETWEEN for exclusive ranges\n- Data
type mismatch in predicates\n- Properly quoting identifiers\n- Using the
correct number of arguments for functions\n- Casting to the correct data
type\n- Using the proper columns for joins\n\nIf there are any of the above
mistakes, rewrite the query. If there are no mistakes, just reproduce the
original query.\n\nOutput the final SQL query only.\n\nSQL Query: '),
llm=ChatOpenAI(client=<openai.resources.chat.completions.Completions object at
0x10742d720>, async_client=<openai.resources.chat.completions.AsyncCompletions
object at 0x10742f7f0>, root_client=<openai.OpenAI object at 0x103d5fac0>,
root_async_client=<openai.AsyncOpenAI object at 0x10742d780>, temperature=0.0,
model_kwargs={}, openai_api_key=SecretStr('**********')),
output_parser=StrOutputParser(), llm_kwargs={}))]
• 工具节点封装
代码块
1 # 获取表信息
2 get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")
3 get_schema_node = ToolNode([get_schema_tool], name="get_schema")
4
5 # 根据SQL查询结果
6 run_query_tool = next(tool for tool in tools if tool.name == "sql_db_query")
7 run_query_node = ToolNode([run_query_tool], name="run_query")
4.3.3.3 节点
list_tables
该节点调用 SQL 工具，查询表有哪些。也同样可以使用SQLDatabase Toolkit工具包实现。
代码块
1 # 节点：获取全量表
2 def list_tables(state: RecommendState):
3 tool_call = {
4 "name": "sql_db_list_tables",
5 "args": {},
6 "id": "abc123",

7 "type": "tool_call",
8 }
9 tool_call_message = AIMessage(content="", tool_calls=[tool_call])
10 list_tables_tool = next(tool for tool in tools if tool.name ==
"sql_db_list_tables")
11 tool_message = list_tables_tool.invoke(tool_call)
12 response = AIMessage(f"可用的表: {tool_message.content}")
13 return {"messages": [tool_call_message, tool_message, response]}
注意，这里我们构造了三个 Messages 返回，包含【有工具调用的AI消息，工具消息，最终的AI结果消
息】，符合聊天模型对话模式：
4.3.3.4 节点
call_get_schema
该节点中，需要 LLM 绑定 工具，强制调用 工具。
get_schema get_schema
代码块
1 # 节点：强制创建一个获取表信息的工具调用
2 def call_get_schema(state: RecommendState):
3 llm_with_tools = model.bind_tools([get_schema_tool], tool_choice="any")
4 response = llm_with_tools.invoke(state["messages"])
5 return {"messages": [response]}
这一步相当于在构建第一个 AI message。前面我们定义好的 是在构建 Tool
get_schema_node
message。

4.3.3.5 节点
generate_query
该节点有两个作用：
• 用来生成查询 SQL 的工具调用。（生成第一个 AI message）
• 生成最终结果。（生成最后一个 AI message）
因此需要 LLM 绑定 工具，但无需强制工具调用。
run_query
代码块
1 # 节点：根据输入判断是否调用查询SQL的工具
2 def generate_query(state: RecommendState):
3 generate_query_system_prompt = """
4 您是一个设计用于与SQL数据库交互的代理。
5 给定一个输入问题，创建一个语法正确的{dialect}查询来运行，然后查看查询的结果并返回答案。
6 需要根据rows from table的示例设置真实查询的值。
7 除非用戶指定了他们希望获得的特定数量的示例，否则始终将查询限制为最多{top_k}个结果。
8 您可以按相关列对结果排序，以返回最感兴趣的结果。不要查询特定表中的所有列，只查询给定问题的
相关列。
9 不要对数据库做任何DML语句（INSERT， UPDATE， DELETE， DROP等)。
10 """
11 # 构建包含用戶信息的系统提示
12 system_prompt = generate_query_system_prompt.format(
13 dialect=db.dialect,
14 top_k=state.get('room_count', 5) or 5

15 )
16 system_message = SystemMessage(content=system_prompt)
17
18 # 在这里没有强制工具调用，以允许模型在获得解决方案时自然响应。
19 llm_with_tools = model.bind_tools([run_query_tool])
20 # 将用戶信息也加入到查询条件中
21 response = llm_with_tools.invoke([system_message] + state["messages"])
22 return {"messages": [response]}
23
4.3.3.6 节点
check_query
该节点的作用是，检查 generate_query 节点生成的 SQL。回顾我们之前设置的条件边，代码如下：
代码块
1 def should_continue(state: RecommendState) -> Literal[END, "check_query"]:
2 messages = state["messages"]
3 last_message = messages[-1]
4 if not last_message.tool_calls:
5 return END
6 else:
7 return "check_query"
8 builder.add_conditional_edges(
9 "generate_query",
10 should_continue, # 查看最后一条消息是否是工具调用。
11 # 是：LLM：（强制调用sql_db_query工具）执行SQL，生成人工用戶消息进行检查
12 # 否：end
13 [END, "check_query"]
14 )
当 generate_query 节点要执行工具调用时，会先走到 check_query 节点，这表示在执行前先进行
SQL 检查，等待检查完毕后再执行工具。
因此。check_query 节点中的 LLM 必须绑定 工具，且设置强制调用！
run_query
代码块
1 # 节点：强制创建一个调用查询SQL的工具调用
2 def check_query(state: RecommendState):
3 check_query_system_prompt = """
4 你是一个非常注重细节的SQL专家。仔细检查{dialect}查询中的常见错误，包括：
5 -使用NULL值的NOT IN
6 -在应该使用UNION ALL时使用UNION
7 -使用BETWEEN表示独占范围

8 -谓词中的数据类型不匹配
9 -正确引用标识符
10 -使用正确数量的函数参数
11 -转换为正确的数据类型
12 -使用合适的列进行连接
13 如果存在上述任何错误，请重写查询。如果没有错误，只需复制原始查询即可。
14 在运行此检查之后，您将调用适当的工具来执行查询。
15 """.format(dialect=db.dialect)
16 system_message = SystemMessage(content=check_query_system_prompt)
17
18 # 生成人工用戶消息进行检查
19 # 上一个节点是generate_query。如果走到这，必定调用了工具。这样获取到的SQL是准确的。
20 tool_call = state["messages"][-1].tool_calls[0]
21 # 将SQL当作用戶消息传入进行检查
22 user_message = HumanMessage(content=tool_call["args"]["query"])
23
24 llm_with_tools = model.bind_tools([run_query_tool], tool_choice="any")
25 response = llm_with_tools.invoke([system_message, user_message])
26 response.id = state["messages"][-1].id
27
28 return {"messages": [response]}
4.4 预定子图--人工介入的预定系统

4.4.1 状态定义
代码块
1 from langgraph.graph import MessagesState
2
3 # 预定状态
4 class ReserveState(MessagesState):
5 title: str # 预定的房源
6 phone_number: str # 预定电话
7 id_card: str # 身份证
8
4.4.2 工作流定义

代码块
1 from langgraph.constants import START, END
2 from langgraph.graph import StateGraph
3 from langgraph.prebuilt import ToolNode, tools_condition
4
5 from src.agent.node.reserve import (
6 get_title,
7 get_phone,
8 get_id,
9 add_reserve_message,
10 call_orders,
11 generate_orders
12 )
13 from src.agent.state.reserve import ReserveState
14
15 builder = StateGraph(ReserveState)
16 builder.add_sequence([get_title, get_phone, get_id, add_reserve_message,
call_orders])
17 builder.add_node("tool_node", ToolNode([generate_orders]))
18 builder.add_edge(START, "get_title")
19 builder.add_conditional_edges(
20 "call_orders",
21 tools_condition,
22 {
23 "tools": "tool_node",
24 "__end__": END,
25 }, )
26 builder.add_edge("tool_node", "call_orders")
27 reserve_graph = builder.compile()
28
4.4.3 节点实现
对于预定子图，获取用戶预定信息的几个节点，都采用循环验证模式：用戶输入有效信息才继续往后
执行。代码如下：
代码块
1 import uuid
2 from typing import Annotated, Any
3
4 from langchain_core.messages import HumanMessage, SystemMessage
5 from langgraph.prebuilt import InjectedStore, ToolRuntime
6 from langgraph.types import interrupt

7 from langchain.tools import tool
8
9 from src.agent.common.llm import model
10 from src.agent.common.store import UserPreferences, ReservedInfo
11 from src.agent.state.reserve import ReserveState
12
13 # 节点：获取用戶预定房源
14 def get_title(state: ReserveState):
15 prompt = "请输入要预定的房源名称"
16 while True:
17 title = interrupt(prompt)
18 if title: # 可以进行验证
19 return {"title": title}
20 # 每次验证失败后，提示信息会更新
21 prompt = f"'{title}' 不是一个有效的房源名称，请更正。"
22
23 # 节点：获取用戶预定电话
24 def get_phone(state: ReserveState):
25 prompt = "请输入要预定的手机号"
26 while True:
27 phone_number = interrupt(prompt)
28 if phone_number: # 可以进行验证
29 return {"phone_number": phone_number}
30 # 每次验证失败后，提示信息会更新
31 prompt = f"'{phone_number}' 不是一个有效的电话，请更正。"
32
33 # 节点：获取用戶身份证
34 def get_id(state: ReserveState):
35 prompt = "请输入要预定的身份证号码"
36 while True:
37 id_card = interrupt(prompt)
38 if id_card:
39 return {"id_card": id_card}
40 # 每次验证失败后，提示信息会更新
41 prompt = f"'{id_card}' 不是一个有效的身份证，请更正。"
42
43 # 节点：新增预定消息
44 def add_reserve_message(state: ReserveState):
45 reserve_prompt = """根据提供的信息，帮我预定房源。
46 - 预定的房源标题: {title}
47 - 用戶预定号码: {phone_number}
48 - 用戶身份证号码: {id_card}"""
49 reserve_message = HumanMessage(content=reserve_prompt.format(
50 title=state['title'],
51 phone_number=state['phone_number'],
52 id_card=state['id_card']
53 ))

54 return {"messages": [reserve_message]}
55
56 # 工具：生成工单
57 # store: Annotated[Any, InjectedStore()] 参考:
58 # https://reference.langchain.com/python/langgraph/agents/?
_gl=1*4ftp91*_gcl_au*NTMxMzI0ODQ1LjE3NjE3MjUyMTM.*_ga*MTU5NDE1NTU4Ny4xNzYwNDExO
DU3*_ga_47WX3HKKY2*czE3Njc1OTY4NTYkbzE4NiRnMSR0MTc2NzU5Njk2OSRqNTckbDAkaDA.#lan
ggraph.prebuilt.tool_node.InjectedState
59 @tool
60 def generate_orders(phone_number: str, id_card: str, house_title: str,
61 runtime: ToolRuntime, store: Annotated[Any,
InjectedStore()]) -> str:
62 """根据用戶电话，身份证，预定房源。
63
64 Args:
65 phone_number: 用戶电话
66 id_card: 身份证
67 house_title: 用戶要预定的房源标题
68 runtime: 工具的运行时信息
69 store: 注入工具的持久存储
70 """
71
72 # 1. 生成工单号
73 order_id = str(uuid.uuid4())
74
75 # 2. 构建预定信息
76 reserved_house = ReservedInfo(
77 order_id=order_id,
78 title=house_title,
79 phone_number=phone_number
80 )
81
82 # 3. 持久化用戶偏好（预定信息）
83 user_id = runtime.context.get("user_id")
84 namespace = (user_id, "preferences")
85 prefs_result = store.search(namespace)
86 if len(prefs_result) == 0:
87 # 没有持久化信息，新增
88 prefs = UserPreferences(
89 reserved_info=[reserved_house]
90 )
91 store.put(
92 namespace,
93 str(uuid.uuid4()),
94 prefs.model_dump(exclude_none=True)
95 )
96 else:

97 # 有值，更新
98 prefs = prefs_result[0].value or {}
99 prefs.setdefault('reserved_info', []).append(reserved_house)
100 store.put(
101 namespace,
102 prefs_result[0].key,
103 prefs
104 )
105
106 # 4. 扩展：持久化订单表
107
108 return f"已成功预定房源：{house_title}，预定工单号为：{order_id}"
109
110 # 节点：生成工单结果
111 def call_orders(state: ReserveState):
112 response = model.bind_tools([generate_orders]).invoke(
113 [SystemMessage(content="你是一个工单生成的助手，支持调用工具进行房源预定工单生
成。支持查看查询的结果并返回最终答案")]
114 + state["messages"]
115 )
116 return {"messages": [response]}
4.5 扩展子图--除业务外的智能问答助手

这部分代码简单，合成一个py文件进行描述：
代码块
1 from langchain_core.messages import AIMessage, SystemMessage
2 from langgraph.constants import START
3 from langgraph.graph import StateGraph, MessagesState
4
5 from src.agent.common.llm import model
6
7 def extend_node(state: MessagesState):
8 response = model.invoke(
9 [SystemMessage(content="你是一个乐于助人的助手，可以根据历史对话进行回复。")]
10 + state["messages"]
11 )
12 return {
13 "messages": [response]
14 }
15
16 extend_graph = (
17 StateGraph(MessagesState)
18 .add_node(extend_node)
19 .add_edge(START, "extend_node")
20 .compile()
21 )

22
5. 项目部署
5.1 自托管部署 & 涉及到的相关组件解释
LangSmith Deployment 构建在开源的 LangGraph 框架上，用于开发有状态的应用程序。
LangGraph 提供核心抽象和执行模型，而 LangSmith 支持从开发到生产的整个生命周期，
LangSmith 增加了托管基础设施、可观察性、部署选项、助手和并发控制等能力。这会将 Agent 应用
打包、构建为 Agent Server，并将其进行部署。
上述流程实际上是 LangSmith 自托管部署，它是一个完整的解决方案，用于在企业自有基础设施中构
建、部署和管理图。其核心由以下几个协同工作的组件构成：
1. Agent Server
◦ 角色：部署和运行图的核心运行时环境。
◦ 功能：提供标准化的 API，处理执行、状态管理和持久化，让开发者专注于业务逻辑而非服务器
基础设施。
2. LangGraph CLI
◦ 角色：命令行工具。
◦ 功能：用于在本地构建、打包图，并与图进行交互，同时为部署到 Agent Server 做准备。
3. Studio
◦ 角色：集成开发环境。
◦ 功能：用于可视化、交互和调试图的专门 IDE。可连接本地 Agent Server 进行开发和测试。
4. Python SDK（自行了解）
◦ 角色：软件开发工具包。
◦ 功能：为应用程序提供编程接口，以与已部署的图和 Agent Server 进行交互。
5. RemoteGraph（自行了解）
◦ 角色：本地代理包装器。
◦ 功能：让你能够像调用本地运行的图一样，与远程部署的图进行交互。
6. Control Plane（控制平面，自行了解）
◦ 角色：管理和配置层。
◦ 功能：用于创建、更新和管理 Agent Server 部署的用戶界面和 API。
7. Data plane（数据平面，自行了解）

◦ 角色：执行层。
◦ 功能：实际运行图的运行时层，包括 Agent Server 实例及其依赖的后端服务（如
PostgreSQL、Redis 等）。
简单来说，开发者使用 LangGraph CLI 和 Studio 在本地开发和测试图，然后将其部署为 Agent
Server。应用程序通过【SDK】、【RemoteGraph】或通过【Agent Server 提供的 API】调用部署好
的服务。整个系统的部署和生命周期由 Control Plane 管理，而具体的任务执行则由 Data plane 完
成。（注意：Control Plane 和 Data plane 可选，只是用法之一。）
5.2 本地启动并测试
• 修改 langgraph.json 配置文件，添加新增的图：
代码块
1 {
2 "$schema": "https://langgra.ph/schema.json",
3 "dependencies": ["."],
4 "graphs": {
5 "house_agent": "./src/agent/graph.py:graph",
6 "recommend_agent": "./src/agent/recommend.py:recommended_graph",
7 "reserve_agent": "./src/agent/reserve.py:reserve_graph",
8 "extend_agent": "./src/agent/extend.py:extend_graph"
9 },
10 "env": ".env",
11 "image_distro": "wolfi"
12 }
• 运行   命令启动本地开发服务器。 命令会以内存模式启动
langgraph dev langgraph dev
Agent Server。该模式适合开发和测试。
• 测试 Graph

例如：
代码块
1 # 测试问题
2 [
3 "在西安，我的预算是1000-2000一个月，帮我推荐4套房子。要求在雁塔区。",
4 "我想在北京海淀租个1室1厅1卫，预算5000以内，最好近地铁。",
5 "帮我推荐几套房子", # 这个会触发信息收集中断
6 ]
5.3 LangSmith 部署方式
Agent Server 可以根据我们的基础设施采用不同的部署方式：
• 云部署（有兴趣自行研究）：云是一种完全托管的模式，其中 LangChain 承担并运营所有
LangSmith 的基础设施和服务：
◦ 完全托管的基础设施：LangChain 负责所有基础设施、更新、扩展和维护。
◦ 从 GitHub 部署：连接您的代码库，只需点击几下即可部署。
◦ 自动化 CI/CD（持续集成/持续部署）：构建过程由平台自动处理。
◦ LangSmith UI：全面访问可观测性、评估、部署管理和工作室。
• 带 Control Plane 的混合/自托管（有兴趣自行研究）：通过 Control Plane，可以在本地构建
Docker 镜像，将它们推送到 Kubernetes 集群可以访问的注册表中，并使用 LangSmith UI 部署它
们。

• 独立服务器：直接部署 Agent Server，不通过 Control Plane 和 LangSmith UI。
5.4 独立部署 Agent Server
这里我们选择直接部署 Agent Server，不通过 Control Plane 和 LangSmith UI。让我们的系统作为独
立服务运行。
5.4.1 工作流程
步骤1：使用 langgraph-cli 或 Studio 在本地定义和测试图形
步骤2：将应用服务打包为 Docker 镜像
步骤3：将 Agent Server 部署到平台：
• Kubernetes：使用 LangSmith Helm 图表在 Kubernetes 集群中运行 Agent Server。这是生产级
部署的推荐选项。（官网自行研究）
• Docker：在任何支持 Docker 的计算平台（本地开发机、VM、ECS等）上运行。这最适合于开发或
小规模工作负载。
5.4.2 部署前的准备工作
部署 Agent Server 时，实际上部署了一个或多个【图】、一个用于持久化的【数据库】和一个【任务
队列】。Agent Server 利用数据库实现持久化和任务队列：
• PostgreSQL 作为 Agent Server 的数据库支持：所有持久化数据（检查点、助手等）都存储在
PostgreSQL 数据库中
• Redis 作为任务队列：被用作发布订阅连接，以实现事件的实时流传输。
如果你使用 LangSmith 云部署，这些组件会被自动管理。我们选择的是独立部署 Agent Server，就
需要自己搭建和管理这些组件。
• 使用 Docker 启动一个Redis容器：
代码块
1 sudo docker run -d \
2 --name redis-6380 \
3 -p 6380:6379 \
4 -v redis-data:/data \
5 redis:7-alpine \
6 redis-server --appendonly yes --requirepass "your_password"
• 使用 Docker 快速安装并启动 postgres：

代1 码块#  1. 拉取 PostgreSQL 镜像
2 docker pull postgres:latest
3
4 # 2. 运行 PostgreSQL 容器
5 # -p 5432:5432: 将容器的5432端口映射到宿主机的5432端口
6 # -e POSTGRES_PASSWORD=bit: 设置PostgreSQL的postgres用戶密码
7 # --name postgres-sql: 给容器命名
8 # -d: 后台运行
9 docker run --name postgres-sql -e POSTGRES_PASSWORD=bit -p 5432:5432 -d
postgres
在 中加入 redis 和 postgres 的配置：
.env
.env
1 # DOCKER 必须
2 DATABASE_URI=postgresql://postgres:bit@192.168.100.233:5432/postgres
3 REDIS_URI=redis://:bite%40123@192.168.100.233:6380
5.4.3 部署姿势1：构建 Docker 镜像并运行
使用 LangGraph CLI 构建 Docker 镜像，命令为 。
langgraph build [OPTIONS]
• 必须设置 REDIS_URI、DATABASE_URI
.env
• 默认端口 8000
• 参数选项 -t 必选： Docker 镜像的标签
代码块
1 $ sudo langgraph build -t house-agent-image
2
3 $ sudo docker image list
4 REPOSITORY TAG IMAGE ID CREATED
SIZE
5 house-agent-image latest 7884c6e8d937 39
minutes ago 626MB
6
7 $ sudo docker run --env-file .env -p 8001:8000 house-agent-image
8 Starting API server

5.4.4 部署姿势2：生成 dockerfile 并组合 Docker compose
使用 命令生成一个用于构建 LangSmith
langgraph dockerfile [OPTIONS] SAVE_PATH
API 服务 Docker 镜像的 Dockerfile。
OPTIONS 选项  默认  描述
-c, --config FILE langgraph.json 配置文件路径，声明依赖关系、图表和环境变量。
--help 显示此信息并退出。
• 第一步：生成 dockerfile：
代码块
1 $ sudo langgraph dockerfile -c langgraph.json Dockerfile
注意：  命令会把   文件里的所有配置转换成
langgraph dockerfile langgraph.json
Dockerfile 命令。使用该命令时，每次更新   文件时都需要重新运行。否则，你
langgraph.json
的更改在构建或运行 dockerfile 时不会被反映出来。
• 第二步：结合 Docker compose 启动
Docker compose 参考：
• 参考1: 由于上面我们已经搭建好了redis 和 postgres，Docker compose 只包含服务：
代码块
1 volumes:
2 langgraph-data:
3 driver: local
4 services:
5 langgraph-api:
6 build: .
7 ports:
8 - "8002:8000"
9 env_file:
10 - .env
• 参考2: 带有 redis 和 postgres 的完整参考（下面的参考中需要先打镜像，再运行）：

1 volumes:
2 langgraph-data:
3 driver: local
4 services:
5 langgraph-redis:
6 image: redis:6
7 healthcheck:
8 test: redis-cli ping
9 interval: 5s
10 timeout: 1s
11 retries: 5
12 langgraph-postgres:
13 image: postgres:16
14 ports:
15 - "5432:5432"
16 environment:
17 POSTGRES_DB: postgres
18 POSTGRES_USER: postgres
19 POSTGRES_PASSWORD: postgres
20 volumes:
21 - langgraph-data:/var/lib/postgresql/data
22 healthcheck:
23 test: pg_isready -U postgres
24 start_period: 10s
25 timeout: 1s
26 retries: 5
27 interval: 5s
28 langgraph-api:
29 image: ${IMAGE_NAME}
30 ports:
31 - "8123:8000"
32 depends_on:
33 langgraph-redis:
34 condition: service_healthy
35 langgraph-postgres:
36 condition: service_healthy
37 env_file:
38 - .env
39 environment:
40 REDIS_URI: redis://langgraph-redis:6379
41 LANGSMITH_API_KEY: ${LANGSMITH_API_KEY}
42 DATABASE_URI: postgres://postgres:postgres@langgraph-
postgres:5432/postgres?sslmode=disable
运行 指令启动：
docker compose up

代1 码块$ sudo docker compose up
2
3 # 源代码更新后可以执行
4 $ sudo docker compose up --build 服务名
5.4.5 部署姿势3：构建 Docker 镜像，并将服务运行在 Data plane 中
执行命令
langgraph up
代码块
1 # 启动 langgraph-api
2 $ sudo langgraph up -p 8000
3
4 # 实际上是依赖了docker
5 $ sudo docker image list
6 REPOSITORY TAG IMAGE ID CREATED
SIZE
7 house-langgraph-api latest 90ae2bcbab92 39
minutes ago 626MB
部署时可能遇到的问题：
langgraph up
中指定 时，和之前本地用到的 是一个库，可能会导致【数据
.env DATABASE_URI postgresql
库迁移失败】的问题❌ ：
简单解释：
•  表中的   字段是   类型
checkpoints thread_id text
•  表中的   字段是   类型
thread thread_id uuid
• 它们需要相同类型才能建立外键关系
解决方案：重新建一个库，环境隔离下。

6. 项目扩展（自行研究）
扩展1：在主图中进行消息管理
可以在适当的位置进行历史会话修剪、会话总结等操作。例如：推荐完房源之后，进行历史消息总
结，删除工具或其它过程消息。避免因推荐房源造成的消息过多，导致单次后续的会话出现 LLM 调用
错误。
扩展2：结构化输出用戶期望信息，如一室一厅、朝向等，最准确做法是和数据库表字段做映射，生成
的 SQL 会更准确。
扩展3：执行 SQL 前，加入中断，人工审核 SQL 准确性。
扩展4：可以自定义流式输出，前端输出更加详细且流式的执行过程。
LangGraph不是终点，而是你构建智能AI应用的起点。从这里开始，创造属于你的智能助手吧！
