# LangChain & LangGraph 学習プロジェクト

## 概要

[LangChain と LangGraph による RAG・AI エージェント［実践］入門](https://gihyo.jp/book/2024/978-4-297-14530-9) の内容を実際に手を動かして学習するためのプロジェクト。Anthropic Claude API を使用して RAG システムと AI エージェントの実装を学習中。
github: https://github.com/GenerativeAgents/agent-book

## 技術スタック

- **Python**: 3.12 (3.10 以上対応)
- **パッケージマネージャー**: uv
- **AI API**: Anthropic Claude (claude-sonnet-4-20250514)
- **開発環境**: Jupyter Lab
- **コード品質**: Ruff (リンター・フォーマッター)
- **環境変数管理**: python-dotenv

## クイックスタート

```shell
# 依存関係のインストール
uv sync

# メインスクリプト実行
uv run main.py

# Jupyter Lab起動
uv run jupyter lab

# コード品質チェック
uv run ruff check
```

## 学習目標・実験要素

### 現在の学習範囲

- Anthropic Claude API の基本的な使用方法
- メッセージ作成とレスポンス処理

### 今後学習予定

- LangChain フレームワークの基礎
- LangGraph によるワークフロー制御
- RAG（Retrieval-Augmented Generation）システムの構築
- AI エージェントの実装とチェイン処理
- ベクトルデータベースとの連携

## プロジェクト構造

```
.
├── main.py           # メインスクリプト
├── *.ipynb          # 実験・学習用ノートブック
├── pyproject.toml    # プロジェクト設定とパッケージ情報
├── uv.lock          # パッケージの厳密なバージョン情報
├── .python-version   # Python バージョン指定
└── README.md        # プロジェクト説明と基本コマンド
```

## 開発メモ

### API 設定

- `ANTHROPIC_API_KEY` を `.env` ファイルに設定
- `.env` ファイルは `.gitignore` に追加して秘匿

### 参考リンク

- [Anthropic API Documentation](https://docs.anthropic.com/en/api/overview#python)
- [書籍公式ページ](https://gihyo.jp/book/2024/978-4-297-14530-9)

### つまづいたポイント・気づき

- Claude Sonnet 4 を使用して最新機能を学習中
- uv 使用により高速な依存関係管理を実現

## 今後の計画

1. 書籍の各章に対応したノートブック作成
2. RAG システムの実装実験
3. 実際のユースケースでの AI エージェント構築
4. パフォーマンス最適化とベストプラクティスの学習
