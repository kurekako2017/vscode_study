# AI 学习快速参考指南

## 🚀 5分钟快速开始

```bash
# 1. 进入项目目录
cd /workspaces/study/python-projects/ai-lab

# 2. 一键环境设置（仅第一次需要）
bash setup.sh

# 如果你想直接执行 ./setup.sh，先赋予执行权限
chmod +x setup.sh

# 如果这里报错 “ensurepip is not available”，先安装 python3-venv
sudo apt install python3.12-venv
# 或
sudo apt install python3-venv

# 3. 激活虚拟环境（每次使用前）
source .venv/bin/activate

# 4. 运行示例代码
python3 01_python_basics.py      # Python基础
python3 02_numpy_intro.py        # NumPy数组
python3 06_ml_intro.py           # 机器学习
```

---

## 📖 学习阶段概览

### 第1阶段：基础（目前完成：60%）

| 内容 | 文件 | 复杂度 | 时间 | 状态 |
|-----|------|--------|------|------|
| Python 基础 | `01_python_basics.py` | ⭐ | 3天 | ✅ |
| NumPy 数组 | `02_numpy_intro.py` | ⭐ | 3天 | ✅ |
| Pandas 数据处理 | `03_pandas_intro.py` | ⭐⭐ | 4天 | ⏳ |
| 数据可视化 | `04_visualization.py` | ⭐⭐ | 3天 | ⏳ |
| 线性代数 | `05_linear_algebra.py` | ⭐⭐ | 2天 | ⏳ |

### 第2阶段：机器学习（目前完成：15%）

| 内容 | 文件 | 复杂度 | 时间 | 状态 |
|-----|------|--------|------|------|
| ML 基本概念 | `06_ml_intro.py` | ⭐⭐ | 2天 | ✅ |
| 线性回归 | `07_regression.py` | ⭐⭐ | 3天 | ⏳ |
| 分类问题 | `08_classification.py` | ⭐⭐ | 3天 | ⏳ |
| 树模型集成 | `09_tree_ensemble.py` | ⭐⭐ | 3天 | ⏳ |
| 聚类算法 | `10_clustering.py` | ⭐⭐ | 2天 | ⏳ |
| 模型评估 | `11_evaluation.py` | ⭐⭐ | 2天 | ⏳ |
| 数据预处理 | `12_preprocessing.py` | ⭐⭐ | 2天 | ⏳ |

### 第3阶段：深度学习（目前完成：0%）

| 内容 | 文件 | 复杂度 | 时间 | 状态 |
|-----|------|--------|------|------|
| 神经网络基础 | `13_neural_networks.py` | ⭐⭐⭐ | 3天 | ⏳ |
| TensorFlow/Keras | `14_tensorflow_intro.py` | ⭐⭐⭐ | 3天 | ⏳ |
| CNN 图像识别 | `15_cnn_images.py` | ⭐⭐⭐ | 4天 | ⏳ |
| RNN 序列模型 | `16_rnn_sequences.py` | ⭐⭐⭐ | 4天 | ⏳ |
| NLP 基础 | `17_nlp_basics.py` | ⭐⭐⭐ | 3天 | ⏳ |
| LLM 应用 | `18_llm_usage.py` | ⭐⭐⭐ | 3天 | ⏳ |
| 端到端项目 | `19_project_end_to_end.py` | ⭐⭐⭐⭐ | 5天 | ⏳ |

---

## 💻 常用命令速查表

### 环境管理

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate              # Windows

# 退出虚拟环境
deactivate

# 安装依赖
pip install -r requirements.txt

# 查看已安装的包
pip list
```

### 运行代码

```bash
# 运行 Python 文件
python3 01_python_basics.py

# 运行并看到输出
python3 01_python_basics.py | less

# 运行前 50 行输出
python3 01_python_basics.py | head -50

# 交互式 Python shell
python3

# IPython shell（更好用）
ipython

# Jupyter Notebook
jupyter notebook
```

### 导入常用库

```python
# 基础数据科学
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 机器学习
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 数学和统计
import math
from scipy import stats

# 深度学习（后续）
import tensorflow as tf
from tensorflow import keras
```

---

## 🎯 关键概念速查

### Python 基础

```python
# 数据类型
int, float, str, bool, list, dict, tuple, set

# 列表操作
my_list = [1, 2, 3]
my_list.append(4)      # 添加
my_list[0]             # 索引
my_list[1:3]           # 切片

# 字典
my_dict = {'name': '小明', 'age': 25}
my_dict['name']        # 访问

# 循环
for i in range(5):
    print(i)

while condition:
    pass

# 函数
def my_func(x, y=10):
    return x + y
```

### NumPy 基础

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3])
arr = np.zeros((3, 3))
arr = np.ones((2, 4))
arr = np.arange(0, 10, 2)

# 索引和切片
arr[0]         # 第一个元素
arr[:3]        # 前3个
arr[::2]       # 每隔一个

# 操作
arr + 1        # 加法
arr * 2        # 乘法
np.sum(arr)    # 求和
np.mean(arr)   # 平均值

# 矩阵运算
A @ B          # 矩阵乘法
A.T            # 转置
```

### Pandas 基础（预告）

```python
import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# 访问
df['A']        # 列
df.loc[0]      # 行

# 统计
df.mean()      # 平均值
df.describe()  # 统计摘要

# 处理缺失值
df.fillna(0)   # 填充
df.dropna()    # 删除
```

### 机器学习基础（预告）

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. 准备数据
X, y = load_data()

