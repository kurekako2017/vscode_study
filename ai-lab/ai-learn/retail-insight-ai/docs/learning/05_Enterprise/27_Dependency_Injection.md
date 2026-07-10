# Retail Insight AI 企业源码架构手册

# Volume 05：Enterprise（企业架构）

# Chapter 27

# Dependency Injection（依赖注入）

> Build Loosely Coupled Enterprise Systems

---

# 文档信息

| 项目     | 内容                      |
| -------- | ------------------------- |
| Volume   | 05                        |
| Chapter  | 27                        |
| 技术主题 | Dependency Injection (DI) |
| 难度     | ⭐⭐⭐⭐☆                |
| 推荐程度 | ⭐⭐⭐⭐⭐                |
| 对应框架 | FastAPI / Spring Boot     |

---

# 学习目标

阅读完本章，你应该能够回答：

- 什么是 Dependency Injection（依赖注入）？
- 什么是 IOC（控制反转）？
- 为什么企业项目几乎都会使用 DI？
- Retail Insight AI 是否已经使用了 DI？
- FastAPI 与 Spring Boot 的 DI 有什么区别？

---

# 一、为什么需要 Dependency Injection？

很多初学者都会这样写代码：

```python
class TaskService:

    def run(self):

        repository = TaskRepository()

        repository.save(...)
```

TaskService 自己创建了 Repository。

程序可以运行。

但是企业项目几乎不会这样写。

为什么？

因为：

TaskService 和 TaskRepository 已经紧紧绑在一起。

以后：

```text
TaskRepository

↓

PostgresRepository
```

或者：

```text
TaskRepository

↓

MockRepository
```

TaskService 都必须修改。

这就是：

**高耦合（High Coupling）**。

---

# 二、什么是 Dependency Injection？

Dependency Injection（DI）

翻译：

**依赖注入。**

意思非常简单：

> **对象不要自己创建依赖，而是由外部提供。**

例如：

以前：

```text
TaskService

↓

new Repository()
```

现在：

```text
Repository

↓

TaskService
```

Repository：

不是自己创建。

而是：

别人提供。

这就是：

Injection（注入）。

---

# 三、什么是 IOC（控制反转）

很多人觉得：

IOC 很复杂。

实际上：

一句话：

> **对象创建权，从程序员手里交给框架。**

以前：

```text
TaskService

↓

Create Repository
```

现在：

```text
FastAPI

↓

Create Repository

↓

Inject

↓

TaskService
```

控制权：

发生了反转。

因此：

叫：

**Inversion of Control。**

---

# 四、Retail Insight AI 当前实现（Current）

当前项目采用：

```text
Browser

↓

FastAPI

↓

Router

↓

TaskService

↓

Repository
```

源码位置：

```text
backend/app/api/

backend/app/services/

backend/app/repositories/
```

目前：

项目已经实现：

- Router
- Service
- Repository

虽然不是完整 IOC Container，

但是已经采用：

**依赖分层思想。**

这也是企业项目最重要的一步。

---

# 五、Source Binding（源码绑定）

建议打开：

```text
backend/app/api/tasks.py
```

观察：

Router 如何调用：

```text
TaskService
```

然后：

打开：

```text
backend/app/services/task_service.py
```

观察：

TaskService 如何调用：

```text
TaskRepository
```

最后：

打开：

```text
backend/app/repositories/
```

查看：

Repository。

阅读路线：

```text
tasks.py

↓

TaskService

↓

TaskRepository
```

不要反过来阅读。

---

# 六、FastAPI 如何实现 DI

FastAPI 使用：

```python
Depends(...)
```

例如：

```python
@router.get("/tasks")

def get_tasks(

    service = Depends(get_task_service)

):
```

框架：

自动：

创建：

TaskService。

然后：

注入：

Router。

Router：

完全不用：

```python
TaskService()
```

这就是：

FastAPI 的 DI。

---

# 七、Spring Boot 如何实现 DI

Spring Boot：

更加成熟。

例如：

```java
@Service
public class TaskService {

    @Autowired

    private TaskRepository repository;

}
```

Spring：

自动：

创建：

Repository。

然后：

注入：

TaskService。

与 FastAPI：

思想：

完全一致。

只是：

语法不同。

---

# 八、为什么企业一定使用 DI？

原因一：

