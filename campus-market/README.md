# 校园二手交易与智能估价平台

一款面向校园场景的二手交易 + 智能估价全栈应用。用户上传 1–3 张商品照片，本地大模型自动识别**分类、成色、价格区间、标签与文案**，微调后一键发布；买家在首页按分类 / 关键词检索，查看详情并一键复制卖家联系方式；卖家可标记已售 / 下架；管理员负责敏感词与违规图片的审核管控。

## ✨ 功能特性

- **AI 智能发布**：上传照片 → 本地 Ollama 多模态大模型识别分类 / 成色 / 估价 / 标签 / 文案 → 用户编辑确认 → 写库发布
- **首页商品流**：卡片网格 + 分类 Tab 过滤 + 关键词搜索 + 分页；已售 / 下架卡片自动变灰
- **详情页**：多图预览、AI 成色标签、一键复制联系方式
- **状态流转**：在售 → 已售 / 已下架
- **合规管控**：敏感词 + 违规图片审核，命中自动进入待审核状态，由管理员通过 / 下架 / 删除
- **账号体系**：JWT 登录注册 + 个人中心 + 管理员后台

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3（组合式 API）+ Vite + Vue Router + Pinia + axios + Tailwind CSS v4 |
| 后端 | FastAPI + Uvicorn + SQLAlchemy 2.0 + Pydantic |
| 数据库 | SQLite |
| AI | 本地 Ollama `qwen3.5:4b`（视觉多模态，OpenAI 兼容接口） |
| 鉴权 | PyJWT + bcrypt |

## 📁 项目结构

```
campus-market/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── main.py         # 应用入口（CORS、静态文件、启动 seed admin）
│   │   ├── config.py       # pydantic-settings 配置（读取 .env）
│   │   ├── database.py     # SQLAlchemy 引擎 / Session
│   │   ├── models.py       # users / listings 表模型
│   │   ├── schemas.py      # Pydantic 请求 / 响应模型
│   │   ├── security.py     # bcrypt 哈希 + JWT 生成 / 校验
│   │   ├── deps.py         # 当前用户 / 管理员依赖
│   │   ├── ai.py           # 本地 Ollama 多模态估价 + JSON 解析
│   │   ├── moderation.py   # 敏感词 + 违规图片审核
│   │   └── routers/
│   │       ├── auth.py     # 注册 / 登录 / me
│   │       ├── listings.py # 分析 / 发布 / 列表 / 详情 / 状态 / 我的
│   │       └── admin.py    # 管理：审核 / 下架 / 删除
│   ├── requirements.txt
│   └── .env.example        # 环境变量示例（复制为 .env）
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── views/          # Home / Publish / ListingDetail / Login / Register / Me / Admin
│   │   ├── components/     # NavBar / ListingCard / SkeletonCard / ImageUploader / TagBadge
│   │   ├── stores/auth.js  # Pinia 鉴权状态
│   │   ├── api/index.js    # axios 实例（注入 token、统一错误 toast）
│   │   ├── router/index.js # 路由 + 登录 / 管理员守卫
│   │   └── style.css       # Tailwind v4 + 淡蓝 brand 主题
│   └── vite.config.js      # /api、/uploads 代理到后端
├── docs/                   # 需求 / 技术 / 设计 / 数据库 / API / 执行 / 测试 标准文件
├── 开发日志/               # 每日「今日完成 / 待办事项」记录
└── CLAUDE.md               # 开发指引（标准文件路径 + 工作说明）
```

## 🚀 快速开始

### 1. 准备本地大模型（Ollama）

安装 [Ollama](https://ollama.com/) 后拉取模型并保持服务运行：

```bash
ollama pull qwen3.5:4b
ollama serve          # 默认监听 http://localhost:11434
```

> 若想改用云端「通义千问 Qwen-VL」，只需在 `.env` 里把 `AI_PROVIDER=dashscope` 并填入 `DASHSCOPE_API_KEY`，无需改代码。

### 2. 启动后端

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env              # Windows；macOS/Linux 用 cp
# 编辑 .env 至少确认 OLLAMA_MODEL 与 ADMIN_PASSWORD
python -m uvicorn app.main:app --reload --port 8000
```

后端启动后会在 `http://localhost:8000/docs` 提供 Swagger 文档，并自动创建管理员账号（默认 `admin` / `admin123`，见 `.env`）。

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173
```

浏览器打开 `http://localhost:5173` 即可体验完整闭环。

## 🔐 管理员账号

| 项 | 默认值（可在 `.env` 修改） |
|----|------|
| 用户名 | `admin` |
| 密码 | `admin123` |

登录管理员账号后，导航栏会出现「管理」入口，可对待审核商品进行**通过 / 下架 / 删除**。

## 🔑 环境变量（backend/.env）

| 变量 | 说明 |
|------|------|
| `AI_PROVIDER` | `ollama`（本地，默认）或 `dashscope`（云端） |
| `OLLAMA_BASE_URL` | Ollama 服务地址，默认 `http://localhost:11434` |
| `OLLAMA_MODEL` | 模型名，默认 `qwen3.5:4b` |
| `DASHSCOPE_API_KEY` | 云端 Qwen-VL 的 Key（仅 dashscope 模式需要） |
| `ENABLE_IMAGE_MODERATION` | 是否启用图片违规审核，默认 `true` |
| `JWT_SECRET` | JWT 签名密钥（**请修改默认值**） |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | 管理员账号 |

> ⚠️ 密钥只存在于 `backend/.env`，该文件已在 `.gitignore` 中排除，**请勿提交到仓库**。

## 📌 核心接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录 |
| GET | `/api/auth/me` | 当前用户 |
| POST | `/api/ai/analyze` | 上传图片 → AI 估价（草稿，不写库） |
| POST | `/api/listings` | 发布商品（命中审核则进入 pending） |
| GET | `/api/listings` | 商品列表（分类 / 关键词 / 分页） |
| GET | `/api/listings/mine` | 我发布的商品 |
| GET | `/api/listings/{id}` | 商品详情 |
| PATCH | `/api/listings/{id}/status` | 标记已售 / 下架 |
| GET | `/api/admin/listings` | 管理端全量列表 |
| POST | `/api/admin/listings/{id}/approve` | 审核通过 |
| POST | `/api/admin/listings/{id}/delist` | 下架 |
| DELETE | `/api/admin/listings/{id}` | 删除 |

## 📚 更多文档

- 需求说明：[docs/01-需求说明.md](docs/01-需求说明.md)
- 技术选型：[docs/02-技术选型.md](docs/02-技术选型.md)
- 设计规范：[docs/03-设计规范.md](docs/03-设计规范.md)
- 数据库设计：[docs/04-数据库设计.md](docs/04-数据库设计.md)
- API 设计：[docs/05-API接口设计.md](docs/05-API接口设计.md)
- 执行步骤：[docs/06-执行步骤.md](docs/06-执行步骤.md)
- 测试验收：[docs/07-测试验收.md](docs/07-测试验收.md)