# 2. 划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. 标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. 训练
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# 5. 预测
y_pred = model.predict(X_test)

# 6. 评估
accuracy = accuracy_score(y_test, y_pred)
```

---

## 📚 文件结构

```
ai-lab/
├── README.md                      # 项目总览
├── LEARNING_GUIDE.md              # 详细学习指南
├── QUICK_REFERENCE.md             # 本文件
├── requirements.txt               # Python 依赖
├── setup.sh                       # 环境设置脚本
│
├── 第1阶段：基础
├── 01_python_basics.py            # Python 基础
├── 02_numpy_intro.py              # NumPy 数组
├── 03_pandas_intro.py             # Pandas 数据处理
├── 04_visualization.py            # 数据可视化
├── 05_linear_algebra.py           # 线性代数
│
├── 第2阶段：机器学习
├── 06_ml_intro.py                 # ML 基本概念
├── 07_regression.py               # 线性回归
├── 08_classification.py           # 分类问题
├── 09_tree_ensemble.py            # 树模型集成
├── 10_clustering.py               # 聚类算法
├── 11_evaluation.py               # 模型评估
├── 12_preprocessing.py            # 数据预处理
│
├── 第3阶段：深度学习
├── 13_neural_networks.py          # 神经网络
├── 14_tensorflow_intro.py         # TensorFlow
├── 15_cnn_images.py               # CNN 图像
├── 16_rnn_sequences.py            # RNN 序列
├── 17_nlp_basics.py               # NLP 基础
├── 18_llm_usage.py                # LLM 应用
├── 19_project_end_to_end.py       # 端到端项目
│
├── notebooks/                     # Jupyter notebooks (可选)
├── data/                          # 数据文件夹 (后续)
└── .venv/                         # 虚拟环境 (自动创建)
```

---

## 📊 学习进度检查

自我检查清单：

### 第1阶段完成标准
- [ ] 理解 Python 基本数据类型（int, float, str, bool）
- [ ] 掌握列表、字典、集合的使用
- [ ] 理解函数定义和调用
- [ ] 掌握列表推导式
- [ ] 理解 NumPy 数组创建和操作
- [ ] 掌握数组索引、切片、广播
- [ ] 理解向量化运算
- [ ] 能够进行基本的矩阵运算

### 第2阶段完成标准
- [ ] 理解监督学习和无监督学习
- [ ] 掌握数据集划分（训练/验证/测试）
- [ ] 理解特征标准化的必要性
- [ ] 掌握 KNN、决策树、随机森林
- [ ] 理解线性回归和逻辑回归
- [ ] 掌握模型评估指标（准确率、精确率、召回率等）
- [ ] 理解过拟合和欠拟合
- [ ] 能够进行基本的超参数调优

---

## 💡 学习技巧

### 1. 充分利用 IPython 的交互性

```bash
# 启动 IPython
ipython

# 在 IPython 中
arr = np.arange(10)      # 创建数组
arr?                      # 查看帮助
arr.<TAB>                 # 自动补全
%timeit arr * 2           # 性能测试
```

### 2. 使用 Jupyter Notebook 进行探索

```bash
jupyter notebook

# 在 Notebook 中：
# - 边写边执行代码
# - 用 Markdown 记笔记
# - 用图表可视化数据
# - 保存整个分析过程
```

### 3. 调试技巧

```python
# 打印调试
print(f"变量值: {var}")

# 类型检查
print(type(var))

# 形状检查（数组）
print(arr.shape)

# 使用 pdb 调试器
import pdb
pdb.set_trace()     # 在这里暂停

# 异常捕获
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"错误: {e}")
```

---

## 🆘 常见问题解决

### 问题1：ModuleNotFoundError: No module named 'numpy'
**解决方案：**
```bash
source .venv/bin/activate    # 确保激活了虚拟环境
pip install numpy            # 安装缺失的包
```

### 问题2：Python 版本不兼容
**解决方案：**
```bash
python3 --version            # 检查版本（需要 3.8+）
python3 -m venv .venv        # 指定 python3
```

### 问题3：代码运行很慢
**解决方案：**
- 检查是否在使用 NumPy 向量化操作（避免 Python 循环）
- 减小数据集大小进行测试
- 使用 `%timeit` 找出瓶颈

### 问题4：数组维度不匹配
**解决方案：**
```python
print(arr.shape)             # 检查形状
arr = arr.reshape(-1)        # 重塑形状
arr = np.expand_dims(arr, axis=0)  # 增加维度
```

---

## 🎬 下一步

完成第1阶段基础后：

1. **深化理解**
   - 复习每个章节的练习题
   - 自己实现算法（不只是调用库）
   - 在自己的数据集上应用

2. **进入第2阶段**
   - 学习机器学习的理论基础
   - 实践完整的 ML 工作流程
   - 做小型项目（分类、回归）

3. **参与社区**
   - 在 Kaggle 参与竞赛
   - 贡献开源项目
   - 在 GitHub 分享你的项目

---

## 📞 获取帮助

如遇问题：

1. **查看文档**
   - `LEARNING_GUIDE.md` - 详细指南
   - `README.md` - 项目总览
   - 官方文档链接

2. **搜索答案**
   - Google + 错误信息
   - StackOverflow
   - GitHub Issues

3. **调试代码**
   - 打印中间变量
   - 简化代码到最小可复现示例
   - 使用 pdb 或 IPython 调试

---

**祝你学习顺利！** 🚀

如有改进建议，欢迎反馈！
