# Emergence Engine 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把「语义扩展器」改造成「创意人的灵感器」——引擎产出意外可用的锚点，支持双词交集涌现，惊艳结果可一键收藏。

**Architecture:** 后端 `api/path-expand.py` 重写提示词人格（创意总监）并翻转权重语义（惊喜度×可用性），新增双概念交集分支；前端 `frontend/index.html` 复用连线模式做「求涌现」，并加 localStorage 灵感卡片。分三个独立可交付的 Story，由内（引擎）而外（体验）。

**Tech Stack:** Python 3.9 + openai==0.28（旧 SDK）+ 原生 JS + D3.v7 + localStorage。API 网关 `https://tok.fan/v1`，模型 `gpt-5.4-mini`。

## Global Constraints

- API 调用必须保留 `max_completion_tokens` → `max_tokens` → 无参 的三级降级（网关拒绝 `max_tokens`），逐字保留现有逻辑，不回退。
- 权重语义 = 惊喜度 × 可用性，**不是**相似度；越像核心词分越低。
- 引擎产出「同义词/教科书目录」即判失败（宪法原则一）。
- 不引入新依赖、不装 spec-kit 脚手架、不做账号/云同步。
- 新增前端文案必须中英双语（项目已有 i18n 结构，`data-i18n` 机制）。
- 不假装存在 GAT 神经网络；保留字段名兼容前端，但注释注明是提示词工程。
- 无既有测试框架：Story 1/2 用「实测脚本 + 人工对照 Acceptance Scenario」验证；Story 3 用浏览器手动走查。每个 Story 完成后按验收标准逐条报告。

---

<!-- PLAN-BODY -->

## File Structure

- `api/path-expand.py` — 后端云函数。Task 1 改 `generate_semantic_concepts` 的提示词；Task 3 加 `generate_intersection_concepts` 方法 + `do_POST` 分支。
- `tests/test_emergence.py` — 新建。轻量实测脚本（非单测框架），调真实 API，打印结果供人工对照 Acceptance Scenario。
- `frontend/index.html` — Task 4 复用连线模式做「求涌现」；Task 5 加灵感卡片 + localStorage。
- `dev_server.py` — 已存在，本地验证用，Task 间重启。

---

## Task 0: 初始化 git（本项目当前非 git 仓库，先建仓才能提交）

**Files:** 无代码文件，仅初始化仓库。

- [ ] **Step 1: 初始化并确认 .env 被忽略**

Run:
```bash
cd /Users/pluviophile/模糊度/wordcloud2tester
git init
grep -q "^.env$" .gitignore && echo "✅ .env 已忽略" || echo ".env" >> .gitignore
git add -A && git commit -m "chore: 初始化仓库（emergence 改造起点）"
```
Expected: 提交成功，`git status` 干净；`.env` 不在追踪列表（`git ls-files | grep .env` 无输出）。

---


## Task 1: 引擎人格重写 + 权重语义翻转（Story 1）

**Files:**
- Modify: `api/path-expand.py:36-51`（`system_prompt` 定义）
- Test: `tests/test_emergence.py`（新建）

**Interfaces:**
- Consumes: 无（起点任务）
- Produces: `generate_semantic_concepts(parent_concept, target_count)` 签名不变，返回结构不变（前端兼容），仅内容质量改变。每个 concept dict 仍含 `name`/`weight`/`weight_source`/`full_semantic_path`。

- [ ] **Step 1: 写实测脚本（会失败——当前引擎出同义词）**

Create `tests/test_emergence.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emergence 引擎实测：调真实 API，人工对照 Acceptance Scenario。
非断言式单测——打印结果 + 机器初筛，最终由人判定惊喜度。"""
import os, sys, importlib.util
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
        print(f"  权重降序前3: {[c['name'] for c in sorted(concepts, key=lambda x: -x['weight'])[:3]]}")

if __name__ == "__main__":
    run()
```

