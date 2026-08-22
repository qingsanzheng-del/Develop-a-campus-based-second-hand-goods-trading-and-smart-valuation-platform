# API 接口设计

前缀统一 `/api`，接口文档见 `http://localhost:8000/docs`。

## 鉴权

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | /api/auth/register | 注册 `{username,password}` | 否 |
| POST | /api/auth/login | 登录 → `{token,user}` | 否 |
| GET | /api/auth/me | 当前用户 | Bearer JWT |

> 启动时自动 seed 管理员账号（`admin` / 密码取 `ADMIN_PASSWORD`，默认 `admin123`）。

## AI 发品

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | /api/ai/analyze | multipart：1–3 张图 + `description` → 结构化草稿（不写库） | 否 |
| POST | /api/listings | JSON：草稿字段 + `contact` + `images` → 合规检测后写库 | Bearer JWT |

## 前台流 / 检索

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | /api/listings | `?category=&q=&page=&page_size=` → 分页列表（active+sold） | 否 |
| GET | /api/listings/{id} | 商品详情 | 否 |

## 状态流转 / 个人中心

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| PATCH | /api/listings/{id}/status | `{status: sold|delisted}`（本人或管理员） | Bearer JWT |
| GET | /api/listings/mine | 我发布的（全状态） | Bearer JWT |

## 管理员

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | /api/admin/listings | `?status=` 全量列表（含 pending） | 管理员 |
| POST | /api/admin/listings/{id}/approve | pending → active | 管理员 |
| POST | /api/admin/listings/{id}/delist | 下架 | 管理员 |
| DELETE | /api/admin/listings/{id} | 删除 | 管理员 |

## 路由顺序注意

`/api/listings/mine` 必须先于 `/api/listings/{id}` 声明，避免 `mine` 被当作 `id` 解析。
