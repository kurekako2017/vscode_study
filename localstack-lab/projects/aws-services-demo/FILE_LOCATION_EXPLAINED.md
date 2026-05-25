# test-file.txt 文件位置说明

## ❓ 问题：test-file.txt 保存在哪里？

### 答案：**文件保存在 LocalStack 容器内的内存中，不在本地磁盘！**

---

## 📍 文件的实际位置

### 1. **不在本地磁盘** ❌

`test-file.txt` **没有**保存在这些位置：
```
❌ D:\dev\study\localstack-lab\projects\aws-services-demo\test-file.txt
❌ D:\dev\study\localstack-lab\test-file.txt  
❌ 你的任何本地目录
```

### 2. **在 LocalStack 容器的内存中** ✅

文件实际保存位置：
```
✅ LocalStack Docker 容器内
✅ 内存模拟的 S3 服务中
✅ Bucket: test-bucket-demo
✅ Key: test-file.txt
```

---

## 🔍 详细解释

### 程序做了什么

查看代码（AwsServicesDemo.java 第 370-400 行）：

```java
private static void testS3() {
    String bucketName = "test-bucket-demo";
    String keyName = "test-file.txt";      // ← 文件名
    
    // 创建 S3 bucket
    s3.createBucket(...);
    
    // 上传文件（从内存中的字符串）
    String content = "Hello from LocalStack S3! Timestamp: " + Instant.now();
    s3.putObject(
        PutObjectRequest.builder()
            .bucket(bucketName)
            .key(keyName)                   // ← 文件的 key
            .build(),
        RequestBody.fromString(content)     // ← 直接从字符串上传
    );
}
```

**关键点**：
1. 程序**没有创建本地文件**
2. 直接从**内存中的字符串**上传到 LocalStack
3. 文件存储在 **LocalStack 容器的模拟 S3 服务中**

---

## 📊 文件存储位置对比

| 位置 | 是否存在 | 说明 |
|------|---------|------|
| 本地项目目录 | ❌ 否 | 程序没有创建本地文件 |
| 本地临时目录 | ❌ 否 | 没有保存到本地 |
| LocalStack 容器内存 | ✅ 是 | 模拟的 S3 存储 |
| 真实的 AWS S3 | ❌ 否 | 使用的是 LocalStack，不是真实 AWS |

---

## 💾 如何查看和访问文件

### 方法 1: 使用 AWS CLI 查看

```powershell
# 列出 bucket 中的文件
aws --endpoint-url=http://localhost:4566 s3 ls s3://test-bucket-demo/

# 输出:
# test-file.txt
```

### 方法 2: 下载文件到本地

```powershell
# 下载到当前目录
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt .

# 下载到指定位置
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt D:\temp\test-file.txt
```

### 方法 3: 查看文件内容（不下载）

```powershell
# 直接输出内容
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt -

# 输出:
# Hello from LocalStack S3! Timestamp: 2026-01-01T15:17:31.402031300Z
```

### 方法 4: 使用 Java 代码下载

修改 `AwsServicesDemo.java`，在 testS3() 方法中添加：

```java
// 下载文件到本地
System.out.println("  - Downloading file to local disk");
File localFile = new File("downloaded-test-file.txt");
s3.getObject(
    GetObjectRequest.builder()
        .bucket(bucketName)
        .key(keyName)
        .build(),
    ResponseTransformer.toFile(localFile)
);
System.out.println("  ✓ File downloaded to: " + localFile.getAbsolutePath());
```

---

## 🗄️ LocalStack 存储机制

### LocalStack 如何存储数据

```
┌─────────────────────────────────────┐
│   Docker 容器: localstack           │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  LocalStack 服务              │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │  S3 模拟服务 (内存)     │ │ │
│  │  │                         │ │ │
│  │  │  Bucket: test-bucket-demo│ │
│  │  │    └─ test-file.txt     │ │ │ ← 文件在这里
│  │  └─────────────────────────┘ │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**特点**：
- 📦 存储在容器内存中
- ⚡ 速度快（内存操作）
- 🔄 容器重启后数据丢失（除非配置持久化）
- 💰 不产生 AWS 费用

---

## 🔧 如果想要持久化存储

### 默认行为（当前）
```
容器停止 → 数据保留（容器仍存在）
容器重启 → 数据丢失
容器删除 → 数据丢失
```

### 配置持久化存储

**方法**: 挂载本地目录到 LocalStack 容器

```powershell
docker run -d \
  --name localstack \
  -p 4566:4566 \
  -v D:/localstack-data:/var/lib/localstack \  # ← 持久化存储
  -e LOCALSTACK_AUTH_TOKEN=$env:LOCALSTACK_AUTH_TOKEN \
  localstack/localstack
```

**效果**：
- ✅ 数据保存到 `D:/localstack-data`
- ✅ 容器重启后数据不丢失
- ✅ 可以在本地查看数据文件

---

## 📝 实际操作示例

### 示例 1: 下载文件到本地

```powershell
# 1. 确保 LocalStack 运行中
docker ps | Select-String localstack

# 2. 列出文件
aws --endpoint-url=http://localhost:4566 s3 ls s3://test-bucket-demo/

# 3. 下载到桌面
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt C:\Users\你的用户名\Desktop\test-file.txt

# 4. 打开文件查看
notepad C:\Users\你的用户名\Desktop\test-file.txt
```

### 示例 2: 查看文件内容

```powershell
# 直接查看
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt - | Write-Output
```

### 示例 3: 在容器内查看

```powershell
# 进入容器
docker exec -it localstack bash

# 在容器内查看 LocalStack 数据
ls -la /var/lib/localstack/
```

---

## 🎯 总结

### 关键要点

| 问题 | 答案 |
|------|------|
| **文件在本地吗？** | ❌ 不在本地磁盘 |
| **文件在哪里？** | ✅ LocalStack 容器内存中 |
| **如何访问？** | 使用 AWS CLI 或 AWS SDK |
| **如何下载？** | `aws s3 cp s3://bucket/key 本地路径` |
| **重启会丢失吗？** | ✅ 会（除非配置持久化） |

### 理解要点

1. **LocalStack 是模拟器**
   - 不是真实的 S3
   - 数据在容器内存中
   - 用于开发和测试

2. **test-file.txt 不是本地文件**
   - 程序直接从内存字符串上传
   - 没有创建本地文件
   - 存储在 LocalStack 的模拟 S3 中

3. **要获取文件内容**
   - 使用 AWS CLI 下载
   - 使用 AWS SDK 代码下载
   - 不能直接在文件浏览器中找到

---

## 📚 相关命令速查

```powershell
# 列出所有 buckets
aws --endpoint-url=http://localhost:4566 s3 ls

# 列出 bucket 中的文件
aws --endpoint-url=http://localhost:4566 s3 ls s3://test-bucket-demo/

# 下载文件
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt ./test-file.txt

# 查看文件内容
aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket-demo/test-file.txt -

# 删除文件
aws --endpoint-url=http://localhost:4566 s3 rm s3://test-bucket-demo/test-file.txt

# 同步整个 bucket 到本地
aws --endpoint-url=http://localhost:4566 s3 sync s3://test-bucket-demo/ ./local-backup/
```

---

**创建时间**: 2026-01-02  
**文档版本**: 1.0

