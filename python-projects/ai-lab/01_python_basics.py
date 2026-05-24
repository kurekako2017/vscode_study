"""
第1阶段：基础理论和Python编程
01_python_basics.py - Python基础语法和数据类型

学习目标：
- 熟悉Python的基本语法
- 理解基本的数据类型
- 学会使用列表、字典等数据结构
- 掌握函数和控制流

预计时间：3天
难度：⭐
"""

# ============================================================
# 1. 基本数据类型
# ============================================================
print("=" * 60)
print("1. 基本数据类型")
print("=" * 60)

# 整数和浮点数
# int: 整数类型，用于存储整数值
age = 25
# float: 浮点数类型，用于存储小数值
height = 1.75
# type() 函数返回变量的数据类型，.__name__ 获取类型的名称字符串
print(f"年龄: {age} (类型: {type(age).__name__})")
print(f"身高: {height} (类型: {type(height).__name__})")

# 字符串
# str: 字符串类型，用于存储文本数据，用引号括起来
name = "小明"
message = "学习AI很有趣"
# f-string: 格式化字符串的现代方式，用 f"...{变量}..." 的形式嵌入变量
print(f"姓名: {name}")
print(f"消息: {message}")

# 布尔值
is_student = True
is_working = False
print(f"是学生吗: {is_student}, 在工作吗: {is_working}")

# ============================================================
# 2. 数据结构：列表（List）
# ============================================================
print("\n" + "=" * 60)
print("2. 列表（List）- 有序、可修改")
print("=" * 60)

# 创建列表
# list: 有序的可修改集合，用方括号 [] 定义，元素用逗号分隔
scores = [85, 90, 78, 92, 88]
print(f"成绩列表: {scores}")
# 列表索引从 0 开始：scores[0] 是第一个元素
print(f"第一个成绩: {scores[0]}")
# 负索引：scores[-1] 表示最后一个元素，scores[-2] 表示倒数第二个，以此类推
print(f"最后一个成绩: {scores[-1]}")

# 列表操作
# append() 方法：在列表末尾添加一个元素
scores.append(95)  # 添加元素
print(f"添加95后: {scores}")

# 通过索引修改列表中的元素
scores[0] = 86  # 修改元素
print(f"修改第一个元素: {scores}")

# sum() 计算列表元素的和，len() 计算列表长度
# :.2f 表示格式化为两位小数的浮点数
average = sum(scores) / len(scores)
print(f"平均成绩: {average:.2f}")

# 列表切片（Slicing）
# 切片语法：list[start:end] 表示从 start 到 end-1 的元素（不包括 end）
# scores[:3] 表示从开始到第3个元素（索引0、1、2）
print(f"前3个成绩: {scores[:3]}")
# scores[-2:] 表示从倒数第2个到末尾的所有元素
print(f"后2个成绩: {scores[-2:]}")

# ============================================================
# 3. 数据结构：字典（Dictionary）
# ============================================================
print("\n" + "=" * 60)
print("3. 字典（Dictionary）- 键值对")
print("=" * 60)

# 创建字典
# dict: 键值对的无序集合，用大括号 {} 定义
# 每个元素由 "键" : 值 组成，键用来标识值
student = {
    "name": "小明",
    "age": 25,
    "major": "计算机科学",
    "gpa": 3.8
}
print(f"学生信息: {student}")
# 通过键来访问字典中的值
print(f"姓名: {student['name']}")
print(f"年龄: {student['age']}")

# 添加新键值对
student['phone'] = '13800138000'
print(f"添加电话后: {student}")

# 遍历字典
# .items() 方法返回字典的所有键值对
# for 循环将每个键值对解包为 key 和 value 变量
print("所有信息:")
for key, value in student.items():
    print(f"  {key}: {value}")

# ============================================================
# 4. 控制流：if 语句
# ============================================================
print("\n" + "=" * 60)
print("4. 控制流：if 语句")
print("=" * 60)

score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
else:
    grade = 'F'

print(f"成绩: {score}, 等级: {grade}")

# ============================================================
# 5. 循环：for 和 while
# ============================================================
print("\n" + "=" * 60)
print("5. 循环：for 和 while")
print("=" * 60)

# for 循环
print("使用 for 循环打印1-5:")
for i in range(1, 6):
    print(f"  数字: {i}")

# 遍历列表
print("\n成绩列表中大于等于85的成绩:")
for score in scores:
    if score >= 85:
        print(f"  {score}")

# while 循环
print("\nwhile 循环计数:")
count = 0
while count < 3:
    print(f"  计数: {count}")
    count += 1

# ============================================================
# 6. 函数定义和调用
# ============================================================
print("\n" + "=" * 60)
print("6. 函数定义和调用")
print("=" * 60)

