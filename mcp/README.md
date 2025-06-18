# MCP サーバー完全ガイド - ずんだもん解説版

## 1. MCP サーバーの概要理解

### MCP とは何なのだ？

Model Context Protocol（MCP）は、Anthropic が 2024 年 11 月に発表したオープンスタンダードなのだ！AI アプリケーションと外部データソース・ツールを接続するための標準化されたプロトコルなのだ。

**「AI アプリケーションの USB-C」**と呼ばれているのだ！USB-C がデバイスと周辺機器を簡単に接続できるように、MCP は AI モデルとデータソース・ツールを簡単に接続できるようにするのだ。

### なぜ MCP が必要なのだ？

従来の問題：

- M 個の AI アプリケーション × N 個のツール = M×N 個の統合が必要だったのだ
- 各データソースごとに個別のコネクタを作る必要があったのだ
- 統合が断片化していて、スケールが困難だったのだ

MCP の解決策：

- M+N 個の実装で済むようになったのだ！
- 標準化されたプロトコルで、どんな AI アプリケーションでも同じ方法でツールに接続できるのだ

### MCP のアーキテクチャ

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  ホスト     │     │  クライアント │     │  サーバー    │
│ (Claude等)  │ ←→  │   (MCP)     │ ←→  │ (ツール)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

- **ホスト**: ユーザーが操作するアプリケーション（Claude Desktop、IDE など）
- **クライアント**: ホスト内で MCP サーバーとの接続を管理
- **サーバー**: ツール、リソース、プロンプトを提供する外部プログラム

### MCP が提供する 3 つの主要機能

1. **Tools（モデル制御）**: AI が実行できるアクション（API 呼び出し、計算など）
2. **Resources（アプリケーション制御）**: AI がアクセスできるデータソース（ファイル、データベースなど）
3. **Prompts（ユーザー制御）**: 事前定義されたインタラクションのテンプレート

## 2. 最小限の構成で試すハンズオン

### 環境準備

WSL2 Ubuntu 22.04 で以下のコマンドを実行するのだ！

```bash
# Python環境の確認
python3 --version  # Python 3.8以上が必要なのだ

# pipのアップグレード
pip3 install --upgrade pip

# MCP Python SDKのインストール
pip3 install mcp

# uvをインストール（MCPサーバーの実行に使用）
pip3 install uv
```

### 最小限の MCP サーバーを作成

`hello_mcp_server.py`というファイルを作成するのだ：

```python
#!/usr/bin/env python3
"""ずんだもんの最小MCPサーバーなのだ！"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# サーバーインスタンスを作成するのだ
server = Server("hello-zundamon")

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """利用可能なリソースを返すのだ"""
    return [
        types.Resource(
            uri="zundamon://greeting",
            name="ずんだもんの挨拶",
            description="ずんだもんが挨拶をするのだ！",
            mime_type="text/plain"
        )
    ]

@server.get_resource()
async def get_resource(uri: str) -> str:
    """リソースの内容を返すのだ"""
    if uri == "zundamon://greeting":
        return "ぼくはずんだもん！ずんだの精霊なのだ！よろしくなのだ！"
    raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """利用可能なツールを返すのだ"""
    return [
        types.Tool(
            name="calculate_zunda",
            description="ずんだもちの必要量を計算するのだ",
            input_schema={
                "type": "object",
                "properties": {
                    "people": {
                        "type": "integer",
                        "description": "人数"
                    }
                },
                "required": ["people"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """ツールを実行するのだ"""
    if name == "calculate_zunda":
        people = arguments.get("people", 1)
        zunda_per_person = 3  # 一人あたり3個なのだ
        total = people * zunda_per_person
        return [
            types.TextContent(
                type="text",
                text=f"{people}人分のずんだもちは{total}個必要なのだ！"
            )
        ]
    raise ValueError(f"Unknown tool: {name}")

# メインエントリーポイント
async def main():
    """サーバーを起動するのだ"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### サーバーの実行とテスト

```bash
# 実行権限を付与
chmod +x hello_mcp_server.py

# サーバーを起動（別のターミナルでテスト用）
python3 hello_mcp_server.py
```

### MCP インスペクターでテスト

別のターミナルで以下を実行するのだ：

```bash
# MCPインスペクターをインストール
npm install -g @modelcontextprotocol/inspector

