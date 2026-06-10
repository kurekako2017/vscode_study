# 功能检查清单

> 这是一页版的测试清单，适合你启动项目时按顺序勾选。

## 1. 先确认模式

- [ ] 我现在是 `MOCK_MODE=true`
- [ ] 或者我现在是 `OpenRouter + NAS MySQL` 真实模式

## 2. 配置是否能读

- [ ] `.env` 已复制到项目根目录
- [ ] `python3 -m app.conf.app_config` 不报错
- [ ] 能成功读到 `app_config`

## 3. Mock 模式检查

- [ ] `MOCK_MODE=true python3 -m uvicorn main:app --host 127.0.0.1 --port 8000` 能启动
- [ ] `curl -N -sS -X POST http://127.0.0.1:8000/api/query -H 'Content-Type: application/json' -d '{"query":"统计华北地区销售额"}'` 能返回 SSE
- [ ] 返回里先有 `progress`
- [ ] 返回里最后有 `result`
- [ ] 前端页面可以显示进度和结果

## 4. 真实模式检查

- [ ] `OPENROUTER_API_KEY` 已填好
- [ ] `DB_META_*` 已指向 NAS MySQL
- [ ] `DB_DW_*` 已指向 NAS MySQL
- [ ] NAS 上有 `meta` 和 `dw`
- [ ] `bash scripts/up_local_stack.sh up` 能把本机基础服务拉起来
- [ ] `python3 -m app.scripts.build_meta_knowledge -c conf/meta_config.yaml` 能跑完
- [ ] `python3 -m uvicorn main:app --host 127.0.0.1 --port 8000` 能启动
- [ ] `curl` 调 `/api/query` 能返回真实 SSE
- [ ] 前端页面能看到真实问数结果

## 5. 服务连通性检查

- [ ] `curl -s http://127.0.0.1:6333` 有 Qdrant 响应
- [ ] `curl -s http://127.0.0.1:9200` 有 Elasticsearch 响应
- [ ] `curl -s http://127.0.0.1:8081` 有 Embedding 响应
- [ ] `mysql -h 192.168.10.2 -P 3306 -u root -p` 能登录 NAS MySQL

## 6. 元数据构建检查

- [ ] `meta.table_info` 有数据
- [ ] `meta.column_info` 有数据
- [ ] `meta.metric_info` 有数据
- [ ] `dw.fact_order` 有数据
- [ ] Qdrant 里有字段和指标 collection
- [ ] Elasticsearch 里有字段值索引

## 7. 问数测试输入

可依次测试这些问题：

- [ ] `统计华北地区销售额`
- [ ] `统计 2025 年第一季度各大区的 GMV，并按 GMV 从高到低排序`
- [ ] `按会员等级统计 2025 年第一季度的订单数和销售额`

## 8. 预期结果

- [ ] 页面先显示执行进度
- [ ] 页面能显示 SQL 摘要
- [ ] 页面能显示结果表格
- [ ] 出错时能看到错误信息，而不是页面卡死

## 9. 排错顺序

1. 先看 `.env`
2. 再看后端启动日志
3. 再看基础服务是否在线
4. 再看 NAS MySQL 是否连通
5. 再看 `build_meta_knowledge` 是否成功
6. 最后再测前端

## 10. 一句话判断

- Mock 成功：前后端联调能跑通
- 真实成功：NAS MySQL + Qdrant + ES + Embedding + OpenRouter 都接通，问数结果能回来
