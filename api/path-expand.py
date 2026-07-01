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
        
        # 优化的提示词 - 专注于语义扩展，并让模型自行评估语义相关强度
        system_prompt = f"""你是一位资深创意总监，专门为广告、设计、写作寻找「意外但精准」的灵感锚点。

给你一个核心概念，你要产出 {target_count} 个概念，但**不是找近义词或相关词**——那些谁都想得到，毫无价值。你要找的是：**同时活在这个核心概念的气质里、却是大多数人第一反应绝对想不到的意外形象**。

铁律：
1. 拒绝同义词、上下位词、教科书目录词。（如核心词「时空」，禁止输出「时间/空间/维度/相对论/黑洞」这类物理课本词；如「孤独」，禁止「寂静/疏离/陪伴」这类同义抽象词。）
2. 追求跨领域、跨文化的意外联想：一个历史人物、一个具体画面、一个自然意象、一个对立面、一种通感……让 {target_count} 个结果散布在不同维度，不要挤在一个角落。
3. 每个概念都必须能勾起一个**具体的形象或画面**，能被创意人直接拿去用，而不是抽象大词。
4. 每个概念简洁（不超过10个字）。

权重是 0.00–1.00 的小数，代表这个概念的「**惊喜度 × 可用性**」：越是意外又精准、越能让人眼前一亮的，分越高；越平庸、越显而易见的，分越低。**不要**给最像核心词的词高分。

输出格式：严格每行一个，竖线分隔概念和权重，不要编号、不要解释：
概念|权重
例如（核心词「孤独」）：
灯塔看守人|0.94
最后一班地铁|0.88
备用钥匙|0.79
..."""

        user_prompt = f"核心概念：{parent_concept}"
        
        try:
            print(f"🚀 调用API生成概念: {parent_concept}")
            print(f"🔧 API配置: {self.base_url}, 模型: {self.model}")

            # 该网关把 gpt-5 系列转发到 Responses API，只接受 max_completion_tokens，
            # 拒绝旧 SDK 默认的 max_tokens。这里逐级降级，保证不同网关都能跑通。
            base_args = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "timeout": 30,
            }
            response = None
            last_err = None
            for extra in ({"max_completion_tokens": 800}, {"max_tokens": 800}, {}):
                try:
                    response = openai.ChatCompletion.create(**base_args, **extra)
                    break
                except Exception as call_err:
                    last_err = call_err
                    msg = str(call_err).lower()
                    # 仅在“参数不被支持”这类错误时才降级重试，其它错误直接抛出
                    if "token" in msg or "unsupported parameter" in msg or "unexpected" in msg:
                        print(f"⚠️  参数不兼容，降级重试: {call_err}")
                        continue
                    raise
            if response is None:
                raise last_err

            content = response.choices[0].message.content.strip()
            print(f"📝 API响应: {content}")
            print(f"📊 响应长度: {len(content)} 字符")
            
            # 解析概念列表
            concepts = []
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            print(f"📋 解析到 {len(lines)} 行内容")
            
            for i, line in enumerate(lines[:target_count]):
                # 解析 "概念|强度" 格式；兼容旧格式（无分隔符则回退按名次估算）
                raw = re.sub(r'^\d+[\.\)]\s*', '', line).strip()  # 移除可能的数字前缀

                concept = raw
                model_weight = None
                if '|' in raw:
                    parts = raw.split('|')
                    concept = parts[0].strip()
                    try:
                        model_weight = float(re.sub(r'[^0-9.]', '', parts[1]))
                    except (ValueError, IndexError):
                        model_weight = None

                concept = concept.strip().strip('"“”\'')
                print(f"🔍 处理第 {i+1} 行: '{line}' -> 概念='{concept}', 权重={model_weight}")

                if concept and len(concept) > 0:
                    # 优先使用模型给出的真实语义强度；缺失时才回退到按名次递减
                    if model_weight is not None and 0 < model_weight <= 1.0:
                        weight = model_weight
                    else:
                        weight = max(0.95 - (i * 0.05), 0.3)

                    concepts.append({
                        "name": concept,
                        "weight": round(weight, 3),
                        "weight_source": "model" if model_weight is not None else "rank",
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