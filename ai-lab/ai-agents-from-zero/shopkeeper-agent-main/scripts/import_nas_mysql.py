"""Import the project's MySQL schema/data into the NAS MySQL instance."""

from __future__ import annotations

import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine


ROOT_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/mysql?charset=utf8mb4"
META_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/meta?charset=utf8mb4"
DW_URL = "mysql+asyncmy://root:123456@192.168.10.2:3306/dw?charset=utf8mb4"


def split_sql(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    parts: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    for ch in raw:
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
    skip_prefixes = (
        "SET NAMES",
        "CREATE DATABASE",
        "GRANT ALL PRIVILEGES",
        "USE ",
    )
    return [stmt for stmt in statements if not stmt.startswith(skip_prefixes)]


async def main() -> None:
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
