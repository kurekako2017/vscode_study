# Coding / GitHub Agent

需求：读取 diff 后做安全审查并生成 review 提案；不自动修改仓库、不 push、不 merge。高危密钥问题阻断后续动作。

```bash
python3 main.py "+ password = 'demo'"
python3 main.py "+ value = parse(data)"
```

验收：疑似密钥返回 `blocked/high`；普通 diff 返回 `proposal`；两者都要求审批。简历表述：实现 diff 风险检测、分级门禁和人工审批式 GitHub 工作流。
