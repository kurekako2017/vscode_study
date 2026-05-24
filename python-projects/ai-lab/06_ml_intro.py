"""
第2阶段：机器学习入门
06_ml_intro.py - 机器学习基本概念和 Scikit-learn

学习目标：
- 理解监督学习和无监督学习的基本概念
- 掌握Scikit-learn库的基本使用
- 学会数据集的划分和基本流程
- 理解过拟合和欠拟合

预计时间：2天
难度：⭐⭐

Scikit-learn是最流行的机器学习库，API简洁一致。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_classification, make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

print("=" * 70)
print("机器学习简介")
print("=" * 70)
print("""
机器学习是让计算机从数据中学习规律，而不是显式编程。

主要类型：
1. 监督学习 (Supervised Learning)
   - 有标签的训练数据
   - 分类问题：输出是离散类别
   - 回归问题：输出是连续值
   
2. 无监督学习 (Unsupervised Learning)
   - 无标签的数据
   - 聚类：发现数据中的分组
   - 降维：减少特征数量

3. 强化学习 (Reinforcement Learning)
   - 通过奖励信号学习

我们从监督学习开始...
""")

# ============================================================
# 1. 机器学习基本流程
# ============================================================
print("\n" + "=" * 70)
print("1. 机器学习的基本流程")
print("=" * 70)
print("""
┌─────────────────────────────────────────┐
│  1. 加载/准备数据                        │
│     ├─ 特征 (Features) X                │
│     └─ 标签 (Labels) y                  │
├─────────────────────────────────────────┤
│  2. 划分数据                             │
│     ├─ 训练集 (通常70-80%)              │
│     └─ 测试集 (通常20-30%)              │
├─────────────────────────────────────────┤
│  3. 数据预处理                           │
│     ├─ 标准化/归一化                     │
│     ├─ 处理缺失值                        │
│     └─ 特征工程                         │
├─────────────────────────────────────────┤
│  4. 选择和训练模型                       │
│     ├─ 创建模型对象                      │
│     └─ 用训练集拟合                      │
├─────────────────────────────────────────┤
│  5. 模型评估                             │
│     ├─ 在测试集上预测                    │
│     └─ 计算评估指标                      │
├─────────────────────────────────────────┤
│  6. 超参数调优                           │
│     ├─ 调整模型参数                      │
│     └─ 交叉验证                         │
├─────────────────────────────────────────┤
│  7. 部署和预测                           │
│     └─ 用模型进行实时预测                │
└─────────────────────────────────────────┘
""")

# ============================================================
# 2. 加载数据集
# ============================================================
print("\n" + "=" * 70)
print("2. 加载数据集")
print("=" * 70)

# 使用经典的 Iris 数据集
iris = load_iris()
X = iris.data  # 特征 (150个样本, 4个特征)
y = iris.target  # 标签 (0, 1, 2三个类别)

print(f"数据集: Iris (鸢尾花分类)")
print(f"样本数: {X.shape[0]}")
print(f"特征数: {X.shape[1]}")
print(f"特征名: {iris.feature_names}")
print(f"类别数: {len(np.unique(y))}")
print(f"类别: {iris.target_names}")

print(f"\n前5个样本的特征:")
print(f"  {X[:5]}")
print(f"对应的标签:")
print(f"  {y[:5]}")

# ============================================================
# 3. 划分数据集
# ============================================================
print("\n" + "=" * 70)
print("3. 划分训练集和测试集")
print("=" * 70)

# 80%训练，20%测试，并固定随机种子以保证可复现性
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"训练集大小: {X_train.shape[0]} (80%)")
print(f"测试集大小: {X_test.shape[0]} (20%)")

# 检查类别分布
train_classes, train_counts = np.unique(y_train, return_counts=True)
print(f"\n训练集类别分布:")
for cls, count in zip(train_classes, train_counts):
    print(f"  类别 {cls} ({iris.target_names[cls]}): {count}个")

# ============================================================
# 4. 特征标准化
# ============================================================
print("\n" + "=" * 70)
print("4. 特征标准化 (Normalization)")
print("=" * 70)
print("""
为什么要标准化？
- 不同特征的尺度可能不同
- 某些算法（如KNN、SVM）对特征尺度敏感
- 加快训练速度，提高数值稳定性

