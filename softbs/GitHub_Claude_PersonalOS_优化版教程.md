# 用 GitHub + Claude Code（或类似大模型）打造个人 AI 管理系统（优化版）

## 概述
目标：用 GitHub（Issues + Projects + Actions）配合 Claude Code（或任意 LLM），搭建一个轻量、输入极简且可长期回溯的个人系统，管理多个维度：任务、目标、日记、学习、健康、财务、灵感等。

设计原则：
- **输入要低摩擦**：手机一键（语音或文本）即可快速记录，支持碎片化输入；
- **分类要清晰**：Issue 类别多元化，能精确描述不同类型的内容，便于后续检索与 AI 提炼；
- **数据要可积累**：所有记录都存入 Git，可版本回溯、搜索、迁移；
- **可用 AI 提炼**：定期把零散记录交给 LLM 进行结构化整理和深度分析。

## 整体流程（推荐闭环）
```
手机快捷指令（或语音）
       ↓
快速输入 → 选择类型 → GitHub Issue 提交
       ↓
GitHub Projects 看板整理 / 标签管理 / 优先级分配
       ↓
每日/定期由 GitHub Actions 自动归档日志为 logs/*.md
       ↓
Claude Code 或其他 LLM 定期读取仓库并提炼知识
       ↓
结构化知识笔记 → knowledge/ 目录
       ↓
周期性回顾（月/季/年）并更新目标
```

---

## 步骤 1：创建仓库与完整的 Issue 分类体系

### 1.1 创建仓库结构
1. 新建一个私有仓库，例如 `life-manager`、`my-second-brain` 或 `personal-os`。
2. 初始化目录结构：
   ```
   .github/
     ISSUE_TEMPLATE/
       task.md           # 任务
       goal.md           # 目标
       article.md        # 文章
       book.md           # 书籍
       habit.md          # 习惯
       workout.md        # 训练
       health.md         # 健康
       insight.md        # 灵感
       review.md         # 回顾
       expense.md        # 支出
       asset.md          # 资产
       quick-log.md      # 快速记录
     workflows/
       daily-log-to-md.yml       # 日志自动归档
       recurring-tasks.yml       # 重复任务生成
   logs/                 # 日志文件（自动生成）
   knowledge/            # AI 提炼的知识库（手动维护）
   docs/
     CATEGORIES.md       # Issue 分类说明
     SHORTCUTS.md        # 快捷指令配置指南
   ```

### 1.2 完整的 Issue 模板体系

#### **1.2.1 工作与学习类**

**`.github/ISSUE_TEMPLATE/task.md`** — 日常任务 / 待办

```markdown
---
name: 📋 任务
about: 日常 ToDo / 行动项
labels: task
---

**优先度**：🔴 高 / 🟡 中 / 🟢 低  
**截止日**：  
**预计时长**：  
**所属目标**（可选）：  

## 任务内容
- [ ] 子任务 1
- [ ] 子任务 2
- [ ] 子任务 3

## 相关文档/链接
- 

## 完成标准
（什么情况下该任务算"完成"）
```

**`.github/ISSUE_TEMPLATE/article.md`** — 文章 / 学习笔记

```markdown
---
name: 📚 文章
about: 阅读、学习、参考文章
labels: article
---

**来源 URL**：  
**标签/领域**：技术 / 产品 / 生活 / 其他  
**优先度**：🔴 高 / 🟡 中 / 🟢 低  
**阅读状态**：⬜ 未读 / 🟡 正在读 / ✅ 已读  

## 核心内容摘要
（关键概念、技术点、启发）

## 关键引用
> "重要的句子或观点"

## 我的反思
（如何应用到工作/生活中）

## 相关文章
```

**`.github/ISSUE_TEMPLATE/book.md`** — 书籍阅读记录

```markdown
---
name: 📖 书籍
about: 图书、教材、专著记录
labels: book
---

**书名**：  
**作者**：  
**类别**：技术 / 传记 / 小说 / 自助 / 其他  
**ISBN**：  
**购入日期**：  
**阅读进度**：0% / ⏳ 开始阅读 / 📖 进行中 / ✅ 已完成  

## 书籍简介

## 关键章节与笔记
- 第 N 章：（记录关键内容）
- 第 M 章：

## 收获与评价
**评分**：⭐⭐⭐⭐⭐（5 分制）  
**推荐指数**：  
**金句摘录**：
- 
- 

## 后续行动
- [ ] 应用这本书的某个概念
- [ ] 推荐给朋友
```