# 定义简单函数
def greet(name):
    """问候函数"""
    return f"你好，{name}！"

message = greet("小明")
print(message)

# 定义有多个参数的函数
def calculate_bmi(weight, height):
    """计算BMI指数
    参数:
        weight: 体重（kg）
        height: 身高（m）
    返回:
        bmi: BMI值
    """
    bmi = weight / (height ** 2)
    return bmi

bmi = calculate_bmi(70, 1.75)
print(f"BMI值: {bmi:.2f}")

# 定义有默认参数的函数
def power(base, exponent=2):
    """计算幂
    参数:
        base: 底数
        exponent: 指数（默认为2）
    """
    return base ** exponent

print(f"2的平方: {power(2)}")
print(f"2的立方: {power(2, 3)}")
print(f"5的4次方: {power(5, 4)}")

# ============================================================
# 7. 列表推导式（List Comprehension）
# ============================================================
print("\n" + "=" * 60)
print("7. 列表推导式")
print("=" * 60)

# 传统方法
numbers = []
for i in range(1, 6):
    numbers.append(i ** 2)
print(f"传统方法 - 平方数: {numbers}")

# 列表推导式（更优雅）
numbers = [i ** 2 for i in range(1, 6)]
print(f"列表推导式 - 平方数: {numbers}")

# 带条件的列表推导式
even_numbers = [i for i in range(1, 11) if i % 2 == 0]
print(f"1-10的偶数: {even_numbers}")

# ============================================================
# 8. 字符串操作
# ============================================================
print("\n" + "=" * 60)
print("8. 字符串操作")
print("=" * 60)

text = "  Python Machine Learning  "
print(f"原文本: '{text}'")
print(f"去除空格: '{text.strip()}'")
print(f"转大写: '{text.upper()}'")
print(f"转小写: '{text.lower()}'")

# 字符串分割和连接
sentence = "Python is awesome"
words = sentence.split()
print(f"分割后: {words}")

joined = "-".join(words)
print(f"用'-'连接: {joined}")

# 字符串格式化
name = "小明"
age = 25
print(f"我叫{name}，今年{age}岁")  # f-string (推荐)
print("我叫{}，今年{}岁".format(name, age))  # format 方法

# ============================================================
# 9. 实践练习
# ============================================================
print("\n" + "=" * 60)
print("9. 实践练习")
print("=" * 60)

# 练习1：计算成绩统计
def analyze_scores(scores_list):
    """分析成绩列表
    返回：平均分、最高分、最低分
    """
    avg = sum(scores_list) / len(scores_list)
    max_score = max(scores_list)
    min_score = min(scores_list)
    return avg, max_score, min_score

test_scores = [85, 90, 78, 92, 88, 95, 80]
avg, max_s, min_s = analyze_scores(test_scores)
print(f"成绩: {test_scores}")
print(f"平均: {avg:.2f}, 最高: {max_s}, 最低: {min_s}")

# 练习2：猜数字游戏
def play_guess_game():
    """简单的猜数字游戏"""
    secret = 42
    guesses = 0
    max_guesses = 5
    
    print("\n猜数字游戏 (1-100):")
    while guesses < max_guesses:
        try:
            guess = int(input(f"请输入你的猜测 (剩余{max_guesses - guesses}次): "))
            guesses += 1
            
            if guess == secret:
                print(f"恭喜！你猜对了！用了{guesses}次")
                return True
            elif guess < secret:
                print("太小了，再试试")
            else:
                print("太大了，再试试")
        except ValueError:
            print("请输入一个有效的数字")
    
    print(f"游戏结束，正确答案是 {secret}")
    return False

# 取消注释以运行游戏
# play_guess_game()

# ============================================================
# 10. 总结
# ============================================================
print("\n" + "=" * 60)
print("10. 总结 - Python基础概念")
print("=" * 60)

summary = """
✓ 数据类型：int, float, str, bool
✓ 数据结构：list（列表）, dict（字典）
✓ 控制流：if-elif-else, for, while
✓ 函数：def 定义，参数，返回值，默认参数
✓ 列表推导式：简洁的列表创建方式
✓ 字符串操作：分割、连接、格式化

下一步学习：NumPy 数组操作
"""
print(summary)

# ============================================================
# 练习题
# ============================================================
print("\n" + "=" * 60)
print("课后练习")
print("=" * 60)
print("""
1. 创建一个列表，包含5个数字，计算它们的和、平均值
2. 创建一个字典表示一个人的信息（名字、年龄、城市等）
3. 写一个函数，判断一个数是否是质数
4. 使用列表推导式，从1到100中找出所有能被3整除的数
5. 写一个函数，将一个句子中的单词反转顺序

答案可以参考：https://github.com/你的用户名/study/blob/main/solutions/
""")
