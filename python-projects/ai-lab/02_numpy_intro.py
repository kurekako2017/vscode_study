"""
第1阶段：基础理论和Python编程
02_numpy_intro.py - NumPy数组操作

学习目标：
- 掌握NumPy数组的创建和索引
- 学会数组的基本操作（加减乘除）
- 理解广播(broadcasting)机制
- 掌握常用的统计函数

预计时间：3天
难度：⭐

NumPy是科学计算的基础库，所有机器学习都基于NumPy数组！
"""

import numpy as np

print("=" * 70)
print("NumPy 简介")
print("=" * 70)
print(f"NumPy版本: {np.__version__}")
print("""
NumPy是Python科学计算的基础库：
- 快速的多维数组处理
- 向量化操作（避免Python循环）
- 与C/Fortran无缝集成
- 是 Pandas, Scikit-learn, TensorFlow 的基础
""")

# ============================================================
# 1. 创建数组
# ============================================================
print("\n" + "=" * 70)
print("1. 创建数组")
print("=" * 70)

# 从列表创建
arr1 = np.array([1, 2, 3, 4, 5])
print(f"从列表创建: {arr1}")
print(f"  形状(shape): {arr1.shape}")
print(f"  数据类型(dtype): {arr1.dtype}")

# 创建特殊数组
zeros = np.zeros(5)  # 全0数组
print(f"\n全0数组: {zeros}")

ones = np.ones((3, 4))  # 3x4全1数组
print(f"\n全1数组 (3x4):\n{ones}")

# 等差数列
linspace = np.linspace(0, 10, 5)  # 0到10均匀分布的5个数
print(f"\nlinspace(0, 10, 5): {linspace}")

arange = np.arange(0, 10, 2)  # 0到10，步长为2
print(f"arange(0, 10, 2): {arange}")

# 随机数
random_arr = np.random.rand(5)  # 0-1之间的随机数
print(f"\n随机数组(0-1): {random_arr}")

random_normal = np.random.randn(5)  # 标准正态分布
print(f"正态分布随机数: {random_normal}")

# ============================================================
# 2. 二维数组（矩阵）
# ============================================================
print("\n" + "=" * 70)
print("2. 二维数组（矩阵）")
print("=" * 70)

# 创建矩阵
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(f"矩阵:\n{matrix}")
print(f"形状: {matrix.shape}")  # (3, 3)
print(f"行数: {matrix.shape[0]}, 列数: {matrix.shape[1]}")

# 创建特殊矩阵
zeros_matrix = np.zeros((3, 3))
print(f"\n3x3零矩阵:\n{zeros_matrix}")

identity = np.eye(3)  # 单位矩阵
print(f"\n单位矩阵:\n{identity}")

# ============================================================
# 3. 数组索引和切片
# ============================================================
print("\n" + "=" * 70)
print("3. 数组索引和切片")
print("=" * 70)

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
print(f"原数组: {arr}")
print(f"第一个元素: {arr[0]}")
print(f"最后一个元素: {arr[-1]}")

# 切片
print(f"\n前3个元素: {arr[:3]}")
print(f"从索引2到5: {arr[2:6]}")
print(f"每隔一个元素: {arr[::2]}")
print(f"反向: {arr[::-1]}")

# 二维数组索引
print(f"\n矩阵:\n{matrix}")
print(f"第(0,0)元素: {matrix[0, 0]}")
print(f"第0行: {matrix[0, :]}")
print(f"第1列: {matrix[:, 1]}")
print(f"左上角2x2:\n{matrix[:2, :2]}")

# 布尔索引
print(f"\n使用布尔索引找出>5的元素:")
mask = arr > 50
print(f"布尔掩码: {mask}")
print(f"结果: {arr[mask]}")

# ============================================================
# 4. 数组的基本操作
# ============================================================
print("\n" + "=" * 70)
print("4. 数组的基本操作（向量化运算）")
print("=" * 70)

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(f"a = {a}")
print(f"b = {b}")