#### **1.2.2 生活与计划类**

**`.github/ISSUE_TEMPLATE/goal.md`** — 目标 / 里程碑

```markdown
---
name: 🎯 目标
about: 短期 / 中期 / 长期目标
labels: goal
---

**目标类型**：个人 / 工作 / 学习 / 健康 / 财务  
**时间周期**：本周 / 本月 / 本季度 / 本年 / 多年  
**优先度**：🔴 高 / 🟡 中 / 🟢 低  
**状态**：🔵 规划中 / 🟡 进行中 / ✅ 已完成 / ❌ 已放弃  

## 目标描述
（SMART 原则：Specific, Measurable, Achievable, Relevant, Time-bound）

## 为什么设定这个目标？
（背景与动机）

## 拆解与行动计划
- [ ] 行动项 1（预计耗时：）
- [ ] 行动项 2（预计耗时：）
- [ ] 行动项 3（预计耗时：）

## 成功指标
- 完成标志 1：
- 完成标志 2：

## 进度跟踪
（请在评论中定期更新）
```

**`.github/ISSUE_TEMPLATE/habit.md`** — 习惯追踪

```markdown
---
name: ✅ 习惯
about: 日常习惯与重复任务
labels: habit
---

**习惯名称**：  
**目标频率**：每天 / 每周 N 次 / 每月  
**开始日期**：  
**所属目标**（可选）：  

## 习惯说明
（为什么要养成这个习惯？期望达到什么效果？）

## 习惯链
（有哪些相关联的习惯？）

## 追踪方式
（周期性检查清单在评论中更新）
- 周一：
- 周二：
- ...

## 挑战与对策
（可能遇到的难点与应对方案）
```

#### **1.2.3 健身与健康类**

**`.github/ISSUE_TEMPLATE/workout.md`** — 训练 / 运动记录

```markdown
---
name: 💪 训练
about: 健身、运动、体能训练
labels: workout
---

**训练类型**：🏃 跑步 / 💪 力量 / 🧘 瑜伽 / 🚴 骑行 / 其他  
**日期**：  
**时长**：（分钟）  
**强度**：🔵 低 / 🟡 中 / 🔴 高  
**天气/环境**：  

## 训练内容
**热身**：  
**主要动作与组数**：  
**冷却与拉伸**：  

## 生理数据
- 平均心率：bpm
- 最大心率：bpm
- 卡路里消耗：kcal
- VO2Max：ml/kg/min（如果有）

## 感受与备注
（身体状态、疲劳度、运动感受）

## 相关目标
```

**`.github/ISSUE_TEMPLATE/health.md`** — 健康数据 / 体检

```markdown
---
name: 🏥 健康
about: 体检、医疗记录、身体数据
labels: health
---

**记录类型**：🩺 体检 / ⚖️ 体重 / 🩹 血压 / 💉 疫苗 / 其他  
**日期**：  
**来源**：医院 / 家用设备 / APP 记录  

## 数据项目
- 身高：cm
- 体重：kg
- BMI：
- 血压：mmHg
- 其他项目：

## 医嘱 / 建议
（医生的建议或自己的分析）

## 后续行动
- [ ] 约医生复诊
- [ ] 调整生活习惯
```

#### **1.2.4 知识与想法类**

**`.github/ISSUE_TEMPLATE/quick-log.md`** — 快速记录 / 日记

```markdown
---
name: 📝 快速记录
about: 日记、灵感、短感悟、碎片笔记
labels: log
---

（直接输入内容，格式随意，支持时间戳和 emoji）
```

**`.github/ISSUE_TEMPLATE/insight.md`** — 灵感 / 想法

```markdown
---
name: 💡 灵感
about: 想法、洞见、创意、待验证假设
labels: insight
---

**灵感分类**：🔧 技术 / 🎨 产品 / 🌱 生活 / 📈 商业 / 其他  
**相关领域**：  
**紧急度**：🔴 立即探索 / 🟡 后续考虑 / 🟢 收藏备用  

## 核心想法
（简明扼要地描述想法）

## 背景与启发
（从哪里得到的启发？谁告诉你的？）

## 潜在价值
（如果实现，会带来什么好处？）

## 验证步骤
- [ ] 验证假设 1
- [ ] 验证假设 2

## 相关灵感/项目
```

**`.github/ISSUE_TEMPLATE/review.md`** — 评论 / 反思 / 回顾

