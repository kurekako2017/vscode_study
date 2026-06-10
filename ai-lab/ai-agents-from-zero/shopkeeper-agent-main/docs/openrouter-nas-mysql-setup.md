# OpenRouter + NAS MySQL 本地方案

> 这份说明对应当前电商问数项目的“推荐本地组合”：如果你已经有可用的 OpenRouter Key，就把模型接入走 OpenRouter；如果你想复用 JtProject 那台 NAS MySQL，就把 `meta` / `dw` 两个数据库接到 NAS 上。

## 1. 推荐组合

- 大模型：`OpenRouter`
- 元数据 MySQL：`192.168.10.2:3306`
- 数仓 MySQL：`192.168.10.2:3306`
- Embedding：本机 Docker TEI，默认 `http://localhost:8081`

这个组合的好处是：

- 模型能力和数据库都可以复用已有环境
- 本地只需要继续跑 Qdrant、Elasticsearch、Embedding 和前后端
- 不用先在本机再起一套 MySQL 容器

## 2. 这套项目里 MySQL 负责什么

- `meta` 库：保存表、字段、指标、字段指标关系等元数据
- `dw` 库：保存教学数仓的事实表和维度表

项目代码不会自动帮你“新建远端数据库”，所以在接 NAS 之前，要先把这两个库准备好。

## 3. NAS MySQL 预期信息

- Host: `192.168.10.2`
- Port: `3306`
- 用户: `root`
- 密码: `123456`

如果你的 NAS 上已经有 JtProject 的 MySQL，通常可以直接复用这个连通信息。

## 4. 环境变量模板

建议复制项目里的 `.env.example` 再按下面调整：

```bash
# 模型
OPENROUTER_API_KEY=你的_openrouter_api_key
LLM_API_KEY=
LLM_MODEL_NAME=openai/gpt-4o-mini
LLM_BASE_URL=https://openrouter.ai/api/v1

# NAS MySQL - 元数据
DB_META_HOST=192.168.10.2
DB_META_PORT=3306
DB_META_USER=root
DB_META_PASSWORD=123456
DB_META_DATABASE=meta

# NAS MySQL - 数仓
DB_DW_HOST=192.168.10.2
DB_DW_PORT=3306
DB_DW_USER=root
DB_DW_PASSWORD=123456
DB_DW_DATABASE=dw
```

> 这里先用 `root / 123456` 做最小连通性验证，确认 NAS Docker MySQL 可以直接接入。
> 如果你更希望使用独立账号，再在 NAS MySQL 里单独创建 `didilili / dili123` 并授权给 `meta` 和 `dw`。
> 如果你更习惯把 key 只放在 `OPENROUTER_API_KEY`，后端也会自动识别，不必再重复写一份到 `LLM_API_KEY`。

## 5. NAS 上的准备步骤

### 5.1 先确认连接

```bash
mysql -h 192.168.10.2 -P 3306 -u root -p
```

能连上后，再继续下一步。

### 5.2 创建账号和数据库

先在 NAS MySQL 上创建项目要用的账号和数据库：

```sql
CREATE USER IF NOT EXISTS 'didilili'@'%' IDENTIFIED BY 'dili123';
CREATE DATABASE IF NOT EXISTS meta DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE DATABASE IF NOT EXISTS dw DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL PRIVILEGES ON meta.* TO 'didilili'@'%';
GRANT ALL PRIVILEGES ON dw.* TO 'didilili'@'%';
FLUSH PRIVILEGES;
```

如果你先用 `root / 123456` 跑通环境，这一步也可以先不做，直接让 root 使用 `meta` 和 `dw` 两个库即可。

### 5.3 导入项目初始化 SQL

项目已经自带两份初始化脚本：

- `docker/mysql/meta.sql`
- `docker/mysql/dw.sql`

你可以在 NAS 上执行它们，把表结构和教学数据准备好。

## 6. 推荐执行顺序

1. 准备 `.env`
2. 确认 NAS MySQL 连通
3. 在 NAS 上创建 `meta` 和 `dw`
4. 导入 `meta.sql` 和 `dw.sql`
5. 执行 `scripts/bootstrap_local_env.sh`
6. 下载 Embedding 模型
7. 启动 Qdrant / Elasticsearch / Embedding
8. 启动后端
9. 启动前端
10. 做一次问数验证

> 当前代码已经把 Embedding 客户端改成了 TEI 适配器，`uvicorn main:app` 已经可以正常启动；后续真正问数是否成功，取决于 NAS MySQL、Qdrant、Elasticsearch 和 TEI 这几个外部服务是否都已就绪。

## 7. 验证结果应该是什么

- 后端能连上 NAS MySQL，不再依赖本机 MySQL 容器
- `meta` 库里有表、字段、指标和关系数据
- `dw` 库里有教学数仓表和样例数据
- `build_meta_knowledge` 可以正常跑通
- 前端可以看到查询过程和结果

## 8. 当前适用范围

这份方案适合你现在的目标：

- 先把项目跑起来
- 先复用现成 NAS
- 先不追求本机完全离线

如果后面你想切回本机 Docker MySQL，再把 `.env` 改回 `localhost` 就行。