标准化公式：z = (x - mean) / std
""")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"标准化前 - 第一个特征的统计:")
print(f"  平均值: {X_train[:, 0].mean():.2f}")
print(f"  标准差: {X_train[:, 0].std():.2f}")
print(f"  最小值: {X_train[:, 0].min():.2f}")
print(f"  最大值: {X_train[:, 0].max():.2f}")

print(f"\n标准化后 - 第一个特征的统计:")
print(f"  平均值: {X_train_scaled[:, 0].mean():.6f}")
print(f"  标准差: {X_train_scaled[:, 0].std():.2f}")
print(f"  最小值: {X_train_scaled[:, 0].min():.2f}")
print(f"  最大值: {X_train_scaled[:, 0].max():.2f}")

# ============================================================
# 5. 训练模型 - KNN (k-Nearest Neighbors)
# ============================================================
print("\n" + "=" * 70)
print("5. 训练模型 - KNN (k-Nearest Neighbors)")
print("=" * 70)
print("""
KNN 算法原理：
- 对于新样本，找到最近的 k 个训练样本
- 用这 k 个样本的标签的多数投票结果作为预测

优点：
- 简单易理解
- 无需训练阶段，是"懒学习"算法
- 适合多分类问题

缺点：
- 计算量大（需要计算与所有训练样本的距离）
- 对特征尺度敏感（需要标准化）
- 对高维数据性能差（维度诅咒）
""")

# 创建并训练 KNN 模型 (k=3)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)
print(f"模型参数: n_neighbors=3")
print(f"模型已训练！")

# ============================================================
# 6. 模型预测
# ============================================================
print("\n" + "=" * 70)
print("6. 模型预测")
print("=" * 70)

# 在测试集上进行预测
y_pred = knn.predict(X_test_scaled)

print(f"前10个预测结果：")
print(f"真实标签:  {y_test[:10]}")
print(f"预测标签:  {y_pred[:10]}")
print(f"是否正确:  {y_test[:10] == y_pred[:10]}")

# ============================================================
# 7. 模型评估
# ============================================================
print("\n" + "=" * 70)
print("7. 模型评估 (Evaluation Metrics)")
print("=" * 70)

# 准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率 (Accuracy): {accuracy:.4f}")
print(f"  定义: 正确预测数 / 总数")
print(f"  公式: (TP + TN) / (TP + TN + FP + FN)")

# 精确率和召回率（针对二分类或多分类的平均）
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
print(f"\n精确率 (Precision): {precision:.4f}")
print(f"  定义: 正确预测的正类 / 所有预测为正类的")
print(f"  公式: TP / (TP + FP)")

print(f"\n召回率 (Recall): {recall:.4f}")
print(f"  定义: 正确预测的正类 / 所有真实正类的")
print(f"  公式: TP / (TP + FN)")

# 混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\n混淆矩阵 (Confusion Matrix):")
print(cm)
print(f"  行表示真实标签")
print(f"  列表示预测标签")
print(f"  对角线上的数字表示正确预测")

# ============================================================
# 8. 使用不同的 k 值比较
# ============================================================
print("\n" + "=" * 70)
print("8. 超参数调优 - 选择最优的 k 值")
print("=" * 70)

k_values = [1, 3, 5, 7, 9, 15]
train_scores = []
test_scores = []

for k in k_values:
    # 训练模型
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train_scaled, y_train)
    
    # 评估
    train_score = knn_temp.score(X_train_scaled, y_train)
    test_score = knn_temp.score(X_test_scaled, y_test)
    
    train_scores.append(train_score)
    test_scores.append(test_score)
    
    print(f"k={k:2d}: 训练准确率={train_score:.4f}, 测试准确率={test_score:.4f}")

# 找出最优 k 值
best_k = k_values[np.argmax(test_scores)]
best_score = max(test_scores)
print(f"\n最优 k 值: {best_k} (测试准确率: {best_score:.4f})")

# ============================================================
# 9. 其他分类器：决策树
# ============================================================
print("\n" + "=" * 70)
print("9. 其他分类器：决策树 (Decision Tree)")
print("=" * 70)
print("""
决策树算法：
- 通过一系列 if-then 规则将数据分割
- 可解释性强
- 无需特征标准化
""")

dt = DecisionTreeClassifier(max_depth=4, random_state=42)
dt.fit(X_train, y_train)  # 注意：不需要标准化
y_pred_dt = dt.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)

print(f"决策树模型:")
print(f"  最大深度: 4")
print(f"  测试准确率: {accuracy_dt:.4f}")

# 比较两个模型
print(f"\n模型对比:")
print(f"  KNN (k=3):       {test_scores[0]:.4f}")
print(f"  决策树 (depth=4): {accuracy_dt:.4f}")

# ============================================================
# 10. 过拟合和欠拟合
# ============================================================
print("\n" + "=" * 70)
print("10. 过拟合 (Overfitting) 和欠拟合 (Underfitting)")
print("=" * 70)
print("""
过拟合（Overfitting）：
- 模型在训练集上表现很好，在测试集上表现差
- 模型"死记硬背"了训练数据
- 泛化能力差

