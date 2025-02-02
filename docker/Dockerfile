# 使用 ARM64 架构的基础镜像进行构建
FROM arm64v8/python:3.12-slim AS builder

WORKDIR /app

# 设置 pipx 和 poetry
ENV PATH=/root/.local/bin:$PATH
RUN pip install pipx && \
    pipx ensurepath && \
    pipx install poetry

# 更新并安装 git
RUN apt update && apt install -y git

# 复制代码
COPY . .

# 配置 poetry 并安装依赖
RUN poetry self add poetry-dynamic-versioning && \
    poetry config virtualenvs.in-project true && \
    poetry install && \
    rm -rf /app/.git


# 使用 ARM64 架构的基础镜像作为运行时环境
FROM arm64v8/python:3.12-slim as runner

WORKDIR /app

# 从 builder 复制构建好的环境
COPY --from=builder /app/ /app/

ENTRYPOINT ["/app/.venv/bin/javsp"]
CMD ["-i", "/video"]
