# Aider 项目实战工作流

## 推荐目录结构
```
project/
├─ src/
├─ tests/
├─ README.md
└─ pyproject.toml
```

## 启动步骤
```powershell
cd project
aider src/**/*.py
```

## 常用指令
```text
/ask      只问不改
/add      添加文件
/drop    移除文件
/diff    查看修改
/undo    回滚
```

## 推荐用法
- 一次只改一个功能
- 明确说明「不要重构全部」

---