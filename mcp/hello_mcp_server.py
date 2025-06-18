#!/usr/bin/env python3
"""ずんだもんの最小MCPサーバーなのだ！"""

import sys
import logging
import asyncio

# エラーハンドリングを強化するのだ
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types
except ImportError as e:
    print(f"MCPパッケージのインポートに失敗したのだ: {e}", file=sys.stderr)
    print("pip install mcp でインストールしてほしいのだ！", file=sys.stderr)
    sys.exit(1)

# ログ設定を追加するのだ
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("zundamon_mcp.log"),
        # STDERRに出力（STDOUTはMCP通信に使用）
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger(__name__)

try:
    # サーバーインスタンスを作成するのだ
    server = Server("hello-zundamon")
    logger.info("ずんだもんMCPサーバーを初期化したのだ！")
except Exception as e:
    logger.error(f"サーバー初期化エラーなのだ: {e}", exc_info=True)
    sys.exit(1)


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """利用可能なリソースを返すのだ"""
    logger.debug("list_resources()が呼ばれたのだ")
    try:
        resources = [
            types.Resource(
                uri="zundamon://greeting",
                name="ずんだもんの挨拶",
                description="ずんだもんが挨拶をするのだ！",
                mimeType="text/plain",  # mimeType（キャメルケース）に修正
            )
        ]
        logger.debug(f"リソース数: {len(resources)}")
        return resources
    except Exception as e:
        logger.error(f"list_resources エラー: {e}", exc_info=True)
        raise


@server.read_resource()
async def get_resource(uri: str) -> str:
    """リソースの内容を返すのだ"""
    logger.debug(f"get_resource()が呼ばれたのだ: uri={uri}")
    try:
        if uri == "zundamon://greeting":
            message = "ぼくはずんだもん！ずんだの精霊なのだ！よろしくなのだ！"
            logger.info(f"挨拶メッセージを返すのだ: {message}")
            return message
        logger.error(f"未知のリソースなのだ: {uri}")
        raise ValueError(f"Unknown resource: {uri}")
    except Exception as e:
        logger.error(f"get_resource エラー: {e}", exc_info=True)
        raise


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """利用可能なツールを返すのだ"""
    logger.debug("list_tools()が呼ばれたのだ")
    try:
        tools = [
            types.Tool(
                name="calculate_zunda",
                description="ずんだもちの必要量を計算するのだ",
                inputSchema={  # inputSchema（キャメルケース）に修正
                    "type": "object",
                    "properties": {
                        "people": {"type": "integer", "description": "人数"}
                    },
                    "required": ["people"],
                },
            )
        ]
        logger.debug(f"ツール数: {len(tools)}")
        return tools
    except Exception as e:
        logger.error(f"list_tools エラー: {e}", exc_info=True)
        raise


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """ツールを実行するのだ"""
    logger.debug(f"call_tool()が呼ばれたのだ: name={name}, arguments={arguments}")

    try:
        if name == "calculate_zunda":
            people = arguments.get("people", 1)
            logger.info(f"ずんだもち計算: {people}人分")

            # 入力値の検証を追加するのだ
            if not isinstance(people, int) or people < 1:
                logger.warning(f"無効な人数が指定されたのだ: {people}")
                people = 1

            zunda_per_person = 3  # 一人あたり3個なのだ
            total = people * zunda_per_person
            result_text = f"{people}人分のずんだもちは{total}個必要なのだ！"
            logger.info(f"計算結果: {result_text}")

            return [types.TextContent(type="text", text=result_text)]

        logger.error(f"未知のツールなのだ: {name}")
        raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"call_tool エラー: {e}", exc_info=True)
        raise


# メインエントリーポイント
async def main():
    """サーバーを起動するのだ"""
    logger.info("ずんだもんMCPサーバーを起動するのだ！")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Event loop: {asyncio.get_event_loop()}")

    try:
        # STDIOサーバーとして起動
        async with stdio_server() as (read_stream, write_stream):
            logger.info("STDIOサーバーが開始されたのだ")
            logger.info("接続を待っているのだ...")

            # サーバーを実行
            init_options = server.create_initialization_options()
            logger.debug(f"初期化オプション: {init_options}")

            await server.run(read_stream, write_stream, init_options)

    except Exception as e:
        logger.error(f"サーバーエラーが発生したのだ: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        logger.info("=== ずんだもんMCPサーバー起動 ===")
        # Windowsでのイベントループポリシー設定
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        # サーバーを起動
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("サーバーが中断されたのだ")
    except Exception as e:
        logger.error(f"予期しないエラーなのだ: {e}", exc_info=True)
        sys.exit(1)
