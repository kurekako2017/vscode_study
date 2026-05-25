# Hello LocalStack Java

使用 AWS SDK v2 连接 LocalStack 的最小 Java 示例（S3 演示）。

## 依赖
- Java 11+
- Maven
- 已启动的 LocalStack（建议端点 `http://s3.localhost.localstack.cloud:4566`）

## 运行
```bash
cd /workspaces/study/localstack-lab/projects/hello-localstack-java
mvn -q package
LOCALSTACK_ENDPOINT_URL=http://s3.localhost.localstack.cloud:4566 mvn -q exec:java
```
可选环境变量：
- `LOCALSTACK_ENDPOINT_URL`（默认 `http://s3.localhost.localstack.cloud:4566`）

程序流程：
1) 创建 bucket `hello-localstack-java`（若已存在会忽略已拥有错误）
2) 上传对象 `hello.txt`
3) 读取并打印内容

示例输出：
```
Endpoint: http://localhost:4566
Bucket: hello-localstack-java
Key: hello.txt
Content:
Hello LocalStack from Java! UTC now: ...
```
