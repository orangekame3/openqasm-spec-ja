タイミング制御と遅延
====================

OpenQASM 3.0では、量子回路の実行タイミングを精密に制御するための包括的な機能を提供します。これにより、量子デコヒーレンス時間内での最適な回路実行や、ハードウェア制約に適応した回路設計が可能になります。

概要
----

タイミング制御の必要性
~~~~~~~~~~~~~~~~~~~~~~

量子コンピューティングでは、以下の理由でタイミング制御が重要です：

- **デコヒーレンス**: 量子ビットの状態は時間とともに劣化
- **同期**: 複数量子ビット操作の正確なタイミング調整
- **最適化**: 回路実行時間の最小化
- **ハードウェア制約**: 物理デバイスの制限への適応

主要な概念
~~~~~~~~~~

1. **duration型**: 具体的な時間長を表現
2. **stretch型**: 可変の時間長を表現
3. **delay命令**: 明示的な待機時間の挿入
4. **barrier命令**: ゲート並び替えの制約
5. **box式**: 回路部分のタイミングスコープ

Duration型
----------

基本的な使用法
~~~~~~~~~~~~~~

``duration``型は時間の長さを表現する専用の型です：

.. code-block:: qasm3

   // 基本的な duration の宣言
   duration d1 = 100ns;     // ナノ秒
   duration d2 = 1.5μs;     // マイクロ秒
   duration d3 = 2ms;       // ミリ秒
   duration d4 = 0.1s;      // 秒

サポートされる単位
~~~~~~~~~~~~~~~~~~

SI単位系：

.. code-block:: qasm3

   duration t1 = 1s;        // 秒
   duration t2 = 500ms;     // ミリ秒
   duration t3 = 250μs;     // マイクロ秒（µsまたはusでも可）
   duration t4 = 10ns;      // ナノ秒

バックエンド依存単位：

.. code-block:: qasm3

   // デバイス固有の時間単位
   duration dt_time = 100dt; // dt: ハードウェア固有の最小時間単位

演算
~~~~

duration型は算術演算をサポートします：

.. code-block:: qasm3

   duration base = 100ns;
   duration double_time = 2 * base;      // 200ns
   duration sum_time = base + 50ns;      // 150ns
   duration diff_time = base - 20ns;     // 80ns

比較演算も可能：

.. code-block:: qasm3

   duration t1 = 100ns;
   duration t2 = 200ns;
   
   bool is_longer = (t2 > t1);          // true
   bool is_equal = (t1 == 100ns);       // true

Stretch型
---------

概念と用途
~~~~~~~~~~

``stretch``型は可変の非負時間長を表現し、コンパイル時に最適化されます：

.. code-block:: qasm3

   stretch flexible_delay;              // 可変遅延
   stretch[100ns, 500ns] bounded_delay; // 境界付き可変遅延

stretch型の特徴：

- コンパイル時に実際の値が決定される
- 回路の最適化時に調整可能
- 最小値と最大値を指定可能

実用例
~~~~~~

.. code-block:: qasm3

   qubit[2] q;
   stretch adaptive_delay;
   
   // 最適化可能な回路構造
   h q[0];
   delay[adaptive_delay] q[0];  // コンパイラが最適な遅延を決定
   cx q[0], q[1];

境界付きstretch：

.. code-block:: qasm3

   // 10ns以上500ns以下の可変遅延
   stretch[10ns, 500ns] bounded_stretch;
   
   delay[bounded_stretch] q;

Delay命令
---------

基本構文
~~~~~~~~

``delay``命令は明示的な待機時間を挿入します：

.. code-block:: qasm3

   qubit q;
   
   // 固定遅延
   delay[100ns] q;
   
   // 変数による遅延
   duration wait_time = 250ns;
   delay[wait_time] q;

複数量子ビットへの適用
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[3] qreg;
   
   // 全量子ビットに同じ遅延
   delay[100ns] qreg;
   
   // 特定の量子ビットに遅延
   delay[50ns] qreg[0];
   delay[75ns] qreg[1], qreg[2];

同期効果
~~~~~~~~

複数量子ビットに対するdelay命令は同期ポイントとして機能します：

.. code-block:: qasm3

   qubit[2] q;
   
   h q[0];                    // 時刻 t0
   x q[1];                    // 時刻 t0（並列実行）
   
   delay[100ns] q[0], q[1];   // 同期ポイント: 両方とも100ns待機
   
   cx q[0], q[1];             // 時刻 t0 + 100ns

実用的なタイミング制御
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[2] q;
   duration gate_time = 20ns;
   duration readout_delay = 1μs;
   
   // 精密なタイミング制御
   h q[0];
   delay[gate_time] q[0];     // ゲート実行時間を明示
   
   cx q[0], q[1];
   delay[readout_delay] q;    // 測定前の安定化時間
   
   bit[2] c = measure q;

Barrier命令
-----------

基本的な使用法
~~~~~~~~~~~~~~

``barrier``命令はゲートの並び替えを防ぎます：

.. code-block:: qasm3

   qubit[3] q;
   
   h q[0];
   h q[1];
   barrier q[0], q[1];        // この前後でゲートの並び替えを禁止
   cx q[0], q[1];
   cx q[1], q[2];

部分的なバリア
~~~~~~~~~~~~~~

特定の量子ビット間のみに制約を設定：

