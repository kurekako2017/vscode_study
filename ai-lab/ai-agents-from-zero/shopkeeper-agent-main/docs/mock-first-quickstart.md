# Mock 优先启动说明

> 这份说明是给“先不修 Docker，先把项目搭起来”的临时方案。
> 目标很简单：先让后端 `/api/query` 和前端页面跑通，方便继续学习和联调。

## 适合什么情况

- 当前 Docker Desktop / WSL 集成暂时不稳定
- 你想先看前端页面能不能正常发起问数请求
- 你想先理解这个项目的整体链路，再回头补真实 MySQL / Qdrant / Elasticsearch / TEI

## 这个模式会做什么

- 后端不连接 MySQL、Qdrant、Elasticsearch、Embedding 服务
- `/api/query` 直接返回一段模拟的 SSE 流
- 前端仍然按真实问数页面运行
- 你可以看到“进度条式”的问数过程和最终结果卡片

## 一次性准备

1. 复制环境文件：

```bash
cp .env.mock.example .env
```

2. 确认 `.env` 里已经有：

```bash
MOCK_MODE=true
VITE_API_BASE_URL=
VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000
```

## 启动后端

```bash
cd ai-lab/ai-agents-from-zero/shopkeeper-agent-main
MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

预期结果：

- 终端出现 `Uvicorn running on http://127.0.0.1:8000`
- 打开后端文档页后，能看到 `/api/query`

## 启动前端

```bash
cd ai-lab/ai-agents-from-zero/shopkeeper-agent-main/frontend
pnpm install
pnpm dev
```

预期结果：

- 前端默认访问 `http://127.0.0.1:3000`
- 页面里的问数框可以正常输入
- 点击发送后，会看到模拟的进度流和结果卡片

## 如何测试

### 测试 1：直接调后端接口

```bash
curl -N -sS -X POST http://127.0.0.1:8000/api/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"统计华北地区销售额"}'
```

预期结果：

- 先连续返回多段 `progress`
- 最后返回一段 `result`
- `result` 里会包含示例 SQL 和示例数据行

### 测试 2：在前端页面输入问题

输入：

```text
统计华北地区销售额
```

预期结果：

- 页面先显示执行步骤
- 然后显示一条模拟 SQL
- 最后显示几行示例结果

## 什么时候切回真实模式

当你后面把 Docker 修好，或者 NAS MySQL、Qdrant、Elasticsearch、TEI 都确认可用了，再切回真实模式：

- 关闭 `MOCK_MODE`
- 补全 `.env` 里的数据库和服务地址
- 重新构建元数据知识库
- 再执行真实问数

## 这条路的价值

- 先让你有“能跑的项目”
- 先把前后端链路和接口格式理解清楚
- 先验证页面交互和 SSE 流程
- 后面再补基础设施时，调试压力会小很多
