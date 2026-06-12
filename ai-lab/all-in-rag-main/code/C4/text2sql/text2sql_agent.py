"""
文件功能概述：`code/C4/text2sql/text2sql_agent.py` 主要是 文本转SQL智能体，这个文件里有 1 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `SimpleText2SQLAgent`：功能概述：这个类是 `SimpleText2SQLAgent`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 milvus_uri, api_key，再调用 SimpleKnowledgeBase、SimpleSQLGenerator 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `connect_database`：先接收输入参数 db_path，再尝试执行核心处理，出错时进入异常兜底，再调用 sqlite3.connect、print、str 等内部步骤完成主要工作，最后返回结果。 3. `load_knowledge_base`：先进入当前步骤，再调用 self.knowledge_base.load_data 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 4. `query`：先接收输入参数 user_question，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 print、self.knowledge_base.search、self.sql_generator.generate_sql 等内部步骤完成主要工作，最后返回结果。 5. `_execute_sql`：先接收输入参数 sql，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.connection.cursor、cursor.execute、startswith 等内部步骤完成主要工作，最后返回结果。 6. `add_example`：先接收输入参数 question, sql，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，再调用 os.path.join、os.path.dirname、os.path.exists 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 7. `get_table_info`：先进入当前步骤，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.connection.cursor、cursor.execute、cursor.fetchall 等内部步骤完成主要工作，最后返回结果。 8. `cleanup`：先进入当前步骤，接着根据条件分支选择不同处理路径，再调用 self.knowledge_base.cleanup、print、self.connection.close 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
"""

import sqlite3
import os
from typing import Dict, Any, List, Tuple
from .knowledge_base import SimpleKnowledgeBase
from .sql_generator import SimpleSQLGenerator


