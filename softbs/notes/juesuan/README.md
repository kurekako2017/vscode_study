# freee会計・法人決算知識庫

## 目的

本ディレクトリは、日本の一人法人（株式会社）向けの

* freee会計
* 法人決算
* 法人税申告
* 消費税申告
* e-Tax
* eLTAX
* 算定基礎届
* 年末調整

を体系的に管理する知識庫である。

---

## 利用ルール

1. AGENTS.md を最優先で参照する。
2. task.md を現在作業として実行する。
3. roadmap.md を長期計画として参照する。
4. 更新履歴を必ず残す。
5. 初心者向け説明を優先する。

---

## ユーザー情報

会社形態：

* 日本株式会社
* 一人法人
* IT・SES事業

会計ソフト：

* freee会計

電子申告：

* e-Tax
* eLTAX

---

## 最終目標

このディレクトリを

「一人法人 freee会計・税務・社会保険 完全実務マニュアル」

として継続的に発展させる。

---

## 手册导航

| 手册 | 用途 |
| --- | --- |
| [freee主手册（完整实战版）](docs/freee/freee主手册.md) | 银行同步、自动记账、应收应付、工资、固定资产、月结、年结和决算准备 |
| [eTax手册](docs/tax/eTax手册.md) | 法人税别表与国税电子申报 |
| [eLTAX手册](docs/tax/eLTAX手册.md) | 法人地方税与工资支付报告书 |
| [算定基礎届手册](docs/social/算定基礎届手册.md) | 算定基础届与月额变更届 |
| [年末調整手册](docs/social/年末調整手册.md) | 年末调整、源泉征收票与法定调书 |
| [消費税手册](docs/tax/消費税手册.md) | 消费税率、税区分、申报与缴纳 |
| [勘定科目辞典](docs/glossary/勘定科目辞典.md) | 常用科目、仕訳和错误修正 |
| [月次检查表](docs/checklist/月次检查表.md) | 每月执行和验收清单 |
| [年次检查表](docs/checklist/年次检查表.md) | 年度日程、决算和申报清单 |

## 实例导航

| 分类 | 实例 |
| --- | --- |
| 法人税・消费税 | [別表一](docs/examples/tax/別表一_实例.md)・[別表四](docs/examples/tax/別表四_实例.md)・[別表五（一）](docs/examples/tax/別表五一_实例.md)・[別表五（二）](docs/examples/tax/別表五二_实例.md)・[消費税申告](docs/examples/tax/消費税申告_实例.md) |
| 社会保险・工资税务 | [算定基礎届](docs/examples/social/算定基礎届_实例.md)・[年末調整](docs/examples/social/年末調整_实例.md)・[住民税](docs/examples/social/住民税_实例.md)・[源泉所得税](docs/examples/social/源泉所得税_实例.md) |
| freee Mock 占位 | [役員借入金](docs/examples/freee/役員借入金_实例.md)・[未払消費税](docs/examples/freee/未払消費税_实例.md)・[給与処理](docs/examples/freee/給与処理_实例.md) |

## 企业级知识库目录树

```text
juesuan/
├── AGENTS.md
├── README.md
├── roadmap.md
├── task.md
├── docs/
│   ├── freee/
│   │   └── freee主手册.md
│   ├── tax/
│   │   ├── eTax手册.md
│   │   ├── eLTAX手册.md
│   │   └── 消費税手册.md
│   ├── social/
│   │   ├── 算定基礎届手册.md
│   │   └── 年末調整手册.md
│   ├── checklist/
│   │   ├── 月次检查表.md
│   │   └── 年次检查表.md
│   ├── glossary/
│   │   ├── 勘定科目辞典.md
│   │   ├── 消費税辞典.md
│   │   ├── 法人税辞典.md
│   │   └── 社会保険辞典.md
│   ├── examples/
│   │   ├── tax/
│   │   ├── social/
│   │   └── freee/
│   └── screenshots/
│       ├── freee/
│       ├── eTax/
│       ├── eLTAX/
│       └── social/
├── archive/
│   └── 历史资料
└── updates/
    └── CHANGELOG.md
```

