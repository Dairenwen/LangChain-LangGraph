# Generated-structure Dockerfile for the LangGraph Agent Server.
# The base image supplies the server process; this layer adds only this project.
FROM langchain/langgraph-api:3.11

WORKDIR /deps/rental-agent
COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts

# Keep package versions compatible with the Agent Server image.
RUN pip install --no-cache-dir -c /api/constraints.txt -e .

ENV LANGSERVE_GRAPHS='{"agent":"/deps/rental-agent/src/agent/graph.py:graph","recommend_graph":"/deps/rental-agent/src/agent/recommend.py:recommend_graph","reserve_graph":"/deps/rental-agent/src/agent/reserve.py:reserve_graph","extend_graph":"/deps/rental-agent/src/agent/node/extend.py:extend_graph"}'
