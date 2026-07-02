# WordCloud Emergence

**Between two concepts, find the third that doesn't yet exist.**

> **LLM-Powered Semantic Network Exploration** - From fuzzy intuition to precise discovery

---

## 🌟 What It Is

WordCloud Emergence is a creative tool and a way of thinking.

It won't tell you "dragon + girl = what," but unfolds a fuzzy territory where concepts converge:
Medusa, Xiaolongnü, Maleficent, Jade Fox...

At the intersections of these neighbors, you'll find the answer that belongs only to you.

---

## 💡 Why It Exists

### Two Scenes

**Scene One: The Classroom**

A student asks: "What is justice?"

A good teacher doesn't answer directly. She says: "There's a story about a watchman..."

The student begins to explore: guard duty, responsibility, solitude, promise...
Among these fuzzy neighbors, they walk toward their own understanding of justice.

**Scene Two: The Creative Studio**

Versace, Year of the Dragon campaign.

The creative director won't simply design "a dragon with a girl."

They write on the whiteboard: **Dragon** · **Girl**

Then ask: "In all of human cultural memory, who lives in both words?"

The team begins listing fuzzy neighbors:

- **Medusa** — Snake-haired gorgon, echoing dragon's reptilian form
- **Xiaolongnü** — Cool serenity and mysterious power in Eastern wuxia
- **Maleficent** — Dark queen transforming into dragon in Sleeping Beauty
- **Jade Fox** — Rebellious soul and weapon in Crouching Tiger, Hidden Dragon
- **The Girl with the Dragon Tattoo** — Violent aesthetics and revenge in Nordic noir
- **Chihiro** — Girl growing before the white dragon god in Spirited Away
- **Nezha** — Gender-fluid dragon prince embodying rebellion and rebirth

The room goes quiet.

Creativity doesn't lie in the direct stacking of "dragon + girl," but at the intersections of these neighbors.

---

## 🧠 Core Philosophy

**Fuzziness Guides Precision** - We're not doing simple keyword matching. Through AI's "fuzzy understanding" capability, we guide users to discover precise connections between concepts. Just like human thinking: starting from fuzzy intuition, gradually crystallizing into concrete conceptual networks.

### Fuzzy Neighbors

The best answers don't lie within concepts themselves.

They exist in the spaces between, where **fuzzy neighbors** dwell.

In teaching, this is Socratic questioning—stories that spark deeper thought.

In creativity, this is concept topology—surprises found at intersections.

### Emergence

"Dragon + Girl" stacked together is dull.

But create distance, and something else appears between.

Medusa brings serpentine danger.
Xiaolongnü brings Eastern serenity.
Maleficent brings the possibility of transformation.
Jade Fox brings rebellious tension.

Students reach their own understanding here.
Creatives find unexpected connections here.
Writers see images that don't yet exist here.

**This is emergence.**

---

## 🎯 How It Works

### Creative Process

**Step 1: Extract Core Concepts**

`Dragon` + `Girl`

**Step 2: Expand Neighbors in Knowledge Graph**

What connects both dragon and feminine?

- **Medusa** — Gorgon with serpentine hair, echoing reptilian forms
- **Xiaolongnü** — Cool serenity and mysterious power in Eastern wuxia
- **Maleficent** — Dark queen transforming into dragon in Sleeping Beauty
- **Jade Fox** — Rebellious soul and weapon in Crouching Tiger, Hidden Dragon
- **The Girl with the Dragon Tattoo** — Violent aesthetics and revenge in Nordic noir
- **Chihiro** — Girl growing before the white dragon god
- **Nezha** — Gender-fluid dragon prince, rebellion and rebirth

**Step 3: Find Unique Creativity at Intersections**

These fuzzy neighbors are where true inspiration lives.

---

## ⚙️ Technical Implementation

### Phase 1: Fuzzy Semantic Understanding
- AI receives user's fuzzy concepts
- Deep learning models understand semantic boundaries
- Generate multiple possible semantic directions

### Phase 2: Attention Weight Calculation
- Calculate attention weights for each related concept
- Weight = Semantic Similarity × Concept Importance
- Form weighted conceptual networks

### Phase 3: Precise Path Discovery
- User clicks trigger new semantic expansion
- System records complete semantic paths
- From fuzzy starting point to precise destination

---

## 🛠️ Technology Stack

