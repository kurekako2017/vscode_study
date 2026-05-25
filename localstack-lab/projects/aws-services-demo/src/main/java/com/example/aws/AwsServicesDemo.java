package com.example.aws;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.*;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URI;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * AWS Services Demo with LocalStack
 *
 * <p>这是一个用于测试 LocalStack 本地 AWS 服务的演示程序。
 *
 * <p><strong>作者</strong>: GitHub Copilot AI
 * <p><strong>创建日期</strong>: 2026-01-02
 * <p><strong>用途</strong>: 演示如何在本地使用 LocalStack 测试 AWS 服务
 *
 * <h2>测试的服务:</h2>
 * <ul>
 *   <li><strong>DynamoDB</strong> - NoSQL 数据库服务</li>
 *   <li><strong>SQS</strong> - 消息队列服务</li>
 *   <li><strong>S3</strong> - 对象存储服务</li>
 * </ul>
 *
 * <h2>前置条件:</h2>
 * <ul>
 *   <li>LocalStack 容器运行在 localhost:4566</li>
 *   <li>Java 11 或更高版本</li>
 *   <li>Maven 3.6 或更高版本</li>
 *   <li>AWS SDK for Java v2</li>
 * </ul>
 *
 * <h2>运行方式:</h2>
 * <pre>
 * mvn clean compile exec:java
 * </pre>
 *
 * <h2>注意事项:</h2>
 * <ul>
 *   <li>LocalStack 端点 (http://localhost:4566) 是 API 端点，不是 Web 界面</li>
 *   <li>要查看服务状态，访问: http://localhost:4566/_localstack/health</li>
 *   <li>使用虚拟凭证 (test/test) 进行认证</li>
 *   <li>所有操作都在本地 LocalStack 容器中执行，不会产生 AWS 费用</li>
 * </ul>
 *
 * @author GitHub Copilot AI
 * @version 1.0.0
 * @since 2026-01-02
 */
public class AwsServicesDemo {

    /**
     * LocalStack API 端点地址
     *
     * <p><strong>注意</strong>: 这是 API 端点，不能直接在浏览器中访问
     * <p>正确的访问方式:
     * <ul>
     *   <li>健康检查: http://localhost:4566/_localstack/health</li>
     *   <li>系统信息: http://localhost:4566/_localstack/info</li>
     *   <li>使用 AWS CLI: aws --endpoint-url=http://localhost:4566 s3 ls</li>
     * </ul>
     */
    private static final String LOCALSTACK_ENDPOINT = "http://localhost:4566";

    /**
     * AWS 区域配置
     *
     * <p>虽然是本地测试，但 AWS SDK 仍需要指定区域
     * <p>使用 us-east-1 作为默认区域
     */
    private static final Region REGION = Region.US_EAST_1;

    /**
     * 日志文件写入器
     *
     * <p>用于将测试结果同时输出到控制台和日志文件
     */
    private static PrintWriter logWriter = null;

    /**
     * 日志文件路径
     */
    private static final String LOG_FILE_PATH = "aws-services-test-result.log";

    /**
     * 程序入口点 - 依次执行所有 AWS 服务测试
     *
     * <p>测试顺序:
     * <ol>
     *   <li>DynamoDB - 测试表创建、数据插入和查询</li>
     *   <li>SQS - 测试队列创建、消息发送和接收</li>
     *   <li>S3 - 测试 Bucket 创建、文件上传和下载</li>
     * </ol>
     *
     * <p>所有测试都使用 try-with-resources 确保资源正确释放
     * <p>测试结果会输出到控制台和日志文件: aws-services-test-result.log
     *
     * @param args 命令行参数（未使用）
     */
    public static void main(String[] args) {
        // 初始化日志文件
        initializeLog();

        logBoth("========================================");
        logBoth("  AWS Services Demo with LocalStack");
        logBoth("  Test Time: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        logBoth("========================================\n");

        // 记录测试状态
        boolean dynamoDbSuccess = false;
        boolean sqsSuccess = false;
        boolean s3Success = false;

        // Test DynamoDB
        try {
            logBoth("[1] Testing DynamoDB...");
            testDynamoDB();
            dynamoDbSuccess = true;
            logBoth("[1] DynamoDB Test: ✓ SUCCESS\n");
        } catch (Exception e) {
            logBoth("[1] DynamoDB Test: ✗ FAILED - " + e.getMessage() + "\n");
            e.printStackTrace(logWriter);
        }

        // Test SQS
        try {
            logBoth("[2] Testing SQS...");
            testSQS();
            sqsSuccess = true;
            logBoth("[2] SQS Test: ✓ SUCCESS\n");
        } catch (Exception e) {
            logBoth("[2] SQS Test: ✗ FAILED - " + e.getMessage() + "\n");
            e.printStackTrace(logWriter);
        }

        // Test S3
        try {
            logBoth("[3] Testing S3...");
            testS3();
            s3Success = true;
            logBoth("[3] S3 Test: ✓ SUCCESS\n");
        } catch (Exception e) {
            logBoth("[3] S3 Test: ✗ FAILED - " + e.getMessage() + "\n");
            e.printStackTrace(logWriter);
        }

        // 输出测试总结
        logBoth("========================================");
        logBoth("  Test Summary");
        logBoth("========================================");
        logBoth("DynamoDB: " + (dynamoDbSuccess ? "✓ PASSED" : "✗ FAILED"));
        logBoth("SQS:      " + (sqsSuccess ? "✓ PASSED" : "✗ FAILED"));
        logBoth("S3:       " + (s3Success ? "✓ PASSED" : "✗ FAILED"));
        logBoth("----------------------------------------");

        int passedTests = (dynamoDbSuccess ? 1 : 0) + (sqsSuccess ? 1 : 0) + (s3Success ? 1 : 0);
        int totalTests = 3;

        if (passedTests == totalTests) {
            logBoth("Result: ✓ ALL TESTS PASSED (" + passedTests + "/" + totalTests + ")");
        } else {
            logBoth("Result: ✗ SOME TESTS FAILED (" + passedTests + "/" + totalTests + " passed)");
        }

        logBoth("========================================");
        logBoth("\nLog file saved to: " + LOG_FILE_PATH);

        // 关闭日志文件
        closeLog();
    }

    /**
     * 初始化日志文件
     *
     * <p>创建或覆盖日志文件，并写入文件头信息
     */
    private static void initializeLog() {
        try {
            logWriter = new PrintWriter(new FileWriter(LOG_FILE_PATH, false));
            System.out.println("Log file initialized: " + LOG_FILE_PATH);
        } catch (IOException e) {
            System.err.println("Failed to initialize log file: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * 关闭日志文件
     *
     * <p>确保所有内容都被写入磁盘
     */
    private static void closeLog() {
        if (logWriter != null) {
            logWriter.flush();
            logWriter.close();
            System.out.println("\nLog file closed: " + LOG_FILE_PATH);
        }
    }

    /**
     * 同时输出到控制台和日志文件
     *
     * @param message 要输出的消息
     */
    private static void logBoth(String message) {
        System.out.println(message);
        if (logWriter != null) {
            logWriter.println(message);
            logWriter.flush();  // 立即刷新，确保实时写入
        }
    }

    /**
     * 创建 DynamoDB 客户端
     *
     * <p>配置说明:
     * <ul>
     *   <li><strong>endpointOverride</strong>: 指向 LocalStack API 端点</li>
     *   <li><strong>region</strong>: AWS 区域（本地测试也需要指定）</li>
     *   <li><strong>credentials</strong>: 虚拟凭证（test/test），LocalStack 不验证真实性</li>
     * </ul>
     *
     * @return 配置好的 DynamoDB 客户端实例
     */
    private static DynamoDbClient createDynamoDbClient() {
        return DynamoDbClient.builder()
            .endpointOverride(URI.create(LOCALSTACK_ENDPOINT))
            .region(REGION)
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create("test", "test")))
            .build();
    }

    /**
     * 创建 SQS 客户端
     *
     * <p>配置与 DynamoDB 客户端相同
     *
     * @return 配置好的 SQS 客户端实例
     */
    private static SqsClient createSqsClient() {
        return SqsClient.builder()
            .endpointOverride(URI.create(LOCALSTACK_ENDPOINT))
            .region(REGION)
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create("test", "test")))
            .build();
    }

    /**
     * 创建 S3 客户端
     *
     * <p>S3 特殊配置:
     * <ul>
     *   <li><strong>forcePathStyle(true)</strong>: 使用路径风格访问</li>
     *   <li>路径风格: http://localhost:4566/bucket-name/key</li>
     *   <li>虚拟主机风格: http://bucket-name.localhost:4566/key（不适用于 LocalStack）</li>
     * </ul>
     *
     * @return 配置好的 S3 客户端实例
     */
    private static S3Client createS3Client() {
        return S3Client.builder()
            .endpointOverride(URI.create(LOCALSTACK_ENDPOINT))
            .region(REGION)
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create("test", "test")))
            .forcePathStyle(true)
            .build();
    }

    /**
     * 测试 DynamoDB 服务
     *
     * <p>测试操作:
     * <ol>
     *   <li><strong>CreateTable</strong>: 创建名为 "TestTable" 的表</li>
     *   <li><strong>PutItem</strong>: 插入一条测试数据</li>
     *   <li><strong>GetItem</strong>: 根据主键查询数据</li>
     *   <li><strong>ListTables</strong>: 列出所有表</li>
     * </ol>
     *
     * <p>表结构:
     * <ul>
     *   <li>主键: id (String 类型)</li>
     *   <li>计费模式: PAY_PER_REQUEST（按需付费）</li>
     * </ul>
     *
     * <p>使用 try-with-resources 自动关闭客户端连接
     *
     * <p><strong>代码逻辑详解</strong>:
     * <pre>
     * 1. 创建 DynamoDB 客户端（连接到 LocalStack）
     * 2. 定义表名 "TestTable"
     * 3. 尝试创建表（如果表已存在则跳过）
     * 4. 构造一个包含 id、name、timestamp 的数据项
     * 5. 将数据项插入表中
     * 6. 根据主键 id 查询刚插入的数据
     * 7. 列出当前所有的表
     * 8. 自动关闭客户端连接（try-with-resources）
     * </pre>
     */
    private static void testDynamoDB() {
        // try-with-resources: 自动管理资源，方法结束时自动调用 dynamoDb.close()
        try (DynamoDbClient dynamoDb = createDynamoDbClient()) {
            String tableName = "TestTable";

            // ==================== 步骤 1: 创建表 ====================
            logBoth("  - Creating DynamoDB table: " + tableName);

            // 构建创建表的请求对象
            CreateTableRequest createTableRequest = CreateTableRequest.builder()
                .tableName(tableName)  // 表名
                // 定义主键结构：id 作为哈希键（分区键）
                .keySchema(
                    KeySchemaElement.builder()
                        .attributeName("id")       // 主键字段名
                        .keyType(KeyType.HASH)     // HASH = 分区键，RANGE = 排序键
                        .build()
                )
                // 定义属性的数据类型（只需定义主键和索引的属性）
                .attributeDefinitions(
                    AttributeDefinition.builder()
                        .attributeName("id")               // 属性名
                        .attributeType(ScalarAttributeType.S)  // S = String, N = Number, B = Binary
                        .build()
                )
                // 按需付费模式（LocalStack 中不产生实际费用）
                .billingMode(BillingMode.PAY_PER_REQUEST)
                .build();

            try {
                // 执行创建表操作
                dynamoDb.createTable(createTableRequest);
                logBoth("  ✓ Table created successfully");
            } catch (ResourceInUseException e) {
                // 如果表已存在，捕获异常并继续执行
                logBoth("  ! Table already exists");
            }

            // ==================== 步骤 2: 插入数据 ====================
            logBoth("  - Putting item into table");

            // 构造要插入的数据项（Map 结构：字段名 -> AttributeValue）
            Map<String, AttributeValue> item = new HashMap<>();
            // id 字段：字符串类型
            item.put("id", AttributeValue.builder().s("test-id-1").build());
            // name 字段：字符串类型
            item.put("name", AttributeValue.builder().s("Test Item").build());
            // timestamp 字段：当前时间戳（字符串格式）
            item.put("timestamp", AttributeValue.builder().s(Instant.now().toString()).build());

            // 构建插入数据的请求对象
            PutItemRequest putItemRequest = PutItemRequest.builder()
                .tableName(tableName)  // 目标表名
                .item(item)            // 要插入的数据项
                .build();

            // 执行插入操作（如果主键相同会覆盖原有数据）
            dynamoDb.putItem(putItemRequest);
            logBoth("  ✓ Item inserted successfully");

            // ==================== 步骤 3: 查询数据 ====================
            logBoth("  - Getting item from table");

            // 构造主键（用于查询）
            Map<String, AttributeValue> key = new HashMap<>();
            key.put("id", AttributeValue.builder().s("test-id-1").build());

            // 构建查询请求对象
            GetItemRequest getItemRequest = GetItemRequest.builder()
                .tableName(tableName)  // 目标表名
                .key(key)              // 主键值
                .build();

            // 执行查询操作，返回查询结果
            GetItemResponse getItemResponse = dynamoDb.getItem(getItemRequest);
            // 打印查询到的数据项（包含所有字段）
            logBoth("  ✓ Item retrieved: " + getItemResponse.item());

            // ==================== 步骤 4: 列出所有表 ====================
            logBoth("  - Listing all tables");
            // 执行列表查询，获取当前所有表名
            ListTablesResponse listTablesResponse = dynamoDb.listTables();
            // 打印表名列表
            logBoth("  ✓ Tables: " + listTablesResponse.tableNames());

        } catch (Exception e) {
            // 捕获所有异常并打印错误信息
            logBoth("  ✗ DynamoDB test failed: " + e.getMessage());
            if (logWriter != null) {
                e.printStackTrace(logWriter);  // 打印完整的堆栈跟踪到日志文件
            }
            e.printStackTrace();  // 同时打印到控制台
            throw new RuntimeException(e);  // 重新抛出异常，以便 main 方法能捕获
        }
        // try-with-resources 自动关闭 dynamoDb 客户端
    }

    /**
     * 测试 SQS (Simple Queue Service) 服务
     *
     * <p>测试操作:
     * <ol>
     *   <li><strong>CreateQueue</strong>: 创建名为 "test-queue" 的标准队列</li>
     *   <li><strong>SendMessage</strong>: 发送一条消息到队列</li>
     *   <li><strong>ReceiveMessage</strong>: 从队列接收消息</li>
     *   <li><strong>DeleteMessage</strong>: 删除已处理的消息</li>
     *   <li><strong>ListQueues</strong>: 列出所有队列</li>
     * </ol>
     *
     * <p>队列特性:
     * <ul>
     *   <li>队列类型: 标准队列（Standard Queue）</li>
     *   <li>消息持久化: 是</li>
     *   <li>消息去重: 否（标准队列不支持）</li>
     * </ul>
     *
     * <p><strong>代码逻辑详解</strong>:
     * <pre>
     * 1. 创建 SQS 客户端（连接到 LocalStack）
     * 2. 创建一个标准队列 "test-queue"
     * 3. 发送一条消息到队列
     * 4. 从队列接收消息（轮询）
     * 5. 删除已处理的消息（防止重复消费）
     * 6. 列出所有队列
     * 7. 自动关闭客户端连接
     * </pre>
     */
    private static void testSQS() {
        // try-with-resources: 自动管理 SQS 客户端资源
        try (SqsClient sqs = createSqsClient()) {
            String queueName = "test-queue";

            // ==================== 步骤 1: 创建队列 ====================
            logBoth("  - Creating SQS queue: " + queueName);

            // 构建创建队列的请求对象
            CreateQueueRequest createQueueRequest = CreateQueueRequest.builder()
                .queueName(queueName)  // 队列名称（在同一区域内唯一）
                .build();

            // 执行创建队列操作，返回队列 URL
            CreateQueueResponse createQueueResponse = sqs.createQueue(createQueueRequest);
            String queueUrl = createQueueResponse.queueUrl();  // 队列 URL 用于后续操作
            logBoth("  ✓ Queue created: " + queueUrl);

            // ==================== 步骤 2: 发送消息 ====================
            logBoth("  - Sending message to queue");
            // 构造消息内容（包含时间戳）
            String messageBody = "Hello LocalStack! Timestamp: " + Instant.now();

            // 构建发送消息的请求对象
            SendMessageRequest sendMessageRequest = SendMessageRequest.builder()
                .queueUrl(queueUrl)      // 目标队列 URL
                .messageBody(messageBody) // 消息内容（最大 256 KB）
                .build();

            // 执行发送消息操作，返回消息 ID
            SendMessageResponse sendMessageResponse = sqs.sendMessage(sendMessageRequest);
            logBoth("  ✓ Message sent, ID: " + sendMessageResponse.messageId());

            // ==================== 步骤 3: 接收消息 ====================
            logBoth("  - Receiving message from queue");

            // 构建接收消息的请求对象
            ReceiveMessageRequest receiveMessageRequest = ReceiveMessageRequest.builder()
                .queueUrl(queueUrl)        // 源队列 URL
                .maxNumberOfMessages(1)    // 一次最多接收 1 条消息（范围 1-10）
                .build();

            // 执行接收消息操作（短轮询，立即返回）
            ReceiveMessageResponse receiveMessageResponse = sqs.receiveMessage(receiveMessageRequest);

            // 检查是否接收到消息
            if (!receiveMessageResponse.messages().isEmpty()) {
                // 获取第一条消息
                Message message = receiveMessageResponse.messages().get(0);
                logBoth("  ✓ Message received: " + message.body());

                // ==================== 步骤 4: 删除消息 ====================
                // 重要：处理完消息后必须删除，否则消息会重新变为可见
                logBoth("  - Deleting message");

                // 构建删除消息的请求对象
                DeleteMessageRequest deleteMessageRequest = DeleteMessageRequest.builder()
                    .queueUrl(queueUrl)                    // 队列 URL
                    .receiptHandle(message.receiptHandle()) // 接收句柄（用于标识具体消息）
                    .build();

                // 执行删除操作
                sqs.deleteMessage(deleteMessageRequest);
                logBoth("  ✓ Message deleted");
            } else {
                // 队列为空或消息未到达
                logBoth("  ! No messages received");
            }

            // ==================== 步骤 5: 列出所有队列 ====================
            logBoth("  - Listing all queues");
            // 执行列表查询，获取所有队列的 URL
            ListQueuesResponse listQueuesResponse = sqs.listQueues();
            // 打印队列 URL 列表
            logBoth("  ✓ Queues: " + listQueuesResponse.queueUrls());

        } catch (Exception e) {
            // 捕获所有异常并打印错误信息
            logBoth("  ✗ SQS test failed: " + e.getMessage());
            if (logWriter != null) {
                e.printStackTrace(logWriter);
            }
            e.printStackTrace();
            throw new RuntimeException(e);
        }
        // try-with-resources 自动关闭 sqs 客户端
    }

    /**
     * 测试 S3 (Simple Storage Service) 服务
     *
     * <p>测试操作:
     * <ol>
     *   <li><strong>CreateBucket</strong>: 创建名为 "test-bucket-demo" 的存储桶</li>
     *   <li><strong>PutObject</strong>: 上传文件到存储桶</li>
     *   <li><strong>GetObject</strong>: 从存储桶下载文件</li>
     *   <li><strong>ListBuckets</strong>: 列出所有存储桶</li>
     * </ol>
     *
     * <p>配置说明:
     * <ul>
     *   <li>访问方式: 路径风格（Path-style）</li>
     *   <li>内容类型: 纯文本字符串</li>
     *   <li>编码: UTF-8</li>
     * </ul>
     *
     * <p><strong>代码逻辑详解</strong>:
     * <pre>
     * 1. 创建 S3 客户端（连接到 LocalStack，使用路径风格）
     * 2. 创建一个 S3 存储桶（Bucket）
     * 3. 上传一个文本文件到存储桶（从内存字符串直接上传）
     * 4. 从存储桶下载文件并读取内容
     * 5. 列出所有存储桶
     * 6. 自动关闭客户端连接
     *
     * 注意：test-file.txt 不会保存在本地磁盘！
     *      它只存在于 LocalStack 容器的模拟 S3 服务中。
     * </pre>
     */
    private static void testS3() {
        // try-with-resources: 自动管理 S3 客户端资源
        try (S3Client s3 = createS3Client()) {
            String bucketName = "test-bucket-demo";  // 存储桶名称（全局唯一）
            String keyName = "test-file.txt";        // 对象键（文件名）

            // ==================== 步骤 1: 创建存储桶 ====================
            logBoth("  - Creating S3 bucket: " + bucketName);

            // 构建创建存储桶的请求对象
            CreateBucketRequest createBucketRequest = CreateBucketRequest.builder()
                .bucket(bucketName)  // 存储桶名称
                .build();

            try {
                // 执行创建存储桶操作
                s3.createBucket(createBucketRequest);
                logBoth("  ✓ Bucket created successfully");
            } catch (Exception e) {
                // 如果存储桶已存在，捕获异常并继续执行
                logBoth("  ! Bucket may already exist");
            }

            // ==================== 步骤 2: 上传文件 ====================
            logBoth("  - Uploading file to bucket");

            // 构造文件内容（纯文本字符串，包含时间戳）
            // 重要：这个字符串只在内存中，不会创建本地文件！
            String content = "Hello from LocalStack S3! Timestamp: " + Instant.now();

            // 构建上传对象的请求
            PutObjectRequest putObjectRequest = PutObjectRequest.builder()
                .bucket(bucketName)  // 目标存储桶
                .key(keyName)        // 对象键（文件路径/名称）
                .build();

            // 执行上传操作
            // RequestBody.fromString() 直接从内存字符串上传，不需要本地文件
            s3.putObject(putObjectRequest,
                software.amazon.awssdk.core.sync.RequestBody.fromString(content));
            logBoth("  ✓ File uploaded successfully");

            // ==================== 步骤 3: 下载文件 ====================
            logBoth("  - Downloading file from bucket");

            // 构建获取对象的请求
            GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                .bucket(bucketName)  // 源存储桶
                .key(keyName)        // 对象键
                .build();

            // 执行下载操作，将对象内容读取为 UTF-8 字符串
            // getObjectAsBytes() 返回字节数组，asUtf8String() 转换为字符串
            String downloadedContent = s3.getObjectAsBytes(getObjectRequest).asUtf8String();
            logBoth("  ✓ File downloaded: " + downloadedContent);

            // ==================== 步骤 4: 列出所有存储桶 ====================
            logBoth("  - Listing all buckets");

            // 执行列表查询，获取所有存储桶
            ListBucketsResponse listBucketsResponse = s3.listBuckets();

            // 使用 Stream API 提取存储桶名称并转换为列表
            logBoth("  ✓ Buckets: " +
                listBucketsResponse.buckets().stream()  // 获取存储桶列表的流
                    .map(Bucket::name)                   // 提取每个存储桶的名称
                    .collect(Collectors.toList()));      // 收集为 List<String>

        } catch (Exception e) {
            // 捕获所有异常并打印错误信息
            logBoth("  ✗ S3 test failed: " + e.getMessage());
            if (logWriter != null) {
                e.printStackTrace(logWriter);
            }
            e.printStackTrace();
            throw new RuntimeException(e);
        }
        // try-with-resources 自动关闭 s3 客户端
    }
}

