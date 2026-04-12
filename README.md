# Web-to-Feishu

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

将任意网页链接或本地文件一键转为结构化 Markdown，并保存到飞书云文档或腾讯 ima 笔记。

## 功能特性

### 支持的信源

| 类型 | 来源 | 说明 |
|------|------|------|
| **X/Twitter** | `x.com` / `twitter.com` | 推文、长文 Article、Thread 线程 |
| **微信公众号** | `mp.weixin.qq.com` | 标题/作者/正文/图片本地化 |
| **YouTube** | `youtube.com` / `youtu.be` | 字幕/元信息提取 |
| **任意网页** | 其他 HTTP 链接 | HTML 转 Markdown |
| **本地文件** | PDF/Word/PPT/Excel/图片/音频等 | 格式转换与 OCR |

### 输出目的地

| 目的地 | 说明 | 凭证需求 |
|--------|------|---------|
| **Markdown 文件** | 生成本地 `.md` 文件 | 无 |
| **飞书云文档** | 创建飞书云端文档 | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` |
| **腾讯 ima 笔记** | 创建 ima 知识库笔记 | `IMA_CLIENT_ID` + `IMA_API_KEY` |

## 快速开始

### 前置依赖

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

### 环境配置

1. 复制凭证模板：

```bash
cp .env.template .env
```

2. 编辑 `.env` 填入你的凭证（参考 [references/](references/) 目录下的配置指南）

3. **重要**：永远不要将 `.env` 提交到 Git！

### 基本用法

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

## 项目结构

```
web-to-feishu/
├── SKILL.md                    # AI Agent 技能入口
├── README.md                   # 本文件
├── LICENSE                     # Apache 2.0 许可证
├── .gitignore                  # Git 忽略规则
├── .env.template               # 环境变量模板
├── scripts/
│   ├── web_to_md.py            # 统一入口：自动识别并转换
│   ├── tweet_to_md.py          # Tweet JSON → 结构化 Markdown
│   ├── feishu_client.py        # 飞书云文档 API 客户端
│   └── ima_client.py           # 腾讯 ima 笔记 API 客户端
└── references/
    ├── feishu-setup.md         # 飞书配置指南
    └── ima-setup.md            # ima 配置指南
```

## 安全说明

⚠️ **凭证安全**：

- 所有 API 凭证通过**环境变量**读取，不硬编码
- `.gitignore` 已配置忽略 `.env` 等敏感文件
- 参考 [references/](references/) 下的指南安全配置凭证

## 依赖

| 依赖 | 用途 |
|------|------|
| [markitdown-plus](https://github.com/jun7799/markitdown-plus) | 通用格式转换 |
| [x-tweet-fetcher](https://github.com/yiyung/x-tweet-fetcher) | X/Twitter 抓取 |
| `requests` | HTTP 请求 |
| `python-dotenv` | 环境变量加载 |

## 致谢

- [microsoft/markitdown](https://github.com/microsoft/markitdown) - 原始转换引擎
- [jun7799/markitdown-plus](https://github.com/jun7799/markitdown-plus) - 微信/X 支持
- [FXTwitter](https://github.com/FixTweet/FxTwitter) - X/Twitter 数据 API

## 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)
