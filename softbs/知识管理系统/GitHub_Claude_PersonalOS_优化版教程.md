# GitHub + Claude Personal OS（进阶增量版）

> 本文档是“易懂版”的增量补充，只讲高级玩法。  
> 主入口（先看）：`softbs/用 GitHub + Claude Code（或类似大模型）打造一个轻量、输入极简、长期可积累的个人任务/日记/知识管理系统.md`

---

## 1. 什么时候需要这份进阶版

当你已经跑通以下最小闭环时再启用：

- 手机输入 -> Daily Issue 评论
- Actions 归档 -> `logs/YYYYMMDD.md`
- AI 周/月总结 -> `knowledge/YYYY-MM-回顾.md`

如果以上还没稳定，不要启用本页内容。

---

## 2. 进阶目录结构（仅新增）

```text
.github/
  ISSUE_TEMPLATE/
    ../notes/task.md
    goal.md
    habit.md
    insight.md
    review.md
    article.md
    book.md
    workout.md
    health.md
    expense.md
    asset.md
  workflows/
    recurring-tasks.yml
    monthly-review-reminder.yml

knowledge/
  reviews/
  dashboards/

docs/
  CATEGORIES.md
  PROMPTS.md
  REVIEW_CHECKLIST.md
```

说明：`quick-log.md` 和 `daily-log-to-md.yml` 在易懂版已覆盖，这里不重复。

---

## 3. Issue 分类的最小升级法

不要一次上 10+ 模板，按下面顺序逐步开：

### 阶段 A（第 2 周）

- `../notes/task.md`
- `goal.md`
- `habit.md`
- `insight.md`

### 阶段 B（第 3~4 周）

- `review.md`
- `article.md`
- `book.md`

### 阶段 C（稳定后）

- `workout.md`
- `health.md`
- `expense.md`
- `asset.md`

原则：模板数量 <= 你每周实际会用到的分类数量。

---

## 4. Projects 看板进阶规则（可直接抄）

建议字段：

- `Type`：task / goal / habit / insight / review
- `Priority`：P1 / P2 / P3
- `Energy`：High / Medium / Low
- `Due`：截止日期

建议泳道：

- Inbox
- This Week
- In Progress
- Done
- Parking Lot

建议规则：

- 新 Issue 默认进 `Inbox`
- `Priority=P1` 且 `Due<=7天` 自动进 `This Week`
- 关闭 Issue 自动进 `Done`

---

## 5. 周期任务自动生成（进阶）

创建：`.github/workflows/recurring-tasks.yml`

```yaml
name: Recurring Tasks
on:
  schedule:
    - cron: '0 0 * * 1'
  workflow_dispatch:

permissions:
  issues: write

jobs:
  create:
    runs-on: ubuntu-latest
    steps:
      - name: Create weekly habit issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          WEEK=$(date +"%G-W%V")
          TITLE="Habit Check ${WEEK}"
          if ! gh issue list --search "$TITLE in:title" --state all --limit 50 | grep -q "$TITLE"; then
            gh issue create \
              --title "$TITLE" \
              --label "habit" \
              --body "- [ ] 本周习惯打卡\n- [ ] 本周复盘"
          fi
```

---

## 6. AI 提炼进阶：三层输出法

每次 AI 总结都产出 3 层文件，避免“看完就忘”：

1. `knowledge/reviews/YYYY-MM-回顾.md`（完整分析）
2. `knowledge/dashboards/next-30-days.md`（未来 30 天行动）
3. `knowledge/dashboards/habit-signals.md`（习惯趋势）

### Prompt 模板（进阶版）

```text
你是我的个人复盘助手。请基于本月 logs/*.md 与已关闭的 task/goal/habit issue，输出：
1) 本月关键进展（不超过 10 条）
2) 重复出现的问题模式（按触发条件分类）
3) 下月 3 个最重要行动（每个含：目标、第一步、风险、兜底方案）
4) 哪些任务应停止（Stop Doing）
输出为 Markdown，分别写入：
- knowledge/reviews/YYYY-MM-回顾.md
- knowledge/dashboards/next-30-days.md
- knowledge/dashboards/habit-signals.md
```

---

## 7. 数据治理（避免系统越用越乱）

每月执行一次：

- 归档 30 天前的已完成 task
- 合并重复 insight
- 删除无内容空 Issue
- 给高价值条目补标签（`evergreen`、`playbook`）

建议在 `docs/REVIEW_CHECKLIST.md` 固定成清单。

---

## 8. 版本策略（避免文档再重复）

本仓库固定规则：

- **易懂版**：唯一主教程（面向执行）
- **进阶版**：只放增量能力（面向优化）
- 同主题不再维护两份完整教程

如果发现重复，优先保留易懂版正文。

---

## 9. 你下一步只做一件事

在本周先加一个功能即可：

- 推荐优先级：`recurring-tasks.yml`

跑一周稳定后，再加 AI 三层输出法。