```markdown
---
name: 🔍 回顾
about: 事件、项目、书籍、课程的评论与反思
labels: review
---

**回顾对象**：  
**日期**：  
**总体评价**：⭐⭐⭐⭐⭐（5 分制）  

## 亮点与收获
-
-

## 不足与改进
-
-

## 对自己的启发

## 个人感受与成长

## 如果再来一次会怎么做？
```

#### **1.2.5 财务与资产类**

**`.github/ISSUE_TEMPLATE/expense.md`** — 支出 / 消费记录

```markdown
---
name: 💰 支出
about: 消费、开支、付款记录
labels: expense
---

**日期**：  
**类别**：🍔 食物 / 🚗 交通 / 🛍️ 购物 / 📚 学习 / 💊 健康 / 🏠 房租 / 其他  
**金额**：¥  
**支付方式**：💳 卡 / 💵 现金 / 📱 手机支付 / 其他  
**必要性**：🔴 必需 / 🟡 重要 / 🟢 可选  

## 商品/服务说明
（购买了什么？从哪里购买？）

## 备注与感受
（值不值？下次会不会这样买？）

## 相关预算类别
```

**`.github/ISSUE_TEMPLATE/asset.md`** — 资产管理 / 设备清单

```markdown
---
name: 🔧 资产
about: 设备、工具、购买记录
labels: asset
---

**资产名称**：  
**型号**：  
**购买日期**：  
**购买价格**：¥  
**供应商/品牌**：  
**状态**：✅ 正常 / 🔧 维修中 / ⚠️ 待更换 / ❌ 已报废  
**保修期至**：  

## 规格与参数
-
-

## 使用说明
-

## 维保记录
- 日期：操作：成本：

## 升级/替代方案

## 出售/处理记录
```

### 1.3 创建 Issue 分类说明文档

在 `docs/CATEGORIES.md` 中维护一份完整的使用指南：

```markdown
# Issue 类别使用指南

## 📋 任务 (task)
**用途**：日常待办、项目任务、行动项  
**特点**：有明确截止日、优先度、完成标准  
**流程**：新建 → 分配 / 标签 → 追踪进度 → 完成关闭  
**使用场景**：工作任务、家务、学习任务、购物清单等

---

## 🎯 目标 (goal)
**用途**：短期 / 中期 / 长期目标  
**特点**：SMART 原则、包含拆解与里程碑、长期追踪  
**流程**：定义目标 → 拆解行动 → 定期更新进度 → 年底评估  
**使用场景**：年度目标、职业发展、学习计划、健身目标等

---

## 📚 文章 (article) & 📖 书籍 (book)
**用途**：阅读资源、参考文档、学习记录  
**特点**：记录来源、阅读进度、核心内容、个人反思  
**流程**：收藏链接 → 开始阅读 → 记录笔记 → 标记完成 → 定期回顾  
**使用场景**：博客、教程、论文、图书等

---

## ✅ 习惯 (habit)
**用途**：日常重复事项、习惯养成  
**特点**：周期性、长期积累、可量化追踪  
**流程**：定义习惯 → 周期性检查 → 记录执行情况 → 定期反思  
**使用场景**：每日运动、冥想、阅读、编码时间等

---

## 💪 训练 (workout) & 🏥 健康 (health)
**用途**：健身记录、健康数据、医疗记录  
**特点**：数据详细、便于分析趋势、与目标关联  
**流程**：记录每次训练 / 体检 → 定期分析 → 调整计划  
**使用场景**：跑步、健身房、瑜伽、体检数据等

---

## 💡 灵感 (insight)
**用途**：想法、创意、待验证假设  
**特点**：轻量级、快速记录、可升级为任务或目标  
**流程**：快速记录想法 → 验证可行性 → 升级为行动项或存档  
**使用场景**：创业点子、产品创意、生活改进方案等

---

## 📝 快速记录 (log)
**用途**：日记、感悟、碎片笔记  
**特点**：格式自由、快速输入、自动归档  
**流程**：在 Daily Log Issue 评论 → Actions 自动生成 md 文件  
**使用场景**：日常反思、事件记录、灵感片段、工作日志等

---

## 🔍 回顾 (review)
**用途**：事件、项目、书籍、课程的评论与反思  
**特点**：结构化总结、包含收获与改进点  
**流程**：事件结束后记录 → 定期查看 → 应用到未来  
**使用场景**：项目总结、课程评价、旅行记录、年度总结等

---

## 💰 支出 (expense) & 🔧 资产 (asset)
**用途**：财务记录、资产管理  
**特点**：分类清晰、便于统计、与预算关联  
**流程**：记录每笔开支 / 资产 → 月度统计 → 年度分析  
**使用场景**：消费追踪、预算管理、物品清单、维保记录等

---

## 标签 (Labels) 推荐
根据需求创建以下标签便于过滤：
- `task`, `goal`, `article`, `book`, `habit`, `workout`, `health`, `insight`, `log`, `review`, `expense`, `asset`
- `urgent` — 紧急项目
- `blocked` — 被阻塞，等待他人
- `next-week` — 下周处理
- `someday` — 有朝一日
- `bug` — 问题/错误
- `enhancement` — 改进/优化
```

