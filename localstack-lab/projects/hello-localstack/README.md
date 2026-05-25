# Hello LocalStack

最小化 LocalStack 示例：使用 boto3 创建 S3 bucket 并上传/读取对象。

## 依赖
- 已启动的 LocalStack（建议端点 `http://s3.localhost.localstack.cloud:4566`）
- Python 3.9+，boto3（`./scripts/bootstrap.sh` 会创建 `.venv` 并安装依赖）

## 快速运行

```bash
cd /workspaces/study/localstack-lab
./scripts/bootstrap.sh
source .venv/bin/activate
# 确保 LocalStack 已启动
python projects/hello-localstack/main.py
```

## 环境
- 可设置 `LOCALSTACK_ENDPOINT_URL`，默认 `http://s3.localhost.localstack.cloud:4566`
- Bucket: `hello-localstack-bucket`
- Object key: `hello.txt`
