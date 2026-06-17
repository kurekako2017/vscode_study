"""Import the project's MySQL schema/data into the NAS MySQL instance."""

from __future__ import annotations

import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine


ROOT_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/mysql?charset=utf8mb4"
META_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/meta?charset=utf8mb4"
DW_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/dw?charset=utf8mb4"


def split_sql(path: Path) -> list[str]:
    """把一个 SQL 文件拆成独立语句，避免一次性执行整份脚本时失控。"""

    raw = path.read_text(encoding="utf-8")
    parts: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    for ch in raw:
        # 这里需要手动跟踪单引号/双引号，避免字符串内部的分号被误判成语句结束。
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        if ch == ";" and not in_single and not in_double:
            stmt = "".join(current).strip()
            if stmt:
                parts.append(stmt)
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def filter_statements(statements: list[str]) -> list[str]:
    """过滤掉导入到目标库时不需要再次执行的初始化语句。"""

    # 这类语句通常只适用于原始导出环境，在 NAS 目标库中重复执行没有意义。
    skip_prefixes = (
        "SET NAMES",
        "CREATE DATABASE",
        "GRANT ALL PRIVILEGES",
        "USE ",
    )
    return [stmt for stmt in statements if not stmt.startswith(skip_prefixes)]


async def main() -> None:
    # 先连接系统库 mysql，确保目标数据库存在，再分别导入 meta 和 dw。
    root_engine = create_async_engine(ROOT_URL, pool_pre_ping=True)
    async with root_engine.connect() as conn:
        await conn.exec_driver_sql(
            "CREATE DATABASE IF NOT EXISTS meta DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
        )
        await conn.exec_driver_sql(
            "CREATE DATABASE IF NOT EXISTS dw DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
        )
        await conn.commit()
    await root_engine.dispose()

    for url, path in [
        (META_URL, Path("docker/mysql/meta.sql")),
        (DW_URL, Path("docker/mysql/dw.sql")),
    ]:
        # 每个数据库单独建立一个 engine，导入结束后立刻释放连接。
        engine = create_async_engine(url, pool_pre_ping=True)
        statements = filter_statements(split_sql(path))
        async with engine.connect() as conn:
            for stmt in statements:
                await conn.exec_driver_sql(stmt)
            await conn.commit()
        await engine.dispose()
        print(f"imported {path.name}: {len(statements)} statements")

    print("mysql schema import done")


if __name__ == "__main__":
    asyncio.run(main())
