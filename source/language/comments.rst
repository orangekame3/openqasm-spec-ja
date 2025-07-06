コメントと基本構文
==================

OpenQASMは、コードの可読性と保守性を向上させるために、コメント機能とファイル構造の管理機能を提供します。これらの機能により、大規模なプログラムの文書化と組織化が可能になります。

コメント構文
------------

OpenQASMは2種類のコメント構文をサポートしています：

単一行コメント
~~~~~~~~~~~~~~

``//``で始まり、行の終端まで続くコメント：

.. code-block:: qasm3

   // これは単一行コメントです
   qubit q;           // 量子ビットの宣言
   h q;               // アダマールゲートの適用
   bit c = measure q; // 測定の実行

複数行コメント（ブロックコメント）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/*``で始まり``*/``で終わるコメント：

.. code-block:: qasm3

   /*
    * これは複数行にわたる
    * ブロックコメントです
    */
   
   qubit q;
   
   /*
   Bell状態の準備回路:
   1. 最初の量子ビットをアダマールゲートで重ね合わせ状態にする
   2. CNOTゲートで2番目の量子ビットとエンタングルする
   */
   h q[0];
   ctrl @ x q[0], q[1];

ネストしたコメント
~~~~~~~~~~~~~~~~~~

ブロックコメントはネストできません：

.. code-block:: qasm3

   /*
   外側のコメント開始
   /* 内側のコメント */ // この*/で外側のコメントが終了
   ここは通常のコードとして解釈される
   */

文書化のベストプラクティス
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   /*
    * 変分量子固有値ソルバー（VQE）の実装
    * Author: OpenQASM翻訳チーム
    * Date: 2024
    */
   
   // ハミルトニアンのパラメータ
   const float h_field = 0.5;  // 磁場の強度
   
   // アンザッツの深さ
   const int circuit_depth = 4;
   
   def vqe_ansatz(qubit[4] qubits, float[8] params) {
       // 変分回路の実装
       // params[0:3]: 最初の層の回転角
       // params[4:7]: 二番目の層の回転角
       
       for i in [0:3] {
           ry(params[i]) qubits[i];    // Y回転
       }
       
       // エンタングリング層
       for i in [0:2] {
           ctrl @ x qubits[i], qubits[i+1];
       }
       ctrl @ x qubits[3], qubits[0];  // 周期境界条件
   }

バージョン文字列
----------------

バージョン宣言の構文
~~~~~~~~~~~~~~~~~~~~

OpenQASMプログラムは、オプションでバージョン文字列を最初の非コメント行に記述できます：

.. code-block:: text

   OPENQASM M.m;

ここで：
- ``M``: メジャーバージョン番号
- ``m``: マイナーバージョン番号（省略可能、省略時は0）

基本的な使用例
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // OpenQASM 3.0プログラム
   OPENQASM 3.0;
   
   qubit q;
   h q;
   bit c = measure q;

.. code-block:: qasm3

   /*
    * 古いバージョンとの互換性を考慮したプログラム
    */
   OPENQASM 3;  // マイナーバージョンを省略（3.0と解釈）
   
   // プログラム本体

バージョン互換性
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.1;  // 将来のマイナーアップデート用
   
   // 新機能を使用したプログラム

バージョン宣言の制約
~~~~~~~~~~~~~~~~~~~~

- バージョン文字列は最初の非コメント行にのみ記述可能
- プログラム内で複数回宣言することはできません
- コメントの後であれば任意の位置に配置可能

.. code-block:: qasm3

   // プログラムのヘッダーコメント
   /*
    * 複雑な量子アルゴリズムの実装
    */
   
   OPENQASM 3.0;  // 正しい位置
   
   qubit q;
   // OPENQASM 3.0;  // エラー: 2回目の宣言

ファイルインクルード
--------------------

include文の構文
~~~~~~~~~~~~~~~

外部ファイルの内容を現在のプログラムに含めるには``include``文を使用します：

.. code-block:: text

   include "filename";

基本的な使用例
~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.0;
   
   // 標準ゲートライブラリをインクルード
   include "stdgates.inc";
   
   qubit[2] q;
   
   // stdgates.incで定義されたゲートを使用
   x q[0];
   y q[1];
   cx q[0], q[1];

複数ファイルのインクルード
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.0;
   
   // 標準ライブラリ
   include "stdgates.inc";
   
   // カスタムゲート定義
   include "custom_gates.inc";
   
   // 量子エラー修正ライブラリ
   include "qec_lib.inc";
   
   // プログラム本体
   qubit[7] code_qubits;
   qubit[3] syndrome_qubits;

インクルードの制約
~~~~~~~~~~~~~~~~~~

- ``include``文はグローバルスコープでのみ使用可能
- 関数やゲート定義内では使用できません
- 循環インクルードは避ける必要があります

