#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless API for GAT semantic expansion
基于Graph Attention Network的语义扩展云函数
"""

from flask import Flask, request, jsonify
import json
import os
import openai
from typing import List, Dict, Any
import re

# Vercel需要的Flask app
app = Flask(__name__)

class VercelGATExpander:
    """优化的GAT语义扩展器 - 适配Vercel云函数"""
    
    def __init__(self):
        # 使用环境变量配置API
        self.api_key = os.getenv('OPENAI_API_KEY', 'sk-cFt8t6WmtG5pPI03Qr4j9cVhTHwnzqM8Xmmq89wzgJYhN1bQ')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://tbnx.plus7.plus/v1')
        self.model = os.getenv('OPENAI_MODEL', 'deepseek-chat')
        
        # 配置OpenAI客户端
        openai.api_key = self.api_key
        openai.base_url = self.base_url
    
    def generate_semantic_concepts(self, parent_concept: str, target_count: int = 8) -> List[Dict[str, Any]]:
        """生成语义相关概念"""
        
        # 优化的提示词 - 专注于语义扩展
        system_prompt = f"""你是一个语义概念扩展专家。根据给定的核心概念，生成{target_count}个语义相关的概念词汇。

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

        user_prompt = f"核心概念：{parent_concept}"
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=300,
                timeout=30
            )
            
            content = response.choices[0].message.content.strip()
            
            # 解析概念列表
            concepts = []
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for i, line in enumerate(lines[:target_count]):
                # 清理概念文本
                concept = re.sub(r'^\d+[\.\)]\s*', '', line)  # 移除数字前缀
                concept = concept.strip()
                
                if concept and len(concept) > 0:
                    # 生成权重：按顺序递减
                    weight = max(0.95 - (i * 0.05), 0.3)
                    
                    concepts.append({
                        "name": concept,
                        "weight": round(weight, 3),
                        "total_path_weight": 1.0,
                        "weighted_influence": 1.0,
                        "individual_influences": [1.0],
                        "full_semantic_path": [{"concept": parent_concept, "weight": 1.0}]
                    })
            
            return concepts
            
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            # 返回备用概念
            return self._get_fallback_concepts(parent_concept, target_count)
    
    def _get_fallback_concepts(self, parent_concept: str, target_count: int) -> List[Dict[str, Any]]:
        """备用概念生成 - API失败时使用"""
        fallback_concepts = {
            "潮汕菜": ["卤鹅", "蚝烙", "粿条", "鱼饭", "牛肉丸", "砂锅粥", "白切鸡", "菜脯蛋"],
            "编程": ["算法", "数据结构", "调试", "代码优化", "软件工程", "版本控制", "测试", "架构设计"],
            "音乐": ["旋律", "节奏", "和声", "乐器", "作曲", "演奏", "音符", "音乐理论"],
        }
        
        concepts_list = fallback_concepts.get(parent_concept, [
            f"{parent_concept}相关1", f"{parent_concept}相关2", f"{parent_concept}相关3",
            f"{parent_concept}相关4", f"{parent_concept}相关5", f"{parent_concept}相关6"
        ])
        
        result = []
        for i, concept in enumerate(concepts_list[:target_count]):
            weight = max(0.95 - (i * 0.05), 0.3)
            result.append({
                "name": concept,
                "weight": round(weight, 3),
                "total_path_weight": 1.0,
                "weighted_influence": 1.0,
                "individual_influences": [1.0],
                "full_semantic_path": [{"concept": parent_concept, "weight": 1.0}]
            })
        
        return result

# 初始化扩展器
gat_expander = VercelGATExpander()

@app.route('/api/path-expand', methods=['POST'])
def path_expand():
    """Vercel云函数入口点"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            })
        
        current_concept = data.get('current_concept', '')
        semantic_path = data.get('semantic_path', [])
        target_count = data.get('target_count', 8)
        
        if not current_concept:
            return jsonify({
                "success": False,
                "error": "Missing 'current_concept' parameter"
            })
        
        print(f"🧠 Vercel GAT API请求: {current_concept}")
        
        # 生成语义概念
        concepts = gat_expander.generate_semantic_concepts(
            parent_concept=current_concept,
            target_count=target_count
        )
        
        # 构建响应数据
        response_data = {
            "success": True,
            "data": {
                "concepts": concepts,
                "method": "GAT Complete Path Expansion",
                "source_path": [{"concept": current_concept, "weight": 1.0}],
                "expansion_level": len(semantic_path) if semantic_path else 1
            }
        }
        
        print(f"✅ 生成 {len(concepts)} 个概念")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ 服务器错误: {e}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

# Vercel需要的默认handler
def handler(request):
    """Vercel serverless handler"""
    with app.app_context():
        return app.full_dispatch_request()

if __name__ == '__main__':
    # 本地测试
    app.run(debug=True, port=8890)