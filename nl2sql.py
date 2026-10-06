#!/usr/bin/env python3
"""nl2sql —— 自然语言 -> SQL（基于 sqlite3，跑通简单查询）。

支持简单模式：
  - “所有 / 全部” -> SELECT * FROM table
  - “按 X 排序” -> ORDER BY x
  - “统计 / 多少” -> COUNT(*)
  - “X 大于 / 等于 y” -> WHERE x = y
零第三方依赖。

用法：
    from nl2sql import build_sql, run_demo
    print(build_sql("列出全部用户", table="users"))
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys

SCHEMA = {
    "users": ["id", "name", "age", "city"],
}

CN_COL = {"城市": "city", "年龄": "age", "姓名": "name", "id": "id"}


def build_sql(query: str, table: str = "users") -> str:
    cols = "*"
    if "数量" in query or "统计" in query or "多少条" in query:
        cols = "COUNT(*)"
    sql = f"SELECT {cols} FROM {table}"
    m = re.search(r"(\w+)\s*(等于|是|为)\s*[:：]?\s*(\w+)", query)
    if m:
        col, val = CN_COL.get(m.group(1), m.group(1)), m.group(3)
        if col in SCHEMA.get(table, []):
            sql += f" WHERE {col} = '{val}'"
    if "排序" in query or "按年龄" in query:
        col = "age" if "年龄" in query else "id"
        direction = "DESC" if "从大到小" in query or "降序" in query else "ASC"
        sql += f" ORDER BY {col} {direction}"
    return sql + ";"


def run_demo() -> list:
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INT, name TEXT, age INT, city TEXT)")
    cur.executemany("INSERT INTO users VALUES (?,?,?,?)", [
        (1, "张三", 20, "北京"),
        (2, "李四", 30, "上海"),
        (3, "王五", 25, "北京"),
    ])
    conn.commit()
    sql = build_sql("列出全部用户按年龄排序")
    rows = cur.execute(sql).fetchall()
    conn.close()
    return rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="自然语言 -> SQL")
    p.add_argument("query", nargs="?")
    args = p.parse_args(argv)
    q = args.query or "列出全部用户"
    print("SQL:", build_sql(q))
    print("demo rows:", run_demo())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