- [ ] **Step 2: 跑基线，确认当前引擎出的是同义词**

Run: `.venv/bin/python tests/test_emergence.py`
Expected: 打印出「时空→时间维度/空间维度」这类教科书词——即 Acceptance Scenario 1 **失败**的基线，留作 A/B 对照。

- [ ] **Step 3: 重写 system_prompt（创意总监人格 + 惊喜权重 + 多维强制）**

Replace `api/path-expand.py:37-51` 的 `system_prompt` 赋值为：

```python
        system_prompt = f"""你是一位资深创意总监，专门为广告、设计、写作寻找「意外但精准」的灵感锚点。

给你一个核心概念，你要产出 {target_count} 个概念，但**不是找近义词或相关词**——那些谁都想得到，毫无价值。你要找的是：**同时活在这个核心概念的气质里、却是大多数人第一反应绝对想不到的意外形象**。

铁律：
1. 拒绝同义词、上下位词、教科书目录词。（如核心词「时空」，禁止输出「时间维度/空间维度/相对论」这类物理课本词。）
2. 追求跨领域、跨文化的意外联想：一个历史人物、一个具体画面、一个自然意象、一个对立面、一种通感……让 {target_count} 个结果散布在不同维度，不要挤在一个角落。
3. 每个概念都必须能勾起一个**具体的形象或画面**，能被创意人直接拿去用，而不是抽象大词。
4. 每个概念简洁（不超过10个字）。

权重是 0.00–1.00 的小数，代表这个概念的「**惊喜度 × 可用性**」：越是意外又精准、越能让人眼前一亮的，分越高；越平庸、越显而易见的，分越低。**不要**给最像核心词的词高分。

输出格式：严格每行一个，竖线分隔，不要编号、不要解释：
概念|权重
例如（核心词「孤独」）：
灯塔看守人|0.94
最后一班地铁|0.88
备用钥匙|0.79
..."""
```

- [ ] **Step 4: 重启 dev server 并重跑实测，人工对照验收标准**

Run:
```bash
pkill -f dev_server.py; sleep 1
.venv/bin/python tests/test_emergence.py
```
Expected（对照 spec Acceptance Scenario 1-4）:
- 「时空」8 个里 ≥3 个跨领域/意外（非物理课本词）
- 权重降序前 3 不是最像的同义词
- 结果散布多维度
- 每词能勾起具体画面

若不达标，回 Step 3 调提示词铁律措辞，重跑。**这是人工判定关口，不达标不进 Task 2。**

- [ ] **Step 5: Commit**

```bash
git add api/path-expand.py tests/test_emergence.py
git commit -m "feat(engine): 重写为创意总监人格，权重改为惊喜度×可用性"
```

---

## Task 2: 交集涌现后端（Story 2 · 后端分支）

**Files:**
- Modify: `api/path-expand.py`（新增 `generate_intersection_concepts` 方法，紧接 `generate_semantic_concepts` 之后，约 141 行）
- Modify: `api/path-expand.py:192-211`（`do_POST` 读参 + 分支）
- Test: `tests/test_emergence.py`（追加交集测试）

**Interfaces:**
- Consumes: Task 1 的 `VercelGATExpander` 实例与降级调用逻辑。
- Produces: `generate_intersection_concepts(concept_a: str, concept_b: str, target_count: int = 8) -> List[Dict]`，返回结构与 `generate_semantic_concepts` 完全一致（`name`/`weight`/`weight_source`/`full_semantic_path`），其中 `full_semantic_path` 为 `[{"concept": concept_a, "weight":1.0}, {"concept": concept_b, "weight":1.0}]`。`do_POST` 新增可选入参 `concept_pair: [a, b]`；存在时走交集分支。

- [ ] **Step 1: 追加交集测试到实测脚本**

在 `tests/test_emergence.py` 的 `run()` 末尾追加：

