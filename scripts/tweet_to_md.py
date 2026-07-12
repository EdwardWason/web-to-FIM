#!/usr/bin/env python3
"""
Tweet JSON → Structured Markdown Converter

Usage:
  python3 tweet_to_md.py --input <tweet.json> --output <output.md>
  python3 tweet_to_md.py --input <tweet.json>  (prints to stdout)

Input: JSON file from x-tweet-fetcher (fetch_tweet.py)
Output: Well-structured Markdown with metadata header, section headers, and images.
"""

import json
import re
import argparse
import sys
from pathlib import Path


# 通用启发式规则：识别推文长文中的段落标题
# 不再硬编码特定推文的标题，而是基于文本特征判断

# Emoji 范围（覆盖常见 Emoji，无需逐个列举）
_EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001F9FF"  # 符号和象形文字
    "\U00002600-\U000027BF"   # 杂项符号
    "\U0001F600-\U0001F64F"   # 表情符号
    "\U0001F680-\U0001F6FF"   # 交通和地图符号
    "]"
)

# 数字编号前缀（如 "1. " "2. " "（1）" 等）
_NUMBERED_PREFIX = re.compile(r'^(\d+[\.\)、）]\s+)')

# 中文标题结尾标点（如果是标题，通常不以这些结尾）
_SENTENCE_ENDINGS = "。！？；，、…～~"


def _is_section_header(line: str) -> bool:
    """通用判断：是否为段落标题（## 级别）"""
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False

    # 规则1: 数字编号开头（1. 2. 3. 等）
    if _NUMBERED_PREFIX.match(stripped):
        return True

    # 规则2: Emoji 开头 + 短行
    if _EMOJI_PATTERN.match(stripped[0]) and len(stripped) < 60:
        return True

    # 规则3: 短行（<30字符）+ 不以句末标点结尾 + 不是完整句子
    # 这类行通常是标题（如"商业价值"、"案例背景"）
    if len(stripped) < 30 and stripped[-1] not in _SENTENCE_ENDINGS:
        # 排除纯数字、纯标点
        if re.match(r'^[\u4e00-\u9fff\w]', stripped) and not stripped.endswith('】'):
            # 进一步检查：标题通常不含逗号/顿号（除非是复合标题）
            if '，' not in stripped and '、' not in stripped:
                return True

    return False


def _is_subsection_header(line: str) -> bool:
    """通用判断：是否为子段落标题（### 级别）

    子标题特征：
    - 包含特定关键词模式（如"XXX模式"、"XXX引擎"、"XXX智能体"）
    - 短行（<80字符）
    - 不以句末标点结尾
    """
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False

    # 不以句末标点结尾
    if stripped[-1] in _SENTENCE_ENDINGS:
        return False

    # 规则: 包含"模式""引擎""智能体""系统""框架""流程""策略""方法"等技术性名词后缀
    tech_suffixes = ["模式", "引擎", "智能体", "系统", "框架", "流程", "策略", "方法", "方案", "架构"]
    for suffix in tech_suffixes:
        if suffix in stripped and len(stripped) < 60:
            return True

    return False


def convert_tweet_to_md(data: dict) -> str:
    tweet = data.get("tweet", {})
    article = tweet.get("article", {})
    url = data.get("url", "")
    username = data.get("username", "")

    md_parts = []

    if article.get("title"):
        title = article["title"]
    elif tweet.get("text"):
        title = tweet["text"][:80].split("\n")[0]
    else:
        title = f"Tweet by @{username}"

    md_parts.append(f"# {title}\n")

    author = tweet.get("author", "")
    screen_name = tweet.get("screen_name", username)
    created_at = tweet.get("created_at", "")
    likes = tweet.get("likes", 0)
    retweets = tweet.get("retweets", 0)
    bookmarks = tweet.get("bookmarks", 0)
    views = tweet.get("views", 0)
    replies_count = tweet.get("replies_count", 0)
    is_article = tweet.get("is_article", False)

    md_parts.append(f"> **作者**: {author} (@{screen_name})  ")
    if created_at:
        md_parts.append(f"> **发布时间**: {created_at}  ")
    md_parts.append(f"> **数据**: {likes} 赞 / {retweets} 转发 / {bookmarks} 收藏 / {views} 浏览 / {replies_count} 评论")
    if is_article:
        md_parts.append(f"> **类型**: X 长文（Article）")
    md_parts.append("")

    if article.get("preview_text"):
        md_parts.append(f"> {article['preview_text']}\n")

    md_parts.append("---\n")

    if is_article and article.get("full_text"):
        full_text = article["full_text"]
        lines = full_text.split("\n")

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("![") and "](" in stripped:
                md_parts.append(f"\n{stripped}\n")
                continue

            if not stripped:
                md_parts.append("")
                continue

            if _is_section_header(stripped):
                md_parts.append(f"\n## {stripped}\n")
                continue

            if _is_subsection_header(stripped):
                md_parts.append(f"\n### {stripped}\n")
                continue

            md_parts.append(line)
    else:
        text = tweet.get("text", "")
        if text:
            md_parts.append(text)

    images = article.get("images", [])
    if images:
        md_parts.append("\n---\n")
        md_parts.append("## 附图\n")
        for img in images:
            img_url = img.get("url", "")
            img_type = img.get("type", "image")
            if img_url:
                label = "封面" if img_type == "cover" else "图片"
                md_parts.append(f"![{label}]({img_url})\n")

    replies = data.get("replies", [])
    if replies:
        md_parts.append("\n---\n")
        md_parts.append("## 评论\n")
        for reply in replies:
            reply_author = reply.get("author", "")
            reply_text = reply.get("text", "")
            reply_likes = reply.get("likes", 0)
            md_parts.append(f"**{reply_author}** (♥ {reply_likes}): {reply_text}\n")
            for nested in reply.get("thread_replies", []):
                nested_text = nested.get("text", "")
                nested_likes = nested.get("likes", 0)
                md_parts.append(f"  ↳ {nested_text} (♥ {nested_likes})\n")

    md_parts.append("\n---\n")
    md_parts.append(f"*来源: [{url}]({url})*\n")

    return "\n".join(md_parts)


def main():
    parser = argparse.ArgumentParser(description="Convert tweet JSON to Markdown")
    parser.add_argument("--input", required=True, help="Input JSON file from x-tweet-fetcher")
    parser.add_argument("--output", help="Output Markdown file (default: stdout)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "error" in data:
        print(f"Error in input data: {data['error']}", file=sys.stderr)
        sys.exit(1)

    markdown = convert_tweet_to_md(data)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"✅ Markdown saved: {output_path} ({len(markdown)} chars)", file=sys.stderr)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
