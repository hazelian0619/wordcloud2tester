#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emergence 引擎实测：调真实 API，人工对照 Acceptance Scenario。
非断言式单测——打印结果 + 机器初筛，最终由人判定惊喜度。"""
import os, importlib.util
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
_spec = importlib.util.spec_from_file_location(
    "pe", os.path.join(os.path.dirname(__file__), "..", "api", "path-expand.py"))
pe = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(pe)

TEST_WORDS = ["时空", "孤独", "潮汕菜"]

def run():
    exp = pe.VercelGATExpander()
    for w in TEST_WORDS:
        concepts = exp.generate_semantic_concepts(w, 8)
        print(f"\n=== 核心词: {w} ===")
        for c in concepts:
            print(f"  {c['name']:<12} {c['weight']:.2f}  [{c['weight_source']}]")
        top3 = [c['name'] for c in sorted(concepts, key=lambda x: -x['weight'])[:3]]
        print(f"  权重降序前3: {top3}")

    print("\n########## 交集涌现 ##########")
    for a, b in [("龙", "少女"), ("咖啡", "雨")]:
        concepts = exp.generate_intersection_concepts(a, b, 8)
        print(f"\n=== {a} × {b} ===")
        for c in concepts:
            print(f"  {c['name']:<12} {c['weight']:.2f}")

if __name__ == "__main__":
    run()