```python
    print("\n########## 交集涌现 ##########")
    for a, b in [("龙", "少女"), ("咖啡", "雨")]:
        concepts = exp.generate_intersection_concepts(a, b, 8)
        print(f"\n=== {a} × {b} ===")
        for c in concepts:
            print(f"  {c['name']:<12} {c['weight']:.2f}")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `.venv/bin/python tests/test_emergence.py`
Expected: FAIL — `AttributeError: 'VercelGATExpander' object has no attribute 'generate_intersection_concepts'`

- [ ] **Step 3: 实现交集方法**

在 `api/path-expand.py` 的 `generate_semantic_concepts` 方法 return 之后、`except` 之前不动；在类内新增方法（`generate_semantic_concepts` 整个方法结束后插入）。为复用降级调用逻辑，抽出一个私有 `_chat(system_prompt, user_prompt)`，并让两个 public 方法都用它。新增代码：

```python
    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """统一的 API 调用，含网关参数三级降级。返回 content 文本。"""
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
2. 追求「大多数人第一反应想不到、但一说就拍案叫绝」的第三者，可以是具体人物、形象、画面、意象。
3. 拒绝把两个词简单拼接（如「龙少女」），要的是真正融合后涌现的**新形象**。
4. 每个简洁（不超过10个字），能被创意人直接拿去用。

权重 0.00–1.00 = 这个第三者的「惊喜度 × 可用性」，越意外又越精准越高。

输出格式：严格每行一个，竖线分隔，不要编号、不要解释：
概念|权重
例如（龙 × 少女）：
美杜莎|0.93
小龙女|0.85
哪吒|0.72
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
```

同时把 `generate_semantic_concepts` 里 Step-1(Task 1) 之后的「调用 + 解析」段（`api/path-expand.py:55-135` 的 try 主体）改为复用 `_chat`/`_parse_concepts`，避免重复（DRY）：把 `try:` 块内从 `response = None` 到解析 for 循环结束，替换为：

```python
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
            raise e
```

- [ ] **Step 4: do_POST 加交集分支**

在 `api/path-expand.py:192-211`，把读参与调用段改为：

```python
            current_concept = data.get('current_concept', '')
            concept_pair = data.get('concept_pair', [])
            semantic_path = data.get('semantic_path', [])
            target_count = data.get('target_count', 8)

            if concept_pair and len(concept_pair) == 2:
                print(f"🔀 交集请求: {concept_pair}")
                concepts = gat_expander.generate_intersection_concepts(
                    concept_pair[0], concept_pair[1], target_count)
                source_path = [{"concept": concept_pair[0], "weight": 1.0},
                               {"concept": concept_pair[1], "weight": 1.0}]
            elif current_concept:
                print(f"🧠 Vercel GAT API请求: {current_concept}")
                concepts = gat_expander.generate_semantic_concepts(
                    parent_concept=current_concept, target_count=target_count)
                source_path = [{"concept": current_concept, "weight": 1.0}]
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self._set_cors(); self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Missing 'current_concept' or 'concept_pair'"
                }, ensure_ascii=False).encode('utf-8'))
                return