class SimpleText2SQLAgent:
    """
    功能概述：这个类是 `SimpleText2SQLAgent`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 milvus_uri, api_key，再调用 SimpleKnowledgeBase、SimpleSQLGenerator 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `connect_database`：先接收输入参数 db_path，再尝试执行核心处理，出错时进入异常兜底，再调用 sqlite3.connect、print、str 等内部步骤完成主要工作，最后返回结果。
    3. `load_knowledge_base`：先进入当前步骤，再调用 self.knowledge_base.load_data 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    4. `query`：先接收输入参数 user_question，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 print、self.knowledge_base.search、self.sql_generator.generate_sql 等内部步骤完成主要工作，最后返回结果。
    5. `_execute_sql`：先接收输入参数 sql，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.connection.cursor、cursor.execute、startswith 等内部步骤完成主要工作，最后返回结果。
    6. `add_example`：先接收输入参数 question, sql，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，再调用 os.path.join、os.path.dirname、os.path.exists 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    7. `get_table_info`：先进入当前步骤，再尝试执行核心处理，出错时进入异常兜底，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 self.connection.cursor、cursor.execute、cursor.fetchall 等内部步骤完成主要工作，最后返回结果。
    8. `cleanup`：先进入当前步骤，接着根据条件分支选择不同处理路径，再调用 self.knowledge_base.cleanup、print、self.connection.close 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    """
    
    def __init__(self, milvus_uri: str = "http://localhost:19530", api_key: str = None):  # 中文名称：初始化
        """初始化代理"""
        self.knowledge_base = SimpleKnowledgeBase(milvus_uri)
        self.sql_generator = SimpleSQLGenerator(api_key)
        self.db_path = None
        self.connection = None
        
        # 配置参数
        self.max_retry_count = 3
        self.top_k_retrieval = 5
        self.max_result_rows = 100
    
    def connect_database(self, db_path: str) -> bool:  # 中文名称：connectdatabase
        """连接SQLite数据库"""
        try:
            self.db_path = db_path
            self.connection = sqlite3.connect(db_path)
            print(f"成功连接到数据库: {db_path}")
            return True
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            return False
    
    def load_knowledge_base(self):  # 中文名称：加载知识base
        """加载知识库"""
        self.knowledge_base.load_data()
    
    def query(self, user_question: str) -> Dict[str, Any]:  # 中文名称：查询
        """执行Text2SQL查询"""
        if not self.connection:
            return {
                "success": False,
                "error": "数据库未连接",
                "sql": None,
                "results": None
            }
        
        print(f"\n=== 处理查询: {user_question} ===")
        
        # 1. 从知识库检索
        print("检索知识库...")
        knowledge_results = self.knowledge_base.search(user_question, self.top_k_retrieval)
        print(f"检索到 {len(knowledge_results)} 条相关信息")
        
        # 2. 生成SQL
        print("生成SQL...")
        sql = self.sql_generator.generate_sql(user_question, knowledge_results)
        print(f"生成的SQL: {sql}")
        
        # 3. 执行SQL（带重试）
        retry_count = 0
        while retry_count < self.max_retry_count:
            print(f"执行SQL (尝试 {retry_count + 1}/{self.max_retry_count})...")
            
            success, result = self._execute_sql(sql)
            
            if success:
                print("SQL执行成功!")
                return {
                    "success": True,
                    "error": None,
                    "sql": sql,
                    "results": result,
                    "retry_count": retry_count
                }
            else:
                print(f"SQL执行失败: {result}")
                
                if retry_count < self.max_retry_count - 1:
                    print("尝试修复SQL...")
                    sql = self.sql_generator.fix_sql(sql, result, knowledge_results)
                    print(f"修复后的SQL: {sql}")
                
                retry_count += 1
        
        return {
            "success": False,
            "error": f"超过最大重试次数 ({self.max_retry_count})",
            "sql": sql,
            "results": None,
            "retry_count": retry_count
        }
    
    def _execute_sql(self, sql: str) -> Tuple[bool, Any]:  # 中文名称：executeSQL
        """执行SQL语句"""
        try:
            cursor = self.connection.cursor()
            
            # 添加LIMIT限制
            if sql.strip().upper().startswith('SELECT') and 'LIMIT' not in sql.upper():
                sql = f"{sql.rstrip(';')} LIMIT {self.max_result_rows}"
            
            cursor.execute(sql)
            
            if sql.strip().upper().startswith('SELECT'):
                # 查询语句
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    result_row = {}
                    for i, value in enumerate(row):
                        result_row[columns[i]] = value
                    results.append(result_row)
                
                cursor.close()
                return True, {
                    "columns": columns,
                    "rows": results,
                    "count": len(results)
                }
            else:
                # 非查询语句
                self.connection.commit()
                cursor.close()
                return True, "SQL执行成功"
        
        except Exception as e:
            return False, str(e)
    
    def add_example(self, question: str, sql: str):  # 中文名称：add示例
        """添加新的Q->SQL示例"""
        # 简化版本：直接保存到文件
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        qsql_path = os.path.join(data_dir, "qsql_examples.json")
        
        try:
            import json
            
            # 读取现有数据
            if os.path.exists(qsql_path):
                with open(qsql_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            # 添加新示例
            data.append({
                "question": question,
                "sql": sql,
                "database": "sqlite"
            })
            
            # 保存
            with open(qsql_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"已添加新示例: {question}")
            
        except Exception as e:
            print(f"添加示例失败: {str(e)}")
    
    def get_table_info(self) -> List[Dict[str, Any]]:  # 中文名称：获取tableinfo
        """获取数据库表信息"""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            table_info = []
            for table in tables:
                table_name = table[0]
                
                # 获取表结构
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                table_info.append({
                    "table_name": table_name,
                    "columns": [
                        {
                            "name": col[1],
                            "type": col[2],
                            "nullable": not col[3],
                            "default": col[4],
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ]
                })
            
            cursor.close()
            return table_info
            
        except Exception as e:
            print(f"获取表信息失败: {str(e)}")
            return []
    
    def cleanup(self):  # 中文名称：cleanup
        """清理资源"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("数据库连接已关闭")
        
        self.knowledge_base.cleanup()
        print("知识库已清理") 