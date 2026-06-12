"""
文件功能概述：`code/C9/rag_modules/graph_indexing.py` 主要是 图indexing，这个文件里有 3 个类、0 个函数，主要用来串起当前章节的处理步骤。

主要函数/类的处理流程：
1. 类 `EntityKeyValue`：功能概述：这个类是 `EntityKeyValue`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
2. 类 `RelationKeyValue`：功能概述：这个类是 `RelationKeyValue`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
3. 类 `GraphIndexingModule`：功能概述：这个类是 `GraphIndexingModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。 调用流程： 1. `__init__`：先接收输入参数 config, llm_client，再调用 defaultdict 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 2. `create_entity_key_values`：先接收输入参数 recipes, ingredients, cooking_steps，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、hasattr、EntityKeyValue 等内部步骤完成主要工作，最后返回结果。 3. `create_relation_key_values`：先接收输入参数 relationships，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、enumerate、self.entity_kv_store.get 等内部步骤完成主要工作，最后返回结果。 4. `_generate_relation_index_keys`：先接收输入参数 source_entity, target_entity, relation_type，接着根据条件分支选择不同处理路径，再调用 getattr、list、keys.extend 等内部步骤完成主要工作，最后返回结果。 5. `_llm_enhance_relation_keys`：先接收输入参数 source_entity, target_entity, relation_type，再尝试执行核心处理，出错时进入异常兜底，再调用 self.llm_client.chat.completions.create、json.loads、result.get 等内部步骤完成主要工作，最后返回结果。 6. `deduplicate_entities_and_relations`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、defaultdict、self.entity_kv_store.items 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 7. `_rebuild_key_mappings`：先进入当前步骤，然后循环处理每一条数据，再调用 self.key_to_entities.clear、self.key_to_relations.clear、self.entity_kv_store.items 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。 8. `get_entities_by_key`：先接收输入参数 key，再调用 self.key_to_entities.get 等内部步骤完成主要工作，最后返回结果。 9. `get_relations_by_key`：先接收输入参数 key，再调用 self.key_to_relations.get 等内部步骤完成主要工作，最后返回结果。 10. `get_statistics`：先进入当前步骤，再调用 len、sum、self.entity_kv_store.values 等内部步骤完成主要工作，最后返回结果。
"""


import json
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

from langchain_core.documents import Document

logger = logging.getLogger(__name__)

