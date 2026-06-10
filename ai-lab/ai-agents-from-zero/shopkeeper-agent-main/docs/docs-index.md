# 文档总目录

> 这个页面把 `shopkeeper-agent-main` 最常用的运行、模板和环境说明集中到一起。

## 0. 一眼看懂

```text
想启动和排错
  -> 看 workspace-run-guide.md
想先确认环境要准备什么
  -> 看 environment-checklist.md
想快速知道功能有哪些、怎么测
  -> 看 feature-usage-test-template.md
想按功能逐项验收
  -> 看 feature-usage-test-full.md
想复用到别的项目
  -> 看 feature-usage-template-generic.md
想快速勾选检查项
  -> 看 feature-checklist.md
想看最终启动 / 验证 / 排错入口
  -> 看 start-verify-troubleshoot-final.md
想直接复制启动命令
  -> 看 quick-start-copy.md
```

## 1. 先看哪份

- 总入口：[`README.md`](../README.md)
- 启动 / 验证 / 排错：[`当前工作区运行指南`](workspace-run-guide.md)
- 环境清单：[`environment-checklist.md`](environment-checklist.md)
- 功能快速一览：[`当前项目功能使用与测试最短版`](feature-usage-test-template.md)
- 功能逐项验收：[`当前项目功能使用与测试完整版`](feature-usage-test-full.md)
- 通用复用模板：[`通用功能使用与测试模板`](feature-usage-template-generic.md)
- 功能检查清单：[`feature-checklist.md`](feature-checklist.md)
- 最终启动 / 验证 / 排错：[`start-verify-troubleshoot-final.md`](start-verify-troubleshoot-final.md)
- 复制即启动：[`quick-start-copy.md`](quick-start-copy.md)

## 2. 运行相关

- [当前工作区运行指南](workspace-run-guide.md)
- [环境清单](environment-checklist.md)
- [OpenRouter + NAS MySQL 说明](local-setup-openrouter-docker-mysql.md)
- [Mock 优先启动说明](mock-first-quickstart.md)
- [真实模式启动说明](openrouter-nas-mysql-quickstart.md)
- [复制即启动](quick-start-copy.md)

## 3. 功能文档模板

- [当前项目功能使用与测试最短版](feature-usage-test-template.md)
- [当前项目功能使用与测试完整版](feature-usage-test-full.md)
- [通用功能使用与测试模板](feature-usage-template-generic.md)
- [功能检查清单](feature-checklist.md)
- [复制即启动](quick-start-copy.md)

## 4. 当前项目已覆盖的功能示例

- mock 问数链路
- 真实问数链路
- 元数据知识库构建
- `/api/query` SSE 接口
- 前端问数页面联动
- NAS MySQL / Qdrant / Elasticsearch / Embedding 连接

## 5. 推荐顺序

1. 先看 [环境清单](environment-checklist.md)
2. 再看 [当前工作区运行指南](workspace-run-guide.md)
3. 先看 [功能使用与测试最短版](feature-usage-test-template.md)
4. 再看 [功能使用与测试完整版](feature-usage-test-full.md)
5. 如果你要新建项目，再看 [通用功能使用与测试模板](feature-usage-template-generic.md)
6. 想快速勾选检查项，再看 [功能检查清单](feature-checklist.md)
7. 想看最终入口，再看 [启动 / 验证 / 排错最终说明](start-verify-troubleshoot-final.md)
8. 想直接复制启动命令，再看 [复制即启动](quick-start-copy.md)

## 6. 说明

- 这份目录页的目标是减少你在多个文档之间来回找链接。
- 如果后面再新增文档，直接把链接补到这里即可。
