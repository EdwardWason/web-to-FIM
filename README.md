# Web-to-FIM | 网页内容转 Markdown/飞书/IMA

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

## 🤖 AI 时代必备的信息库基础技能

在 AI 时代，无论是使用 **OpenClaw**、**Hermes Agent**，还是实践 **Obsidian + LLM** 的信息管理方法论，**一键入库、人机共用**的 AI 信息库搭建都是必备的基础设施。

**Web-to-FIM** 就是这样一个基础技能：它将任意网络内容（X/Twitter、微信公众号、小红书、微博、YouTube、任意网页、本地文件）一键转换为结构化 Markdown，并同步到：
- 📝 **Obsidian Vault** - 本地个人知识库，带 frontmatter
- 📚 **飞书云文档** - 云端团队协作
- 🧠 **腾讯 IMA 笔记** - AI 原生知识库

---

## 🎯 适用平台 | Supported Platforms

| 平台 | 说明 |
|------|------|
| **OpenClaw** | 通过 Skills 管理界面安装使用 |
| **Hermes Agent** | 通过 Skills 目录安装，在 Agent 对话中调用 |
| **独立使用** | 直接运行 Python 脚本 |

---

## ✨ 功能特性 | Features

### 支持的信源 | Supported Sources

| 类型 | 来源 | 说明 |
|------|------|------|
| **X/Twitter** | `x.com` / `twitter.com` | 推文、长文 Article、Thread 线程 |
| **微信公众号** | `mp.weixin.qq.com` | 标题/作者/正文/图片本地化 |
| **小红书** | `xiaohongshu.com` / `xhslink.com` | 图文/视频笔记、互动数据 |
| **微博** | `weibo.com` | 微博内容抓取 |
| **YouTube** | `youtube.com` / `youtu.be` | 字幕/元信息提取 |
| **任意网页** | 其他 HTTP 链接 | HTML 转 Markdown |
| **本地文件** | PDF/Word/PPT/Excel/图片/音频等 | 格式转换与 OCR |

### 输出目的地 | Output Destinations

| 目的地 | 说明 | 凭证 |
|--------|------|------|
| **Obsidian Vault** | 本地保存到 `E:\Obsidian\md\inbox`，带 frontmatter | 无 |
| **Markdown 文件** | 生成本地 `.md` 文件 | 无 |
| **飞书云文档** | 创建飞书云端文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` |
| **腾讯 IMA 笔记** | 创建 IMA 知识库笔记（**云端 API**，无需本地客户端） | `IMA_CLIENT_ID` + `IMA_API_KEY` |

---

## 🚀 快速开始 | Quick Start

### 一键同步所有目的地 | One-Click Sync to All Destinations

```bash
# 转换并保存到 Obsidian/飞书/IMA
python scripts/web_to_all.py --url "https://x.com/user/status/123456"

# 仅保存到 Obsidian（跳过飞书和 IMA）
python scripts/web_to_all.py --url "https://..." --no-feishu --no-ima

# 自定义标题
python scripts/web_to_all.py --url "https://..." --title "我的笔记"
```

### 基本用法 | Basic Usage

```bash
# X/Twitter 推文转 Markdown
python scripts/web_to_md.py --url "https://x.com/user/status/123456" --output tweet.md

# 微信公众号文章转 Markdown
python scripts/web_to_md.py --url "https://mp.weixin.qq.com/s/xxxxx" --output article.md

# 小红书笔记转 Markdown
python scripts/web_to_md.py --url "https://www.xiaohongshu.com/..." --output xhs.md

