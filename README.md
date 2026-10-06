# nl2sql-lite

自然语言 → SQL，基于 `sqlite3` 跑通简单查询。零第三方依赖。

## 功能简介

- 支持 SELECT * / COUNT(*) / WHERE / ORDER BY；
- `build_sql(query)` 生成 SQL；
- `run_demo()` 在内存库上插入示例数据并真实执行。

## 快速开始

```bash
python3 nl2sql.py "列出全部用户按年龄排序"
```

## 无 API key 如何运行

纯本地 sqlite3，**不需要任何 API key**。

## 目录结构

```
nl2sql-lite/
├── nl2sql.py
├── tests/test_nl2sql.py
├── README.md / LICENSE / .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## 许可证

[MIT](./LICENSE) © 2026 ljiang9
