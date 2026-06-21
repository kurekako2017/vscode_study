"""file_io_example.py

示例：JSON 和 CSV 的读写操作。
运行：`python3 file_io_example.py`
"""

import json
import csv
from pathlib import Path


# 用 Path 表示文件路径，比直接拼字符串更清晰。
# 这里生成的文件会出现在当前运行目录。
DATA_JSON = Path("sample.json")
DATA_CSV = Path("sample.csv")


def write_json() -> None:
    # data 是一个普通 Python 字典，模拟后端或模型处理后的结构化数据。
    data = {"items": [1, 2, 3], "note": "示例数据"}
    # 把 Python 对象序列化为 JSON 并写入文件（UTF-8 编码）
    # ensure_ascii=False 用于正常保存中文；indent=2 让文件更易读。
    DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", DATA_JSON)


def read_json() -> None:
    # 从文件读取并解析为 Python 对象
    # read_text 得到字符串，json.loads 把字符串解析回 dict/list。
    s = DATA_JSON.read_text(encoding="utf-8")
    data = json.loads(s)
    print("Read JSON:", data)


def write_csv() -> None:
    # CSV 适合保存表格类数据，例如测试问题集、评估结果。
    rows = [(1, "Alice"), (2, "Bob")]
    # newline="" 是 csv 模块推荐写法，避免不同系统下多出空行。
    with DATA_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 第一行通常写表头。
        writer.writerow(["id", "name"])
        # writerows 一次写入多行数据。
        writer.writerows(rows)
    print("Wrote", DATA_CSV)


def read_csv() -> None:
    # 使用 csv.DictReader 按列名读取 CSV 行，返回字典对象
    # 这样后续可以通过 row["id"]、row["name"] 访问字段。
    with DATA_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("row:", row)


if __name__ == "__main__":
    print("MODEL: provider=local model=none mode=file-io")
    # 按“先写后读”的顺序演示 JSON 和 CSV。
    # 运行后会在当前目录生成 sample.json 和 sample.csv。
    write_json()
    read_json()
    write_csv()
    read_csv()
