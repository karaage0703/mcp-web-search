# MCP Web Search

Google Custom Search APIを使用したMCPサーバーです。

## クレジット

このコードは [suckgeun/book_code](https://github.com/suckgeun/book_code/blob/master/servers/src/server_google_search.py) を参考にして作成されました。

## セットアップ

### 1. Google Custom Search APIの準備

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Custom Search APIを有効化
3. APIキーを作成
4. [Programmable Search Engine](https://programmablesearchengine.google.com/)で検索エンジンを作成
5. 検索エンジンIDを取得

### 2. 環境変数の設定

環境変数を設定します:

```bash
export GOOGLE_API_KEY="your-api-key-here"
export GOOGLE_SEARCH_ENGINE_ID="your-search-engine-id-here"
```

永続化する場合は、`~/.zshrc` または `~/.bashrc` に追加してください。

### 3. MCP設定

`.mcp.json` または `claude_desktop_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/karaage0703/mcp-web-search.git",
        "mcp-web-search"
      ],
      "env": {
        "GOOGLE_API_KEY": "your-api-key-here",
        "GOOGLE_SEARCH_ENGINE_ID": "your-search-engine-id-here"
      }
    }
  }
}
```

**セキュリティ上の推奨**: 設定ファイルに直接APIキーを書く代わりに、環境変数を参照することを推奨します。

## 開発

環境変数を設定してから実行:

```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_SEARCH_ENGINE_ID="your-cx-id"

# uvx でローカル実行
uvx --from . mcp-web-search

# または開発モードでインストール
uv pip install -e .
python -m mcp_web_search.server
```