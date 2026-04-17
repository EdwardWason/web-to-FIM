# Release Notes | 版本说明

## v2.1.0 - 2026-04-17

### 🎯 平台支持增强 | Platform Support Enhancement

#### 1. Hermes Agent 完整支持 | Full Hermes Agent Support
- 更新了 README.md，新增「适用平台」表格
- 新增 Hermes Agent 详细安装说明
- 强调技能同时支持 OpenClaw 和 Hermes Agent
- 文档中明确标注双平台兼容性

### 📚 文档更新 | Documentation Updates

#### 2. README.md 优化
- 新增「适用平台」章节，列出 OpenClaw、Hermes Agent、独立使用三种方式
- 安装说明分为「安装到 OpenClaw」和「安装到 Hermes Agent」两部分
- 分别提供 Releases 安装和手动安装的详细步骤
- 完善了 Hermes Agent 技能目录路径说明

---

## v2.0.0 - 2026-04-17

### 🚀 重大升级 | Major Upgrade

#### 1. 项目重命名 | Project Rename
- **从** `web-to-feishu` 
- **改为** `web-to-FIM` (F=Feishu, I=IMA, M=Markdown)
- 更新了所有相关引用、文档、文件名

#### 2. AI 时代信息库必备技能定位 | AI Era Information Management Skill
在 README.md 中新增了详细的定位说明：
- 🤖 强调对 **OpenClaw**、**Hermes Agent** 的支持
- 📝 强调对 **Obsidian + LLM** 信息管理方法论的支持
- ⚡ 定位为**一键入库、人机共用**的 AI 信息库搭建必备基础技能

### ✨ 新功能 | New Features

#### 3. Obsidian Vault 集成 | Obsidian Vault Integration
- 新增 `web_to_all.py` 一键同步脚本
- 支持保存到 Obsidian Vault：`E:\Obsidian\md\inbox`
- 自动生成带 frontmatter 的 Markdown 文件（包含 title、date、source 等元数据）
- 支持 `--no-feishu` 和 `--no-ima` 参数，可选择性跳过某些目的地

#### 4. 新增信源支持 | New Source Support
- 小红书 (`xiaohongshu.com` / `xhslink.com`)
- 微博 (`weibo.com`)

#### 5. 路径修复 | Path Fix
- 修复了 `web_to_md.py` 中对 `tweet_to_md.py` 的硬编码路径问题
- 改用 `Path(__file__).parent` 动态获取脚本目录，增强跨平台兼容性

### 📚 文档更新 | Documentation Updates

#### 6. README.md 全面重构
- 新增 AI 时代信息库说明章节
- 新增「一键同步所有目的地」快速开始指南
- 更新所有链接和引用为 web-to-FIM
- 优化项目结构展示

#### 7. SKILL.md 更新
- 更新技能名称和标签
- 更新描述和触发词
- 新增 Obsidian Vault 代码示例
- 完善 AI 时代信息库定位说明

### 🔒 安全说明 | Security
- ✅ 所有 API 凭证通过环境变量读取
- ✅ 无硬编码密钥
- ✅ `.gitignore` 配置正确

### 📦 依赖 | Dependencies
| 依赖 | 说明 |
|------|------|
| markitdown-plus | 通用格式转换 |
| x-tweet-fetcher | X/Twitter 抓取 |
| requests | HTTP 请求 |
| python-dotenv | 环境变量加载 |

---

## 升级指南 | Upgrade Guide

### 从 v1.x 升级到 v2.0

1. **下载新版本压缩包**：`web-to-FIM.zip`
2. **卸载旧版本**：在 OpenClaw 中卸载 `web-to-feishu` 技能
3. **安装新版本**：在 OpenClaw 中安装 `web-to-FIM.zip`
4. **重新配置环境变量**（如果之前在技能中配置过）
5. **更新本地仓库 remote URL**（可选，仅开发者）：
   ```bash
   git remote set-url origin https://github.com/EdwardWason/web-to-FIM.git
   ```

---

## 致谢 | Acknowledgments

- [microsoft/markitdown](https://github.com/microsoft/markitdown)
- [jun7799/markitdown-plus](https://github.com/jun7799/markitdown-plus)
- [ythx-101/x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher)
- [FXTwitter](https://github.com/FixTweet/FxTwitter)
