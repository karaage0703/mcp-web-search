"""
Google Custom Search MCP Server

Based on code from: https://github.com/suckgeun/book_code/blob/master/servers/src/server_google_search.py
"""

from mcp.server.fastmcp import FastMCP, Context
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import argparse

mcp = FastMCP("google_search_server")


def parse_args():
    """コマンドライン引数をパースして環境変数を設定（オプション）"""
    parser = argparse.ArgumentParser(description="Google Custom Search MCP Server")
    parser.add_argument("--api-key", help="Google API Key (optional, can use GOOGLE_API_KEY env var)")
    parser.add_argument("--cx-id", help="Google Search Engine ID (optional, can use GOOGLE_SEARCH_ENGINE_ID env var)")

    args, _ = parser.parse_known_args()

    # コマンドライン引数が指定されていれば環境変数を上書き
    if args.api_key:
        os.environ["GOOGLE_API_KEY"] = args.api_key
    if args.cx_id:
        os.environ["GOOGLE_SEARCH_ENGINE_ID"] = args.cx_id


@mcp.tool()
async def google_search(query: str, ctx: Context) -> str:
    """
    指定されたクエリでGoogle検索を行い、最初の5件の結果を返します。
    日本からの検索として扱い、日本語の結果を優先します。

    Args:
        query (str): 検索クエリ
        ctx (Context): ロギング用のMCPコンテキスト
    """
    # 入力検証処理

    # 検索クエリが空の場合、エラーを返す
    if not query or not query.strip():
        raise ValueError("検索クエリを入力してください")

    # 検索クエリが長すぎる場合、エラーを返す
    if len(query) > 100:
        raise ValueError("検索クエリは100文字以内で入力してください")

    # API設定の確認（環境変数から取得）
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if not API_KEY or not CX_ID:
        raise Exception(
            "Google検索APIが設定されていません。環境変数 GOOGLE_API_KEY と GOOGLE_SEARCH_ENGINE_ID を確認してください。"
        )

    # 検索実行ログを残す（infoレベル）
    await ctx.info(f"Google検索を実行: '{query}'")

    # 検索実施
    try:  # エラー処理のため、tryで囲む
        # Google Custom Search APIの呼び出し
        service = build("customsearch", "v1", developerKey=API_KEY)
        resp = (
            service.cse()
            .list(
                q=query,
                cx=CX_ID,
                num=5,  # 上位5件を返す
                gl="jp",  # 日本からの検索
                lr="lang_ja",  # 日本語優先
            )
            .execute()
        )

    except HttpError as e:
        # Google APIのエラー処理
        if e.resp.status == 403:
            await ctx.error("APIの利用制限エラー")  # errorレベルでロギング
            raise Exception("Google検索APIの利用制限に達しました。1日100回までの制限を超えた可能性があります。")
        else:
            await ctx.error(f"APIエラー: {str(e)}")
            raise Exception("Google検索APIでエラーが発生しました。しばらく待ってから再試行してください。")

    except Exception as e:
        # その他のエラー（ネットワークエラーなど）
        await ctx.error(f"検索エラー: {str(e)}")
        raise Exception("検索中にエラーが発生しました。インターネット接続を確認してください。")

    # 検索結果の処理
    items = resp.get("items", [])
    if not items:
        return "検索結果が見つかりませんでした"

    cleaned = []
    for rank, it in enumerate(items, 1):  # 取得された検索結果を整理する
        meta = (it.get("pagemap", {}).get("metatags") or [{}])[0]
        published = meta.get("article:published_time") or meta.get("og:updated_time")

        cleaned.append(
            {
                "rank": rank,
                "title": it["title"],
                "snippet": it["snippet"],
                "url": it["link"],
                "domain": it.get("displayLink"),
                "published_at": published,  # 公開日時（存在しない場合はNone）
            }
        )

    # 検索結果についてもログを残す
    await ctx.info(f"検索完了: {len(cleaned)}件の結果")

    return str(cleaned)


def main():
    """Entry point for uvx execution"""
    parse_args()  # コマンドライン引数をパース
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
