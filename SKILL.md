---
name: web-to-FIM
label: 网页内容转 Markdown/飞书/IMA
slug: web-to-fim
displayName: web-to-FIM
version: 3.2.0
summary: 将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian、飞书云文档、腾讯 IMA 知识库。
license: MIT-0
description: >
  将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian Vault、飞书云文档、腾讯 IMA 知识库。
  支持的信源：(1) X/Twitter 推文、长文 Article、Thread 线程（逐字转录）；(2) 微信公众号文章（带图片，IMA 服务端抓取保留排版）；
  (3) 飞书 wiki 文档（WebFetch 全文转录）；(4) 小红书笔记；(5) 微博；(6) YouTube 视频；
  (7) 任意 HTML 网页（带图片，IMA 服务端抓取）；(8) 本地文件：PDF、Word、PPT、Excel、图片、音频等。
  三处存放：Obsidian（本地 Markdown+frontmatter+tags）+ 飞书云文档（团队协作）+ IMA 知识库（FIM知识库，AI 原生）。
  IMA 智能路由：公众号/网页 → import_urls 保留图片；X/Twitter/飞书 → 纯文本笔记逐字转录。
  批量模式支持断点恢复，Obsidian 写入失败自动 fallback。
  工作流：自动识别 URL/文件类型 → 路由到最佳抓取工具 → 结构化 Markdown → 三处存放。
  触发词：转文档、抓网页存飞书、网页转文档、web to feishu、url转文档、文件转飞书、存到ima、存到obsidian、web to fim、三处存放。
  当用户提供任意 URL 或本地文件并要求转存为文档时触发。
  Do NOT use for 创建文档内容、编辑飞书文档正文、代码开发、非文档转存任务。
---

# Web-to-FIM | 网页内容转 Markdown/飞书/IMA

## 🤖 AI 时代必备的信息库基础技能

在 AI 时代，无论是使用 **OpenClaw**、**Hermes Agent**，还是实践 **Obsidian + LLM** 的信息管理方法论，**一键入库、人机共用**的 AI 信息库搭建都是必备的基础设施。

**Web-to-FIM** 就是这样一个基础技能：它将任意网络内容一键转换为结构化 Markdown，并同步到：
- 📝 **Obsidian Vault** - 本地个人知识库，带 frontmatter
- 📚 **飞书云文档** - 云端团队协作
- 🧠 **腾讯 IMA 知识库** - AI 原生知识库（FIM知识库）

将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian Vault、飞书云文档、腾讯 IMA 知识库。

## 支持的信源

| 信源 | URL 特征 | 抓取方式 |
|------|---------|---------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher（逐字转录） |
| 微信公众号 | `mp.weixin.qq.com` | markitdown + 移动端 UA fallback |
| 飞书 wiki | `*.feishu.cn/wiki/` | WebFetch 全文转录 |
| 小红书 | `xiaohongshu.com` / `xhslink.com` | markitdown |
| 微博 | `weibo.com` | markitdown |
| YouTube | `youtube.com` / `youtu.be` | markitdown |
| 任意网页 | 其他 `http(s)://` 链接 | markitdown |

### 本地文件支持

| 类型 | 扩展名 |
|------|--------|
| PDF | `.pdf` |
| Word | `.docx` / `.doc` |
| PowerPoint | `.pptx` / `.ppt` |
| Excel | `.xlsx` / `.xls` |
| 图片 | `.png` `.jpg` `.jpeg` `.gif` `.webp` |
| 音频 | `.mp3` `.wav` `.m4a` `.flac` |
| 数据 | `.csv` `.json` `.xml` |

## 输出目的地

| 目的地 | 环境变量 | 说明 |
|--------|---------|------|
| Obsidian Vault | `OBSIDIAN_VAULT_PATH` | 本地保存到指定目录，带 frontmatter（默认：`E:\Obsidian\md\inbox`） |
| 飞书云文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | 云端服务，参考 `references/feishu-setup.md` |
| 腾讯 IMA | `IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` | **云端 API v1.1.7**，两步流程存入知识库，参考 `references/ima-setup.md` |

### Obsidian Vault 路径配置
跨平台支持，通过环境变量 `OBSIDIAN_VAULT_PATH` 配置：

```bash
# Windows (PowerShell)
$env:OBSIDIAN_VAULT_PATH = "C:\Users\YourName\Obsidian\Vault\inbox"

# Windows (CMD)
set OBSIDIAN_VAULT_PATH=C:\Users\YourName\Obsidian\Vault\inbox

# macOS/Linux
export OBSIDIAN_VAULT_PATH=~/Obsidian/Vault/inbox
```

如果未设置，默认使用：
- Windows: `E:\Obsidian\md\inbox`
- macOS/Linux: `~/Obsidian/inbox`

## 一键保存到所有目的地

