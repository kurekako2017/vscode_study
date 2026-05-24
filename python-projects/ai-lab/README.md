# AI 学习项目

从零开始学习人工智能和机器学习，包含完整的学习路径、示例代码和实践项目。

## 🎯 项目目标

帮助初学者通过**动手实践**系统学习 AI/ML，从基础到进阶。

- **第1阶段**：Python 基础 + NumPy + Pandas + 可视化
- **第2阶段**：机器学习基础 + 经典算法
- **第3阶段**：深度学习 + NLP + LLM 应用

## 🚀 快速开始

### 1. 一键环境设置

```bash
cd /workspaces/study/python-projects/ai-lab
bash setup.sh
```

这个脚本会：
- ✅ 创建Python虚拟环境
- ✅ 安装所有依赖包
- ✅ 验证安装成功

如果你想用 `./setup.sh`，先执行一次：

```bash
chmod +x setup.sh
```

前置条件：如果你的 Ubuntu/WSL 里没有 `python3-venv`，`bash setup.sh` 会在创建虚拟环境时失败。先安装下面任意一个包再继续：

```bash
sudo apt install python3.12-venv
# 或
sudo apt install python3-venv
```

### 2. 激活虚拟环境

```bash
source .venv/bin/activate
```

### 3. 运行第一个示例

```bash
# 运行 Python 基础示例
python3 01_python_basics.py

# 运行 NumPy 示例
python3 02_numpy_intro.py

# 运行机器学习示例
python3 06_ml_intro.py
```

## 📚 学习路径

详见 [LEARNING_GUIDE.md](LEARNING_GUIDE.md)

### 第1阶段：基础理论（2-3周）

| # | 主题 | 文件 | 状态 |
|---|------|------|------|
| 1.1 | Python 基础语法 | `01_python_basics.py` | ✅ |
| 1.2 | NumPy 数组操作 | `02_numpy_intro.py` | ✅ |
| 1.3 | Pandas 数据处理 | `03_pandas_intro.py` | ⏳ |
| 1.4 | 数据可视化 | `04_visualization.py` | ⏳ |
| 1.5 | 线性代数基础 | `05_linear_algebra.py` | ⏳ |

### 第2阶段：机器学习入门（3-4周）

| # | 主题 | 文件 | 状态 |
|---|------|------|------|
| 2.1 | ML 基本概念 | `06_ml_intro.py` | ✅ |
| 2.2 | 线性回归 | `07_regression.py` | ⏳ |
| 2.3 | 分类问题 | `08_classification.py` | ⏳ |
| 2.4 | 树模型集成 | `09_tree_ensemble.py` | ⏳ |
| 2.5 | 聚类算法 | `10_clustering.py` | ⏳ |
| 2.6 | 模型评估 | `11_evaluation.py` | ⏳ |
| 2.7 | 数据预处理 | `12_preprocessing.py` | ⏳ |

### 第3阶段：深度学习和高级应用（4-6周）

| # | 主题 | 文件 | 状态 |
|---|------|------|------|
| 3.1 | 神经网络基础 | `13_neural_networks.py` | ⏳ |
| 3.2 | TensorFlow/Keras | `14_tensorflow_intro.py` | ⏳ |
| 3.3 | CNN 图像识别 | `15_cnn_images.py` | ⏳ |
| 3.4 | RNN 序列模型 | `16_rnn_sequences.py` | ⏳ |
| 3.5 | NLP 基础 | `17_nlp_basics.py` | ⏳ |
| 3.6 | LLM 应用 | `18_llm_usage.py` | ⏳ |
| 3.7 | 端到端项目 | `19_project_end_to_end.py` | ⏳ |

## 📖 如何使用本项目

### 方式1：命令行运行（推荐初期）

```bash
# 激活环境
source .venv/bin/activate

# 运行任何示例
python3 01_python_basics.py
python3 02_numpy_intro.py
python3 06_ml_intro.py
```

如果你第一次运行脚本，先确保已经执行过：

```bash
bash setup.sh
```

如果这一步报错，通常就是缺少 `python3-venv`。

### 方式2：Jupyter Notebook（推荐交互式学习）