# 逐元素运算
print(f"\n加法: a + b = {a + b}")
print(f"减法: b - a = {b - a}")
print(f"乘法: a * b = {a * b}")
print(f"除法: b / a = {b / a}")
print(f"乘方: a ** 2 = {a ** 2}")

# 与标量的运算
print(f"\na + 100 = {a + 100}")
print(f"a * 2 = {a * 2}")
print(f"a / 2 = {a / 2}")

# 数学函数
print(f"\nnp.sqrt(a) = {np.sqrt(a)}")
print(f"np.exp(a) = {np.exp(a)[:3]}...")  # 只显示前3个
print(f"np.log(a) = {np.log(a)}")
print(f"np.sin(a) = {np.sin(a)}")

# ============================================================
# 5. 数组形状操作
# ============================================================
print("\n" + "=" * 70)
print("5. 数组形状操作")
print("=" * 70)

arr = np.arange(12)
print(f"原数组 (12,): {arr}")

# reshape - 改变形状
reshaped = arr.reshape(3, 4)
print(f"\nreshape(3, 4):\n{reshaped}")

reshaped2 = arr.reshape(2, 2, 3)
print(f"\nreshape(2, 2, 3):\n{reshaped2}")

# flatten - 展平
flattened = reshaped.flatten()
print(f"\nflatten后: {flattened}")

# transpose - 转置
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n原矩阵 (2x3):\n{matrix}")
print(f"转置后 (3x2):\n{matrix.T}")

# ============================================================
# 6. 数组连接
# ============================================================
print("\n" + "=" * 70)
print("6. 数组连接")
print("=" * 70)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# 水平连接
concat_h = np.concatenate([arr1, arr2])
print(f"水平连接: {concat_h}")

# 堆叠
stacked = np.stack([arr1, arr2])
print(f"\n堆叠:\n{stacked}")

# 二维数组的连接
matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

print(f"\n矩阵1:\n{matrix1}")
print(f"矩阵2:\n{matrix2}")
print(f"水平连接:\n{np.hstack([matrix1, matrix2])}")
print(f"垂直连接:\n{np.vstack([matrix1, matrix2])}")

# ============================================================
# 7. 统计函数
# ============================================================
print("\n" + "=" * 70)
print("7. 统计函数")
print("=" * 70)

data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
print(f"数据: {data}")

print(f"\n基本统计:")
print(f"  求和: {np.sum(data)}")
print(f"  平均值: {np.mean(data)}")
print(f"  中位数: {np.median(data)}")
print(f"  标准差: {np.std(data):.2f}")
print(f"  最大值: {np.max(data)}")
print(f"  最小值: {np.min(data)}")

# 二维数组的统计
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"\n矩阵:\n{matrix}")
print(f"全局求和: {np.sum(matrix)}")
print(f"按行求和: {np.sum(matrix, axis=1)}")
print(f"按列求和: {np.sum(matrix, axis=0)}")

# ============================================================
# 8. 广播 (Broadcasting)
# ============================================================
print("\n" + "=" * 70)
print("8. 广播 (Broadcasting) - NumPy的强大特性")
print("=" * 70)

# 案例1：数组与标量的广播
arr = np.array([1, 2, 3, 4, 5])
scalar = 10
result = arr + scalar
print(f"数组 {arr} + 标量 {scalar}")
print(f"结果: {result}")

# 案例2：不同形状的数组
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # 形状 (2, 3)
vector = np.array([10, 20, 30])  # 形状 (3,)
result = matrix + vector  # vector被广播到(2,3)
print(f"\n矩阵 (2x3):\n{matrix}")
print(f"向量 (3,): {vector}")
print(f"相加结果:\n{result}")

