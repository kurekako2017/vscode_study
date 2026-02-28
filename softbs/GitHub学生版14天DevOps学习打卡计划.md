# GitHub 学生版 14 天 DevOps 学习打卡计划（每天 30~60 分钟）

> 适配当前仓库：`java-projects/JtProject`、`python-projects/ai-lab`、`softbs/student-pages-demo`

## 使用说明

- 每天只做一个可交付结果（提交、截图、PR、页面更新）。
- 每天结束时写 3 行复盘：做了什么、卡在哪、明天做什么。
- 所有任务尽量走标准流：Issue -> Branch -> PR -> Merge。

---

## Day 1：环境与仓库认知

目标：清楚仓库结构与目标。

- 阅读并整理 3 个重点目录：`java-projects/JtProject`、`python-projects/ai-lab`、`softbs`。
- 在 `softbs` 写一页“我的学习目标”（可附在已有教程后）。
- 新建一个 GitHub Project 看板，列为 `Todo / In Progress / Done`。

产出检查：

- 有一个可用看板。
- 至少 3 个卡片（Pages、CI、CodeQL）。

---

## Day 2：分支与 PR 基础

目标：形成规范协作节奏。

- 创建 Issue：`setup devops learning flow`。
- 新建分支：`feature/day2-pr-flow`。
- 修改一处文档后发起 PR，写清改动原因与验证方式。

产出检查：

- 完成 1 个 Issue + 1 个 PR。

---

## Day 3：Pages 页面第一版

目标：能对外展示学习成果。

- 修改 `softbs/student-pages-demo/index.html`：填入你的姓名、方向、学习目标。
- 增加“项目列表 + 链接”版块。
- 推送后观察 `Deploy softbs Pages` 是否成功。

产出检查：

- Pages 地址可访问。
- 页面信息不是占位内容。

---

## Day 4：Pages 内容迭代

目标：让页面有作品集价值。

- 在页面补充 3 个条目：JtProject、LocalStack、AI Lab。
- 每个条目写“我学到了什么”。
- 优化版式（仅在现有样式基础上小改）。

产出检查：

- 页面可读性提升，有明确学习成果叙述。

---

## Day 5：JtProject CI 跑通

目标：Java 改动能自动校验。

- 在 `java-projects/JtProject` 做一个小改动（文档或安全代码改动）。
- 推送并观察 `JtProject CI`。
- 若失败，定位失败步骤并记录解决过程。

产出检查：

- 一次成功的 CI 记录。

---

## Day 6：CI 结果沉淀

目标：把 CI 变成你的“质量门禁”。

- 在教程或 README 增加 CI 状态说明。
- 总结：哪些改动会触发 CI（`paths` 规则）。
- 为下周准备 2 个“会被 CI 拦截”的实验点（如格式问题、测试失败）。

产出检查：

- 文档里有“如何解读 CI”的说明。

---

## Day 7：周复盘（第 1 周）

目标：纠偏与提效。

- 复盘本周所有 PR：哪些描述写得不清楚。
- 复盘看板：是否有卡片堆积。
- 把未完成项重排优先级。

产出检查：

- 一页周复盘（可放到 `softbs`）。

---

## Day 8：CodeQL 扫描上手

目标：会看安全扫描结果。

- 修改 `java-projects/JtProject` 或 `python-projects/ai-lab` 任意文件触发 `CodeQL`。
- 查看 Code scanning Alerts（无告警也要记录“已检查”）。
- 记下 1 条你理解的安全规则。

产出检查：

- 有一次 CodeQL 运行记录 + 复盘笔记。

---

## Day 9：Dependabot 机制理解

目标：会处理依赖升级 PR。

- 进入 `Insights -> Dependency graph -> Dependabot`。
- 确认已启用并记录更新频率（weekly）。
- 当出现 Dependabot PR 时，完成一次审阅并合并（或标记暂缓）。

产出检查：

- 至少形成一条“依赖升级处理规范”。

---

## Day 10：Python 侧质量练习

目标：形成跨语言一致质量意识。

- 在 `python-projects/ai-lab` 增补一段学习脚本说明或小示例。
- 用 PR 描述写明“为什么改、如何验证、潜在风险”。
- 观察 CodeQL 与常规检查是否通过。

产出检查：

- 1 个 Python 相关 PR，描述完整。

---

## Day 11：Issue 模板化（轻量）

目标：减少沟通成本。

- 新建 2 类 Issue 模板（Bug / Task）草稿（可先文档化，不强求立即上模板文件）。
- 定义每个 Issue 必填字段：背景、验收标准、风险。
- 在看板里应用到新任务。

产出检查：

- 你的任务描述更统一、可执行。

---

## Day 12：发布与可见性

目标：让成果对外“看得见”。

- 在 Pages 页面添加：GitHub 仓库链接、教程链接、学习路径。
- 在主教程中加入“最近一次完成日期”。
- 更新首页一句话价值主张（你能提供什么能力）。

产出检查：

- 页面既是学习笔记，也是简历补充材料。

---

## Day 13：模拟一次端到端交付

目标：走完整 DevOps 闭环。

- 开一个小需求（Issue）。
- 分支开发 + PR + CI + CodeQL + 合并。
- 更新 Pages 展示该次交付。

产出检查：

- 你能完整演示：Plan -> Code -> Build/Test -> Release -> Feedback。

---

## Day 14：总复盘与下一阶段路线

目标：形成可持续学习系统。

- 统计 14 天成果：PR 数、通过的工作流数、页面迭代次数。
- 总结 3 个高频问题和解决策略。
- 制定下一阶段 30 天计划（可聚焦：测试自动化、部署自动化、团队协作规范）。

产出检查：

- 一份可分享的阶段总结（建议放在 `softbs`）。

---

## 每日打卡模板（复制即用）

```markdown
### Day X 打卡（日期：YYYY-MM-DD）
- 今日目标：
- 今日完成：
- 证据链接（PR / Actions / Pages）：
- 遇到问题：
- 明日计划：
```

## 最终达成标准（14 天后）

- 你可以独立维护一个公开可访问的学习主页（Pages）。
- 你可以给 Java/Python 项目接入并解释 CI/安全扫描流程。
- 你可以用 Issue/PR/Project 完成一次标准化协作交付。
- 你有一套可复用的个人 DevOps 学习方法。
