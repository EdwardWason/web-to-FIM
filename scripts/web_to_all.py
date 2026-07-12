#!/usr/bin/env python3
"""
Web Content → Markdown → Obsidian/Feishu/IMA

Convert any web URL or local file to Markdown, then:
1. Save to Obsidian Vault (configurable via OBSIDIAN_VAULT_PATH)
2. Save to Feishu Cloud Document (optional)
3. Save to Tencent IMA Note (optional)

Usage:
  python3 web_to_all.py --url <url_or_path>
  python3 web_to_all.py --url <url_or_path> --title "Custom Title"
  python3 web_to_all.py --url <url_or_path> --no-feishu --no-ima
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from web_to_md import convert as convert_to_md
from feishu_client import FeishuClient
from ima_client import IMAClient


def get_obsidian_vault_path() -> Path:
    r"""
    Get Obsidian Vault path from environment variable or use default.
    
    Environment variable: OBSIDIAN_VAULT_PATH
    
    Defaults:
    - Windows: E:\Obsidian\md\inbox
    - macOS/Linux: ~/Obsidian/inbox
    """
    env_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_path:
        return Path(env_path).expanduser()
    
    # Default paths by OS
    if sys.platform.startswith("win"):
        return Path(r"E:\Obsidian\md\inbox")
    else:
        return Path.home() / "Obsidian" / "inbox"


OBSIDIAN_VAULT = get_obsidian_vault_path()


def _extract_source_name(url: str) -> str:
    """从 URL 提取来源标识用于文件命名（v3.2.0）"""
    if not url:
        return "local"
    lower = url.lower()
    if "waytoagi" in lower:
        return "waytoagi"
    if "feishu.cn" in lower or "larkoffice" in lower:
        return "feishu"
    if "x.com" in lower or "twitter.com" in lower:
        return "x"
    if "mp.weixin.qq.com" in lower:
        return "wechat"
    if "weibo.com" in lower:
        return "weibo"
    if "xiaohongshu.com" in lower or "xhslink.com" in lower:
        return "xiaohongshu"
    if "github.com" in lower:
        return "github"
    if "youtube.com" in lower or "youtu.be" in lower:
        return "youtube"
    from urllib.parse import urlparse
    try:
        netloc = urlparse(url).netloc
        parts = netloc.split(".")
        return parts[-2] if len(parts) >= 2 else netloc
    except Exception:
        return "webpage"


def save_to_obsidian(content: str, title: str, url: str = None) -> str:
    """Save Markdown to Obsidian Vault"""
    vault_path = Path(OBSIDIAN_VAULT)
    vault_path.mkdir(parents=True, exist_ok=True)

    # 文件名规则：YYYYMMDD-标题-来源.md（v3.2.0）
    import re
    date_str = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 保留用于 fallback
    source = _extract_source_name(url)
    # Windows 禁止字符替换为下划线，中文标点（含：）保留
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title).strip()
    safe_title = re.sub(r'_+', '_', safe_title).strip("_ ").strip()
    safe_title = safe_title.rstrip(".")
    # 限制标题长度，避免文件名过长
    if len(safe_title) > 60:
        safe_title = safe_title[:60].strip("_ ").strip()
    filename = f"{date_str}-{safe_title}-{source}.md"
    filepath = vault_path / filename

    frontmatter = []
    frontmatter.append("---")
    frontmatter.append(f"title: {title}")
    frontmatter.append(f"date: {datetime.now().isoformat()}")
    if url:
        frontmatter.append(f"source: {url}")
        # 根据 URL 来源自动生成 tags
        lower_url = url.lower()
        if "x.com" in lower_url or "twitter.com" in lower_url:
            tags = "web-to-fim, x-twitter"
        elif "mp.weixin.qq.com" in lower_url:
            tags = "web-to-fim, wechat"
        elif "weibo.com" in lower_url:
            tags = "web-to-fim, weibo"
        elif "xiaohongshu.com" in lower_url or "xhslink.com" in lower_url:
            tags = "web-to-fim, xiaohongshu"
        elif "github.com" in lower_url:
            tags = "web-to-fim, github"
        elif "youtube.com" in lower_url or "youtu.be" in lower_url:
            tags = "web-to-fim, youtube"
        else:
            tags = "web-to-fim, webpage"
    else:
        tags = "web-to-fim, local-file"
    frontmatter.append(f"tags: [{tags}]")
    frontmatter.append("---")
    frontmatter_str = "\n".join(frontmatter)

    full_content = f"{frontmatter_str}\n\n{content}"

    for attempt in range(3):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)
            break
        except PermissionError:
            if attempt < 2:
                time.sleep(1)
            else:
                # Fallback: use ASCII-only filename
                ascii_filename = f"note_{timestamp}.md"
                ascii_filepath = vault_path / ascii_filename
                try:
                    with open(ascii_filepath, "w", encoding="utf-8") as f:
                        f.write(full_content)
                    filepath = ascii_filepath
                    break
                except PermissionError:
                    # Last resort: save to script directory
                    fallback_path = Path(__file__).parent.parent / "saved" / ascii_filename
                    fallback_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(fallback_path, "w", encoding="utf-8") as f:
                        f.write(full_content)
                    filepath = fallback_path
                    break

    print(f"✅ Obsidian: {filepath}")
    return str(filepath)


def save_to_feishu(content: str, title: str) -> dict:
    """Save to Feishu Cloud Document"""
    try:
        client = FeishuClient()
        result = client.create_document(title=title, content_md=content)
        print(f"✅ Feishu: {result.get('url', 'N/A')}")
        return result
    except Exception as e:
        print(f"⚠️ Feishu failed: {e}", file=sys.stderr)
        return None


def save_to_ima(content: str, title: str, knowledge_base: str = None, source_url: str = None) -> dict:
    """Save to Tencent IMA knowledge base.

    Two strategies based on source_url:
    - Has URL (公众号/网页): use import_urls → IMA server-side fetch (preserves images/layout)
    - No URL (飞书转录/手动内容): use create_note + add_knowledge (plain text note)

    IMA has two separate API systems:
    - Notes API (/openapi/note/v1/): creates notes, manages notebooks
    - Knowledge Base API (/openapi/wiki/v1/): manages knowledge bases, adds content

    Args:
        content: Markdown content (used when source_url is None)
        title: Note title
        knowledge_base: Target knowledge base name. If None, reads from IMA_KB_NAME env var,
                        defaults to "FIM知识库".
        source_url: Original article URL. If it's a 公众号/网页 URL, use import_urls
                    for server-side fetch (preserves images). None for plain text note.
    """
    # 优先用传入参数，其次环境变量 IMA_KB_NAME，最后默认值
    if knowledge_base is None:
        knowledge_base = os.environ.get("IMA_KB_NAME", "FIM知识库")

    try:
        client = IMAClient()
        kb_id = client.find_knowledge_base_by_name(knowledge_base) if knowledge_base else None

        # Strategy 1: URL import (公众号/网页) — IMA server-side fetch, preserves images
        if source_url and _is_importable_url(source_url):
            results = client.import_urls(
                knowledge_base_id=kb_id,
                urls=[source_url],
            )
            if results and results[0].get("success"):
                print(f"✅ IMA (→ {knowledge_base}, URL导入): {source_url}")
                return {
                    "note_id": "",
                    "title": title,
                    "url": source_url,
                    "media_id": results[0].get("media_id", ""),
                    "method": "import_urls",
                }
            else:
                ret_code = results[0].get("ret_code", -1) if results else -1
                print(f"⚠️ IMA import_urls failed (ret_code={ret_code}), fallback to note", file=sys.stderr)

        # Strategy 2: Plain text note (飞书转录/手动内容/URL导入失败fallback)
        note_result = client.create_note(title=title, content=content)
        note_id = note_result.get("note_id", "")
        if not note_id:
            raise Exception("创建笔记失败：未返回 note_id")

        if kb_id:
            client.add_note_to_knowledge_base(
                note_id=note_id,
                title=title,
                knowledge_base_id=kb_id,
            )
            print(f"✅ IMA (→ {knowledge_base}): {note_result.get('url', 'N/A')}")
        else:
            print(f"✅ IMA: {note_result.get('url', 'N/A')}")

        return note_result
    except Exception as e:
        print(f"⚠️ IMA failed: {e}", file=sys.stderr)
        return None


def _is_importable_url(url: str) -> bool:
    """Check if URL is suitable for IMA import_urls (server-side fetch).

    IMA import_urls supports:
    - 微信公众号文章: mp.weixin.qq.com/s
    - 普通网页: any http(s):// URL (except feishu wiki and X/Twitter)

    Returns False for:
    - feishu wiki URLs (require login auth, IMA can't fetch)
    - X/Twitter URLs (must be transcribed per web-to-fim skill rules, not server-fetched)

    Rationale: X/Twitter content must be 逐字转录 per SKILL.md rules.
    Server-side fetch via import_urls would not preserve the full thread/article structure.
    """
    if not url:
        return False
    lower = url.lower()
    # 飞书 wiki 需要登录认证，IMA 服务端无法抓取
    if "feishu.cn" in lower or "larkoffice" in lower:
        return False
    # X/Twitter 必须逐字转录（web-to-fim 技能规则），不用 IMA 服务端抓取
    if "x.com" in lower or "twitter.com" in lower:
        return False
    # 公众号文章和普通网页都可以
    if lower.startswith("http://") or lower.startswith("https://"):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Web Content → Markdown → Obsidian/Feishu/IMA"
    )
    parser.add_argument("--url", help="URL or local file path to convert")
    parser.add_argument("--urls-file", help="File containing one URL per line (batch mode)")
    parser.add_argument("--title", help="Custom title for the document")
    parser.add_argument("--no-feishu", action="store_true", help="Skip Feishu")
    parser.add_argument("--no-ima", action="store_true", help="Skip IMA")
    parser.add_argument("--no-obsidian", action="store_true", help="Skip Obsidian")
    parser.add_argument("--dry-run", action="store_true", help="Only convert to Markdown, don't save anywhere")
    args = parser.parse_args()

    # Batch mode: read URLs from file
    if args.urls_file:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"📋 Batch mode: {len(urls)} URLs from {args.urls_file}\n")

        # 断点恢复：读取进度文件，跳过已完成的 URL
        progress_file = Path(args.urls_file).with_suffix(".progress.json")
        completed_urls = set()
        if progress_file.exists():
            with open(progress_file, "r", encoding="utf-8") as f:
                completed_urls = set(json.load(f))
            if completed_urls:
                print(f"♻️ Resuming: {len(completed_urls)} URLs already completed, skipping...\n")

        success, fail = 0, 0
        for i, url in enumerate(urls, 1):
            if url in completed_urls:
                print(f"--- [{i}/{len(urls)}] SKIP (already done) {url} ---")
                continue
            print(f"--- [{i}/{len(urls)}] {url} ---")
            try:
                _process_single(url, args)
                success += 1
                completed_urls.add(url)
                # 每条完成后立即写入进度（崩溃可恢复）
                with open(progress_file, "w", encoding="utf-8") as f:
                    json.dump(list(completed_urls), f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"❌ Failed: {e}", file=sys.stderr)
                fail += 1
        print(f"\n✅ Batch done: {success} success, {fail} failed")
        if fail == 0:
            # 全部成功，清理进度文件
            if progress_file.exists():
                progress_file.unlink()
        return 0 if fail == 0 else 1

    # Single mode
    if not args.url:
        parser.error("either --url or --urls-file is required")
    return _process_single(args.url, args)


def _process_single(url: str, args) -> int:
    """Process a single URL: convert → save to destinations."""
    print(f"🔍 Converting: {url}")
    try:
        markdown = convert_to_md(url)
    except Exception as e:
        print(f"❌ Conversion failed: {e}", file=sys.stderr)
        return 1

    title = args.title
    if not title:
        lines = markdown.strip().split("\n")
        first_line = lines[0] if lines else ""
        if first_line.startswith("# "):
            title = first_line[2:].strip()
        elif first_line.startswith("title:"):
            title = first_line.split("title:", 1)[1].strip()
        else:
            # 尝试从 frontmatter 提取 title
            for line in lines[:10]:
                if line.strip().startswith("title:"):
                    title = line.split("title:", 1)[1].strip()
                    break
            else:
                # 从 URL 生成标题
                if url.startswith("http"):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    domain = parsed.netloc.replace("www.", "")
                    title = f"{domain} - {datetime.now().strftime('%Y-%m-%d')}"
                else:
                    title = f"Untitled - {datetime.now().strftime('%Y-%m-%d')}"

    print(f"\n📄 Title: {title}")
    print(f"📝 Markdown length: {len(markdown)} chars\n")

    if args.dry_run:
        print("🔇 Dry run — not saving anywhere")
        print(f"\n--- Markdown preview (first 500 chars) ---\n{markdown[:500]}")
        return 0

    results = {}

    if not args.no_obsidian:
        try:
            results["obsidian"] = save_to_obsidian(markdown, title, url)
        except Exception as e:
            print(f"⚠️ Obsidian failed: {e}", file=sys.stderr)

    if not args.no_feishu:
        try:
            results["feishu"] = save_to_feishu(markdown, title)
        except Exception as e:
            print(f"⚠️ Feishu failed: {e}", file=sys.stderr)

    if not args.no_ima:
        try:
            results["ima"] = save_to_ima(markdown, title, source_url=url)
        except Exception as e:
            print(f"⚠️ IMA failed: {e}", file=sys.stderr)

    print(f"\n✅ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