使用 `web_to_all.py` 一键转换并保存到 Obsidian/飞书/IMA：

```bash
python3 scripts/web_to_all.py --url "<url_or_path>"
python3 scripts/web_to_all.py --url "<url>" --title "自定义标题"
python3 scripts/web_to_all.py --url "<url>" --no-feishu --no-ima  # 仅保存 Obsidian
```

## 安全配置

⚠️ **凭证必须通过环境变量配置**，禁止硬编码：

### 飞书配置

```bash
# 设置环境变量
$env:FEISHU_APP_ID = "your_app_id"
$env:FEISHU_APP_SECRET = "your_app_secret"
```

参考 [references/feishu-setup.md](references/feishu-setup.md) 获取凭证。

### ima 配置

```bash
# 设置环境变量（v3.0 — IMA OpenAPI v1.1.7）
$env:IMA_OPENAPI_CLIENTID = "your_client_id"
$env:IMA_OPENAPI_APIKEY = "your_api_key"

# 可选：指定知识库名称（默认 "FIM知识库"）
$env:IMA_KB_NAME = "FIM知识库"
```

> ⚠️ **v3.0 变更**：环境变量从 `IMA_CLIENT_ID`/`IMA_API_KEY` 改为 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`（旧名仍兼容回退）。IMA 存储从"笔记本"改为"知识库"两步流程。

参考 [references/ima-setup.md](references/ima-setup.md) 获取凭证。

## 工作流

### 步骤 1：转换为 Markdown

```bash
python3 scripts/web_to_md.py --url "<url_or_path>" --output <output.md>
```

路由逻辑：
- **X/Twitter** → x-tweet-fetcher 抓取 JSON → tweet_to_md.py 结构化转换（逐字转录）
- **飞书 wiki**（`*.feishu.cn/wiki/`）→ WebFetch 抓取全文 → 检查原文链接 → 有则优先抓取原文（v3.2.0）
- **公众号**（`mp.weixin.qq.com`）→ markitdown 转换，反爬时自动 fallback 到移动端 UA
- **其他网页/本地文件** → markitdown 直接转换

> **v3.2.0 飞书 wiki 原文链接优先转录**：
> - 抓取飞书 wiki 后，检查文章头部是否有"原文链接"（如 `🔗 原文链接：[url]`）
> - 有原文链接 → 优先抓取原文链接内容（公众号/X 等），获得更完整的正文和图片
> - 无原文链接 → 用飞书 wiki 内容
> - IMA 存放：有公众号原文链接 → import_urls（保留图片）；无 → 纯文本笔记

> **v3.0 新增信源支持**：
> - 飞书 wiki 文档：通过 WebFetch 转录飞书知识库文章全文
> - 公众号反爬 fallback：markitdown 返回验证页时自动切换移动端 UA 重试

> **v3.2.0 新增**：
> - Obsidian 文件命名规范化：`YYYYMMDD-标题-来源.md`（如 `20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`）
> - 来源自动提取：从 URL 域名提取来源标识（waytoagi/feishu/x/wechat/weibo/xiaohongshu/github/youtube/webpage）
> - 飞书 wiki 原文链接优先转录：抓取飞书 wiki 后检查原文链接，有则优先抓取原文内容（更完整）
> - Windows 文件名安全：禁止字符替换为下划线，中文标点（含：）保留

> **v3.1 新增**：
> - 批量模式断点恢复：崩溃后重跑自动跳过已完成 URL（`.progress.json` 进度文件）
> - Obsidian frontmatter 自动 tags：根据 URL 来源分类标签
> - 推文结构化转换通用化：去硬编码，基于启发式规则识别段落标题
> - subprocess 加 120 秒 timeout：防止网络异常永久挂起
> - 公众号正文提取改进：保留图片、段落结构、引用块

### 步骤 2：存入目的地

#### Obsidian Vault

文件名规则：`YYYYMMDD-标题-来源.md`（v3.2.0）
- 来源从 URL 自动提取（waytoagi/feishu/x/wechat 等）
- 示例：`20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`

```python
from scripts.web_to_all import save_to_obsidian
filepath = save_to_obsidian(markdown_content, title, url)
```

#### 飞书云文档

```python
from scripts.feishu_client import FeishuClient

client = FeishuClient()
result = client.create_document(title="文档标题", content_md=markdown_content)
print(f"文档 URL: {result['url']}")
```

#### 腾讯 ima（v3.0 — 知识库两步流程 + 图片保留）

IMA 有**两套独立 API**，不可混用：
- **Notes API**（`/openapi/note/v1/`）：管笔记、笔记本
- **Knowledge Base API**（`/openapi/wiki/v1/`）：管知识库、知识条目

「FIM知识库」是**知识库**（wiki API），不是笔记本（note API）。必须用两步流程。

> **v3.0 核心功能 — 公众号/网页带图片转录**：
> - 公众号和普通网页 URL 通过 `import_urls` 让 IMA 服务端抓取，**保留原文图片和排版**
> - X/Twitter 和飞书 wiki 走纯文本笔记（逐字转录），因为 X 要求逐字转录、飞书需登录认证

```python
from scripts.web_to_all import save_to_ima