```

并把随后的 `response` 字典里 `"source_path": [...]` 改为 `"source_path": source_path`。

- [ ] **Step 5: 重启 + 跑实测，人工对照验收**

Run:
```bash
pkill -f dev_server.py; sleep 1
PORT=8787 .venv/bin/python -u dev_server.py > dev_server.log 2>&1 &
sleep 3
.venv/bin/python tests/test_emergence.py
```
Expected（对照 spec Story 2 Acceptance）:
- 「龙 × 少女」结果同时咬住两词（既有龙性又有少女性）
- ≥半数是意外形象（美杜莎/小龙女类，而非「龙女孩」拼接）
- 单词扩展（Task 1）仍正常，未被破坏

- [ ] **Step 6: Commit**

```bash
git add api/path-expand.py tests/test_emergence.py
git commit -m "feat(engine): 新增双概念交集涌现分支 + 抽取 _chat/_parse_concepts"
```

---
<!-- PLAN-NEXT -->

## Task 3: 「求涌现」前端交互（Story 2 · 前端）

**Files:**
- Modify: `frontend/index.html` — i18n 词条（约 19-95 行区）、按钮区（约 762-766 行）、连线模式逻辑（`handleConnectionClick` 约 1969 行、`toggleConnectionMode`）、节点点击路由（`handleNodeClick` 约 1945 行）

**Interfaces:**
- Consumes: Task 2 的 `POST /api/path-expand` 新增 `concept_pair: [a, b]` 入参；返回结构同单词扩展。
- Produces: 新函数 `requestEmergence(nodeA, nodeB)`：调交集 API，把第三者作为新 fuzzy 节点落在两节点中点，对两个源节点各连一条实线。新按钮 id `emergenceBtn`，新模式标志 `wordCloudData.emergenceMode`。

- [ ] **Step 1: 加 i18n 词条**

在 zh 与 en 两套 `button` 对象里各加一项：

```javascript
// zh.button 内新增
emergence: '求涌现',
// en.button 内新增
emergence: 'Find Emergence',
```

- [ ] **Step 2: 加「求涌现」按钮**

在 `frontend/index.html:766`（连线模式按钮之后）插入：

```html
                    <button class="btn btn-secondary" onclick="toggleEmergenceMode()" id="emergenceBtn" data-i18n="button.emergence">求涌现</button>
```

- [ ] **Step 3: 实现模式切换 + 双选逻辑**

在 `<script>` 内（`toggleConnectionMode` 附近）新增：

```javascript
        function toggleEmergenceMode() {
            wordCloudData.emergenceMode = !wordCloudData.emergenceMode;
            if (wordCloudData.emergenceMode) { wordCloudData.connectionMode = false; }
            firstEmergenceNode = null;
            d3.selectAll('.word-node').classed('node-connecting', false);
            document.getElementById('emergenceBtn').classList.toggle('active', wordCloudData.emergenceMode);
            updateDebugInfo(wordCloudData.emergenceMode
                ? '✨ 涌现模式：请依次点击两个概念，撞出它们之间的第三者'
                : '涌现模式已关闭');
        }

        let firstEmergenceNode = null;
        function handleEmergenceClick(node) {
            if (!firstEmergenceNode) {
                firstEmergenceNode = node;
                d3.select(event.target).classed('node-connecting', true);
                updateDebugInfo(`✨ 已选第一个：${node.name}，再点一个概念`);
            } else if (firstEmergenceNode.id === node.id) {
                firstEmergenceNode = null;
                d3.selectAll('.word-node').classed('node-connecting', false);
                updateDebugInfo('✨ 已取消');
            } else {
                requestEmergence(firstEmergenceNode, node);
                firstEmergenceNode = null;
                d3.selectAll('.word-node').classed('node-connecting', false);
            }
        }
```

- [ ] **Step 4: 在 handleNodeClick 里路由到涌现模式**

在 `frontend/index.html:1948`（`if (wordCloudData.connectionMode)` 判断之前）插入：

```javascript
            if (wordCloudData.emergenceMode) {
                handleEmergenceClick(d);
                return;
            }
