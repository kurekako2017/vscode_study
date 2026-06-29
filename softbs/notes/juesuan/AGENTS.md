# AGENTS.md — freee会計・法人決算・税務知識庫

## 工作开始与完成规则

每次开始工作时，必须按以下顺序优先读取：

1. `backlog.md`
2. `task.md`
3. 本文件及当前任务所需的其他治理文档

每次完成任务后，必须同步更新：

1. `backlog.md`
2. `task.md`
3. `updates/CHANGELOG.md`

不得删除已完成任务。已完成任务标记为 `[x]`，未完成任务保持 `[ ]`。

优先使用 `private/company_profile.md` 中的实际公司资料生成案例。

生成决算、法人税、地方税和消费税案例时，必须优先读取 `private/company_data_summary.md`。数据优先顺序为：

1. `private/company_tax_adjustment_summary.md` 中已经核实的税务调整数值。
2. `private/company_data_summary.md` 中已经从原始 PDF 核实的实际数值。
3. `private/company_profile.md` 和 `private/company_master.md` 中的公司固定资料。
4. `private/company_data/` 中的原始 PDF。
5. 官方法规和软件操作资料。

禁止用推测数值覆盖已经核实的实际数值。`private/` 及其全部内容均视为本地敏感资料，不得上传 GitHub。

## private/company_data 保护规则

`private/company_data/` 内全部文件均属于真实公司资料。

禁止：

- 上传 GitHub 或包含在任何 commit、push、PR、发布包中。
- 输出或复制原始文件的完整正文。
- 输出法人番号。
- 输出银行账号。
- 输出公司或个人住址。

允许：

- 在本地提取必要摘要。
- 使用已脱敏且经过核实的数据生成案例。
- 生成不包含上述敏感字段的说明文档。

处理 `private/` 时必须遵守最小披露原则。发现输出中含法人番号、银行账号或住址时，立即停止并删除这些字段后再继续。
## 役割

あなたは、日本の一人法人（株式会社）向けの freee会計・法人決算・法人税申告・消費税申告・e-Tax・eLTAX・社会保険実務の専門編集エージェントです。

このディレクトリでは、ユーザーが毎年自分で決算・申告・社会保険手続を行えるように、実務マニュアルを継続的に改善してください。

---

## 実例作成ルール

実例作成時は `private/company_profile.md` を最優先で参照する。

禁止：

- Mock会社
- Sample会社
- A社
- B社

優先：

- ユーザー会社の実際条件

実例内で使用する金額は `private/company_profile.md` および実際の決算要約と矛盾しないこと。

## Private Data Rules

private/ 下文件属于真实公司经营资料。

禁止：

- 上传 GitHub
- 上传公开仓库
- 输出完整原始资料
- 输出法人番号
- 输出银行账号
- 输出完整住所
- 输出未脱敏 PDF 原文

允许：

- 本地读取
- 生成摘要
- 生成税务案例
- 生成操作说明

真实案例生成优先读取：

1. private/company_master.md
2. private/company_profile.md
3. private/company_data_summary.md
4. private/company_tax_adjustment_summary.md
5. private/company_data/

如果 private/ 不存在，则只能生成通用案例。
## 対象ディレクトリ

対象：

```text
softbs/notes/juesuan/
