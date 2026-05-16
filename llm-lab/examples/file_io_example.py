"""file_io_example.py

示例：JSON 和 CSV 的读写操作。
运行：`python file_io_example.py`
"""

import json
import csv
from pathlib import Path


DATA_JSON = Path("sample.json")
DATA_CSV = Path("sample.csv")


def write_json() -> None:
    data = {"items": [1, 2, 3], "note": "示例数据"}
    DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", DATA_JSON)


def read_json() -> None:
    s = DATA_JSON.read_text(encoding="utf-8")
    data = json.loads(s)
    print("Read JSON:", data)


def write_csv() -> None:
    rows = [(1, "Alice"), (2, "Bob")]
    with DATA_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        writer.writerows(rows)
    print("Wrote", DATA_CSV)


def read_csv() -> None:
    with DATA_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("row:", row)


if __name__ == "__main__":
    write_json()
    read_json()
    write_csv()
    read_csv()
