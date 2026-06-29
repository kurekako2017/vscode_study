# Codex Current Task

## Project

freee会計・法人決算・税務・社会保険知識庫

---

# Current Status

## 已完成

### 知識庫基礎架構

- [x] AGENTS.md
- [x] README.md
- [x] roadmap.md
- [x] task.md
- [x] backlog.md

### 手冊

- [x] freee手冊
- [x] eTax手冊
- [ ] eLTAX手冊完整实战版
- [x] 算定基礎届手冊
- [x] 年末調整手冊
- [x] 消費税手冊基础版

### 辭典

- [x] 勘定科目辭典
- [x] 法人税辭典
- [x] 消費税辭典
- [x] 社會保險辭典

### 範例

- [x] 別表一
- [x] 別表四
- [x] 別表五（一）
- [x] 別表五（二）
- [x] 消費税申告
- [x] 算定基礎届
- [x] 年末調整
- [x] 源泉所得税
- [x] 住民税

---

# Current Priority

以下按照順序執行。

---

## P1

状态：`[x] 已完成`

eTax手冊完善

檔案：

docs/tax/eTax手冊.md

要求：

* 法人税電子申告
* 消費税電子申告
* 利用者識別番号
* マイナンバーカード
* 電子署名
* 受信通知

必須：

* 日文
* 中文
* 編號步驟

---

## P2

状态：`[ ] 未完成`

eLTAX手冊完善

檔案：

docs/tax/eLTAX手冊.md

要求：

* 法人住民税
* 法人事業税
* 給与支払報告書
* 地方税共通納税

---

## P3

状态：`[x] 已完成`

算定基礎届手冊完善

檔案：

docs/social/算定基礎届手冊.md

要求：

* 4月
* 5月
* 6月

計算方式

申報方式

電子申請方式

---

## P4

状态：`[x] 已完成`

年末調整手冊完善

檔案：

docs/social/年末調整手冊.md

要求：

* 扶養控除
* 保険料控除
* 源泉徴収票
* 法定調書
* 給与支払報告書

---

## P5

状态：`[ ] 未完成`（分类目录已建立，截图内容尚未补充）

freee截圖操作指南

要求：

建立：

docs/screenshots

所有截圖必須脫敏。

---

# Editing Rules

1. 必须先按顺序读取：

* backlog.md
* task.md
* AGENTS.md
* README.md
* roadmap.md

2. 不刪除歷史內容。

3. 不重構目錄。

4. 不新增無意義文件。

5. 優先完善現有手冊。

6. freee操作必須編號。

7. 稅務術語必須：

* 日文
* 中文解釋

8. 涉及法規時以官方資料為準。

---

## Private Data Rule

以后所有真实公司数据都放在：

private/

不再放在 juesuan 根目录。

生成真实案例时优先读取 private/。

禁止将 private/ 内容复制到公开文档中。
只能提取必要摘要。

# Completion Rules

每次完成後：

1. 更新目标文件更新履历。
2. 更新 `backlog.md`，已完成任务改为 `[x]`，不删除历史任务。
3. 更新 `task.md`。
4. 更新 `updates/CHANGELOG.md`。
5. 汇报修改内容。
6. 不 commit。
7. 不 push。

## 2026-06-29 状态同步

- [x] 创建 `backlog.md`。
- [x] 增加开工时优先检查 backlog、task 的规则。
- [x] 增加完工后同步更新 backlog、task、CHANGELOG 的规则。
- [x] 按现有成果校准 P1、P3、P4 为已完成。
- [ ] P2：完善 eLTAX 手册。
- [ ] P5：补充脱敏截图内容。