欠拟合（Underfitting）：
- 模型在训练集和测试集上都表现差
- 模型没有学到数据的真实规律
- 太简单或训练不足

最优情况：
- 训练和测试错误都很小
- 两者比较接近（泛化能力强）
""")

# 演示：改变决策树深度
depths = range(1, 11)
train_scores_dt = []
test_scores_dt = []

for depth in depths:
    dt_temp = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt_temp.fit(X_train, y_train)
    
    train_score = dt_temp.score(X_train, y_train)
    test_score = dt_temp.score(X_test, y_test)
    
    train_scores_dt.append(train_score)
    test_scores_dt.append(test_score)

print(f"\n决策树深度与准确率:")
print(f"深度  | 训练准确率 | 测试准确率 | 差异")
print(f"------|-----------|-----------|----")
for depth, train_acc, test_acc in zip(depths, train_scores_dt, test_scores_dt):
    diff = train_acc - test_acc
    print(f"{depth:2d}   | {train_acc:.4f}    | {test_acc:.4f}    | {diff:.4f}")

# ============================================================
# 11. 总结
# ============================================================
print("\n" + "=" * 70)
print("总结 - 机器学习基本概念")
print("=" * 70)
print("""
✓ 监督学习 vs 无监督学习
✓ 数据划分：训练集/验证集/测试集
✓ 特征标准化：提高模型性能和收敛速度
✓ 模型训练：fit() 方法学习数据规律
✓ 模型预测：predict() 方法进行预测
✓ 模型评估：accuracy, precision, recall, F1-score
✓ 超参数调优：找到最优的模型参数
✓ 过拟合和欠拟合：模型选择的关键考虑
✓ 不同算法的权衡：准确率、可解释性、速度

关键工具：Scikit-learn
- 简洁的 API: fit() 和 predict()
- 丰富的算法库
- 完整的评估工具

下一步学习：线性回归和分类
""")

# ============================================================
# 练习题
# ============================================================
print("\n" + "=" * 70)
print("课后练习")
print("=" * 70)
print("""
1. 尝试不同的 k 值（1到20），绘制训练和测试准确率曲线
   观察什么时候出现过拟合

2. 使用其他分类器（SVM、随机森林等），比较它们的性能

3. 尝试使用不同的特征子集（只用前2个特征），
   观察特征对性能的影响

4. 编写函数实现 k-fold 交叉验证

5. 在自己的数据集上应用这些分类器

参考代码：
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=200, n_features=5, n_informative=3,
                           n_classes=2, random_state=42)

运行本文件：python 06_ml_intro.py
""")