.. code-block:: qasm3

   qubit[4] q;
   
   h q[0];
   h q[1];
   h q[2];
   h q[3];
   
   barrier q[0], q[1];        // q[0], q[1]のみ制約
   // q[2], q[3]は自由に並び替え可能
   
   cx q[0], q[1];
   cx q[2], q[3];

全量子ビットバリア
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[4] q;
   
   // 準備フェーズ
   h q;
   
   barrier q;                 // 全量子ビットで同期
   
   // エンタングリングフェーズ
   for i in [0:2] {
       cx q[i], q[i+1];
   }

Box式
-----

基本構文
~~~~~~~~

``box``式は回路の一部をタイミングスコープで囲みます：

.. code-block:: qasm3

   qubit[2] q;
   
   box {
       h q[0];
       cx q[0], q[1];
       h q[1];
   }

時間制約付きbox
~~~~~~~~~~~~~~~

最大実行時間を指定：

.. code-block:: qasm3

   qubit[2] q;
   
   box [maxduration[500ns]] {
       h q[0];
       delay[100ns] q[0];
       cx q[0], q[1];
       // 合計時間が500nsを超えてはいけない
   }

固定時間box
~~~~~~~~~~~

正確な実行時間を強制：

.. code-block:: qasm3

   qubit q;
   
   box [duration[200ns]] {
       h q;
       // 残り時間は自動的に遅延で埋められる
   }

ネストしたbox
~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[3] q;
   
   box [maxduration[1μs]] {
       h q[0];
       
       box [duration[100ns]] {
           x q[1];
           delay[80ns] q[1];    // 合計100nsに調整
       }
       
       cx q[0], q[2];
   }

実践的な例
----------

量子エラー修正での使用
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[7] data;
   qubit[6] ancilla;
   duration syndrome_time = 1μs;
   
   // シンドローム測定サイクル
   box [duration[syndrome_time]] {
       // パリティ測定
       for i in [0:5] {
           cx data[i], ancilla[i];
           cx data[i+1], ancilla[i];
       }
       
       // 安定化時間
       stretch stabilization;
       delay[stabilization] data;
       
       // シンドローム読み出し
       bit[6] syndrome = measure ancilla;
   }

アダプティブアルゴリズム
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   bit result;
   duration max_attempts = 10μs;
   
   box [maxduration[max_attempts]] {
       int attempts = 0;
       
       repeat {
           h q;
           result = measure q;
           
           if (result) break;
           
           attempts += 1;
           reset q;
           delay[100ns] q;        // 安定化遅延
       } until (attempts >= 100);
   }

並列量子回路
~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[4] q;
   duration sync_point = 500ns;
   
   // 並列処理ブロック1
   box [duration[sync_point]] {
       h q[0];
       ry(π/4) q[0];
       stretch pad1;
       delay[pad1] q[0];
   }
   
   // 並列処理ブロック2（同期）
   box [duration[sync_point]] {
       x q[1];
       rz(π/3) q[1];
       stretch pad2;
       delay[pad2] q[1];
   }
   
   // 同期後の操作
   barrier q[0], q[1];
   cx q[0], q[1];

最適化とコンパイル
------------------

タイミング最適化
~~~~~~~~~~~~~~~~

コンパイラによる自動最適化：

.. code-block:: qasm3

   qubit[2] q;
   
   // 最適化前
   h q[0];
   delay[100ns] q[0];
   h q[1];
   delay[100ns] q[1];
   cx q[0], q[1];
   
   // 最適化後（概念的）
   // h q[0], q[1];  // 並列実行
   // delay[100ns] q;  // 統合された遅延
   // cx q[0], q[1];

Stretch解決
~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   stretch flexible;
   
   box [duration[1μs]] {
       h q;
       delay[flexible] q;  // flexibleは自動的に計算される
       x q;
   }

ハードウェア制約
----------------

デバイス固有の制約
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // ハードウェア制約の例
   duration min_gate_separation = 10ns;
   duration coherence_time = 100μs;
   
   qubit[2] q;
   
   h q[0];
   delay[min_gate_separation] q[0];  // 最小分離時間
   cx q[0], q[1];
   
   box [maxduration[coherence_time]] {
       // デコヒーレンス時間内で実行
       for i in [0:9] {
           ry(π/10) q[0];
           delay[1μs] q[0];
       }
   }

実行時考慮事項
--------------

タイミング精度
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 高精度タイミングが必要な場合
   duration precise_delay = 123.456ns;
   
   qubit q;
   h q;
   delay[precise_delay] q;    // ハードウェアの精度に依存
   measure q;

リアルタイム制約
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   bit feedback;
   duration reaction_time = 50ns;  // リアルタイム応答時間
   
   feedback = measure q;
   
   box [maxduration[reaction_time]] {
       if (feedback) {
           x q;  // 高速フィードバック
       }
   }

デバッグとプロファイリング
--------------------------

タイミング解析
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // タイミング解析用の注釈
   duration analysis_start = now();  // 仮想的な時刻取得
   
   box [duration[1μs]] {
       h q[0];
       cx q[0], q[1];
   }
   
   duration analysis_end = now();
   duration actual_time = analysis_end - analysis_start;

まとめ
------

OpenQASMのタイミング制御機能は：

- **精密制御**: nanosecond精度のタイミング管理
- **柔軟性**: stretchによる適応的最適化
- **同期**: barrier命令による明示的制約
- **構造化**: box式による論理的グループ化
- **最適化**: コンパイラによる自動調整

これらの機能により、高度な量子アルゴリズムの実装と、ハードウェア制約への適応が可能になります。