# 方式1：直接用 save_to_ima（推荐，自动路由）
# - 公众号/普通网页 URL → import_urls（服务端抓取，保留图片）
# - X/Twitter/飞书 URL → 纯文本笔记（逐字转录）
result = save_to_ima(content, title, knowledge_base="FIM知识库", source_url=url)

# 方式2：手动两步流程
from scripts.ima_client import IMAClient
client = IMAClient()
# Step 1: 创建笔记（Notes API）
note = client.create_note(title="标题", content=markdown_content)
# Step 2: 添加到知识库（Wiki API）
kb_id = client.find_knowledge_base_by_name("FIM知识库")
client.add_note_to_knowledge_base(note_id=note["note_id"], title="标题", knowledge_base_id=kb_id)
```

**IMA 存放路由规则（v3.0）**：

| source_url 类型 | IMA 存放方式 | 原因 |
|----------------|------------|------|
| 公众号（`mp.weixin.qq.com`） | `import_urls`（服务端抓取） | 保留图片和排版 |
| 普通网页 | `import_urls`（服务端抓取） | 保留图片和排版 |
| **X/Twitter** | **纯文本笔记（逐字转录）** | 技能规则要求逐字转录 |
| 飞书 wiki | 纯文本笔记（逐字转录） | 需登录认证，IMA 无法抓取 |
| 无 URL | 纯文本笔记 | 手动内容/飞书转录 |

### 验证连接

```bash
# 验证飞书
python scripts/feishu_client.py --action test

# 验证 ima
python scripts/ima_client.py --action test
```

## 故障处理

| 问题 | 解决方案 |
|------|---------|
| x.com SSL 超时 | x-tweet-fetcher 使用 FxTwitter API 中转 |
| markitdown 模块丢失 | `pip install markitdown` |
| 微信反爬拦截 | markitdown 返回72字符验证页，需 fallback 到 WebFetch 或移动端 UA |
| 飞书凭证无效 | 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` |
| 飞书 blocks 400 错误 | 单次最多 50 个 blocks，长文章需分批插入（见 `references/feishu-blocks.md`） |
| 飞书 block_type 错误 | Code=14、Quote=15、Text=2、Heading1-3=3-5、Bullet=12（见 `references/feishu-blocks.md`） |
| ima 凭证无效 | 检查 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY`（v3.0） |
| IMA 笔记不在知识库中 | 知识库≠笔记本，必须用两步流程：create_note → add_knowledge |
| IMA import_urls 文件夹不存在 | folder_id 不等于 knowledge_base_id，需用 `get_root_folder_id()` 获取 |
| X 链接 IMA 存储错误 | X/Twitter 必须逐字转录（纯文本笔记），不可用 import_urls |

## 依赖与安装

### 完整依赖列表

| 依赖 | 安装命令 | 说明 |
|------|---------|------|
| markitdown | `pip install markitdown` | 网页转 Markdown 核心库 |
| requests | `pip install requests` | HTTP 请求 |
| python-dotenv | `pip install python-dotenv` | 环境变量管理 |
| x-tweet-fetcher | 克隆到 `~/.aily/workspace/skills/x-tweet-fetcher` | X/Twitter 专用抓取（可选） |

### 一键安装所有依赖

```bash
# 安装 Python 依赖
pip install markitdown requests python-dotenv
```

### x-tweet-fetcher（可选，仅用于 X/Twitter）
```bash
# 克隆到技能目录
cd ~/.aily/workspace/skills
git clone https://github.com/EdwardWason/x-tweet-fetcher.git
```

如果不安装 x-tweet-fetcher，X/Twitter 链接将使用 markitdown 直接处理。

---

## 安全声明

### 🔒 安全设计原则

1. **凭证安全**
   - 所有 API 凭证通过环境变量配置，**无硬编码**
   - 支持 `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY`（v3.0）
   - 旧变量名 `IMA_CLIENT_ID`/`IMA_API_KEY` 仍兼容回退

2. **文件操作**
   - 仅在用户明确指定时写入文件
   - Obsidian Vault 路径完全可控
   - 支持通过 `--no-feishu` / `--no-ima` 选择性禁用功能

3. **隐私保护**
   - 不读取任何未经授权的用户配置文件
   - 所有网络请求仅针对用户提供的 URL
   - 本地文件仅用于转换，不主动扫描

4. **权限透明**
   - 文件写入范围：Obsidian Vault 目录、临时 Markdown 文件
   - 文件读取范围：用户指定的 URL、本地输入文件
