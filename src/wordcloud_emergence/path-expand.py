#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Semantic Concept Expander with Knowledge Graph Integration
基于ConceptNet知识图谱的语义扩展增强器
"""

import json
import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from http.server import BaseHTTPRequestHandler
import openai
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConceptNetKnowledgeGraph:
    """
    ConceptNet知识图谱集成器
    为词云测试器提供真实的概念关系数据
    """

    def __init__(self):
        self.conceptnet_api_base = "http://api.conceptnet.io"
        self.writing_concepts_cache = {}
        self.concept_relations_cache = {}
        self.initialized = False

    async def initialize(self):
        """初始化ConceptNet知识图谱连接"""
        try:
            # 预加载创意写作相关核心概念
            core_creative_concepts = [
                "creativity", "imagination", "inspiration", "expression",
                "concept", "idea", "thought", "mind", "brain",
                "semantic", "meaning", "understanding", "connection",
                "network", "relation", "association", "link",
                "visualization", "word", "language", "communication"
            ]

            logger.info("开始加载ConceptNet创意概念...")
            for concept in core_creative_concepts:
                await self._load_concept_relations(concept)
                await asyncio.sleep(0.1)  # 避免API限流

            self.initialized = True
            logger.info(f"✅ ConceptNet知识图谱初始化完成，加载了{len(self.writing_concepts_cache)}个概念")

        except Exception as e:
            logger.error(f"ConceptNet初始化失败: {e}")
            # 使用本地备用知识库
            self._load_fallback_knowledge()

    async def _load_concept_relations(self, concept: str):
        """加载单个概念的关系网络"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                # 获取概念的相关关系
                url = f"{self.conceptnet_api_base}/c/en/{concept}"
                async with session.get(url, params={'limit': 20}) as response:
                    if response.status == 200:
                        data = await response.json()
                        relations = self._parse_conceptnet_relations(data)
                        self.writing_concepts_cache[concept] = relations

        except Exception as e:
            logger.warning(f"加载概念{concept}失败: {e}")
            # 使用备用数据
            self.writing_concepts_cache[concept] = self._get_fallback_relations(concept)

    def _parse_conceptnet_relations(self, conceptnet_data: dict) -> dict:
        """解析ConceptNet返回的关系数据"""
        relations = {
            'related_to': [],
            'is_a': [],
            'used_for': [],
            'has_property': [],
            'causes': [],
            'part_of': []
        }

        for edge in conceptnet_data.get('edges', []):
            rel_type = edge.get('rel', {}).get('label', '').lower()
            end_concept = edge.get('end', {}).get('label', '')

            if rel_type in ['relatedto', 'synonym']:
                relations['related_to'].append(end_concept)
            elif rel_type in ['isa', 'instanceof']:
                relations['is_a'].append(end_concept)
            elif rel_type in ['usedfor', 'capableof']:
                relations['used_for'].append(end_concept)
            elif rel_type in ['hasproperty', 'hascontext']:
                relations['has_property'].append(end_concept)
            elif rel_type in ['causes', 'motivatedbygoal']:
                relations['causes'].append(end_concept)
            elif rel_type in ['partof', 'memberof']:
                relations['part_of'].append(end_concept)

        return relations

    def _load_fallback_knowledge(self):
        """加载备用本地知识库"""
        fallback_knowledge = {
            'creativity': {
                'related_to': ['imagination', 'innovation', 'art', 'invention'],
                'is_a': ['mental_process', 'cognitive_ability'],
                'used_for': ['problem_solving', 'expression', 'creation'],
                'has_property': ['original', 'novel', 'valuable'],
                'causes': ['satisfaction', 'achievement', 'growth'],
                'part_of': ['human_nature', 'intelligence']
            },
            'concept': {
                'related_to': ['idea', 'notion', 'thought', 'understanding'],
                'is_a': ['mental_representation', 'cognitive_unit'],
                'used_for': ['communication', 'reasoning', 'learning'],
                'has_property': ['abstract', 'meaningful', 'connected'],
                'causes': ['knowledge', 'insight', 'comprehension'],
                'part_of': ['mind', 'knowledge_base']
            },
            'semantic': {
                'related_to': ['meaning', 'significance', 'interpretation'],
                'is_a': ['linguistic_concept', 'cognitive_process'],
                'used_for': ['understanding', 'communication', 'analysis'],
                'has_property': ['contextual', 'relational', 'dynamic'],
                'causes': ['clarity', 'understanding', 'connection'],
                'part_of': ['language', 'cognition']
            }
        }

        self.writing_concepts_cache.update(fallback_knowledge)
        logger.info("使用本地备用知识库")

    def _get_fallback_relations(self, concept: str) -> dict:
        """获取概念的备用关系"""
        return {
            'related_to': [f"{concept}_related"],
            'is_a': ['concept'],
            'used_for': ['understanding'],
            'has_property': ['meaningful'],
            'causes': ['insight'],
            'part_of': ['knowledge']
        }

    def get_concept_relations(self, concept: str) -> dict:
        """获取概念的关系网络"""
        if concept in self.writing_concepts_cache:
            return self.writing_concepts_cache[concept]

        # 尝试找到相似概念
        similar_concepts = [k for k in self.writing_concepts_cache.keys()
                          if concept.lower() in k.lower() or k.lower() in concept.lower()]

        if similar_concepts:
            return self.writing_concepts_cache[similar_concepts[0]]

        return self._get_fallback_relations(concept)

    def enhance_prompt_with_knowledge(self, base_prompt: str, context_concepts: list) -> str:
        """使用知识图谱增强提示内容"""
        try:
            enhanced_elements = []

            for concept in context_concepts[:3]:  # 限制概念数量避免过载
                relations = self.get_concept_relations(concept)

                # 添加相关概念启发
                if relations['related_to']:
                    related = relations['related_to'][:2]  # 取前2个相关概念
                    enhanced_elements.append(f"联想{concept}时，可以考虑: {', '.join(related)}")

                # 添加用途建议
                if relations['used_for']:
                    purposes = relations['used_for'][:2]
                    enhanced_elements.append(f"{concept}可用于: {', '.join(purposes)}")

            if enhanced_elements:
                enhanced_prompt = base_prompt + "\n\n知识图谱启发:\n" + "\n".join(enhanced_elements)
                return enhanced_prompt

        except Exception as e:
            logger.warning(f"知识图谱增强失败: {e}")

        return base_prompt


