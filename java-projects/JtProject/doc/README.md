# JtProject 文档总索引

相关入口：

- 项目根入口：[README.md](../README.md)
- Java 项目总导航：[Java项目总启动导航.md](../../Java项目总启动导航.md)
- Java 项目文档入口：[doc/README.md](../../doc/README.md)

`doc/` 目录已经按用途整理为以下 4 类：

## 建议先看

如果你是第一次看这个项目，推荐顺序：

1. [README.md](../README.md)
2. [手动启动项目完整指南.md](./guides/手动启动项目完整指南.md)
3. [启动到登录页面的完整流程.md](./reference/启动到登录页面的完整流程.md)
4. [项目框架与调用流程完整总结.md](./reference/项目框架与调用流程完整总结.md)
5. [doc/jp-docs/README.md](./jp-docs/README.md)

## 1. guides

路径：`doc/guides/`

适合直接上手和操作执行的文档：

- [手动启动项目完整指南.md](./guides/手动启动项目完整指南.md)
- [手动启动项目完整指南-IDEA版.md](./guides/手动启动项目完整指南-IDEA版.md)
- [启动失败解决方案.md](./guides/启动失败解决方案.md)
- [REFACTORING_GUIDE.md](./guides/REFACTORING_GUIDE.md)
- [TESTING_GUIDE.md](./guides/TESTING_GUIDE.md)

## 2. reference

路径：`doc/reference/`

适合理解项目结构、调用链和环境配置的文档：

- [CONTROLLER_注释说明.md](./reference/CONTROLLER_注释说明.md)
- [ENV_CONFIG.md](./reference/ENV_CONFIG.md)
- [JAVADOC_LOGGING_SUMMARY.md](./reference/JAVADOC_LOGGING_SUMMARY.md)
- [数据访问层与调用链学习文档.md](./reference/数据访问层与调用链学习文档.md)
- [userLogin.jsp跳转到UserController的完整流程.md](./reference/userLogin.jsp跳转到UserController的完整流程.md)
- [启动到登录页面的完整流程.md](./reference/启动到登录页面的完整流程.md)
- [测试类已禁用说明.md](./reference/测试类已禁用说明.md)
- [项目框架与内容总结.md](./reference/项目框架与内容总结.md)
- [项目框架与调用流程完整总结.md](./reference/项目框架与调用流程完整总结.md)

## 3. jp-docs

路径：`doc/jp-docs/`

面向日本项目风格的交付文档：

- [README.md](./jp-docs/README.md)
- 設計書、基本設計書、詳細設計書、製造説明書
- 単体テスト仕様書、結合テスト仕様書、総合テスト仕様書
- 障害票、改修票、調査票

## 4. history

路径：`doc/history/`

归档历史性文档，保留过程记录，但不作为主入口。

建议先看合并后的 3 份主文档：

- [01_启动历史总结.md](./history/01_启动历史总结.md)
- [02_问题修复历史总结.md](./history/02_问题修复历史总结.md)
- [03_历史归档索引.md](./history/03_历史归档索引.md)

旧目录说明：

- `startup/`: 启动成功、快速启动、旧启动方案
- `fixes/`: 问题修复、运行按钮、登录 404 等修复记录
- `notes/`: 临时导航、memo

## 使用建议

- 想先把项目跑起来：先看 [README.md](../README.md)
- 想按步骤启动并排障：先看 [手动启动项目完整指南.md](./guides/手动启动项目完整指南.md)
- 想看页面如何进入 Controller：先看 [启动到登录页面的完整流程.md](./reference/启动到登录页面的完整流程.md)
- 想理解整体结构：先看 [项目框架与调用流程完整总结.md](./reference/项目框架与调用流程完整总结.md)
- 想查看日式项目资料：先看 [doc/jp-docs/README.md](./jp-docs/README.md)
