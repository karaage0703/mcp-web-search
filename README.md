# MCP Web Search

Google Custom Search APIを使用したMCPサーバーです。

## セットアップ

### 1. Google Custom Search APIの準備

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Custom Search APIを有効化
3. APIキーを作成
4. [Programmable Search Engine](https://programmablesearchengine.google.com/)で検索エンジンを作成
5. 検索エンジンIDを取得

### 2. インストールと設定

`.mcp.json` または `claude_desktop_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "uvx",
      "args": [
        "mcp-web-search",
        "--api-key", "your-api-key-here",
        "--cx-id", "your-search-engine-id-here"
      ]
    }
  }
}
```

## 開発

```bash
# 依存関係のインストール
pip install -e .

# ローカル実行
python -m mcp_web_search.server --api-key YOUR_KEY --cx-id YOUR_CX_ID
```