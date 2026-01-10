# Aider 参数调优（32GB 内存优化）

## 推荐启动参数
```powershell
aider ^
  --model ollama/qwen2.5-coder:14b ^
  --edit-format diff ^
  --auto-commits false ^
  --stream
```

## 参数说明
| 参数 | 作用 |
|----|----|
| --edit-format diff | 更安全的代码修改 |
| --auto-commits false | 防止自动提交 |
| --stream | 实时输出 |
| --show-diffs | 修改前后对比 |

## Ollama 模型建议
- 优先 Q5
- 显存不足再用 Q4

---