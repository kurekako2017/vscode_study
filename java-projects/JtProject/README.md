# JtSpringProject 学习与启动入口

这个项目文档较多，建议只从本文件开始。先跑起来，再按学习路线看细节文档。

## 1) 快速启动（Windows / PowerShell）

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

## 2) 账号与验证

- 管理员：`admin / 123`
- 普通用户：`lisa / 765`

验证建议：

1. 用户登录
2. 管理员登录
3. 打开商品管理页，测试新增/更新/删除

## 3) 学习路线（按顺序）

1. `doc/🚀快速启动指南.md`（先确认你能稳定启动）
2. `doc/启动到登录页面的完整流程.md`（理解请求入口和页面跳转）
3. `CONTROLLER_注释说明.md`（看 Controller 层职责）
4. `REFACTORING_GUIDE.md`（了解当前重构方向）
5. `TESTING_GUIDE.md`（后续补测试再看）

> 说明：`doc` 目录里有很多“启动成功/问题修复总结”类文档，历史价值大于学习价值。优先按以上 5 个文档阅读即可。

## 4) 文档索引（按用途）

| 用途 | 推荐文档 | 说明 |
| --- | --- | --- |
| 首次启动（命令行） | `doc/手动启动项目完整指南.md` | 最完整、当前版本维护中 |
| 首次启动（IDEA） | `doc/手动启动项目完整指南-IDEA版.md` | 面向IDEA新手 |
| 启动后排障 | `doc/启动失败解决方案.md` | 历史问题集合，按关键词查阅 |
| 请求链路学习 | `doc/启动到登录页面的完整流程.md` | 理解Controller与页面跳转 |
| 架构重构学习 | `REFACTORING_GUIDE.md` | 接口分层与重构说明 |
| 测试入门 | `TESTING_GUIDE.md` | 测试命令和实践建议 |

## 5) 环境切换（可选）

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

数据库配置详见：`ENV_CONFIG.md`
