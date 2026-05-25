# onamae.com RSプラン 说明与可行性评估

## 📋 文档目的与概述

本文档把对 onamae.com RSプラン（共享主机）可行性评估与产品说明合并在一处，便于决策与实施。文档包含：
- 技术规格与关键限制（说明）
- 可行性评估与部署方案对比（评估）
- 推荐替代：PaaS / 边缘平台列表
- onamae 上可选的可运行环境产品线（如何选择）

**评估日期**：2026年1月5日  
**评估对象**：onamae.com RSプラン（共享主机服务）

---

## 🔍 RSプラン（说明 — 技术规格与支持）

### 套餐对比（概要）

| 项目 | RS1 | RS2 | RS3 |
|------|-----|-----|-----|
| **月费** | ¥900-1,200 | ¥1,800-2,400 | ¥3,600-4,800 |
| **年费** | ¥10,800-14,400 | ¥21,600-28,800 | ¥43,200-57,600 |
| **磁盘空间** | 200GB | 400GB | 600GB |
| **数据库** | MySQL 1个 | MySQL 无限 | MySQL 无限 |
| **邮箱** | 无限 | 无限 | 无限 |
| **SSL证书** | 免费 | 免费 | 免费 |

### 技术支持情况（说明）

| 技术 | 支持情况 | 说明 |
|------|----------|------|
| **PHP** | ✅ 支持 | PHP 7.x/8.x，适合传统网站与 WordPress |
| **MySQL** | ✅ 支持 | 标准 MySQL（托管在同一主机） |
| **Node.js** | ❌ 不支持 | 共享主机通常不允许常驻 Node 进程 |
| **Python** | ❌ 受限 | 通常仅以 CGI/有限脚本方式支持，无法运行常驻 WSGI/ASGI 服务 |
| **静态文件** | ✅ 支持 | HTML/CSS/JS 可直接托管 |
| **FTP/SFTP** | ✅ 支持 | 手动部署/上传文件 |

---

## ⚠️ 关键技术限制（对本项目的影响，评估）

1) 无法运行常驻 Node.js 或现代 Python Web 服务（例如 Next.js SSR、FastAPI/ASGI、Django 作为长期运行进程），因此：
- ❌ 无法直接在 RSプラン 上运行 Next.js 的 Server、API Routes 或 Server Actions

2) 部署流程受限：
- ❌ 通常缺乏 Git 自动部署与 CI/CD 集成
- ⚠️ 仅能通过 FTP/SFTP 手动上传构建产物

3) 性能与可用性：
- ⚠️ 资源共享可能导致并发/性能瓶颈
- ⚠️ 不具备全球 CDN，访问延迟依赖机房位置（日本机房对中国访问可能较慢）

---

## 💡 可行性评估（建议与对比）

### 方案 A（推荐） — 现代托管（推荐等级：⭐⭐⭐⭐⭐）

架构：Next.js（Vercel）或静态前端 + Supabase 等托管服务

优点：低成本、自动部署、CDN、SSR/ISR 支持、托管数据库与 Auth

适用场景：生产网站、需要全球访问与自动扩展的项目

---

### 方案 B（在 RSプラン 上的折衷） — 静态导出 + PHP 后端

思路：将 Next.js 导出为静态站点（SSG），并把需要的 API 用 PHP 重写或通过外部 API 提供

限制：失去 SSR/ISR、手动部署、维护成本高、性能与功能受限

---

### 方案 C（混合） — 前端托管到 CDN/边缘，后端保留在 onamae

思路：前端部署到 Vercel/Netlify，后端或数据库放在 onamae（PHP/MySQL）或外部托管

优点/缺点：前端性能好，但后端仍需运维与可能面临跨域问题

---

## ✅ 结论（评估）

- 如果目标是尽量降低成本且保持现代功能（SSR/ISR、自动部署、全球访问），推荐使用 **方案 A**（Vercel + Supabase / 托管 PaaS）。
- 仅当有强烈的法规/合规或必须把所有数据放在日本且不能使用云服务时，才考虑把业务完全迁移到 RS プラン 或专用服务器（但需承担更高运维与成本）。

---

## 推荐的 PaaS / 边缘平台（便于运行 Node.js / Python / Next.js）

- **Vercel** — Next.js 官方推荐平台，内置 SSR/ISR、Edge Functions 与自动部署（Git 集成）。
- **Netlify** — 适合静态与 Jamstack，提供 Functions（Serverless）与自动部署。
- **Render** — 支持 Web 服务、后台 worker，适合运行 Node/Python 服务，部署简单。
- **Fly.io** — 边缘虚拟服务器，适合需要低延迟的全栈部署（支持 Docker、Node、Python）。
- **Railway** — 简化的 PaaS，支持快速部署 Node/Python 服务与数据库。 
- **Heroku（付费或替代）** — 传统 PaaS，适合小型生产部署（注意费用模型）。
- **Cloudflare Pages + Workers / Pages Functions** — 静态与边缘函数组合，可实现部分动态功能（Workers 有运行时限制，需要核对兼容性）。
- **Supabase** — 托管数据库 + Auth + Edge Functions，适合作为后端数据层。

选择建议：对 Next.js 优先选 Vercel；需要更底层运行环境或 Docker 支持时，选 Render、Fly 或 VPS。

---

## onamae 上支持运行环境的产品线（如何选择）

说明：`RSプラン` 是共享主机，不支持常驻 Node/Python。若想在 onamae 平台上运行 Node.js 或 Python 应用，请在 onamae 的产品线中寻找以下类型：

- **VPS（Virtual Private Server / 仮想専用サーバ）**：通常允许你安装 Node.js、Python、Docker 等，适合需要控制运行时的场景。
- **専用サーバ / Dedicated Server（物理服务器）**：完全控制，成本较高，适合高性能或合规需求。
- **クラウド / Cloud Server（若提供）**：按需分配资源，类似 VPS，支持现代运行时。

操作建议：

1. 访问 onamae 官方页面（https://www.onamae.com/），在产品目录中查找“VPS”、“レンタルサーバ（プラン分类外）”、“専用サーバ”或“クラウドサーバ”条目；
2. 查看对应产品是否说明支持自定义运行时（SSH root 访问 / apt 安装 / Docker 支持）；
3. 若找到 VPS/Cloud 产品，可在其上安装 Node.js / Python，并部署 Docker 容器或使用 PM2 / systemd 管理进程。

注意：不同产品的机房、可用性与价格差异较大，建议在购买前核实官方文档或联系 onamae 支持确认细节。

---

## 操作建议与下一步

1. 若你需要我整理一个“迁移到 Vercel+Supabase”的具体步骤清单（包括 DNS、环境变量、迁移脚本），我可以生成并添加到本仓库的 `docs/` 中；
2. 若你仍希望使用 onamae 托管，请让我在线（我可帮你检索）或你手动确认 onamae 的 VPS/云产品，之后我可以给出部署脚本（Docker/PM2）与配置建议；
3. 我已把本合并文档保存为当前文件；若需把原评估副本删除或归档，请确认。

---

## 🔗 相关资源

- [onamae.com 官方网站](https://www.onamae.com/)
- Vercel, Netlify, Render, Fly.io 各自官网（可按需补充链接）

**文档版本**：1.1  
**最后更新**：2026年5月16日  
**评估结论**：推荐使用 PaaS/边缘平台（方案 A），RSプラン 仅适合静态或 PHP 场景