@dataclass
class EntityKeyValue:
    """
    功能概述：这个类是 `EntityKeyValue`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    entity_name: str
    index_keys: List[str]  # 索引键列表
    value_content: str     # 详细描述内容
    entity_type: str       # 实体类型 (Recipe, Ingredient, CookingStep)
    metadata: Dict[str, Any]

@dataclass 
class RelationKeyValue:
    """
    功能概述：这个类是 `RelationKeyValue`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. 这个类没有单独的方法，通常用于保存配置或做简单占位。
    """
    relation_id: str
    index_keys: List[str]  # 多个索引键（可包含全局主题）
    value_content: str     # 关系描述内容
    relation_type: str     # 关系类型
    source_entity: str     # 源实体
    target_entity: str     # 目标实体
    metadata: Dict[str, Any]

class GraphIndexingModule:
    """
    功能概述：这个类是 `GraphIndexingModule`，主要负责把一组相关步骤收拢在一起，方便外部直接创建对象并调用。
    调用流程：
    1. `__init__`：先接收输入参数 config, llm_client，再调用 defaultdict 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    2. `create_entity_key_values`：先接收输入参数 recipes, ingredients, cooking_steps，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、hasattr、EntityKeyValue 等内部步骤完成主要工作，最后返回结果。
    3. `create_relation_key_values`：先接收输入参数 relationships，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、enumerate、self.entity_kv_store.get 等内部步骤完成主要工作，最后返回结果。
    4. `_generate_relation_index_keys`：先接收输入参数 source_entity, target_entity, relation_type，接着根据条件分支选择不同处理路径，再调用 getattr、list、keys.extend 等内部步骤完成主要工作，最后返回结果。
    5. `_llm_enhance_relation_keys`：先接收输入参数 source_entity, target_entity, relation_type，再尝试执行核心处理，出错时进入异常兜底，再调用 self.llm_client.chat.completions.create、json.loads、result.get 等内部步骤完成主要工作，最后返回结果。
    6. `deduplicate_entities_and_relations`：先进入当前步骤，接着根据条件分支选择不同处理路径，然后循环处理每一条数据，再调用 logger.info、defaultdict、self.entity_kv_store.items 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    7. `_rebuild_key_mappings`：先进入当前步骤，然后循环处理每一条数据，再调用 self.key_to_entities.clear、self.key_to_relations.clear、self.entity_kv_store.items 等内部步骤完成主要工作，最后把结果交给下一步或直接结束。
    8. `get_entities_by_key`：先接收输入参数 key，再调用 self.key_to_entities.get 等内部步骤完成主要工作，最后返回结果。
    9. `get_relations_by_key`：先接收输入参数 key，再调用 self.key_to_relations.get 等内部步骤完成主要工作，最后返回结果。
    10. `get_statistics`：先进入当前步骤，再调用 len、sum、self.entity_kv_store.values 等内部步骤完成主要工作，最后返回结果。
    """
    
    def __init__(self, config, llm_client):  # 中文名称：初始化
        self.config = config
        self.llm_client = llm_client
        
        # 键值对存储
        self.entity_kv_store: Dict[str, EntityKeyValue] = {}
        self.relation_kv_store: Dict[str, RelationKeyValue] = {}
        
        # 索引映射：key -> entity/relation IDs
        self.key_to_entities: Dict[str, List[str]] = defaultdict(list)
        self.key_to_relations: Dict[str, List[str]] = defaultdict(list)
        
    def create_entity_key_values(self, recipes: List[Any], ingredients: List[Any], 
                                cooking_steps: List[Any]) -> Dict[str, EntityKeyValue]:  # 中文名称：创建entitykeyvalues
        """
        为实体创建键值对结构
        每个实体使用其名称作为唯一索引键
        """
        logger.info("开始创建实体键值对...")
        
        # 处理菜谱实体
        for recipe in recipes:
            entity_id = recipe.node_id
            entity_name = recipe.name or f"菜谱_{entity_id}"
            
            # 构建详细内容
            content_parts = [f"菜品名称: {entity_name}"]
            
            if hasattr(recipe, 'properties'):
                props = recipe.properties
                if props.get('description'):
                    content_parts.append(f"描述: {props['description']}")
                if props.get('category'):
                    content_parts.append(f"分类: {props['category']}")
                if props.get('cuisineType'):
                    content_parts.append(f"菜系: {props['cuisineType']}")
                if props.get('difficulty'):
                    content_parts.append(f"难度: {props['difficulty']}")
                if props.get('cookingTime'):
                    content_parts.append(f"制作时间: {props['cookingTime']}")
            
            # 创建键值对
            entity_kv = EntityKeyValue(
                entity_name=entity_name,
                index_keys=[entity_name],  # 使用名称作为唯一索引键
                value_content='\n'.join(content_parts),
                entity_type="Recipe",
                metadata={
                    "node_id": entity_id,
                    "properties": getattr(recipe, 'properties', {})
                }
            )
            
            self.entity_kv_store[entity_id] = entity_kv
            self.key_to_entities[entity_name].append(entity_id)
        
        # 处理食材实体
        for ingredient in ingredients:
            entity_id = ingredient.node_id
            entity_name = ingredient.name or f"食材_{entity_id}"
            
            content_parts = [f"食材名称: {entity_name}"]
            
            if hasattr(ingredient, 'properties'):
                props = ingredient.properties
                if props.get('category'):
                    content_parts.append(f"类别: {props['category']}")
                if props.get('nutrition'):
                    content_parts.append(f"营养信息: {props['nutrition']}")
                if props.get('storage'):
                    content_parts.append(f"储存方式: {props['storage']}")
            
            entity_kv = EntityKeyValue(
                entity_name=entity_name,
                index_keys=[entity_name],
                value_content='\n'.join(content_parts),
                entity_type="Ingredient",
                metadata={
                    "node_id": entity_id,
                    "properties": getattr(ingredient, 'properties', {})
                }
            )
            
            self.entity_kv_store[entity_id] = entity_kv
            self.key_to_entities[entity_name].append(entity_id)
        
        # 处理烹饪步骤实体
        for step in cooking_steps:
            entity_id = step.node_id
            entity_name = f"步骤_{entity_id}"
            
            content_parts = [f"烹饪步骤: {entity_name}"]
            
            if hasattr(step, 'properties'):
                props = step.properties
                if props.get('description'):
                    content_parts.append(f"步骤描述: {props['description']}")
                if props.get('order'):
                    content_parts.append(f"步骤顺序: {props['order']}")
                if props.get('technique'):
                    content_parts.append(f"技巧: {props['technique']}")
                if props.get('time'):
                    content_parts.append(f"时间: {props['time']}")
            
            entity_kv = EntityKeyValue(
                entity_name=entity_name,
                index_keys=[entity_name],
                value_content='\n'.join(content_parts),
                entity_type="CookingStep", 
                metadata={
                    "node_id": entity_id,
                    "properties": getattr(step, 'properties', {})
                }
            )
            
            self.entity_kv_store[entity_id] = entity_kv
            self.key_to_entities[entity_name].append(entity_id)
        
        logger.info(f"实体键值对创建完成，共 {len(self.entity_kv_store)} 个实体")
        return self.entity_kv_store
    
    def create_relation_key_values(self, relationships: List[Tuple[str, str, str]]) -> Dict[str, RelationKeyValue]:  # 中文名称：创建relationkeyvalues
        """
        为关系创建键值对结构
        关系可能有多个索引键，包含从LLM增强的全局主题
        """
        logger.info("开始创建关系键值对...")
        
        for i, (source_id, relation_type, target_id) in enumerate(relationships):
            relation_id = f"rel_{i}_{source_id}_{target_id}"
            
            # 获取源实体和目标实体信息
            source_entity = self.entity_kv_store.get(source_id)
            target_entity = self.entity_kv_store.get(target_id)
            
            if not source_entity or not target_entity:
                continue
            
            # 构建关系描述
            content_parts = [
                f"关系类型: {relation_type}",
                f"源实体: {source_entity.entity_name} ({source_entity.entity_type})",
                f"目标实体: {target_entity.entity_name} ({target_entity.entity_type})"
            ]
            
            # 生成多个索引键（包含全局主题）
            index_keys = self._generate_relation_index_keys(
                source_entity, target_entity, relation_type
            )
            
            # 创建关系键值对
            relation_kv = RelationKeyValue(
                relation_id=relation_id,
                index_keys=index_keys,
                value_content='\n'.join(content_parts),
                relation_type=relation_type,
                source_entity=source_id,
                target_entity=target_id,
                metadata={
                    "source_name": source_entity.entity_name,
                    "target_name": target_entity.entity_name,
                    "created_from_graph": True
                }
            )
            
            self.relation_kv_store[relation_id] = relation_kv
            
            # 为每个索引键建立映射
            for key in index_keys:
                self.key_to_relations[key].append(relation_id)
        
        logger.info(f"关系键值对创建完成，共 {len(self.relation_kv_store)} 个关系")
        return self.relation_kv_store
    
    def _generate_relation_index_keys(self, source_entity: EntityKeyValue, 
                                    target_entity: EntityKeyValue, 
                                    relation_type: str) -> List[str]:  # 中文名称：generaterelation索引keys
        """
        为关系生成多个索引键，包含全局主题
        """
        keys = [relation_type]  # 基础关系类型键
        
        # 根据关系类型和实体类型生成主题键
        if relation_type == "REQUIRES":
            # 菜谱-食材关系的主题键
            keys.extend([
                "食材搭配",
                "烹饪原料",
                f"{source_entity.entity_name}_食材",
                target_entity.entity_name
            ])
        elif relation_type == "HAS_STEP":
            # 菜谱-步骤关系的主题键
            keys.extend([
                "制作步骤",
                "烹饪过程",
                f"{source_entity.entity_name}_步骤",
                "制作方法"
            ])
        elif relation_type == "BELONGS_TO_CATEGORY":
            # 分类关系的主题键
            keys.extend([
                "菜品分类",
                "美食类别",
                target_entity.entity_name
            ])
        
        # 使用LLM增强关系索引键（可选）
        if getattr(self.config, 'enable_llm_relation_keys', False):
            enhanced_keys = self._llm_enhance_relation_keys(source_entity, target_entity, relation_type)
            keys.extend(enhanced_keys)
        
        # 去重并返回
        return list(set(keys))
    
    def _llm_enhance_relation_keys(self, source_entity: EntityKeyValue, 
                                 target_entity: EntityKeyValue, 
                                 relation_type: str) -> List[str]:  # 中文名称：大模型enhancerelationkeys
        """
        使用LLM增强关系索引键，生成全局主题
        """
        prompt = f"""
        分析以下实体关系，生成相关的主题关键词：
        
        源实体: {source_entity.entity_name} ({source_entity.entity_type})
        目标实体: {target_entity.entity_name} ({target_entity.entity_type})
        关系类型: {relation_type}
        
        请生成3-5个相关的主题关键词，用于索引和检索。
        返回JSON格式：{{"keywords": ["关键词1", "关键词2", "关键词3"]}}
        """
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.config.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result.get("keywords", [])
            
        except Exception as e:
            logger.error(f"LLM增强关系索引键失败: {e}")
            return []
    
    def deduplicate_entities_and_relations(self):  # 中文名称：deduplicateentitiesandrelations
        """
        去重相同的实体和关系，优化图操作
        """
        logger.info("开始去重实体和关系...")
        
        # 实体去重：基于名称
        name_to_entities = defaultdict(list)
        for entity_id, entity_kv in self.entity_kv_store.items():
            name_to_entities[entity_kv.entity_name].append(entity_id)
        
        # 合并重复实体
        entities_to_remove = []
        for name, entity_ids in name_to_entities.items():
            if len(entity_ids) > 1:
                # 保留第一个，合并其他的内容
                primary_id = entity_ids[0]
                primary_entity = self.entity_kv_store[primary_id]
                
                for entity_id in entity_ids[1:]:
                    duplicate_entity = self.entity_kv_store[entity_id]
                    # 合并内容
                    primary_entity.value_content += f"\n\n补充信息: {duplicate_entity.value_content}"
                    # 标记删除
                    entities_to_remove.append(entity_id)
        
        # 删除重复实体
        for entity_id in entities_to_remove:
            del self.entity_kv_store[entity_id]
        
        # 关系去重：基于源-目标-类型
        relation_signature_to_ids = defaultdict(list)
        for relation_id, relation_kv in self.relation_kv_store.items():
            signature = f"{relation_kv.source_entity}_{relation_kv.target_entity}_{relation_kv.relation_type}"
            relation_signature_to_ids[signature].append(relation_id)
        
        # 合并重复关系
        relations_to_remove = []
        for signature, relation_ids in relation_signature_to_ids.items():
            if len(relation_ids) > 1:
                # 保留第一个，删除其他
                for relation_id in relation_ids[1:]:
                    relations_to_remove.append(relation_id)
        
        # 删除重复关系
        for relation_id in relations_to_remove:
            del self.relation_kv_store[relation_id]
        
        # 重建索引映射
        self._rebuild_key_mappings()
        
        logger.info(f"去重完成 - 删除了 {len(entities_to_remove)} 个重复实体，{len(relations_to_remove)} 个重复关系")
    
    def _rebuild_key_mappings(self):  # 中文名称：rebuildkeymappings
        """重建键到实体/关系的映射"""
        self.key_to_entities.clear()
        self.key_to_relations.clear()
        
        # 重建实体映射
        for entity_id, entity_kv in self.entity_kv_store.items():
            for key in entity_kv.index_keys:
                self.key_to_entities[key].append(entity_id)
        
        # 重建关系映射
        for relation_id, relation_kv in self.relation_kv_store.items():
            for key in relation_kv.index_keys:
                self.key_to_relations[key].append(relation_id)
    
    def get_entities_by_key(self, key: str) -> List[EntityKeyValue]:  # 中文名称：获取entitiesbykey
        """根据索引键获取实体"""
        entity_ids = self.key_to_entities.get(key, [])
        return [self.entity_kv_store[eid] for eid in entity_ids if eid in self.entity_kv_store]
    
    def get_relations_by_key(self, key: str) -> List[RelationKeyValue]:  # 中文名称：获取relationsbykey
        """根据索引键获取关系"""
        relation_ids = self.key_to_relations.get(key, [])
        return [self.relation_kv_store[rid] for rid in relation_ids if rid in self.relation_kv_store]
    

    
    def get_statistics(self) -> Dict[str, Any]:  # 中文名称：获取statistics
        """获取键值对存储统计信息"""
        return {
            "total_entities": len(self.entity_kv_store),
            "total_relations": len(self.relation_kv_store),
            "total_entity_keys": sum(len(kv.index_keys) for kv in self.entity_kv_store.values()),
            "total_relation_keys": sum(len(kv.index_keys) for kv in self.relation_kv_store.values()),
            "entity_types": {
                "Recipe": len([kv for kv in self.entity_kv_store.values() if kv.entity_type == "Recipe"]),
                "Ingredient": len([kv for kv in self.entity_kv_store.values() if kv.entity_type == "Ingredient"]),
                "CookingStep": len([kv for kv in self.entity_kv_store.values() if kv.entity_type == "CookingStep"])
            }
        } 