.. code-block:: qasm3

   OPENQASM 3.0;
   include "gates.inc";  // 正しい: グローバルスコープ
   
   def my_function() {
       // include "other.inc";  // エラー: 関数内では不可
   }

条件付きインクルード
~~~~~~~~~~~~~~~~~~~~

OpenQASMは条件付きインクルードを直接サポートしていませんが、設計パターンで対応可能：

.. code-block:: qasm3

   // main.qasm
   OPENQASM 3.0;
   
   // 必要に応じて異なるライブラリをインクルード
   include "basic_gates.inc";      // 基本セット
   // include "extended_gates.inc";  // 拡張セット（コメントアウト）

標準ライブラリファイル
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 典型的なstdgates.incの内容例
   /*
    * OpenQASM 3.0 標準ゲートライブラリ
    */
   
   // パウリゲート
   gate x q { U(π, 0, π) q; }
   gate y q { U(π, π/2, π/2) q; }
   gate z q { U(0, 0, π) q; }
   
   // アダマールゲート
   gate h q { U(π/2, 0, π) q; }
   
   // 位相ゲート
   gate s q { U(0, 0, π/2) q; }
   gate t q { U(0, 0, π/4) q; }

プリプロセッサ機能
------------------

マクロ定義（概念的）
~~~~~~~~~~~~~~~~~~~~

OpenQASMは直接的なマクロをサポートしませんが、定数とゲート定義で類似の効果を実現：

.. code-block:: qasm3

   // 定数による「マクロ」
   const int N_QUBITS = 5;
   const float ROTATION_ANGLE = π/4;
   
   qubit[N_QUBITS] qreg;
   
   // ゲート定義による「マクロ」
   gate my_rotation q {
       ry(ROTATION_ANGLE) q;
   }

ファイル組織のパターン
----------------------

プロジェクト構造
~~~~~~~~~~~~~~~~

.. code-block:: text

   project/
   ├── main.qasm          // メインプログラム
   ├── lib/
   │   ├── stdgates.inc   // 標準ゲート
   │   ├── qft.inc        // 量子フーリエ変換
   │   └── vqe.inc        // VQEライブラリ
   └── algorithms/
       ├── shor.qasm      // Shorのアルゴリズム
       └── grover.qasm    // Groverのアルゴリズム

モジュラー設計
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // algorithms/shor.qasm
   OPENQASM 3.0;
   
   include "../lib/stdgates.inc";
   include "../lib/qft.inc";
   
   /*
    * Shorのアルゴリズム実装
    * 15 = 3 × 5 の因数分解例
    */
   
   def period_finding(qubit[4] control, qubit[4] target) {
       // 周期発見ルーチン
   }

名前空間の管理
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // lib/custom_gates.inc
   /*
    * カスタムゲートライブラリ
    * プレフィックス: cg_ (custom gates)
    */
   
   gate cg_controlled_ry(theta) ctrl, target {
       ctrl @ ry(theta) ctrl, target;
   }
   
   gate cg_bell_prep ctrl, target {
       h ctrl;
       ctrl @ x ctrl, target;
   }

実行時の考慮事項
----------------

コンパイル順序
~~~~~~~~~~~~~~

include文は静的に解決されるため、コンパイル時にファイルが存在する必要があります：

.. code-block:: qasm3

   OPENQASM 3.0;
   
   // コンパイル時に解決される
   include "gates.inc";
   
   // 実行時のファイル操作は不可
   // include runtime_file;  // エラー

パフォーマンスへの影響
~~~~~~~~~~~~~~~~~~~~~~

- include文はコンパイル時に処理されるため、実行時のオーバーヘッドはありません
- 大きなライブラリファイルのインクルードはコンパイル時間に影響する可能性

デバッグとトラブルシューティング
--------------------------------

コメントによるデバッグ
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[3] q;
   
   // デバッグ用の中間測定
   h q[0];
   // bit debug = measure q[0];  // 一時的にコメントアウト
   
   ctrl @ x q[0], q[1];
   ctrl @ x q[1], q[2];

条件付きコンパイル（パターン）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // DEBUG mode (手動で切り替え)
   /*
   // デバッグ版
   def debug_measure(qubit q) -> bit {
       bit result = measure q;
       // print(result);  // 仮想的なデバッグ出力
       return result;
   }
   */
   
   // リリース版
   def debug_measure(qubit q) -> bit {
       return measure q;
   }

まとめ
------

OpenQASMのコメントと基本構文機能は：

- **文書化**: コードの理解と保守性の向上
- **バージョン管理**: 言語バージョンの明示的指定
- **モジュラリティ**: ファイル分割によるコード組織化
- **再利用性**: ライブラリファイルの共有

これらの機能により、大規模で保守性の高い量子プログラムの開発が可能になります。