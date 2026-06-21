# Tracing 与成本观测

`tracing_demo` 将每个 span 的 trace/span ID、耗时、状态、错误、token 和估算成本写入 JSONL，便于后续接 OpenTelemetry、LangSmith 或平台日志。

```bash
cd tracing_demo
python3 main.py
python3 main.py --fail
```

验收：成功路径写入三个 `ok` span；失败路径同时记录子 span 和父 span 的错误原因。生产环境不得把 prompt、客户资料或密钥直接写入 trace。
