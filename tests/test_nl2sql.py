import sqlite3
import unittest

from nl2sql import build_sql, run_demo


class TestNl2Sql(unittest.TestCase):
    def test_select_all(self):
        sql = build_sql("列出全部用户")
        self.assertIn("SELECT", sql)
        self.assertIn("FROM users", sql)

    def test_count(self):
        sql = build_sql("用户数量")
        self.assertIn("COUNT(*)", sql)

    def test_order(self):
        sql = build_sql("按年龄排序")
        self.assertIn("ORDER BY age", sql)

    def test_where(self):
        sql = build_sql("城市等于北京")
        self.assertIn("WHERE city = '北京'", sql)

    def test_sql_executable(self):
        sql = build_sql("列出全部用户")
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id INT, name TEXT, age INT, city TEXT)")
        conn.execute(sql.rstrip(";"))
        conn.close()

    def test_demo_runs(self):
        rows = run_demo()
        self.assertEqual(len(rows), 3)


if __name__ == "__main__":
    unittest.main()