降低耦合。

例如：

```text
SQLite

↓

PostgreSQL
```

Service：

不用修改。

---

原因二：

方便测试。

例如：

正式环境：

```text
Repository
```

测试：

```text
Mock Repository
```

Service：

完全不知道。

---

原因三：

统一对象生命周期。

框架：

负责：

创建。

释放。

缓存。

复用。

程序员：

只负责：

业务。

---

# 九、Current vs Enterprise

当前 Retail Insight AI：

```text
Router

↓

TaskService

↓

Repository
```

未来企业版：

```text
FastAPI

↓

Depends

↓

Service

↓

Repository Interface

↓

PostgreSQL
```

进一步：

增加：

```text
Redis

RabbitMQ

VectorDB

External API
```

Service：

完全不用修改。

---

# 十、为什么这样设计（Why）

如果：

TaskService：

自己：

创建：

Repository。

以后：

数据库：

变化。

所有：

Service：

都要修改。

采用：

Dependency Injection：

以后：

修改：

Repository。

Service：

保持不变。

这就是：

企业：

最重要的：

**低耦合设计。**

---

# 十一、Java / Spring 对照

| Retail Insight AI | Spring Boot   |
| ----------------- | ------------- |
| FastAPI Depends   | @Autowired    |
| Router            | Controller    |
| Service           | Service       |
| Repository        | Repository    |
| Depends           | IOC Container |

设计思想一致。

---

# 十二、VS Code 阅读路线

建议：

```text
backend/app/api/

↓

tasks.py

↓

TaskService

↓

TaskRepository
```

观察：

对象：

什么时候：

创建。

什么时候：

传递。

什么时候：

调用。

---

# 十三、Learning Trace 对应

Learning Trace：

看到：

```text
TaskService

↓

Repository
```

说明：

业务：

进入：

Repository。

Learning Trace：

不会：

显示：

IOC。

因为：

IOC：

属于：

框架行为。

---

# 十四、面试回答（中文）

**面试官：**

为什么企业项目喜欢 Dependency Injection？

**回答：**

Dependency Injection 将对象创建与业务逻辑解耦，业务层只依赖接口，而不负责创建对象。这样可以降低耦合度，提高测试能力和扩展能力。例如 Retail Insight AI 中，Service 不直接关心 Repository 的具体实现，将来切换 PostgreSQL、Redis 或 Mock Repository 时，业务代码几乎不需要修改。

---

# 十五、面试回答（日语）

**面接官：**

Dependency Injection を採用する理由を説明してください。

**回答例：**

Dependency Injection はオブジェクト生成をフレームワークへ委譲する設計です。Service は Repository の実装に依存せず、必要なオブジェクトだけを利用します。そのため保守性・拡張性・テスト容易性が向上し、多くの企業システムで採用されています。

---

# 十六、日本 SES 常见追问

### Q：DI 和 Factory Pattern 有什么区别？

Factory：

负责：

创建对象。

Dependency Injection：

负责：

提供对象。

Factory：

解决：

"怎么创建？"

DI：

解决：

"谁来提供？"

两者：

可以：

一起使用。

不是：

互相替代。

---

# 十七、本章练习

请完成：

① 阅读：

```text
backend/app/api/tasks.py
```

↓

② 阅读：

```text
backend/app/services/task_service.py
```

↓

③ 阅读：

```text
backend/app/repositories/
```

↓

④ 思考：

如果：

Repository：

改成：

PostgreSQL。

TaskService：

需要修改吗？

---

# 十八、本章核心记忆图

```text
          Framework
               │
               ▼
     Create Dependency
               │
               ▼
      Dependency Injection
               │
               ▼
          TaskService
               │
               ▼
          Repository
               │
               ▼
            Database
```

---

# 本章总结

一句话：

```text
Don't create.

Inject.
```

Dependency Injection 的核心思想不是语法。

而是：

**业务对象不负责创建依赖，而是专注于业务逻辑。**

通过依赖注入，可以降低系统耦合度，提高可维护性、可测试性和扩展能力，这也是现代企业级系统广泛采用的架构设计思想。

---

# 下一章

**Chapter 28：Background Task Pattern（后台任务模式）**

学习：

- BackgroundTasks
- Async
- Producer / Consumer
- Long Running Task
- 为什么 AI Workflow 必须异步执行