## 知识库导航设计

- `docs/freee/`：freee 日常记账、月结和决算主流程。
- `docs/tax/`：法人国税、地方税和消费税。
- `docs/social/`：社会保险及工资年度手续。
- `docs/checklist/`：可以直接执行的月次、年次清单。
- `docs/glossary/`：勘定科目与仕訳查询入口。
- `docs/examples/`：使用虚构数据说明填写步骤和表间联动；不能直接提交。
- `docs/screenshots/`：只保存完成脱敏的操作截图。
- `archive/`：保留不再作为主入口的历史资料。
- `updates/`：记录知识库结构和内容变更。
- 根目录：治理规则、路线图、当前任务及历史总稿。

## 知识库导航（按业务主题）

1. **freee操作**：[freee主手册](docs/freee/freee主手册.md)・[勘定科目辞典](docs/glossary/勘定科目辞典.md)・[freee实例](docs/examples/freee/)
2. **法人税**：[eTax与法人税手册](docs/tax/eTax手册.md)・[法人税辞典](docs/glossary/法人税辞典.md)・[別表实例](docs/examples/tax/)
3. **消費税**：[消費税手册](docs/tax/消費税手册.md)・[消費税辞典](docs/glossary/消費税辞典.md)・[申告实例](docs/examples/tax/消費税申告_实例.md)
4. **e-Tax**：[eTax手册](docs/tax/eTax手册.md)・[eTax截图目录](docs/screenshots/eTax/)
5. **eLTAX**：[eLTAX手册](docs/tax/eLTAX手册.md)・[eLTAX截图目录](docs/screenshots/eLTAX/)
6. **算定基礎届**：[算定基礎届手册](docs/social/算定基礎届手册.md)・[填写实例](docs/examples/social/算定基礎届_实例.md)
7. **年末調整**：[年末調整手册](docs/social/年末調整手册.md)・[处理实例](docs/examples/social/年末調整_实例.md)
8. **实例库**：[税务实例](docs/examples/tax/)・[社会保险实例](docs/examples/social/)・[freee实例](docs/examples/freee/)
9. **术语库**：[勘定科目](docs/glossary/勘定科目辞典.md)・[消费税](docs/glossary/消費税辞典.md)・[法人税](docs/glossary/法人税辞典.md)・[社会保险](docs/glossary/社会保険辞典.md)

变更记录：[CHANGELOG](updates/CHANGELOG.md)。

## 历史资料

- [freee会計・法人決算・税務運用マスターガイド](freee_法人決算税務運用マスターガイド.md)：分册前的历史总稿，继续保留。
- [freee_法人決算完整指南](archive/freee_法人決算完整指南.md)：既有中文决算指南。
- [不购买申告方案的法人税操作手册](archive/freee会計（不购买申告プラン）法人税申告操作手册.md)：既有特定场景资料。
- [freee法人公司决算操作指南 PDF](archive/freee会计法人公司决算操作指南.pdf)：既有 PDF 资料。

## 推荐使用顺序

1. 从 `docs/freee/freee主手册.md` 了解整体流程。
2. 每月执行 `docs/checklist/月次检查表.md`。
3. 决算前执行 `docs/checklist/年次检查表.md`。
4. 遇到具体事项时进入对应专题手册。
5. 税率、期限和软件功能每年从官方网站重新确认。

## 更新履历

### 2026-06-29

- 将历史总稿拆分为 9 份专题手册。
- 增加手册导航、历史资料入口和推荐使用顺序。
- 第二阶段建立 `docs/` 企业级分类结构并修复相对链接。
- 新增 `docs/examples/` 与 9 份 Mock 实例导航。
- 第三阶段新增截图分区、archive、CHANGELOG、examples分类和三类术语库。
- 将 `docs/freee/freee主手册.md` 扩充为完整实战版，加入 13 类核心操作流程、日中双语说明、验证标准和官方画面参考。