# インスペクターでサーバーをテスト
mcp-inspector python3 hello_mcp_server.py
```

ブラウザが開いて、MCP サーバーの機能をテストできるのだ！

## 3. MCP サーバーについてもう一段階深い理解

### MCP の技術仕様

#### 通信プロトコル

- **JSON-RPC 2.0**をベースにしているのだ
- **stdio**（標準入出力）を使った通信が基本なのだ
- Language Server Protocol（LSP）のメッセージフローを参考にしているのだ

#### サーバーのライフサイクル

1. **初期化フェーズ**

   ```
   Client → Server: initialize request
   Server → Client: initialize response (capabilities)
   Client → Server: initialized notification
   ```

2. **実行フェーズ**

   - リソースのリスト取得・読み取り
   - ツールのリスト取得・実行
   - プロンプトのリスト取得・実行

3. **シャットダウンフェーズ**
   ```
   Client → Server: shutdown request
   Server → Client: shutdown response
   ```

### 高度な機能の実装例

`advanced_mcp_server.py`を作成するのだ：

```python
#!/usr/bin/env python3
"""高度な機能を持つMCPサーバーなのだ！"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from datetime import datetime
import json
import os
from typing import Any

server = Server("advanced-zundamon")

# サーバーの状態を保持
class ServerState:
    def __init__(self):
        self.memo = {}  # メモを保存する辞書なのだ

state = ServerState()

# サンプリング機能（AIへのヒント提供）
@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """利用可能なプロンプトテンプレートを返すのだ"""
    return [
        types.Prompt(
            name="zundamon_analysis",
            description="ずんだもん流の分析を行うテンプレートなのだ",
            arguments=[
                types.PromptArgument(
                    name="topic",
                    description="分析したいトピック",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    """プロンプトの内容を生成するのだ"""
    if name == "zundamon_analysis":
        topic = arguments.get("topic", "不明なトピック")
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""
ずんだもん流の分析を実行するのだ！

トピック: {topic}

以下の観点で分析してほしいのだ：
1. ずんだ的視点: このトピックとずんだの関係性
2. 技術的側面: 実装や仕組みについて
3. 将来性: 今後の発展可能性
4. ずんだもんからのアドバイス

語尾は「〜のだ」「〜なのだ」を使って、ずんだもんらしく説明してほしいのだ！
"""
                    )
                )
            ]
        )
    raise ValueError(f"Unknown prompt: {name}")

