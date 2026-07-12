[English](./README.en.md) | 中文

# web-to-FIM

> 将任意网页链接或本地文件一键转为结构化 Markdown，并三处存放到 Obsidian Vault、飞书云文档、腾讯 IMA 知识库。

## 核心功能

### 支持的信源（7 类 URL + 本地文件）

| 信源 | URL 特征 | 抓取方式 |
|------|---------|---------|
| X/Twitter | `x.com` / `twitter.com` | x-tweet-fetcher（逐字转录） |
| 微信公众号 | `mp.weixin.qq.com` | markitdown + 移动端 UA fallback |
| 飞书 wiki | `*.feishu.cn/wiki/` | WebFetch 全文转录 |
| 小红书 | `xiaohongshu.com` / `xhslink.com` | markitdown |
| 微博 | `weibo.com` | markitdown |
| YouTube | `youtube.com` / `youtu.be` | markitdown |
| 任意网页 | 其他 `http(s)://` 链接 | markitdown |

本地文件支持：PDF、Word、PPT、Excel、图片、音频、CSV/JSON/XML 等。

### 三处存放

| 目的地 | 环境变量 | 说明 |
|--------|---------|------|
| Obsidian Vault | `OBSIDIAN_VAULT_PATH` | 本地 Markdown + frontmatter + tags |
| 飞书云文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | 云端团队协作 |
| 腾讯 IMA | `IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY` | AI 原生知识库（FIM知识库） |

## 快速开始

```bash
# Install dependencies
pip install markitdown requests python-dotenv

# Convert and save to all three destinations
python3 scripts/web_to_all.py --url "<url_or_path>"

# Convert with custom title
python3 scripts/web_to_all.py --url "<url>" --title "自定义标题"

# Save to Obsidian only
python3 scripts/web_to_all.py --url "<url>" --no-feishu --no-ima
```

## 环境变量配置

```bash
# Obsidian Vault path (optional, has default)
$env:OBSIDIAN_VAULT_PATH = "C:\Users\YourName\Obsidian\Vault\inbox"

# Feishu credentials
$env:FEISHU_APP_ID = "your_app_id"
$env:FEISHU_APP_SECRET = "your_app_secret"

# IMA credentials (v3.0 - OpenAPI v1.1.7)
$env:IMA_OPENAPI_CLIENTID = "your_client_id"
$env:IMA_OPENAPI_APIKEY = "your_api_key"

# Optional: IMA knowledge base name (default: FIM知识库)
$env:IMA_KB_NAME = "FIM知识库"
```

> 凭证必须通过环境变量配置，禁止硬编码。旧变量名 `IMA_CLIENT_ID` / `IMA_API_KEY` 仍兼容回退。

## 使用示例

```bash
# X/Twitter tweet
python3 scripts/web_to_all.py --url "https://x.com/user/status/123"

# WeChat article
python3 scripts/web_to_all.py --url "https://mp.weixin.qq.com/s/xxxxx"

# Feishu wiki
python3 scripts/web_to_all.py --url "https://xxx.feishu.cn/wiki/xxxxx"

# Local PDF file
python3 scripts/web_to_all.py --url "C:\docs\report.pdf"

# Only convert to Markdown, no storage
python3 scripts/web_to_md.py --url "<url>" --output output.md
```

## 触发词

转文档、抓网页存飞书、网页转文档、web to feishu、url转文档、文件转飞书、存到ima、存到obsidian、web to fim、三处存放。

当用户提供任意 URL 或本地文件并要求转存为文档时触发。

## 验证连接

```bash
# Verify Feishu connection
python scripts/feishu_client.py --action test

# Verify IMA connection
python scripts/ima_client.py --action test
```

## IMA 智能路由（v3.0）

| source_url 类型 | IMA 存放方式 | 原因 |
|----------------|------------|------|
| 公众号 / 普通网页 | `import_urls`（服务端抓取） | 保留图片和排版 |
| X/Twitter | 纯文本笔记（逐字转录） | 技能规则要求逐字转录 |
| 飞书 wiki | 纯文本笔记（逐字转录） | 需登录认证，IMA 无法抓取 |

## 版本历史

- **v3.1.0**：批量模式断点恢复；Obsidian frontmatter 自动 tags；推文结构化转换通用化；subprocess 120 秒 timeout；公众号正文提取改进
- **v3.0.0**：IMA 改用知识库两步流程；公众号/网页带图片转录（import_urls）；新增飞书 wiki 信源；公众号反爬 fallback
- **v2.x**：基础三处存放功能；X/Twitter 逐字转录；飞书云文档集成

详见 [CHANGELOG.md](./CHANGELOG.md)。

## License

MIT-0 (c) 2026 EdwardWason
