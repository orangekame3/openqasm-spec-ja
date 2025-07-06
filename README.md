# OpenQASM 3.0 仕様書 日本語版

OpenQASM 3.0 の公式仕様書の日本語翻訳プロジェクトです。

## 概要

このプロジェクトは [OpenQASM](https://github.com/openqasm/openqasm) の仕様書を日本語に翻訳し、日本の量子コンピューティング学習者・研究者・開発者にとって理解しやすい形で提供することを目的としています。

🌐 **オンラインドキュメント**: https://orangekame3.github.io/openqasm-spec-ja/

## ビルド方法

### 必要な環境

- Python 3.8+
- pip

### セットアップ

```bash
# uvを使用した依存関係のインストール
uv sync

# HTMLドキュメントのビルド
uv run make html

# PDFドキュメントのビルド（オプション）
uv run make pdf

# ローカルサーバーでプレビュー
uv run make serve
```

### 従来のpipを使用する場合

```bash
# 依存関係のインストール
pip install -r requirements.txt

# HTMLドキュメントのビルド
make html
```

## プロジェクト構造

```
openqasm-spec-ja/
├── source/           # ソースファイル
│   ├── conf.py      # Sphinx設定
│   ├── index.rst    # メインインデックス
│   ├── intro.rst    # イントロダクション
│   ├── language/    # 言語リファレンス
│   └── grammar/     # 文法定義
├── build/           # ビルド出力
├── requirements.txt # Python依存関係
└── Makefile        # ビルドスクリプト
```

## 翻訳について

現在、基本的な文書構造とイントロダクション部分の翻訳が完了しています。詳細な仕様書の翻訳は順次進めていく予定です。

### 翻訳方針

- **LLMの活用**: この翻訳プロジェクトでは、翻訳の効率性と一貫性を高めるためにLarge Language Model (LLM)を活用しています
- **人間による校正**: LLMによる翻訳結果を人間が校正・検証し、専門用語の正確性を確保します
- **コミュニティ参加**: GitHubを通じて翻訳の改善提案を受け付けています

### 翻訳状況

- ✅ プロジェクト基盤構築
- ✅ イントロダクション
- 🔄 言語仕様（作業中）
- 🔄 文法定義（作業中）
- ⏳ 詳細仕様（予定）

### 注意事項

⚠️ **重要**: この翻訳はLLMを活用して作成されているため、専門用語の翻訳や文脈理解に不正確な部分が含まれる可能性があります。重要な技術的判断を行う際は、必ず[原文](https://github.com/openqasm/openqasm)を確認してください。

## 貢献方法

翻訳の改善や追加についての提案は、GitHubのIssuesまたはPull Requestsでお願いします。

## ライセンス

このプロジェクトは元のOpenQASMプロジェクトと同じライセンスを継承しています。

## 参考リンク

- [OpenQASM 公式リポジトリ](https://github.com/openqasm/openqasm)
- [Qiskit](https://qiskit.org/)
- [免責事項](DISCLAIMER.md)