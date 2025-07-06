基本命令
========

OpenQASMは量子計算における基本的な操作を実行するための組み込み命令を提供します。これらの命令は量子ビットの初期化、測定、および特殊な制御に使用されます。

概要
----

基本命令には以下の3つがあります：

- **reset**: 量子ビットを |0⟩ 状態に初期化
- **measure**: Z基底での測定を実行
- **nop**: 無操作（明示的な量子ビット使用マーカー）

reset命令
---------

``reset``命令は量子ビットまたは量子レジスタを基底状態 |0⟩ に初期化します。

構文
~~~~

.. code-block:: text

   reset qubit;
   reset qubit[];

基本的な使用法
~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   qubit[5] qreg;
   
   // 単一量子ビットのリセット
   reset q;
   
   // 量子レジスタ全体のリセット
   reset qreg;
   
   // 特定の量子ビットのリセット
   reset qreg[0];
   reset qreg[1:3];  // qreg[1], qreg[2], qreg[3]をリセット

動作の詳細
~~~~~~~~~~

``reset``命令の実行により：

1. 対象の量子ビットは確実に |0⟩ 状態になる
2. 以前の量子もつれは破棄される
3. 実装依存の最適化が可能（測定+条件付きX操作など）

.. code-block:: qasm3

   qubit q;
   
   // 任意の状態を準備
   h q;
   ry(π/3) q;
   
   // 確実に |0⟩ に戻す
   reset q;
   
   // この時点でqは |0⟩ 状態

実用例
~~~~~~

.. code-block:: qasm3

   // 量子アルゴリズムの繰り返し実行
   qubit[3] qubits;
   bit[3] results;
   
   for i in [0:9] {
       // 初期化
       reset qubits;
       
       // 量子回路の実行
       h qubits[0];
       ctrl @ x qubits[0], qubits[1];
       ctrl @ x qubits[1], qubits[2];
       
       // 測定
       results = measure qubits;
       
       // 結果の処理...
   }

measure命令
-----------

``measure``命令は量子ビットのZ基底測定を実行し、結果を古典ビットに代入します。

構文
~~~~

.. code-block:: text

   bit = measure qubit;
   bit[] = measure qubit[];

基本的な使用法
~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   qubit[5] qreg;
   bit c;
   bit[5] creg;
   
   // 単一量子ビットの測定
   c = measure q;
   
   // 量子レジスタ全体の測定
   creg = measure qreg;
   
   // 特定の量子ビットの測定
   creg[0] = measure qreg[0];

測定の性質
~~~~~~~~~~

Z基底測定では：

- 測定結果は 0 または 1
- 確率は量子状態の振幅の二乗に従う
- 測定後、量子ビットは測定結果に対応する固有状態に収束

.. code-block:: qasm3

   qubit q;
   bit result;
   
   // 重ね合わせ状態の準備
   h q;  // |+⟩ = (|0⟩ + |1⟩)/√2
   
   // 測定（50%の確率で0または1）
   result = measure q;

条件付き操作
~~~~~~~~~~~~

測定結果に基づく条件分岐：

.. code-block:: qasm3

   qubit[2] q;
   bit[2] c;
   
   // Bell状態の準備
   h q[0];
   ctrl @ x q[0], q[1];
   
   // 最初の量子ビットを測定
   c[0] = measure q[0];
   
   // 測定結果に基づく操作
   if (c[0]) {
       x q[1];  // c[0]=1の場合、q[1]を反転
   }
   
   c[1] = measure q[1];

測定とデコヒーレンス
~~~~~~~~~~~~~~~~~~

測定は非可逆操作です：

.. code-block:: qasm3

   qubit q;
   bit c;
   
   // エンタングルメントの準備
   h q;
   
   // 測定によりエンタングルメントが破壊される
   c = measure q;
   
   // 測定後、qは古典的な0または1の状態

nop命令
-------

