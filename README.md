# Web-to-Feishu | 网页内容转飞书/ima文档

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

将任意网页链接或本地文件一键转为结构化 Markdown，并保存到飞书云文档或腾讯 ima 笔记。

Convert any web URL or local file to structured Markdown and save to Feishu Cloud Documents or Tencent ima Notes.

## 功能特性 | Features

### 支持的信源 | Supported Sources

| 类型 | 来源 | Description |
|------|------|-------------|
| **X/Twitter** | `x.com` / `twitter.com` | 推文、长文 Article、Thread 线程 |
| **微信公众号** | `mp.weixin.qq.com` | 标题/作者/正文/图片本地化 |
| **YouTube** | `youtube.com` / `youtu.be` | 字幕/元信息提取 |
| **任意网页** | 其他 HTTP 链接 | HTML 转 Markdown |
| **本地文件** | PDF/Word/PPT/Excel/图片/音频等 | 格式转换与 OCR |

### 输出目的地 | Output Destinations

| 目的地 | 说明 | Credentials |
|--------|------|-------------|
| **Markdown 文件** | 生成本地 `.md` 文件 | 无 / None |
| **飞书云文档** | 创建飞书云端文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` |
| **腾讯 ima 笔记** | 创建 ima 知识库笔记 | `IMA_CLIENT_ID` + `IMA_API_KEY` |

## 安装说明 | Installation

### 方法一：通过 Releases 安装（推荐）| Method 1: Install via Releases (Recommended)

1. **下载技能压缩包 | Download Skill Package**：
   - 访问 [GitHub Releases](https://github.com/EdwardWason/web-to-feishu/releases)
   - 下载最新版本的 `web-to-feishu.zip` 文件

2. **安装到 OpenClaw | Install to OpenClaw**：
   - 打开 OpenClaw
   - 进入「技能管理」页面
   - 点击「安装技能」按钮
   - 选择下载的 `web-to-feishu.zip` 文件
   - 等待安装完成

3. **配置环境变量 | Configure Environment Variables**：
   - 安装完成后，在 OpenClaw 技能管理页面找到「web-to-feishu」技能
   - 点击「配置」按钮
   - 填写所需的环境变量
   - 保存配置

### 方法二：手动安装到 OpenClaw | Method 2: Manual Installation to OpenClaw

1. **克隆仓库 | Clone Repository**：
   ```bash
   git clone https://github.com/EdwardWason/web-to-feishu.git
   cd web-to-feishu
   ```

2. **复制技能到 OpenClaw | Copy Skill to OpenClaw**：
   - Windows：
     ```bash
     robocopy ".main\skills\web-to-feishu" "C:\Users\你的用户名\.openclaw\skills\web-to-feishu" /E
     ```
   - macOS/Linux：
     ```bash
     cp -r .main/skills/web-to-feishu ~/.openclaw/skills/
     ```

3. **安装依赖 | Install Dependencies**：
   ```bash
   pip install requests python-dotenv
   ```

4. **配置环境变量 | Configure Environment Variables**：
   - 在 OpenClaw 中配置环境变量，或参考 `references/` 目录下的配置指南

## 快速开始 | Quick Start

### 前置依赖 | Prerequisites

```bash
# 安装 Python 依赖
pip install requests python-dotenv

# 安装 markitdown-plus（用于通用格式转换）
git clone https://github.com/jun7799/markitdown-plus.git
cd markitdown-plus
pip install -e 'packages/markitdown[all]'

# 安装 x-tweet-fetcher（用于 X/Twitter 抓取）
git clone https://github.com/yiyung/x-tweet-fetcher.git ~/.aily/workspace/skills/x-tweet-fetcher
```

### 环境配置 | Environment Setup

1. 复制凭证模板 | Copy credential template：
```bash
cp .env.template .env
```

2. 编辑 `.env` 填入你的凭证（参考 `references/` 目录下的配置指南）
Edit `.env` with your credentials (see guides in `references/`)

3. **重要 | Important**：永远不要将 `.env` 提交到 Git！Never commit `.env` to Git!

### 基本用法 | Basic Usage

```bash
# X/Twitter 推文转 Markdown
python scripts/web_to_md.py --url "https://x.com/user/status/123456" --output tweet.md

# 微信公众号文章转 Markdown
python scripts/web_to_md.py --url "https://mp.weixin.qq.com/s/xxxxx" --output article.md

# 本地文件转 Markdown
python scripts/web_to_md.py --url "document.pdf" --output doc.md

# 飞书云文档创建
python scripts/feishu_client.py --action create --title "我的笔记" --content doc.md

# ima 笔记创建
python scripts/ima_client.py --action create --title "我的笔记" --content doc.md
```

## 项目结构 | Project Structure

```
web-to-feishu/
├── .env.template               # 环境变量模板 / Environment template
├── .gitignore                  # Git 忽略规则 / Git ignore rules
├── LICENSE                     # Apache 2.0 许可证 / License
├── README.md                   # 本文件 / This file
├── SKILL.md                    # AI Agent 技能入口 / AI Agent skill entry
├── scripts/
│   ├── web_to_md.py            # 统一入口 / Unified entry
│   ├── tweet_to_md.py          # Tweet → MD 转换 / Tweet conversion
│   ├── feishu_client.py        # 飞书 API 客户端 / Feishu API client
│   └── ima_client.py           # ima API 客户端 / ima API client
└── references/
    ├── feishu-setup.md         # 飞书配置指南 / Feishu setup guide
    └── ima-setup.md            # ima 配置指南 / ima setup guide
```

## 安全说明 | Security

⚠️ **凭证安全 | Credential Security**：

- 所有 API 凭证通过**环境变量**读取，不硬编码
- All API credentials read from **environment variables**, never hardcoded
- `.gitignore` 已配置忽略 `.env` 等敏感文件
- `.gitignore` configured to ignore `.env` and sensitive files
- 参考 `references/` 下的指南安全配置凭证

## 依赖 | Dependencies

| 依赖 | 用途 | Description |
|------|------|-------------|
| [markitdown-plus](https://github.com/jun7799/markitdown-plus) | 通用格式转换 | Universal format conversion |
| [x-tweet-fetcher](https://github.com/yiyung/x-tweet-fetcher) | X/Twitter 抓取 | X/Twitter fetching |
| `requests` | HTTP 请求 | HTTP requests |
| `python-dotenv` | 环境变量加载 | Environment variable loading |

## 致谢 | Acknowledgments

- [microsoft/markitdown](https://github.com/microsoft/markitdown) - 原始转换引擎 / Original conversion engine
- [jun7799/markitdown-plus](https://github.com/jun7799/markitdown-plus) - 微信/X 支持 / WeChat/X support
- [FXTwitter](https://github.com/FixTweet/FxTwitter) - X/Twitter 数据 API / X/Twitter data API

## 许可证 | License

Apache License 2.0 - 详见 [LICENSE](LICENSE)