### Backend (Python)
- **Runtime**: Vercel Python Serverless Function (stdlib `http.server` handler, no heavy framework)
- **AI/ML**: OpenAI-compatible LLM API (prompt-engineered semantic expansion; the model self-assigns each concept a 0–1 relatedness weight)
- **APIs**: single `POST /api/path-expand` endpoint for concept expansion

### Frontend (JavaScript)
- **Visualization**: D3.js v7 force-directed graph + word cloud (incremental rendering — expanding a node grows new nodes without redrawing/re-zooming the whole graph)
- **UI**: Vanilla JS with modern CSS, single self-contained `index.html`
- **Internationalization**: built-in zh / en i18n
- **Responsive**: Mobile-friendly design

### Infrastructure
- **Deployment**: Vercel (static frontend + Python serverless function, configured in `vercel.json`)
- **Local dev**: `dev_server.py` serves the frontend and proxies `/api/path-expand` to the function handler
- **Config**: API key & model via environment variables (`OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`)

---

## ✨ Core Features

- 🧠 **Fuzzy Semantic Understanding** - AI's "fuzzy understanding," not exact matching
- ⚡ **Attention Weights** - Concept importance visualized through weights
- 🔄 **Path Tracking** - Record complete journey from fuzzy to precise
- 📊 **Dynamic Layout** - Weight-based force-directed graph layout
- 🎯 **Spotlight Mode** - Focus on current exploration path

---

## 🚀 Try It Online

**[Experience Now →](https://wordcloud2tester.vercel.app/)**

---

## 🎯 Technical Demonstrations

### Space-Time Exploration
**Input**: `Space-Time`

**Fuzzy Understanding**: time, space, dimension, relativity, travel, parallel universe, quantum, eternity

**Attention Weight Analysis**:
- Relativity (0.95) - Core physics theory
- Dimension (0.90) - Spatial concept
- Travel (0.85) - Sci-fi imagination
- Parallel Universe (0.82) - Theoretical physics
- Quantum (0.80) - Microscopic world

**Precise Path Discovery**:
```
Space-Time → Relativity → Einstein → E=mc²
Space-Time → Dimension → 4D Space → Spacetime Curvature
```

---

## 📁 Project Structure

```
wordcloud2tester/
├── api/
│   └── path-expand.py       # Vercel Python serverless function (LLM semantic expansion)
├── frontend/
│   ├── index.html           # Self-contained UI: D3 graph + all app JS
│   └── i18n-translations.js  # zh / en strings
├── dev_server.py            # Local dev server (serves frontend + proxies /api)
├── vercel.json              # Vercel build & routing config
├── requirements.txt         # Runtime deps (openai, python-dotenv)
├── tests/                   # Engine smoke tests
├── docs/                    # Detailed docs & deploy guide
└── README.md                # This file
```

---

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8+
- An OpenAI-compatible API key

### Installation & Local Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/hazelian0619/wordcloud2tester.git
   cd wordcloud2tester
   ```

2. **Install dependencies**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the API** — create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your-key-here
   OPENAI_BASE_URL=https://api.openai.com/v1   # or any OpenAI-compatible gateway
   OPENAI_MODEL=gpt-4o-mini                    # any chat model the gateway supports
   ```
   > `.env` is git-ignored — your key is never committed.

4. **Run locally** — one command serves both frontend and the API:
   ```bash
   python dev_server.py
   # Visit http://localhost:8000
   ```
   `dev_server.py` serves `frontend/index.html` and proxies `POST /api/path-expand`
   to the same handler Vercel runs in production.

### Deployment (Vercel)

This project is **not** a static-only site — it needs the Python function, so
GitHub Pages will not work. Deploy on Vercel:

1. Push this repo to GitHub.
2. On [vercel.com](https://vercel.com), "Add New Project" → import this GitHub repo.
3. In the project's **Settings → Environment Variables**, add
   `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`.
4. Deploy. Vercel reads `vercel.json` and hosts the static frontend + Python
   function together, giving you a public `*.vercel.app` link.

> ⚠️ **Cost note:** the `/api/path-expand` endpoint is public and unauthenticated.
> Anyone with your deployed link can trigger LLM calls billed to your key.
> Add rate-limiting or access control before sharing widely.

---

## 🤝 Contributing

This project incorporates elements from the Creative-Writing repository (https://github.com/hazelian0619/Creative-Writing) to enhance functionality, particularly in API architecture, visualization techniques, and deployment practices.

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see LICENSE file for details
