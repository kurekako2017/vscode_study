"""
本地知识库子智能体配置模块

将 app/prompt/prompts.yml 中的本地知识库配置与本地检索工具组装成
DeepAgents 可识别的字典式子智能体。主智能体后续会根据 description
决定是否把企业内部非结构化文档查询任务分派给它。
"""

from app.agent.prompts import sub_agents_content
from app.tools.local_kb_tools import create_ask_delete, get_assistant_list

# 本地知识库子智能体处理内部非结构化文档，与网络搜索助手、数据库查询助手形成互补
# 它遵循“先查助手列表 -> 再向指定助手提问”的工作顺序
# tools 列表声明该子智能体可以发现知识库助手，并发起一次性检索查询
knowledge_base_agent = {
    "name": sub_agents_content["local_kb"]["name"],
    "description": sub_agents_content["local_kb"]["description"],
    "system_prompt": sub_agents_content["local_kb"]["system_prompt"],
    "tools": [get_assistant_list, create_ask_delete],
}
