文法定義
========

.. note::
   この章は現在翻訳作業中です。詳細な内容は今後追加される予定です。

OpenQASM 3.0の正式な文法定義について説明します。

.. toctree::
   :maxdepth: 2
   :caption: 文法仕様

   字句解析 <lexical>
   構文解析 <syntax>
   意味解析 <semantics>

概要
----

OpenQASM 3.0の文法はEBNF（Extended Backus-Naur Form）記法を使用して定義されています。

基本構造
--------

プログラムの基本構造は以下の通りです：

.. code-block:: ebnf

   program = version_string (statement)*
   statement = quantum_statement | classical_statement
   
文法ルール
-----------

詳細な文法ルールについては、各セクションを参照してください。

.. note::
   完全な文法定義の翻訳は順次進めていきます。最新の情報については原文を参照してください。