```

- [ ] **Step 5: 实现 requestEmergence（调交集 API + 落节点 + 加载态）**

在 `<script>` 内新增（加载提示顺带解决 spec 4.4「点击后数秒无反馈」）：

```javascript
        async function requestEmergence(nodeA, nodeB) {
            updateDebugInfo(`✨ 正在 ${nodeA.name} × ${nodeB.name} 交叉处寻找涌现物…`);
            try {
                const resp = await fetch('/api/path-expand', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ concept_pair: [nodeA.name, nodeB.name], target_count: 8 })
                });
                const result = await resp.json();
                if (!result.success) { updateDebugInfo(`❌ 涌现失败: ${result.error}`); return; }
                const midX = (nodeA.x + nodeB.x) / 2, midY = (nodeA.y + nodeB.y) / 2;
                result.data.concepts.forEach((concept, idx) => {
                    const angle = (idx / result.data.concepts.length) * 2 * Math.PI;
                    const newNode = {
                        id: `emrg_${Date.now()}_${idx}`, name: concept.name, type: 'fuzzy',
                        weight: concept.weight, source: 'emergence',
                        semanticPath: [nodeA.name, nodeB.name, concept.name], pathDepth: 3,
                        x: midX + Math.cos(angle) * 80, y: midY + Math.sin(angle) * 80
                    };
                    wordCloudData.nodes.push(newNode);
                    createSemanticLink(nodeA, newNode, 'solid');
                    createSemanticLink(nodeB, newNode, 'solid');
                });
                renderWordCloud(); updateStats();
                updateDebugInfo(`✨ 涌现出 ${result.data.concepts.length} 个第三者！最强：${result.data.concepts[0].name}`);
            } catch (e) {
                updateDebugInfo(`❌ 涌现请求出错: ${e.message}`);
            }
        }
```

- [ ] **Step 6: 浏览器手动走查（对照 Story 2 Acceptance）**

打开 http://localhost:8787 → 生成「龙」→ 添加核心词「少女」→ 点「求涌现」→ 依次点龙、少女。
Expected: 两词中间涌现出美杜莎/小龙女类第三者，各连实线；结果同时咬住两词；点击后有加载提示。

- [ ] **Step 7: Commit**

```bash
git add frontend/index.html
git commit -m "feat(ui): 求涌现模式——选两概念撞出中间的第三者"
```

---

## Task 4: 灵感卡片收藏（Story 3）

**Files:**
- Modify: `frontend/index.html` — i18n 词条、节点右键/入口、新增卡片抽屉 DOM + CSS + localStorage 逻辑

**Interfaces:**
- Consumes: 现有 `wordCloudData.nodes` 节点结构（`name`/`weight`/`semanticPath`）。
- Produces: `pinDiscovery(node)` 存卡片；`renderDiscoveryDrawer()` 渲染列表；`exportDiscoveries()` 导出。localStorage key `wc_discoveries`，值为 `[{id, concept, path, note, ts}]`。

- [ ] **Step 1: 加 i18n 词条**

zh/en 各加：`pin: '钉住灵感' / 'Pin'`、`myInspiration: '我的灵感' / 'My Inspiration'`、`exportCards: '导出灵感' / 'Export'`。

- [ ] **Step 2: 加存储层（含降级）**

在 `<script>` 内新增：

```javascript
        const DISCOVERY_KEY = 'wc_discoveries';
        let discoveryMem = [];
        function loadDiscoveries() {
            try { return JSON.parse(localStorage.getItem(DISCOVERY_KEY) || '[]'); }
            catch { return discoveryMem; }
        }
        function saveDiscoveries(list) {
            discoveryMem = list;
            try { localStorage.setItem(DISCOVERY_KEY, JSON.stringify(list)); } catch {}
        }
        function pinDiscovery(node) {
            const list = loadDiscoveries();
            const path = (node.semanticPath || [node.name]).join(' → ');
            list.push({ id: `d_${Date.now()}`, concept: node.name, path, note: '', ts: Date.now() });
            saveDiscoveries(list);
            renderDiscoveryDrawer();
            updateDebugInfo(`☆ 已钉住灵感：${node.name}`);
        }
        function deleteDiscovery(id) {
            saveDiscoveries(loadDiscoveries().filter(d => d.id !== id));
            renderDiscoveryDrawer();
        }
        function updateDiscoveryNote(id, note) {
            const list = loadDiscoveries();
            const item = list.find(d => d.id === id);
            if (item) { item.note = note; saveDiscoveries(list); }
        }