---

## 步骤 2：手机端实现"超低摩擦输入"（关键）

### 2.1 方式 A：快速创建新 Issue（任选模板）

**iPhone 快捷指令配置**（通用方案）：
1. 显示菜单，让用户选择 Issue 类型（task / goal / article / book / workout 等）
2. 根据选择构造对应的 GitHub Issue 新建 URL
3. 在 Safari 打开该 URL，用户可在页面上快速填充内容

示例 URL：
```
https://github.com/<用户名>/<仓库>/issues/new?title=标题&labels=task&template=task.md
```

可替换的模板列表：
- `task.md` — 任务（最常用）
- `goal.md` — 目标
- `article.md` — 文章
- `book.md` — 书籍
- `habit.md` — 习惯
- `workout.md` — 训练
- `health.md` — 健康
- `insight.md` — 灵感
- `review.md` — 回顾
- `expense.md` — 支出
- `asset.md` — 资产

### 2.2 方式 B（推荐）：快速日记 + API 评论

**最低摩擦的输入方案** — 所有日记/灵感都通过单一快捷指令扔进 Daily Issue：

#### **Step 1: 生成 PAT（Personal Access Token）**
1. 登录 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 勾选权限：`repo`（访问公开和私有仓库）
4. 复制 token 并妥善保管（只会显示一次）

#### **Step 2: 创建快捷指令**（支持语音输入）

快捷指令流程：
```
显示菜单（选择记录类型）
     ↓
获取输入文本或语音
     ↓
构建 API 请求
     ↓
POST 到 GitHub
     ↓
播放成功提示音
```

快捷指令伪代码：
```
1. 显示菜单
   - 日记
   - 灵感
   - 想法
   - 反思
   - 其他

2. 询问输入（或语音识别）
   - 如果选了"日记"，则问"今天有什么值得记录吗？"
   - 如果选了"灵感"，则问"什么灵感？"

3. 构建请求体
   - 类型标记：**[日记]** 或 **[灵感]**
   - 用户输入
   - 当前时间戳

4. POST 请求
   - URL: API 评论端点
   - Header: PAT 认证
   - Body: JSON 格式内容

5. 播放提示
   - "已记录"（语音或弹窗）
```

#### **Step 3: API 请求参数**

```
URL: https://api.github.com/repos/<用户名>/<仓库>/issues/123/comments
（123 改为你的 Daily Issue 编号）

Method: POST

Headers:
  Accept: application/vnd.github+json
  Authorization: Bearer <你的PAT>

Body (JSON):
{
  "body": "**[日记]** 今天很开心，学到了很多东西\n\n时间: 2025-01-20 下午 3:30"
}
```

#### **Step 4: 高级用法——为不同记录添加标签**（可选）

如果希望不同类型的日记能带上不同标签：
1. 先在 GitHub 创建对应的 Labels（log / insight / thought 等）
2. 在快捷指令中根据用户选择拼接不同的 label 参数
3. 调用 GitHub GraphQL API 或 REST API 为 Issue 添加标签

示例（添加标签）：
```bash
curl -X PATCH https://api.github.com/repos/<用户名>/<仓库>/issues/123 \
  -H "Authorization: Bearer <PAT>" \
  -H "Accept: application/vnd.github+json" \
  -d '{"labels": ["log", "personal"]}'
```

### 2.3 方式 C：直接创建 Issue（API 新建）

如果想通过 API 直接创建新 Issue（绕过 web 表单）：

```bash
curl -X POST https://api.github.com/repos/<用户名>/<仓库>/issues \
  -H "Authorization: Bearer <PAT>" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title": "周一的训练计划",
    "body": "- 跑步 5 km\n- 力量训练 30 分钟",
    "labels": ["task", "workout"]
  }'
```

### 2.4 推荐的快捷指令组织方案

