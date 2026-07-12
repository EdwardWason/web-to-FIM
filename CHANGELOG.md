# Changelog

本文件记录 web-to-fim 技能的版本演进。版本号遵循 [语义化版本](https://semver.org/)。

## [3.3.0] - 2026-07-12

### 新增
- **原文链接自动提取**：`extract_original_url()` 函数从 Markdown 前 800 字符自动识别"原文链接"/"转载自"/"本文首发"等关键词
- **IMA 路由精细化**：GitHub URL 改为纯文本笔记（IMA 抓取 HTML 页面效果差），不再走 import_urls
- **飞书 wiki 自动路由函数**：`_is_feishu_wiki()` 和 `_fetch_feishu_wiki_via_webfetch()` 新增

### 修复
- **IMA 路由规则修正**：原文链接为 GitHub 时，原逻辑走 import_urls 导致 IMA 抓取 HTML 页面内容混乱。改为纯文本笔记存转录 MD
- **路由规则文档化**：IMA 路由规则精细化（公众号/普通网页→import_urls；X/Twitter/飞书/GitHub→纯文本笔记）

## [3.2.0] - 2026-07-12

### 新增
- **Obsidian 文件命名规范化**：`YYYYMMDD-标题-来源.md`（如 `20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`）
- **来源自动提取**：`_extract_source_name()` 函数从 URL 域名提取来源标识（waytoagi/feishu/x/wechat/weibo/xiaohongshu/github/youtube/webpage）
- **飞书 wiki 原文链接优先转录**：抓取飞书 wiki 后检查文章头部"原文链接"，有则优先抓取原文内容（公众号/X 等），获得更完整的正文和图片
- **IMA 智能路由优化**：飞书 wiki 有公众号原文链接 → import_urls（保留图片）；无原文链接 → 纯文本笔记

### 修复
- Windows 文件名安全：禁止字符（`\ / : * ? " < > |`）替换为下划线，中文标点（含 `：`）保留
- 文件名长度限制：标题超过 60 字符自动截断，避免文件名过长

## [3.1.0] - 2026-07-11

### 新增
- 批量模式断点恢复：自动生成 `.progress.json` 进度文件，崩溃后重跑自动跳过已完成 URL，全部成功后自动清理
- Obsidian frontmatter 增加 `tags` 字段：根据 URL 来源自动分类标签（x-twitter/wechat/weibo/xiaohongshu/github/youtube/webpage/local-file）
- `save_to_obsidian` 三级 fallback 机制：重试 3 次 → ASCII 文件名 → 脚本目录 `saved/`
- `_process_single` 每个存储操作独立 try/except：一处失败不阻断其他存储

### 修复
- **Critical**: `tweet_to_md.py` 去掉硬编码的段落标题列表，改为通用启发式规则（Emoji 模式匹配 + 数字编号 + 短行特征 + 技术名词后缀）
- **Critical**: `web_to_md.py` `_run()` 函数加 120 秒 timeout，防止 x-tweet-fetcher 网络异常时永久挂起
- **Important**: `_fetch_wechat_mobile()` 改进正文提取：保留图片（data-src）、段落结构（`<p>`/`<section>`）、引用块（blockquote），不再丢失内容
- **Minor**: 标题提取改进：支持从 frontmatter `title:` 提取，fallback 到 URL 域名生成标题，不再出现 `Untitled`
- **Minor**: `import time` / `import json` 移到文件顶部
- **Minor**: `.gitignore` 补充 `saved/`、`batch_urls.txt`、`*.progress.json`、`batch_run.log` 等临时文件

## [3.0.2] - 2026-07-11

### 修复
- 同步本地版本号与 ClawHub 线上版本（本地从 3.0.1 对齐到 3.0.2）
- 修复 SKILL.md 安全声明章节的 Markdown 语法瑕疵：
  - 第 261 行 `--no-ima` 反引号缺失
  - 第 258 / 263 / 268 行 `**文件操作` / `**隐私保护` / `**权限透明` 加粗未闭合

### 文档
- 新增 CHANGELOG.md，补齐版本演进记录

## [3.0.1] - 2026-07-11

### 修复
- 更新 ClawHub 页面 Short summary，反映 v3.0 的信源与存储能力
  - frontmatter description 增加公众号/网页图片保留、飞书 wiki 转录说明
  - 信源表标注 IMA 存储路由（IMA 笔记 → IMA 知识库）

## [3.0.0] - 2026-07-10

### 新增
- **IMA 智能路由**：公众号/普通网页 → `import_urls` 服务端抓取，保留原文图片和排版
- **飞书 wiki 信源**：通过 WebFetch 转录飞书知识库文章全文
- **公众号反爬 fallback**：markitdown 返回验证页时自动切换移动端 UA 重试
- **批量模式**：`--urls-file` 参数支持从文件逐行读取 URL 批量处理
- **试运行模式**：`--dry-run` 参数仅转 Markdown 不入库

### 变更
- **IMA API 迁移到 v1.1.7**：创建笔记改用 `/openapi/note/v1/import_doc`
- **IMA 存储从"笔记本"改为"知识库"两步流程**：
  1. `create_note` 创建笔记（Notes API）
  2. `add_note_to_knowledge_base` 添加到知识库（Wiki API）
- **环境变量更名**：`IMA_CLIENT_ID` / `IMA_API_KEY` → `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`（旧名仍兼容回退）
- X/Twitter 链接强制走纯文本笔记逐字转录，不使用 `import_urls`

### 安全
- 凭证全部通过环境变量配置，无硬编码
- 清理临时脚本中的真实 IMA 凭证
- 完善 .gitignore 排除规则