# 案例3：列向量和行向量
col_vector = np.array([[1], [2], [3]])  # 形状 (3, 1)
row_vector = np.array([10, 20, 30])  # 形状 (3,)
result = col_vector + row_vector  # 广播到 (3, 3)
print(f"\n列向量 (3,1):\n{col_vector}")
print(f"行向量 (3,):\n{row_vector}")
print(f"相加结果:\n{result}")

# ============================================================
# 9. 矩阵运算
# ============================================================
print("\n" + "=" * 70)
print("9. 矩阵运算")
print("=" * 70)

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"矩阵A:\n{A}")
print(f"矩阵B:\n{B}")

# 逐元素乘法
print(f"\n逐元素乘法 (A * B):\n{A * B}")

# 矩阵乘法（点积）
print(f"\n矩阵乘法 (A @ B):\n{A @ B}")
print(f"也可以用: (np.dot(A, B)):\n{np.dot(A, B)}")

# 矩阵转置
print(f"\nA的转置:\n{A.T}")

# 矩阵的逆（仅限可逆矩阵）
try:
    A_inv = np.linalg.inv(A)
    print(f"\nA的逆:\n{A_inv}")
    print(f"A @ A_inv =\n{A @ A_inv}")
except np.linalg.LinAlgError:
    print("矩阵不可逆")

# ============================================================
# 10. 实践案例
# ============================================================
print("\n" + "=" * 70)
print("10. 实践案例")
print("=" * 70)

# 案例：学生成绩分析
print("案例：计算学生成绩统计")
scores = np.array([85, 90, 78, 92, 88, 95, 80, 87, 91, 89])
print(f"成绩: {scores}")
print(f"平均分: {np.mean(scores):.2f}")
print(f"最高分: {np.max(scores)}")
print(f"最低分: {np.min(scores)}")
print(f"标准差: {np.std(scores):.2f}")

# 及格人数和及格率
passing_score = 80
passed = scores >= passing_score
print(f"及格人数: {np.sum(passed)}/{len(scores)}")
print(f"及格率: {np.mean(passed)*100:.1f}%")

# 案例：图像像素处理（模拟）
print("\n\n案例：图像像素处理")
# 模拟一个3x3的图像（像素值0-255）
image = np.array([
    [100, 150, 200],
    [120, 180, 220],
    [140, 200, 255]
])
print(f"原图像:\n{image}")

# 降低亮度（乘以0.5）
darkened = (image * 0.5).astype(np.uint8)
print(f"降低亮度:\n{darkened}")

# 增加亮度（加50，限制在255以内）
brightened = np.minimum(image + 50, 255)
print(f"增加亮度:\n{brightened}")

# ============================================================
# 11. 总结
# ============================================================
print("\n" + "=" * 70)
print("总结 - NumPy核心概念")
print("=" * 70)
print("""
✓ 数组创建：array(), zeros(), ones(), arange(), linspace()
✓ 索引和切片：基本索引、布尔索引、花式索引
✓ 向量化操作：避免Python循环，利用NumPy的C底层优化
✓ 形状操作：reshape(), flatten(), transpose()
✓ 统计函数：sum(), mean(), std(), max(), min()
✓ 广播机制：自动扩展数组维度进行运算
✓ 矩阵运算：@或dot()进行矩阵乘法

关键概念：向量化（Vectorization）
- 不要写显式循环
- 使用NumPy函数充分利用C底层优化
- 代码更快、更简洁

下一步学习：Pandas 数据处理
""")

# ============================================================
# 练习题
# ============================================================
print("\n" + "=" * 70)
print("课后练习")
print("=" * 70)
print("""
1. 创建一个1-100的数组，找出其中所有能被5整除的数
2. 创建一个3x3的随机矩阵，计算其转置和与原矩阵的乘积
3. 已知两个数组a=[1,2,3,4,5], b=[5,4,3,2,1]，计算它们的内积
4. 创建一个10x10的矩阵，计算其对角线元素之和
5. 使用广播，将一个向量应用到矩阵的每一行

运行本文件：python 02_numpy_intro.py
""")