class EnhancedSemanticExpander:
    """增强版语义扩展器 - 集成知识图谱"""

    def __init__(self):
        # 配置OpenAI
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://tbnx.plus7.plus/v1')
        self.model = os.getenv('OPENAI_MODEL', 'deepseek-chat')

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        openai.api_key = self.api_key
        openai.api_base = self.base_url

        # 初始化知识图谱
        self.kg = ConceptNetKnowledgeGraph()

        # 缓存已初始化的标记
        self._initialized = False

        logger.info(f"🔧 API配置: {self.base_url}, 模型: {self.model}")

    async def _ensure_initialized(self):
        """确保知识图谱已初始化"""
        if not self._initialized:
            await self.kg.initialize()
            self._initialized = True

    def generate_semantic_concepts(self, parent_concept: str, target_count: int = 8) -> List[Dict[str, Any]]:
        """生成语义相关概念 - 同步版本用于兼容性"""
        # 创建事件循环并运行异步方法
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环已在运行，创建新任务
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._generate_semantic_concepts_async(parent_concept, target_count))
                    return future.result()
            else:
                return loop.run_until_complete(self._generate_semantic_concepts_async(parent_concept, target_count))
        except RuntimeError:
            # 没有事件循环，创建新的
            return asyncio.run(self._generate_semantic_concepts_async(parent_concept, target_count))

    async def _generate_semantic_concepts_async(self, parent_concept: str, target_count: int = 8) -> List[Dict[str, Any]]:
        """异步生成语义相关概念"""
        await self._ensure_initialized()

        # 使用知识图谱增强的提示词
        relations = self.kg.get_concept_relations(parent_concept.lower())
        context_concepts = [parent_concept]
        if relations['related_to']:
            context_concepts.extend(relations['related_to'][:2])

        base_prompt = f"""你是一个语义概念扩展专家。根据给定的核心概念，生成{target_count}个语义相关的概念词汇。

要求：
1. 生成的概念应该在语义上与核心概念紧密相关
2. 按照相关性强度降序排列
3. 每个概念都应该是简洁的词汇或短语
4. 涵盖不同的语义维度（如类别、属性、功能、关联等）

输出格式：只返回概念列表，每行一个，不需要编号：
概念1
概念2
概念3
..."""

        enhanced_prompt = self.kg.enhance_prompt_with_knowledge(base_prompt, context_concepts)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的语义分析专家，擅长概念关联和词汇扩展。"},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            concepts_text = response.choices[0].message.content.strip()
            concept_lines = [line.strip() for line in concepts_text.split('\n') if line.strip()]

            # 转换为字典格式，添加权重
            concepts = []
            for i, concept in enumerate(concept_lines[:target_count]):
                # 基于位置和知识图谱关系计算权重
                base_weight = 1.0 - (i * 0.1)  # 位置权重递减

                # 知识图谱增强权重
                kg_boost = 0.0
                if concept.lower() in relations['related_to']:
                    kg_boost = 0.2
                elif any(rel in concept.lower() for rel in relations['used_for']):
                    kg_boost = 0.1

                weight = min(1.0, base_weight + kg_boost)

                concepts.append({
                    "name": concept,
                    "weight": round(weight, 3),
                    "source": "enhanced_kg" if kg_boost > 0 else "ai_generated",
                    "relations": relations
                })

            return concepts

        except Exception as e:
            logger.error(f"AI生成概念失败: {e}")
            # 返回基础概念作为fallback
            return [
                {"name": f"{parent_concept}相关{i+1}", "weight": 0.8 - i*0.1, "source": "fallback", "relations": {}}
                for i in range(min(target_count, 5))
            ]


