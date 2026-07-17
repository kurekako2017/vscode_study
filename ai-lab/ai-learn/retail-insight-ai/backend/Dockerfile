# ERIP Backend 生产镜像：FastAPI + Alembic 启动链。
# 禁止 COPY .env；Secret 仅运行时注入。

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 系统依赖：psycopg 二进制轮已足够；保留 curl 供 healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 应用代码与迁移（不含 .env / tests / venv）
# db/schema.sql：Postgres 仓库启动时 initialize_schema 需要（Alembic 之后的幂等补齐）
# data/：KPI / Research 本地静态样例（sales.csv 等）；缺省会导致 Task API 在 Compose 中失败
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY db ./db
COPY data ./data
COPY scripts/docker-entrypoint.sh ./scripts/docker-entrypoint.sh

RUN chmod +x ./scripts/docker-entrypoint.sh \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=40s --retries=5 \
  CMD curl -fsS http://127.0.0.1:8000/health >/dev/null || exit 1

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