创建多个快捷指令满足不同场景，方便一键启动或 Siri 语音调用：

**快速记录类（频率最高，一键启动）**：
- **快捷指令 1**: 「💡 日记速记」— 支持语音输入，快速扔进 Daily Log Issue（推荐设置为 Siri 快捷方式）
- **快捷指令 2**: 「✨ 灵感记录」— 记录突然想到的想法/创意
- **快捷指令 3**: 「🤔 想法反思」— 记录对某事的思考

**正式表单类（需要逐项填充）**：
- **快捷指令 4**: 「📋 新建任务」— 弹出表单填充任务信息，新建 task Issue
- **快捷指令 5**: 「🎯 设定目标」— 新建 goal Issue，含拆解
- **快捷指令 6**: 「📚 开始读书」— 新建 book Issue，填充书籍信息
- **快捷指令 7**: 「📰 保存文章」— 新建 article Issue，附上 URL

**生活记录类（定期使用）**：
- **快捷指令 8**: 「💪 记录训练」— 新建 workout Issue，记录心率/时长
- **快捷指令 9**: 「⚖️ 记录体重」— 新建 health Issue，快速输入数据
- **快捷指令 10**: 「💰 记录开支」— 新建 expense Issue，记录消费

**定期总结类**：
- **快捷指令 11**: 「🔍 月度回顾」— 新建 review Issue，准备月度总结
- **快捷指令 12**: 「✅ 习惯检查」— 新建 habit Issue 或在现有习惯 Issue 下评论本周执行情况

这样用户可以：
- 在 iPhone 主屏添加"日记速记"作为 widget，一键快速启动
- 语音呼唤 Siri："嘿 Siri，日记速记"，不需要解锁手机
- 在快捷指令 app 中浏览全部快捷指令，选择相应的

---

## 步骤 3：GitHub Actions 自动归档日志

在 `.github/workflows/daily-log-to-md.yml` 中添加：

```yaml
name: Daily Log → Markdown

on:
  schedule:
    - cron: '0 15 * * *'   # UTC 15:00 = JST 0:00（每天午夜）
  workflow_dispatch:        # 允许手动触发

jobs:
  archive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set date
        run: echo "TODAY=$(date +'%Y%m%d')" >> $GITHUB_ENV

      - name: Get comments from daily issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh issue view 1 --comments --json comments --jq '.comments[].body' > comments.txt
          # 改为你的 Daily Issue 编号（例如 1, 2, 等）

      - name: Create markdown file if has content
        run: |
          if [ -s comments.txt ]; then
            mkdir -p logs
            echo "# ${{ env.TODAY }}" > logs/${{ env.TODAY }}.md
            echo "" >> logs/${{ env.TODAY }}.md
            cat comments.txt >> logs/${{ env.TODAY }}.md
            
            git config user.name "GitHub Actions"
            git config user.email "actions@github.com"
            git add logs/
            git commit -m "docs: daily log ${{ env.TODAY }}" || echo "No changes"
            git push
          fi
```

**结果**：每天午夜自动生成 `logs/20250120.md`，包含当天所有评论。

---

## 步骤 4：自动生成重复任务（可选）

例如每周一自动创建"本周健身计划"：

```yaml
name: Recurring Tasks

on:
  schedule:
    - cron: '0 0 * * 1'   # 每周一 09:00 JST

jobs:
  create:
    runs-on: ubuntu-latest
    steps:
      - name: Create weekly workout
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          WEEK=$(date +"%Y年第%V周")
          if ! gh issue list --label "workout" | grep -q "$WEEK"; then
            gh issue create \
              --title "💪 本周健身计划 ($WEEK)" \
              --label "workout" \
              --body "- [ ] 周一：跑步 5km\n- [ ] 周三：力量训练\n- [ ] 周五：瑜伽"
          fi
```

---

## 步骤 5：用 Claude Code（或任意 LLM）提炼知识

### 5.1 定期提炼工作流
- **频率**：每月末或每周五晚上
- **对象**：`logs/*.md` + 相关 Issue
- **输出**：结构化知识笔记存入 `knowledge/` 目录

### 5.2 示例 Prompt（中文）

