# JtProject 学习与启动入口

相关入口：

- 项目总导航：[Java项目总启动导航.md](../Java项目总启动导航.md)
- Java 项目根入口：[README.md](../README.md)
- 项目文档总索引：[doc/README.md](./doc/README.md)

这个项目的 Markdown 文档已经按用途整理到 `doc/` 下。

建议先看：

1. 本文件
2. [doc/README.md](./doc/README.md)
3. 再按启动、参考、测试或日式项目文档继续深入

## 快速启动（Windows / PowerShell）

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject
.\mvnw.cmd spring-boot:run
```

如果你在 Linux / macOS：

```bash
./mvnw spring-boot:run
```

启动成功后访问：

- 首页：[http://localhost:8082/](http://localhost:8082/)
- 管理员登录：[http://localhost:8082/admin/login](http://localhost:8082/admin/login)

默认端口是 `8082`（见 `src/main/resources/application.properties`）。

## 账号与验证

- 管理员：`admin / 123`
- 普通用户：`lisa / 765`

验证建议：

1. 用户登录
2. 管理员登录
3. 打开商品管理页，测试新增/更新/删除

## 学习文档

1. [手动启动项目完整指南.md](./doc/guides/手动启动项目完整指南.md)
2. [启动到登录页面的完整流程.md](./doc/reference/启动到登录页面的完整流程.md)
3. [CONTROLLER_注释说明.md](./doc/reference/CONTROLLER_注释说明.md)
4. [REFACTORING_GUIDE.md](./doc/guides/REFACTORING_GUIDE.md)
5. [TESTING_GUIDE.md](./doc/guides/TESTING_GUIDE.md)

历史性的启动成功、问题修复、临时记录文档已统一归档到 `doc/history/`。

## 脚本入口

- PowerShell: `.\scripts\start\run.ps1`
- CMD: `scripts\start\run.cmd`
- Linux / macOS: `./scripts/start/start.sh`
- 脚本导航: [scripts/README.md](./scripts/README.md)

## 文档索引

| 用途 | 推荐文档 | 说明 |
| --- | --- | --- |
| 总导航 | `doc/README.md` | 所有文档分类入口 |
| 首次启动（命令行） | `doc/guides/手动启动项目完整指南.md` | 最完整、当前版本维护中 |
| 首次启动（IDEA） | `doc/guides/手动启动项目完整指南-IDEA版.md` | 面向 IDEA 新手 |
| 启动后排障 | `doc/guides/启动失败解决方案.md` | 常见启动异常排查 |
| 请求链路学习 | `doc/reference/启动到登录页面的完整流程.md` | 理解 Controller 与页面跳转 |
| 架构与实现参考 | `doc/reference/项目框架与调用流程完整总结.md` | 理解整体结构 |
| 架构重构学习 | `doc/guides/REFACTORING_GUIDE.md` | 接口分层与重构说明 |
| 测试入门 | `doc/guides/TESTING_GUIDE.md` | 测试命令和实践建议 |
| 日式项目文档 | `doc/jp-docs/README.md` | 設計書、テスト仕様書、障害票等 |
| 历史归档 | `doc/history/` | 旧启动记录、修复记录、临时笔记 |

## 环境切换

默认命令使用当前配置（`application.properties`）。如需切 profile：

```powershell
.\mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=local
.\mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=mysql
.\mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=remote
```

Linux / macOS 对应命令：

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
./mvnw spring-boot:run -Dspring-boot.run.profiles=mysql
./mvnw spring-boot:run -Dspring-boot.run.profiles=remote
```

数据库配置详见：[ENV_CONFIG.md](./doc/reference/ENV_CONFIG.md)

## Batch 运行目录说明

项目里现在已经补了一套学习用模擬 batch，因此运行后会出现几类 batch 相关目录：

| 目录 | 作用 | 说明 |
| --- | --- | --- |
| `batch-work/` | batch 专用本地数据库目录 | `batch` profile 使用的 H2 文件 DB 会落在这里 |
| `batch-output/` | batch 结果输出目录 | 例如库存整合检查 CSV 会输出到这里 |
| `logs/batch/` | batch 日志目录 | batch 运行日志会输出到这里 |

当前 `batch` profile 的数据库配置在 [application-batch.properties](./src/main/resources/application-batch.properties)，其中：

- `spring.datasource.url=jdbc:h2:file:./batch-work/jtproject-batch...`
- `logging.file.name=logs/batch/product-inventory-check.log`
- `batch.output.dir=batch-output`

也就是说：

- `batch-work` 负责存放 batch 运行时的本地 H2 数据文件
- `batch-output` 负责存放 batch 业务输出结果
- `logs/batch` 负责存放 batch 运行日志

如果你看到 [batch-work](./batch-work) 目录里的 `.mv.db`、`.trace.db` 文件，它们不是源码，而是 batch 执行时生成的本地数据库文件。

## 使用建议

- 想先把项目跑起来：先看 [手动启动项目完整指南.md](./doc/guides/手动启动项目完整指南.md)
- 想理解 JSP 页面怎么进入 Controller：先看 [启动到登录页面的完整流程.md](./doc/reference/启动到登录页面的完整流程.md)
- 想理解整体结构：先看 [项目框架与调用流程完整总结.md](./doc/reference/项目框架与调用流程完整总结.md)
- 想查设计书和测试资料：进入 [doc/jp-docs/README.md](./doc/jp-docs/README.md)
