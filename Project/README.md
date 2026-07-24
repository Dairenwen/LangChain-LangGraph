# Wandor 租房 AI

面向中文租房场景的 LangGraph 应用：支持城市/区域别名、流式输出、可中断补充条件、预订流程、跨会话偏好和历史对话。

## 架构

```text
浏览器 React 前端 (5173)
        │ HTTP + SSE
LangGraph Agent Server (50699)
   ├── MySQL 8：house 房源库（1,000 条中国一二线城市演示数据）
   ├── PostgreSQL 16：用户档案、线程、消息、运行、检查点、长期记忆
   └── Redis 7：后台运行和流式事件分发
```

`user_id` 是前端首次访问时生成并保存在浏览器中的 UUID；每个线程在创建时携带此 ID。它用于隔离用户的历史会话和长期偏好。生产环境应由登录系统提供经过验证的用户 ID，不能仅信任浏览器传入的值。

## 一键运行（Docker Compose）

1. 安装 Docker Desktop，并复制配置：

```bash
cp .env.example .env
```

2. 编辑 `.env`：填写 `PACKYAPI_API_KEY`、`PACKYAPI_BASE_URL`、`PACKYAPI_MODEL`，以及自托管 LangGraph Agent Server 所需的 `LANGSMITH_API_KEY`、`LANGGRAPH_CLOUD_LICENSE_KEY`。请不要把真实密钥提交到 Git。

3. 构建并启动：

```bash
docker compose up --build
```

4. 打开：

- Web：<http://127.0.0.1:5173>
- API 文档：<http://127.0.0.1:50699/docs>
- 健康检查：<http://127.0.0.1:50699/ok>

首次启动会初始化 MySQL 的 `house` 表，并由 `seed-houses` 写入可复现的 1,000 条演示房源（4 个一线城市、16 个二线城市）。数据库卷会保留；后续启动检测到已有数据会跳过填充。

停止服务但保留数据：

```bash
docker compose down
```

## PostgreSQL 持久化与长期记忆

LangGraph Agent Server 在容器中接收 `DATABASE_URI`，并将下列内容存到 `langgraph-postgres`：

- 线程与消息：用于历史对话、刷新恢复和中断后 `Command(resume=...)`；
- 运行与检查点：用于可靠恢复图执行；
- BaseStore：按 `(user_id, "profile")` 保存用户服务档案，按 `(user_id, "preferences")` 保存预算偏好与预订记录；
- 线程元数据：包含 `source=wandor-rental-web` 与 `user_id`，前端可只检索当前用户的对话。

项目不在 `graph.compile()` 中硬编码 `PostgresSaver`。这是因为 Agent Server 会在运行时注入受它管理的 PostgreSQL checkpointer 与 BaseStore；手动注入反而会绕过服务器的线程、运行和流式协调。

## 本地开发

后端保持原有 Studio 工作流：

```bash
pip install -e . "langgraph-cli[inmem]"
langgraph dev --port 50699
```

前端：

```bash
cd frontend
npm install
npm run dev
```

本地 Vite 前端默认请求 `http://127.0.0.1:50699`；可在 `frontend/.env.local` 写入 `VITE_API_BASE_URL` 和 `VITE_ASSISTANT_ID` 覆盖。Compose 的生产前端默认走同域 `/api` 反向代理，因此不依赖浏览器跨域策略。

## 验证

```bash
PYTHONPATH=src python3 -m pytest tests/unit_tests -q
cd frontend && npm run build
docker compose config
```

`Dockerfile` 是项目专用的 Agent Server 镜像，`frontend/Dockerfile` 是 React 生产镜像，`Dockerfile.seed` 只负责导入演示房源。Compose 中的端口和数据卷都已固定在本项目范围内。
