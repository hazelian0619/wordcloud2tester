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
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://tok.fan/v1')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-5.5')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # 配置OpenAI客户端（openai==0.28 使用 api_base）
        openai.api_key = self.api_key
        openai.api_base = self.base_url
        
        print(f"🔧 API配置: {self.base_url}, 模型: {self.model}")
    
    def generate_semantic_concepts(self, parent_concept: str, target_count: int = 8) -> List[Dict[str, Any]]:
        """生成语义相关概念"""
        
        # 优化的提示词 - 专注于语义扩展，并让模型自行评估语义相关强度
        system_prompt = f"""你是一个语义概念扩展专家。根据给定的核心概念，生成{target_count}个语义相关的概念词汇，并为每个概念评估它与核心概念的“语义相关强度”。

要求：
1. 生成的概念应该在语义上与核心概念相关，但要覆盖不同的语义维度（类别、属性、功能、文化关联、对立面等），不要只给近义词
2. 语义相关强度是一个 0.00–1.00 的小数：1.00 表示几乎等价/核心关联，越低表示越是外围、跨界、意外的联想
3. 强度要真实反映你的判断，允许出现并列或非线性的分布，不要机械地按名次递减
4. 每个概念都应该是简洁的词汇或短语（不超过10个字）

输出格式：严格每行一个，用竖线分隔概念和强度，不要编号、不要多余说明：
概念|强度
例如：
相对论|0.95
平行宇宙|0.82
永恒|0.61
..."""

        user_prompt = f"核心概念：{parent_concept}"

        try:
            print(f"🚀 调用API生成概念: {parent_concept}")
            content = self._chat(system_prompt, user_prompt)
            print(f"📝 API响应: {content}")
            path = [{"concept": parent_concept, "weight": 1.0}]
            concepts = self._parse_concepts(content, target_count, path)
            if not concepts:
                print(f"❌ 没有生成任何概念，原始响应: {content}")
                raise ValueError(f"No concepts generated from API response: {content}")
            print(f"✅ 成功生成 {len(concepts)} 个概念: {[c['name'] for c in concepts]}")
            return concepts
        except Exception as e:
            print(f"❌ API调用失败: {type(e).__name__}: {e}")
            # 直接抛出异常，不使用备用数据
            raise e

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """统一的 API 调用，含网关参数三级降级。返回 content 文本。
        该网关把 gpt-5 系列转发到 Responses API，只接受 max_completion_tokens，
        拒绝旧 SDK 默认的 max_tokens；逐级降级保证不同网关都能跑通。"""
        base_args = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.9,
            "timeout": 30,
        }
        last_err = None
        for extra in ({"max_completion_tokens": 800}, {"max_tokens": 800}, {}):
            try:
                resp = openai.ChatCompletion.create(**base_args, **extra)
                return resp.choices[0].message.content.strip()
            except Exception as call_err:
                last_err = call_err
                msg = str(call_err).lower()
                if "token" in msg or "unsupported parameter" in msg or "unexpected" in msg:
                    print(f"⚠️  参数不兼容，降级重试: {call_err}")
                    continue
                raise
        raise last_err

    def _parse_concepts(self, content: str, target_count: int, path: list) -> List[Dict[str, Any]]:
        """解析 '概念|权重' 文本为 concept dict 列表。"""
        concepts = []
        lines = [l for l in content.split("\n") if l.strip()]
        for i, line in enumerate(lines[:target_count]):
            raw = re.sub(r'^\d+[\.\)]\s*', '', line).strip()
            concept, model_weight = raw, None
            if '|' in raw:
                parts = raw.split('|')
                concept = parts[0].strip()
                try:
                    model_weight = float(re.sub(r'[^0-9.]', '', parts[1]))
                except (ValueError, IndexError):
                    model_weight = None
            concept = concept.strip().strip('"“”\'')
            if not concept:
                continue
            if model_weight is not None and 0 < model_weight <= 1.0:
                weight, src = model_weight, "model"
            else:
                weight, src = max(0.95 - (i * 0.05), 0.3), "rank"
            concepts.append({
                "name": concept, "weight": round(weight, 3), "weight_source": src,
                "total_path_weight": 1.0, "weighted_influence": 1.0,
                "individual_influences": [1.0], "full_semantic_path": path,
            })
        return concepts

    def generate_intersection_concepts(self, concept_a: str, concept_b: str,
                                       target_count: int = 8) -> List[Dict[str, Any]]:
        """双概念交集涌现：找同时活在两个概念里的意外第三者。"""
        system_prompt = f"""你是一位资深创意总监。给你两个概念，你要找出 {target_count} 个「**同时活在这两个概念交叉处**」的意外形象。

铁律：
1. 每个结果必须**同时咬住两个概念**——既有第一个的气质，又有第二个的气质，缺一不可。只沾一个的直接淘汰。
2. **优先输出神话、文化、历史、现实中已经存在的独立形象**——它本身就是一个大家能认出的名字或事物，恰好同时满足两个概念。例如「龙 × 少女」应优先给出：美杜莎、哪吒、小龙女、玛琳菲森、九头蛇、娜迦；而不是「龙女祭司」「驯龙歌姬」这种把两个词拼起来新造的合成词。
3. 至少前 {max(target_count // 2, 3)} 个必须是这种「已存在的独立形象」。剩下的名额，才允许出现有质感、有画面的合成意象。
4. 追求「大多数人第一反应想不到、但一说就拍案叫绝」的第三者。
5. 每个简洁（不超过10个字），能被创意人直接拿去用。

权重 0.00–1.00 = 这个第三者的「惊喜度 × 可用性」，越意外又越精准越高。已存在的独立形象通常应比合成词权重更高。

输出格式：严格每行一个，竖线分隔，不要编号、不要解释：
概念|权重
例如（龙 × 少女）：
美杜莎|0.93
小龙女|0.88
哪吒|0.85
玛琳菲森|0.82
..."""
        user_prompt = f"两个概念：{concept_a}、{concept_b}"
        print(f"🔀 交集涌现: {concept_a} × {concept_b}")
        content = self._chat(system_prompt, user_prompt)
        print(f"📝 交集响应: {content}")
        path = [{"concept": concept_a, "weight": 1.0}, {"concept": concept_b, "weight": 1.0}]
        concepts = self._parse_concepts(content, target_count, path)
        if not concepts:
            raise ValueError(f"No intersection concepts generated: {content}")
        print(f"✅ 交集生成 {len(concepts)} 个: {[c['name'] for c in concepts]}")
        return concepts

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
            concept_pair = data.get('concept_pair', [])

            # 交集涌现分支：给两个概念，求它们之间的意外第三者
            if concept_pair and len(concept_pair) == 2:
                print(f"🔀 交集请求: {concept_pair}")
                concepts = gat_expander.generate_intersection_concepts(
                    concept_pair[0], concept_pair[1], target_count)
                source_path = [{"concept": concept_pair[0], "weight": 1.0},
                               {"concept": concept_pair[1], "weight": 1.0}]
                response = {
                    "success": True,
                    "data": {
                        "concepts": concepts,
                        "method": "Intersection Emergence",
                        "source_path": source_path,
                        "expansion_level": 1
                    }
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._set_cors()
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            if not current_concept:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self._set_cors()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Missing 'current_concept' or 'concept_pair' parameter"
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