```

- [ ] **Step 3: 加抽屉 DOM + CSS**

在 `frontend/index.html:803`（`wordcloudContainer` 之后）插入抽屉容器：

```html
        <div class="discovery-drawer" id="discoveryDrawer">
            <div class="discovery-header">
                <span data-i18n="button.myInspiration">我的灵感</span>
                <button class="btn-compact" onclick="exportDiscoveries()" data-i18n="button.exportCards">导出灵感</button>
            </div>
            <div class="discovery-list" id="discoveryList"></div>
        </div>
```

在 `<style>` 内加（沿用深色卡片风）：

```css
        .discovery-drawer { position: fixed; right: 16px; bottom: 16px; width: 280px;
            max-height: 50vh; overflow-y: auto; background: rgba(20,20,30,0.92);
            border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 12px;
            color: #eee; font-size: 13px; z-index: 50; }
        .discovery-header { display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 8px; font-weight: 600; }
        .discovery-card { background: rgba(255,255,255,0.06); border-radius: 8px;
            padding: 8px; margin-bottom: 8px; }
        .discovery-card .path { opacity: 0.6; font-size: 11px; margin-top: 2px; }
        .discovery-card textarea { width: 100%; background: transparent; border: none;
            color: #ccc; font-size: 12px; resize: vertical; margin-top: 4px; }
```

- [ ] **Step 4: 渲染 + 导出 + 初始化**

```javascript
        function renderDiscoveryDrawer() {
            const list = loadDiscoveries();
            const el = document.getElementById('discoveryList');
            el.innerHTML = list.map(d => `
                <div class="discovery-card">
                    <div><strong>${d.concept}</strong>
                        <span style="float:right;cursor:pointer" onclick="deleteDiscovery('${d.id}')">✕</span></div>
                    <div class="path">${d.path}</div>
                    <textarea placeholder="写下灵感注解…" onchange="updateDiscoveryNote('${d.id}', this.value)">${d.note}</textarea>
                </div>`).join('');
        }
        function exportDiscoveries() {
            const list = loadDiscoveries();
            const md = ['# 我的灵感', '', ...list.map(d =>
                `- **${d.concept}**（${d.path}）${d.note ? '：' + d.note : ''}`)].join('\n');
            const blob = new Blob([md], { type: 'text/markdown' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob); a.download = 'inspiration.md'; a.click();
            URL.revokeObjectURL(a.href);
        }
```

在 `window.onload`（约 2600 行）内追加 `renderDiscoveryDrawer();`。

- [ ] **Step 5: 节点加「钉住」入口**

在 `handleNodeClick` 里（选择模式分支内），改为双击钉住；或在节点右键菜单加入口。最小实现：节点 `dblclick` 事件绑定。在渲染节点处（约 1807 行 `.on('click', handleNodeClick)` 之后）追加：

```javascript
                .on('dblclick', (event, d) => { event.stopPropagation(); pinDiscovery(d); })
```

- [ ] **Step 6: 浏览器手动走查（对照 Story 3 Acceptance）**

生成词云 → 双击一个惊艳节点 → 抽屉出现卡片 → 写注解 → **刷新页面** → 确认卡片和注解还在 → 点「导出灵感」→ 得到 markdown 文件。

- [ ] **Step 7: Commit**

```bash
git add frontend/index.html
git commit -m "feat(ui): 灵感卡片收藏——双击钉住、注解、localStorage 持久化、导出"
```

---

## 执行顺序与关口

1. Task 0（git init）→ Task 1（引擎，**人工验收关口**，不达标不前进）→ Task 2（交集后端）→ Task 3（涌现前端）→ Task 4（灵感卡片）。
2. Story 1 是地基：Task 1 的 Acceptance 不过，后续全部暂停，回头调提示词。
3. 每个 Task 独立可交付、独立可回滚。



