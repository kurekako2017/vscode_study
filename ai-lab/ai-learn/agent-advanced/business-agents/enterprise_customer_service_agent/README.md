# 企业客服 Agent

需求：租户校验后仅按知识库证据回答并返回来源；证据不足必须转人工，不能编造。

```bash
python3 main.py "退款需要几天" --tenant acme
python3 main.py "我要修改合同" --tenant acme
python3 main.py "退款" --tenant unknown
```

验收：已知问题返回 `source`；未知问题为 `handoff`；非法租户为 `rejected`。简历表述：实现租户隔离、知识引用和低置信人工转接。