``nop``（No Operation）命令は量子ビットに対して何も操作を行いませんが、コンパイラに対して明示的に量子ビットが「使用」されていることを示します。

構文
~~~~

.. code-block:: text

   nop qubit[, qubit, ...];

基本的な使用法
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 単一量子ビットに対するnop
   nop $2;
   
   // 複数量子ビットに対するnop
   nop $3, $0, $5;

用途と重要性
~~~~~~~~~~~~

``nop``命令は以下の場面で重要です：

1. **ボックス化されたスコープ**: 量子ビットの明示的な使用表明
2. **並列実行の制御**: タイミング調整
3. **デバッグ**: 量子ビットの状態追跡

.. code-block:: qasm3

   // ボックス化されたスコープでの使用例
   box [maxduration[1us]] {
       h $0;
       nop $1;  // $1も同じボックス内で使用されることを明示
       h $2;
   }

実装の考慮事項
~~~~~~~~~~~~~~

- **最適化**: コンパイラはnopを除去する可能性があるが、スケジューリング情報は保持
- **タイミング**: ハードウェアレベルでの同期に使用
- **並列性**: 複数量子ビットの同時「使用」の表現

.. code-block:: qasm3

   // 並列操作の同期
   box {
       h $0;
       h $1;
       nop $2, $3;  // $2と$3も同時に「使用」
   }

命令の組み合わせ
----------------

基本命令の効果的な組み合わせ例：

量子状態のトモグラフィー
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   bit[3] results;
   
   // 未知の状態を準備（例）
   ry(π/3) q;
   
   // X基底測定
   h q;
   results[0] = measure q;
   reset q;
   
   // Y基底測定
   ry(π/3) q;  // 状態を再準備
   s_dg q;
   h q;
   results[1] = measure q;
   reset q;
   
   // Z基底測定
   ry(π/3) q;  // 状態を再準備
   results[2] = measure q;

エラー検出
~~~~~~~~~~

.. code-block:: qasm3

   qubit[3] data;
   qubit[2] ancilla;
   bit[2] syndrome;
   
   // データ量子ビットの準備
   h data[0];
   ctrl @ x data[0], data[1];
   
   // シンドローム測定
   ctrl @ x data[0], ancilla[0];
   ctrl @ x data[1], ancilla[0];
   ctrl @ x data[1], ancilla[1];
   ctrl @ x data[2], ancilla[1];
   
   syndrome = measure ancilla;
   
   // エラー修正
   if (syndrome == 0b01) x data[0];
   else if (syndrome == 0b10) x data[2];
   else if (syndrome == 0b11) x data[1];

実行時の考慮事項
----------------

デコヒーレンス時間
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   bit c;
   
   // 長時間の操作は避ける
   h q;
   delay[1ms];  // デコヒーレンスにより情報が失われる可能性
   c = measure q;

測定の順序
~~~~~~~~~~

.. code-block:: qasm3

   qubit[2] q;
   bit[2] c;
   
   // Bell状態
   h q[0];
   ctrl @ x q[0], q[1];
   
   // 測定順序は結果に影響しない（同時測定）
   c[0] = measure q[0];
   c[1] = measure q[1];

最適化とコンパイル
------------------

コンパイラの最適化
~~~~~~~~~~~~~~~~~~

- **測定の遅延**: 不要な早期測定の回避
- **リセットの最適化**: 測定+条件付きX操作への変換
- **nopの除去**: タイミング情報を保持しつつ物理操作を最小化

.. code-block:: qasm3

   qubit q;
   bit c;
   
   // 最適化前
   reset q;
   h q;
   c = measure q;
   reset q;
   
   // 最適化後（概念的）
   // reset操作が測定+条件付きX操作に変換される可能性

まとめ
------

OpenQASMの基本命令は：

- **初期化**: resetによる確実な状態準備
- **観測**: measureによる量子から古典への情報変換
- **制御**: nopによる明示的な量子ビット管理

これらの命令は量子アルゴリズムの実装において不可欠な要素です。