```
请读取我的 GitHub 仓库 https://github.com/<用户名>/<仓库>，
重点查看 logs 目录的最近一个月日记、以及 Issues 中标签为 goal/article/insight 的内容。

根据这些信息，按以下三个维度总结本月的核心内容：

## 1️⃣ 技术与工作学习
- 学到的重要知识点
- 解决的技术难题
- 职业成长

## 2️⃣ 生活与健康
- 习惯变化与成果
- 健身/运动进展
- 饮食与睡眠改善

## 3️⃣ 思维与成长
- 人生观念的改变
- 重要的领悟或洞察
- 对自己的新认识

请用 Markdown 格式输出，包含要点、数据支撑（如果有）、以及可落地的后续行动建议。
文件名格式：2025-01-月度总结.md

输出内容后，请帮我新增到知识库，并可选地提出下个月的改进方向。
```

### 5.3 如何使用 Claude Code
1. 在 VS Code 中打开仓库
2. 打开 Claude Code（或 Cursor / Windsurf）
3. 粘贴上述 Prompt
4. 模型会自动：
   - 读取仓库内容
   - 分析日记与 Issue
   - 生成结构化总结
   - 建议后续行动

---

## 步骤 6：GitHub Projects 看板管理

### 6.1 创建看板
1. 在仓库 Projects 中新建一个看板（例如"生活管理"或"年度目标"）
2. 自定义列（Status）：
   - 📥 Inbox — 新创建的 Issue，待分类
   - 🔵 To Do — 待处理项目
   - 🟡 In Progress — 进行中
   - 🟢 Review — 待确认/审视
   - ✅ Done — 已完成

### 6.2 自动化规则（可选）
- 新 Issue 自动进入 Inbox
- 标记为 `done` 的 Issue 自动进入 Done 列
- 带有里程碑的 Issue 自动到 In Progress

---

## 最小可行起步计划（今天可执行）

**第 1 天**:
1. 新建仓库，创建 Daily Log Issue（记下编号，如 `#1`）
2. 在 iPhone 上测试手动创建 Issue（通过 GitHub 网页）

**第 2-7 天**:
3. 在手机上做一个快捷指令，把文本/语音发送为该 Issue 的评论
4. 每天坚持用快捷指令记录 1-3 条日记
5. 观察流程是否顺手，是否需要调整

**第 2 周**:
6. 添加 GitHub Actions 工作流，自动归档日志为 `logs/*.md`
7. 验证每天早上是否能生成日志文件

**第 3 周+**:
8. 尝试创建其他 Issue 模板（task / goal / article 等），测试不同类型的记录
9. 用 Claude 做第一次周度或月度总结，评估效果
10. 根据实际情况优化快捷指令、标签、看板视图

---

## 安全与注意事项

- **PAT 密钥管理**：仅授予 `repo` 权限，将 token 存储在 iPhone 的密钥链中，不要明文保存或分享
- **仓库隐私**：建议设为 Private，避免个人日记暴露
- **敏感信息脱敏**：日记中若含有隐私信息（如电话、地址），可在提交前删除
- **Git 历史**：一旦 commit，历史会被保留；若不小心提交了敏感信息，可用 `git-filter-branch` 或 GitHub 的重写历史功能修复

---

## 常见问题

**Q: 为什么不直接用 Notion / Obsidian / 其他笔记应用？**  
A: GitHub 的优势是：
- 完全免费（私有仓库）
- 版本控制（不会丢失历史）
- 支持 Markdown（纯文本、易迁移）
- 天然支持 API（便于自动化）
- 与代码工作流集成（如果有开发需求）

**Q: 我可以有多个 Daily Log Issue 吗？**  
A: 可以。例如一个用于工作日记，一个用于生活日记。在 Actions 中分别处理它们。

**Q: Claude Code 是付费的吗？**  
A: Claude Code（Anthropic 的）是免费的。Cursor 等编辑器的高级功能是付费的，但 VS Code + 免费 Claude 也可用。

**Q: GitHub Issue 有数量限制吗？**  
A: 没有。但如果长期累积，搜索可能变慢。建议定期存档或使用标签归类。

---

## 结语

这个系统的核心优势：
✅ **输入极简**：一键快速记录，支持语音  
✅ **分类清晰**：十几个 Issue 模板覆盖生活各个方面  
✅ **自动归档**：日志自动生成 md，无需手工整理  
✅ **AI 赋能**：定期用 LLM 进行智能总结与洞察  
✅ **永久保存**：Git 版本控制，可搜索、可迁移、可回溯  

从今天开始，建仓库、建快捷指令、坚持记录一个月，你将看到自己的成长轨迹与知识积累。

---

**有问题或需要进一步的技术支持（如快捷指令 JSON 导入、GitHub Actions 调试等），随时告诉我！**
