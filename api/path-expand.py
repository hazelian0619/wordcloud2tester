#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless API for GAT semantic expansion
基于Graph Attention Network的语义扩展云函数
"""

import json
import os
import openai
from typing import List, Dict, Any
import re
from http.server import BaseHTTPRequestHandler

class VercelGATExpander:
    """优化的GAT语义扩展器 - 适配Vercel云函数"""
    
    def __init__(self):
        # 使用环境变量配置API
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://tbnx.plus7.plus/v1')
        self.model = os.getenv('OPENAI_MODEL', 'deepseek-chat')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # 配置OpenAI客户端（openai==0.28 使用 api_base）
        openai.api_key = self.api_key
        openai.api_base = self.base_url
        
        print(f"🔧 API配置: {self.base_url}, 模型: {self.model}")
    
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
            print(f"🚀 调用API生成概念: {parent_concept}")
            print(f"🔧 API配置: {self.base_url}, 模型: {self.model}")
            
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
            print(f"📝 API响应: {content}")
            print(f"📊 响应长度: {len(content)} 字符")
            
            # 解析概念列表
            concepts = []
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            print(f"📋 解析到 {len(lines)} 行内容")
            
            for i, line in enumerate(lines[:target_count]):
                # 清理概念文本
                concept = re.sub(r'^\d+[\.\)]\s*', '', line)  # 移除数字前缀
                concept = concept.strip()
                print(f"🔍 处理第 {i+1} 行: '{line}' -> '{concept}'")
                
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
            
            if not concepts:
                print(f"❌ 没有生成任何概念，原始响应: {content}")
                raise ValueError(f"No concepts generated from API response: {content}")
            
            print(f"✅ 成功生成 {len(concepts)} 个概念: {[c['name'] for c in concepts]}")
            return concepts
            
        except Exception as e:
            print(f"❌ API调用失败: {type(e).__name__}: {e}")
            print(f"🔍 错误详情: {str(e)}")
            # 直接抛出异常，不使用备用数据
            raise e

# 初始化扩展器
try:
    gat_expander = VercelGATExpander()
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    gat_expander = None

class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless handler using BaseHTTPRequestHandler"""

    def _set_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._set_cors()
        self.end_headers()
        import json
        response = {"status": "success", "message": "path-expand API is working", "method": "GET"}
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_POST(self):
        try:
            if gat_expander is None:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._set_cors()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "API service not initialized"
                }, ensure_ascii=False).encode('utf-8'))
                return

            content_length = int(self.headers.get('Content-Length', '0'))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(raw_body.decode('utf-8') or '{}')
            except Exception:
                data = {}

            current_concept = data.get('current_concept', '')
            semantic_path = data.get('semantic_path', [])
            target_count = data.get('target_count', 8)

            if not current_concept:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self._set_cors()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Missing 'current_concept' parameter"
                }, ensure_ascii=False).encode('utf-8'))
                return

            print(f"🧠 Vercel GAT API请求: {current_concept}")
            concepts = gat_expander.generate_semantic_concepts(
                parent_concept=current_concept,
                target_count=target_count
            )

            response = {
                "success": True,
                "data": {
                    "concepts": concepts,
                    "method": "GAT Complete Path Expansion",
                    "source_path": [{"concept": current_concept, "weight": 1.0}],
                    "expansion_level": len(semantic_path) if semantic_path else 1
                }
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            print(f"❌ 服务器错误: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "error": f"Server error: {str(e)}"
            }, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    # 本地测试
    print("🧪 本地测试模式")
    try:
        gat_expander = VercelGATExpander()
        concepts = gat_expander.generate_semantic_concepts("测试概念", 5)
        print(f"✅ 测试成功，生成概念: {concepts}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")