```bash
# 激活环境
source .venv/bin/activate

# 启动 Jupyter
jupyter notebook

# 然后在浏览器中打开 http://localhost:8888
# 创建新 Notebook 或编辑 .py 文件
```

### 方式3：在 VS Code 中运行

1. 打开此文件夹
2. 选择虚拟环境作为 Python Interpreter
3. 右键单击 .py 文件，选择 "Run Python File in Terminal"

## 运行顺序建议

如果你第一次运行这个项目，按下面顺序最稳：

```bash
cd python-projects/ai-lab
bash setup.sh
source .venv/bin/activate
python3 01_python_basics.py
```

如果 `python` 命令在你的系统里没有安装，但 `python3` 有安装，就统一用 `python3`。

## 💡 学习建议

### ✅ 做这些事情

- **边学边写代码** - 不要只看，要动手实践
- **修改代码观察结果** - 改变参数、改变数据，看看会发生什么
- **记笔记** - 总结关键概念和公式
- **完成练习题** - 每个示例都有课后练习
- **参考多个资源** - 书籍、视频、博客、官方文档

### ❌ 避免这些事情

- **跳过基础直接学高级** - 深度学习基于线性代数和概率
- **只看不练** - 编程必须动手
- **死记硬背** - 理解原理比记公式更重要
- **忽视错误** - 错误和调试是学习的一部分

## 📊 进度跟踪

在此追踪你的学习进度（复制下表到文件中更新）：

```
| 章节 | 内容 | 完成 | 日期 | 笔记 |
|-----|------|------|------|------|
| 1.1 | Python基础 | ✅ | 2024-01-03 | |
| 1.2 | NumPy | ⏳ | | |
| 1.3 | Pandas | ⬜ | | |
```

## 🔗 有用的资源

### 理论学习

- **Andrew Ng 机器学习课程** - Coursera 上的经典课程
- **3Blue1Brown 线性代数** - YouTube 上最好的线性代数可视化讲解
- **Fast.ai 实用深度学习** - 自顶向下的深度学习入门

### 官方文档

- [NumPy 官方文档](https://numpy.org/doc/)
- [Pandas 官方文档](https://pandas.pydata.org/docs/)
- [Scikit-learn 官方文档](https://scikit-learn.org/)
- [TensorFlow 官方文档](https://www.tensorflow.org/)

### 实践平台

- **Kaggle** - 数据集和竞赛
- **GitHub** - 开源项目学习
- **Hugging Face** - 预训练模型库

## 🤔 常见问题

### Q1: 如果我没有 ML 背景怎么办？
**A:** 完全没问题！本项目从零开始设计。建议按顺序学习，不要跳过基础阶段。

### Q2: 需要多长时间完成？
**A:** 取决于投入时间和学习速度：
- 基础阶段：2-3周（每周15-20小时）
- 中级阶段：3-4周
- 进阶阶段：4-6周
- **总计：3-4 个月的投入**

### Q3: 需要什么硬件？
**A:** 
- CPU：任何现代处理器都可以
- 内存：8GB 以上推荐
- GPU：非必须，但大幅加快深度学习训练

### Q4: 遇到问题怎么办？
**A:** 
1. 检查错误信息，试着理解哪里出错
2. 查看官方文档或搜索 StackOverflow
3. 在 GitHub Issues 中提问
4. 如果是环境问题，重新运行 setup.sh

## 📝 许可证

MIT License - 自由使用和修改

## 🎓 学完之后

完成这个项目后，你将能够：

✅ 使用 Python + NumPy + Pandas 进行数据处理  
✅ 用 Scikit-learn 构建机器学习模型  
✅ 理解监督学习、无监督学习、强化学习  
✅ 用 TensorFlow/PyTorch 构建深度神经网络  
✅ 进行 NLP 任务和 LLM 应用开发  
✅ 部署和优化机器学习模型  
✅ 独立完成端到端的 ML 项目  

**下一步可以：**
- 在 Kaggle 上参与竞赛
- 贡献开源 ML 项目
- 做自己感兴趣的 ML 项目
- 学习专业的 ML 技能（强化学习、图神经网络等）

---

**祝你学习愉快！** 🚀

如有问题或建议，欢迎提 Issue 或 PR！