# 本地文件转 Markdown
python scripts/web_to_md.py --url "document.pdf" --output doc.md
```

---

## 📦 安装说明 | Installation

### 方法一：通过 Releases 安装（推荐）| Method 1: Install via Releases (Recommended)

#### 安装到 OpenClaw | Install to OpenClaw

1. **下载技能压缩包 | Download Skill Package**：
   - 访问 [GitHub Releases](https://github.com/EdwardWason/web-to-FIM/releases)
   - 下载最新版本的 `web-to-FIM.zip` 文件

2. **安装到 OpenClaw | Install to OpenClaw**：
   - 打开 OpenClaw
   - 进入「技能管理」页面
   - 点击「安装技能」按钮
   - 选择下载的 `web-to-FIM.zip` 文件
   - 等待安装完成

3. **配置环境变量 | Configure Environment Variables**：
   - 安装完成后，在 OpenClaw 技能管理页面找到「web-to-FIM」技能
   - 点击「配置」按钮
   - 填写所需的环境变量
   - 保存配置

#### 安装到 Hermes Agent | Install to Hermes Agent

1. **下载技能压缩包 | Download Skill Package**：
   - 访问 [GitHub Releases](https://github.com/EdwardWason/web-to-FIM/releases)
   - 下载最新版本的 `web-to-FIM.zip` 文件

2. **安装到 Hermes Agent | Install to Hermes Agent**：
   - 解压 `web-to-FIM.zip`
   - 将解压后的整个目录复制到 Hermes Agent 的 Skills 目录：
     - Windows：`C:\Users\你的用户名\.hermes\skills\`
     - 或参考 Hermes Agent 文档中的技能目录位置
   - 重启 Hermes Agent 加载新技能

3. **配置环境变量 | Configure Environment Variables**：
   - 在 Hermes Agent 的配置文件或环境变量中设置所需的凭证
   - 或创建 `.env` 文件在技能目录下

### 方法二：手动安装 | Method 2: Manual Installation

#### 安装到 OpenClaw

1. **克隆仓库 | Clone Repository**：
   ```bash
   git clone https://github.com/EdwardWason/web-to-FIM.git
   cd web-to-FIM
   ```

2. **复制技能到 OpenClaw | Copy Skill to OpenClaw**：
   - Windows：
     ```bash
     robocopy ".main\skills\web-to-FIM" "C:\Users\你的用户名\.openclaw\skills\web-to-FIM" /E
     ```
   - macOS/Linux：
     ```bash
     cp -r .main/skills/web-to-FIM ~/.openclaw/skills/
     ```

3. **安装依赖 | Install Dependencies**：
   ```bash
   pip install requests python-dotenv
   ```

4. **配置环境变量 | Configure Environment Variables**：
   - 在 OpenClaw 中配置环境变量，或参考 `references/` 目录下的配置指南

#### 安装到 Hermes Agent

1. **克隆仓库 | Clone Repository**：
   ```bash
   git clone https://github.com/EdwardWason/web-to-FIM.git
   cd web-to-FIM
   ```

2. **复制技能到 Hermes Agent | Copy Skill to Hermes Agent**：
   - Windows：
     ```bash
     robocopy ".main\skills\web-to-FIM" "C:\Users\你的用户名\.hermes\skills\web-to-FIM" /E
     ```
   - macOS/Linux：
     ```bash
     cp -r .main/skills/web-to-FIM ~/.hermes/skills/
     ```

3. **安装依赖 | Install Dependencies**：
   ```bash
   pip install requests python-dotenv
   ```

4. **配置环境变量 | Configure Environment Variables**：
   - 在 Hermes Agent 配置中设置环境变量，或参考 `references/` 目录下的配置指南

---

## 📁 项目结构 | Project Structure

```
web-to-FIM/
├── .env.template               # 环境变量模板 / Environment template
├── .gitignore                  # Git 忽略规则 / Git ignore rules
├── LICENSE                     # Apache 2.0 许可证 / License
├── README.md                   # 本文件 / This file
├── SKILL.md                    # AI Agent 技能入口 / AI Agent skill entry
├── scripts/
│   ├── web_to_md.py            # 统一入口 / Unified entry
│   ├── web_to_all.py           # 一键同步所有目的地 / One-click sync to all
│   ├── tweet_to_md.py          # Tweet → MD 转换 / Tweet conversion
│   ├── feishu_client.py        # 飞书 API 客户端 / Feishu API client
│   └── ima_client.py           # IMA API 客户端 / IMA API client
└── references/
    ├── feishu-setup.md         # 飞书配置指南 / Feishu setup guide
    └── ima-setup.md            # IMA 配置指南 / IMA setup guide
```

---

## 🔒 安全说明 | Security

⚠️ **凭证安全 | Credential Security**：

- 所有 API 凭证通过**环境变量**读取，不硬编码
- All API credentials read from **environment variables**, never hardcoded
- `.gitignore` 已配置忽略 `.env` 等敏感文件
- `.gitignore` configured to ignore `.env` and sensitive files
- 参考 `references/` 下的指南安全配置凭证

---

## 📚 依赖 | Dependencies

| 依赖 | 用途 | 说明 |
|------|------|------|
| [markitdown-plus](https://github.com/jun7799/markitdown-plus) | 通用格式转换 | Universal format conversion |
| [x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) | X/Twitter 抓取 | X/Twitter fetching |
| `requests` | HTTP 请求 | HTTP requests |
| `python-dotenv` | 环境变量加载 | Environment variable loading |

---

## 🙏 致谢 | Acknowledgments

- [microsoft/markitdown](https://github.com/microsoft/markitdown) - 原始转换引擎 / Original conversion engine
- [jun7799/markitdown-plus](https://github.com/jun7799/markitdown-plus) - 微信/X/小红书支持 / WeChat/X/Xiaohongshu support
- [ythx-101/x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) - X/Twitter 抓取 / X/Twitter fetching
- [FXTwitter](https://github.com/FixTweet/FxTwitter) - X/Twitter 数据 API / X/Twitter data API

---

## 📄 许可证 | License

Apache License 2.0 - 详见 [LICENSE](LICENSE)
