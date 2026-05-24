# AI 学习完全指南

从零开始系统学习 AI/机器学习，分为 **基础、中级、进阶** 三个阶段。

## 📚 学习路径总览

```
第1阶段: 基础理论 + Python编程 (2-3周)
    ├─ Python 基础和数据结构
    ├─ NumPy/Pandas 数据处理
    ├─ 数据可视化 (Matplotlib)
    └─ 线性代数基础

       ↓

第2阶段: 机器学习入门 (3-4周)
    ├─ 机器学习基本概念
    ├─ 监督学习（回归、分类）
    ├─ 无监督学习（聚类）
    ├─ 模型评估和超参数调整
    └─ 使用 Scikit-learn

       ↓

第3阶段: 深度学习/高级应用 (4-6周)
    ├─ 神经网络基础
    ├─ TensorFlow/PyTorch 框架
    ├─ CNN/RNN 深度学习
    ├─ NLP 自然语言处理
    ├─ LLM 大模型应用
    └─ 项目实战
```

---

## 🎯 第1阶段：基础理论和 Python 编程

**时间：** 2-3周  
**学习目标：**
- 掌握 Python 语言基础
- 学会使用数据处理库
- 理解基本的数学概念

### 学习顺序

| # | 主题 | 难度 | 预计时间 | 文件 |
|----|------|------|--------|------|
| 1.1 | Python 基础语法和类型 | ⭐ | 3天 | `01_python_basics.py` |
| 1.2 | NumPy 数组操作 | ⭐ | 3天 | `02_numpy_intro.py` |
| 1.3 | Pandas 数据处理 | ⭐⭐ | 4天 | `03_pandas_intro.py` |
| 1.4 | 数据可视化 (Matplotlib) | ⭐⭐ | 3天 | `04_visualization.py` |
| 1.5 | 线性代数基础 | ⭐⭐ | 2天 | `05_linear_algebra.py` |

---

## 🎯 第2阶段：机器学习入门

**时间：** 3-4周  
**学习目标：**
- 理解监督学习和无监督学习
- 实现常见的机器学习算法
- 学会模型评估和调优

### 学习顺序

| # | 主题 | 难度 | 预计时间 | 文件 |
|----|------|------|--------|------|
| 2.1 | ML 基本概念 + Scikit-learn | ⭐⭐ | 2天 | `06_ml_intro.py` |
| 2.2 | 线性回归和多项式回归 | ⭐⭐ | 3天 | `07_regression.py` |
| 2.3 | 逻辑回归和分类 | ⭐⭐ | 3天 | `08_classification.py` |
| 2.4 | 决策树和随机森林 | ⭐⭐ | 3天 | `09_tree_ensemble.py` |
| 2.5 | 聚类算法 (K-means) | ⭐⭐ | 2天 | `10_clustering.py` |
| 2.6 | 模型评估和验证 | ⭐⭐ | 2天 | `11_evaluation.py` |
| 2.7 | 数据预处理管道 | ⭐⭐ | 2天 | `12_preprocessing.py` |

---

## 🎯 第3阶段：深度学习和高级应用

**时间：** 4-6周  
**学习目标：**
- 掌握深度学习框架
- 实现神经网络和CNN/RNN
- 学会使用 LLM 和 NLP

### 学习顺序

| # | 主题 | 难度 | 预计时间 | 文件 |
|----|------|------|--------|------|
| 3.1 | 神经网络基础 (前向/反向传播) | ⭐⭐⭐ | 3天 | `13_neural_networks.py` |
| 3.2 | TensorFlow/Keras 入门 | ⭐⭐⭐ | 3天 | `14_tensorflow_intro.py` |
| 3.3 | CNN 卷积神经网络 | ⭐⭐⭐ | 4天 | `15_cnn_images.py` |
| 3.4 | RNN/LSTM 序列模型 | ⭐⭐⭐ | 4天 | `16_rnn_sequences.py` |
| 3.5 | NLP 自然语言处理基础 | ⭐⭐⭐ | 3天 | `17_nlp_basics.py` |
| 3.6 | 使用 LLM (OpenAI/Ollama) | ⭐⭐⭐ | 3天 | `18_llm_usage.py` |
| 3.7 | 端到端项目实战 | ⭐⭐⭐⭐ | 5天 | `19_project_end_to_end.py` |

---

## 📦 环境搭建

### 1. 创建虚拟环境

```bash
cd /workspaces/study/python-projects/ai-lab
python3 -m venv .venv
source .venv/bin/activate  # 在 Linux/Mac 上
# 或 .venv\Scripts\activate  # 在 Windows 上
```

### 2. 安装依赖

```bash
# 基础数据科学栈
pip install numpy pandas matplotlib scikit-learn

# 深度学习框架（选一个）
pip install tensorflow    # 或
pip install torch         # PyTorch

# NLP 和 LLM
pip install transformers langchain openai

# 其他工具
pip install jupyter notebook ipython
```

### 3. 完整的 requirements.txt

见 [requirements.txt](./requirements.txt)

---

## 💡 学习建议

### 1. **动手实践最重要**
- 不要只看理论，要边学边写代码
- 每个概念都有对应的示例代码
- 修改代码，观察结果变化

### 2. **遵循学习顺序**
- 按阶段循序渐进
- 不要跳过基础阶段直接学深度学习
- 如果遇到不懂的概念，回头复习前面的内容

### 3. **理论与实践结合**
- 先理解数学原理
- 再看代码实现
- 最后自己实现一遍

### 4. **学习方法**
```
阅读理论 → 运行示例 → 修改代码 → 自己实现 → 做项目
```

---

## 🔗 推荐资源

### 在线课程
- **Andrew Ng 机器学习课程** (Coursera)
- **Fast.ai 实用深度学习** (自顶向下)
- **3Blue1Brown 线性代数** (直观理解)

### 书籍
- 《Python 机器学习》(Sebastian Raschka)
- 《深度学习》(Goodfellow et al.)
- 《动手学深度学习》(李沐)

### 实践平台
- Kaggle (数据集和竞赛)
- Hugging Face (预训练模型)
- GitHub (开源项目学习)

---

## 📊 进度跟踪

使用此表格跟踪你的学习进度：

| 阶段 | 主题 | 状态 | 完成日期 | 备注 |
|-----|------|------|--------|------|
| 基础 | Python 基础语法 | ⬜ 未开始 | | |
| 基础 | NumPy | ⬜ 未开始 | | |
| 基础 | Pandas | ⬜ 未开始 | | |
| ... | ... | ... | ... | |

---

## 🎓 使用本学习资源

每个阶段的代码都可以直接运行：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行示例
python 01_python_basics.py

# 或在 Jupyter 中交互式学习
jupyter notebook
```

---

## 🏁 最后

这个学习路径设计得很完整，但**关键是坚持**！

- 每天至少花 2-3 小时学习
- 完成每个阶段的所有示例
- 做项目来巩固知识
- 定期复习之前学过的内容

祝你学习愉快！🚀