# 複数のツールを実装
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """利用可能なツールのリストなのだ"""
    return [
        types.Tool(
            name="save_memo",
            description="メモを保存するのだ",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "メモのキー"},
                    "content": {"type": "string", "description": "メモの内容"}
                },
                "required": ["key", "content"]
            }
        ),
        types.Tool(
            name="get_memo",
            description="保存したメモを取得するのだ",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "メモのキー"}
                },
                "required": ["key"]
            }
        ),
        types.Tool(
            name="list_memos",
            description="すべてのメモのキーを表示するのだ",
            input_schema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """ツールを実行するのだ"""
    if name == "save_memo":
        key = arguments["key"]
        content = arguments["content"]
        state.memo[key] = {
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        return [types.TextContent(
            type="text",
            text=f"メモ '{key}' を保存したのだ！"
        )]

    elif name == "get_memo":
        key = arguments["key"]
        if key in state.memo:
            memo = state.memo[key]
            return [types.TextContent(
                type="text",
                text=f"メモ '{key}':\n{memo['content']}\n(保存日時: {memo['timestamp']})"
            )]
        return [types.TextContent(
            type="text",
            text=f"メモ '{key}' は見つからなかったのだ..."
        )]

    elif name == "list_memos":
        if not state.memo:
            return [types.TextContent(
                type="text",
                text="まだメモが保存されていないのだ！"
            )]
        keys = list(state.memo.keys())
        return [types.TextContent(
            type="text",
            text=f"保存されているメモ: {', '.join(keys)}"
        )]

    raise ValueError(f"Unknown tool: {name}")

# 動的リソースの実装
@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """動的にリソースを生成するのだ"""
    resources = [
        types.Resource(
            uri="zundamon://system/info",
            name="システム情報",
            description="現在のシステム情報なのだ",
            mime_type="application/json"
        )
    ]

    # 保存されたメモもリソースとして公開
    for key in state.memo:
        resources.append(types.Resource(
            uri=f"zundamon://memo/{key}",
            name=f"メモ: {key}",
            description=f"保存されたメモ '{key}' の内容なのだ",
            mime_type="text/plain"
        ))

    return resources

@server.get_resource()
async def get_resource(uri: str) -> str:
    """リソースの内容を返すのだ"""
    if uri == "zundamon://system/info":
        info = {
            "server": "advanced-zundamon",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "memo_count": len(state.memo),
            "python_version": os.sys.version
        }
        return json.dumps(info, indent=2, ensure_ascii=False)

    if uri.startswith("zundamon://memo/"):
        key = uri.replace("zundamon://memo/", "")
        if key in state.memo:
            return state.memo[key]["content"]

    raise ValueError(f"Unknown resource: {uri}")

async def main():
    """高度なMCPサーバーを起動するのだ"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### エラーハンドリングとログ

`robust_mcp_server.py`の例：

```python
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("zundamon-mcp")

server = Server("robust-zundamon")

@server.error_handler()
async def handle_error(error: Exception) -> None:
    """エラーをログに記録するのだ"""
    logger.error(f"エラーが発生したのだ: {error}", exc_info=True)

# 以下、通常の実装...
```

## 4. GitHub の MCP サーバーを Claude Code に導入するハンズオン

### Claude Code のセットアップ

1. **Claude Code のインストール確認**

   ```bash
   # Claude Codeがインストールされているか確認
   which claude-code || echo "Claude Codeがインストールされていないのだ！"
   ```

2. **設定ファイルの場所を確認**
   ```bash
   # 設定ディレクトリを作成
   mkdir -p ~/.config/claude-code
   ```

### GitHub から MCP サーバーをクローン

人気のある MCP サーバーを例にするのだ：

```bash
# 作業ディレクトリを作成
mkdir -p ~/mcp-servers
cd ~/mcp-servers

# ファイルシステムMCPサーバーをクローン
git clone https://github.com/modelcontextprotocol/servers.git mcp-official
cd mcp-official/src/filesystem

# Python環境をセットアップ
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Claude Code 用の設定ファイルを作成

`~/.config/claude-code/mcp-config.json`を作成するのだ：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "/home/YOUR_USERNAME/mcp-servers/mcp-official/src/filesystem/venv/bin/python",
      "args": ["-m", "mcp_server_filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/YOUR_USERNAME/workspace"
      }
    },
    "zundamon-advanced": {
      "command": "python3",
      "args": ["/home/YOUR_USERNAME/advanced_mcp_server.py"],
      "env": {}
    }
  }
}
```

### 複数の MCP サーバーを組み合わせる

`combined_setup.sh`スクリプトを作成するのだ：

```bash
#!/bin/bash
# 複数のMCPサーバーをセットアップするスクリプトなのだ

echo "ずんだもんMCPセットアップを開始するのだ！"

# 1. 公式サーバーのセットアップ
setup_official_servers() {
    echo "公式MCPサーバーをセットアップするのだ..."

    # Git関連
    cd ~/mcp-servers/mcp-official/src/git
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
    deactivate

    # Slack（要API token）
    cd ~/mcp-servers/mcp-official/src/slack
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
    deactivate
}

# 2. コミュニティサーバーの例
setup_community_servers() {
    echo "コミュニティサーバーをセットアップするのだ..."

    # 例: GitHub統合
    cd ~/mcp-servers
    git clone https://github.com/example/mcp-github-integration.git
    cd mcp-github-integration
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
}

# 3. カスタムサーバーのテンプレート生成
create_custom_template() {
    echo "カスタムサーバーのテンプレートを作成するのだ..."

    mkdir -p ~/mcp-servers/my-custom-server
    cd ~/mcp-servers/my-custom-server

    # pyproject.tomlを生成
    cat > pyproject.toml << 'EOF'
[project]
name = "my-custom-mcp-server"
version = "0.1.0"
description = "カスタムMCPサーバーなのだ"
requires-python = ">=3.8"
dependencies = [
    "mcp>=1.0.0",
]

[project.scripts]
my-custom-server = "my_custom_server:main"
EOF

    # サーバー実装
    mkdir -p my_custom_server
    cat > my_custom_server/__init__.py << 'EOF'
from .server import main

__all__ = ["main"]
EOF

    cat > my_custom_server/server.py << 'EOF'
#!/usr/bin/env python3
"""カスタムMCPサーバーのテンプレートなのだ"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import asyncio

server = Server("my-custom-server")

# ここにツール、リソース、プロンプトを実装するのだ

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
EOF

    # 仮想環境をセットアップ
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
    deactivate
}

# メイン実行
main() {
    setup_official_servers
    setup_community_servers
    create_custom_template

    echo "すべてのセットアップが完了したのだ！"
    echo "Claude Codeの設定ファイルを更新することを忘れないでほしいのだ！"
}

main
```

### Claude Code での使用例

1. **設定の反映**

   ```bash
   # Claude Codeを再起動して設定を反映
   pkill -f claude-code
   claude-code
   ```

2. **MCP サーバーの動作確認**

   - Claude Code の設定メニューから MCP サーバーの状態を確認
   - コマンドパレットから「MCP: List Available Servers」を実行

3. **実際の使用例**

   ```
   # Claude Codeのチャットで以下のようなコマンドを試すのだ

   "ファイルシステムのリソースを表示して"
   "現在のワークスペースのファイル一覧を取得"
   "GitHubのリポジトリ情報を取得"
   ```

### トラブルシューティング

```bash
# ログの確認
tail -f ~/.config/claude-code/logs/mcp-*.log

# 権限の確認
ls -la ~/.config/claude-code/

# プロセスの確認
ps aux | grep mcp

# ポートの確認（必要な場合）
netstat -tlnp | grep python3
```

### セキュリティのベストプラクティス

1. **環境変数で機密情報を管理**

   ```bash
   # .envファイルを作成
   cat > ~/mcp-servers/.env << EOF
   GITHUB_TOKEN=your_token_here
   SLACK_BOT_TOKEN=your_token_here
   ALLOWED_DIRECTORIES=/home/user/safe_directory
   EOF

   # 設定で環境変数を読み込む
   source ~/mcp-servers/.env
   ```

2. **アクセス制限の設定**
   - ファイルシステムアクセスは特定のディレクトリのみ
   - API トークンは最小限の権限で作成
   - ローカル実行のみに制限

これで MCP サーバーの基礎から実践まで学べたのだ！質問があれば何でも聞いてほしいのだ！