# 全局实例
expander = EnhancedSemanticExpander()


class VercelEnhancedExpander:
    """增强版Vercel语义扩展器"""

    def __init__(self):
        self.expander = expander

    def generate_response(self, parent_concept: str, target_count: int = 8) -> Dict[str, Any]:
        """生成扩展响应"""
        try:
            concepts = self.expander.generate_semantic_concepts(parent_concept, target_count)

            return {
                "success": True,
                "data": {
                    "parent_concept": parent_concept,
                    "concepts": concepts,
                    "total_count": len(concepts),
                    "enhanced_features": ["knowledge_graph", "semantic_weighting", "relation_analysis"]
                }
            }

        except Exception as e:
            logger.error(f"扩展失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": {
                    "parent_concept": parent_concept,
                    "concepts": [],
                    "total_count": 0
                }
            }


# Vercel handler
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            # 提取参数
            parent_concept = request_data.get('concept', '')
            target_count = request_data.get('count', 8)

            if not parent_concept:
                self._send_error("Missing 'concept' parameter")
                return

            # 生成响应
            expander = VercelEnhancedExpander()
            response_data = expander.generate_response(parent_concept, target_count)

            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

        except json.JSONDecodeError:
            self._send_error("Invalid JSON format")
        except Exception as e:
            logger.error(f"Request handling error: {e}")
            self._send_error(f"Internal server error: {str(e)}")

    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send_error(self, message: str, status_code: int = 400):
        """发送错误响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        error_response = {
            "success": False,
            "error": message
        }
        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))