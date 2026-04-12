#!/usr/bin/env python3
"""
Tencent IMA Notes API Client

安全说明:
- 所有凭证通过环境变量读取，不硬编码
- 支持 .env 文件加载（需 python-dotenv）
- 凭证不写入日志或任何输出

Usage:
    from ima_client import IMAClient
    client = IMAClient()
    note = client.create_note(title="我的笔记", content="# Hello")
"""

import os
import json
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    print("❌ requests 库未安装: pip install requests")
    raise


class IMAClient:
    BASE_URL = "https://ima.im.qq.com/openapi"

    def __init__(self, client_id: str = None, api_key: str = None):
        self.client_id = client_id or os.environ.get("IMA_CLIENT_ID")
        self.api_key = api_key or os.environ.get("IMA_API_KEY")

        if not self.client_id or not self.api_key:
            raise ValueError(
                "缺少 ima 凭证。请设置环境变量 IMA_CLIENT_ID 和 IMA_API_KEY，"
                "或参考 references/ima-setup.md 获取凭证"
            )

    def _headers(self) -> Dict[str, str]:
        """生成认证头"""
        return {
            "Client-ID": self.client_id,
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        """验证 ima 连接"""
        try:
            url = f"{self.BASE_URL}/v1/notebook/list"
            resp = requests.get(url, headers=self._headers(), timeout=30)
            return resp.status_code == 200
        except Exception:
            return False

    def list_notebooks(self) -> List[Dict[str, Any]]:
        """
        获取笔记本列表

        Returns:
            笔记本列表
        """
        url = f"{self.BASE_URL}/v1/notebook/list"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("notebooks", [])

    def create_note(self, title: str, content: str = "") -> Dict[str, Any]:
        """
        在 ima 中创建笔记

        Args:
            title: 笔记标题
            content: 笔记内容（支持 Markdown）

        Returns:
            包含笔记信息的字典
        """
        url = f"{self.BASE_URL}/v1/note/create"
        payload = {
            "title": title,
            "content": content,
            "format": "markdown"
        }

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建 ima 笔记失败: {data.get('message')}")

        note = data.get("note", {})
        return {
            "note_id": note.get("note_id"),
            "title": title,
            "url": note.get("url", f"https://ima.qq.com/note/{note.get('note_id')}")
        }

    def update_note(self, note_id: str, content: str, append: bool = True) -> bool:
        """
        更新 ima 笔记

        Args:
            note_id: 笔记 ID
            content: 追加或覆盖的内容
            append: True 追加内容，False 覆盖全部

        Returns:
            是否成功
        """
        url = f"{self.BASE_URL}/v1/note/update"
        payload = {
            "note_id": note_id,
            "content": content,
            "append": append
        }

        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("code") == 0

    def get_note(self, note_id: str) -> Dict[str, Any]:
        """
        获取笔记详情

        Args:
            note_id: 笔记 ID

        Returns:
            笔记详情
        """
        url = f"{self.BASE_URL}/v1/note/get"
        payload = {"note_id": note_id}
        resp = requests.get(url, headers=self._headers(), params=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("note", {})

    def search_notes(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索笔记

        Args:
            keyword: 搜索关键词
            limit: 返回数量限制

        Returns:
            匹配的笔记列表
        """
        url = f"{self.BASE_URL}/v1/note/search"
        payload = {
            "query": keyword,
            "limit": limit
        }
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("notes", [])


def main():
    import argparse

    parser = argparse.ArgumentParser(description="腾讯 ima 笔记 API 客户端")
    parser.add_argument("--action", choices=["test", "list", "create", "search"], default="test", help="操作类型")
    parser.add_argument("--title", help="笔记标题")
    parser.add_argument("--content", help="笔记内容或内容文件路径")
    parser.add_argument("--note-id", help="笔记 ID")
    parser.add_argument("--keyword", help="搜索关键词")
    args = parser.parse_args()

    try:
        client = IMAClient()

        if args.action == "test":
            if client.test_connection():
                print("✅ ima 连接成功")
            else:
                print("❌ ima 连接失败")

        elif args.action == "list":
            notebooks = client.list_notebooks()
            print(f"📚 笔记本列表 ({len(notebooks)} 个):")
            for nb in notebooks:
                print(f"   - {nb.get('name', '未命名')}")

        elif args.action == "create":
            if not args.title:
                print("❌ 需要指定 --title")
                return

            content = ""
            if args.content:
                if os.path.isfile(args.content):
                    with open(args.content, "r", encoding="utf-8") as f:
                        content = f.read()
                else:
                    content = args.content

            result = client.create_note(args.title, content)
            print(f"✅ 笔记创建成功:")
            print(f"   ID: {result['note_id']}")
            print(f"   URL: {result['url']}")

        elif args.action == "search":
            if not args.keyword:
                print("❌ 需要指定 --keyword")
                return

            notes = client.search_notes(args.keyword)
            print(f"🔍 搜索结果 ({len(notes)} 条):")
            for note in notes:
                print(f"   - {note.get('title', '未命名')} (ID: {note.get('note_id')})")

    except ValueError as e:
        print(f"❌ 配置错误: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
