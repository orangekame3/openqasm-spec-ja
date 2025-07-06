標準ライブラリ
==============

OpenQASM 3.0には、最も一般的に使用される量子ゲートを定義した標準ライブラリが付属しています。このライブラリは``stdgates.inc``ファイルとして提供され、量子回路設計における基本的な構成要素を提供します。

概要
----

標準ライブラリの特徴
~~~~~~~~~~~~~~~~~~~~

- **統一性**: よく知られた量子ゲートの標準的な定義
- **互換性**: OpenQASM 2.0との後方互換性
- **拡張性**: カスタムゲートとの組み合わせが可能
- **最適化**: ハードウェア固有の実装が可能

ライブラリの使用
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.0;
   include "stdgates.inc";  // 標準ライブラリをインクルード
   
   qubit[2] q;
   
   // 標準ライブラリのゲートを使用
   h q[0];           // アダマールゲート
   cx q[0], q[1];    // 制御NOTゲート

単一量子ビットゲート
--------------------

パウリゲート
~~~~~~~~~~~~

基本的なパウリ演算子：

.. code-block:: qasm3

   // パウリXゲート（NOTゲート）
   gate x q { U(π, 0, π) q; }
   
   // パウリYゲート
   gate y q { U(π, π/2, π/2) q; }
   
   // パウリZゲート
   gate z q { U(0, 0, π) q; }

使用例：

.. code-block:: qasm3

   qubit q;
   
   x q;  // |0⟩ → |1⟩ または |1⟩ → |0⟩
   y q;  // |0⟩ → i|1⟩ または |1⟩ → -i|0⟩
   z q;  // |0⟩ → |0⟩ または |1⟩ → -|1⟩

アダマールゲート
~~~~~~~~~~~~~~~~

重ね合わせ状態を作成する基本ゲート：

.. code-block:: qasm3

   gate h q { U(π/2, 0, π) q; }

.. math::

   H = \frac{1}{\sqrt{2}}\begin{pmatrix}
   1 & 1 \\
   1 & -1
   \end{pmatrix}

使用例：

.. code-block:: qasm3

   qubit q;
   h q;  // |0⟩ → (|0⟩ + |1⟩)/√2

位相ゲート
~~~~~~~~~~

位相を操作するゲート：

.. code-block:: qasm3

   // Sゲート（π/2位相）
   gate s q { U(0, 0, π/2) q; }
   
   // S†ゲート（Sの逆操作）
   gate sdg q { U(0, 0, -π/2) q; }
   
   // Tゲート（π/4位相）
   gate t q { U(0, 0, π/4) q; }
   
   // T†ゲート（Tの逆操作）
   gate tdg q { U(0, 0, -π/4) q; }

.. math::

   S = \begin{pmatrix}
   1 & 0 \\
   0 & i
   \end{pmatrix}, \quad
   T = \begin{pmatrix}
   1 & 0 \\
   0 & e^{i\pi/4}
   \end{pmatrix}

回転ゲート
~~~~~~~~~~

パラメータ化された回転操作：

.. code-block:: qasm3

   // X軸周りの回転
   gate rx(θ) q { U(θ, -π/2, π/2) q; }
   
   // Y軸周りの回転
   gate ry(θ) q { U(θ, 0, 0) q; }
   
   // Z軸周りの回転
   gate rz(θ) q { U(0, 0, θ) q; }

.. math::

   R_x(\theta) = \begin{pmatrix}
   \cos(\theta/2) & -i\sin(\theta/2) \\
   -i\sin(\theta/2) & \cos(\theta/2)
   \end{pmatrix}

使用例：

.. code-block:: qasm3

   qubit q;
   
   rx(π/4) q;  // X軸周りにπ/4回転
   ry(π/3) q;  // Y軸周りにπ/3回転
   rz(π/2) q;  // Z軸周りにπ/2回転

2量子ビットゲート
-----------------

制御ゲート
~~~~~~~~~~

最も重要な2量子ビットゲートです：

.. code-block:: qasm3

   // 制御NOTゲート（CNOTゲート）
   gate cx ctrl, target { ctrl @ x ctrl, target; }
   
   // 制御Yゲート
   gate cy ctrl, target { ctrl @ y ctrl, target; }
   
   // 制御Zゲート
   gate cz ctrl, target { ctrl @ z ctrl, target; }

.. math::

   \text{CNOT} = \begin{pmatrix}
   1 & 0 & 0 & 0 \\
   0 & 1 & 0 & 0 \\
   0 & 0 & 0 & 1 \\
   0 & 0 & 1 & 0
   \end{pmatrix}

使用例：

.. code-block:: qasm3

   qubit[2] q;
   
   // Bell状態の準備
   h q[0];
   cx q[0], q[1];

制御回転ゲート
~~~~~~~~~~~~~~

パラメータ化された制御回転：

.. code-block:: qasm3

   // 制御X回転
   gate crx(theta) ctrl, target { ctrl @ rx(theta) ctrl, target; }
   
   // 制御Y回転
   gate cry(theta) ctrl, target { ctrl @ ry(theta) ctrl, target; }
   
   // 制御Z回転
   gate crz(theta) ctrl, target { ctrl @ rz(theta) ctrl, target; }

SWAPゲート
~~~~~~~~~~

2つの量子ビットの状態を交換：

.. code-block:: qasm3

   gate swap a, b {
       cx a, b;
       cx b, a;
       cx a, b;
   }

.. math::

   \text{SWAP} = \begin{pmatrix}
   1 & 0 & 0 & 0 \\
   0 & 0 & 1 & 0 \\
   0 & 1 & 0 & 0 \\
   0 & 0 & 0 & 1
   \end{pmatrix}

3量子ビットゲート
-----------------

Toffoliゲート（CCXゲート）
~~~~~~~~~~~~~~~~~~~~~~~~~~

双制御NOTゲート：

.. code-block:: qasm3

   gate ccx ctrl1, ctrl2, target {
       h target;
       cx ctrl2, target;
       tdg target;
       cx ctrl1, target;
       t target;
       cx ctrl2, target;
       tdg target;
       cx ctrl1, target;
       t ctrl2;
       t target;
       h target;
       cx ctrl1, ctrl2;
       t ctrl1;
       tdg ctrl2;
       cx ctrl1, ctrl2;
   }

使用例：

.. code-block:: qasm3

   qubit[3] q;
   
   // 3ビット加算器の一部
   ccx q[0], q[1], q[2];  // q[2] = q[0] AND q[1]

Fredkinゲート（制御SWAP）
~~~~~~~~~~~~~~~~~~~~~~~~~

制御されたSWAP操作：

.. code-block:: qasm3

   gate cswap ctrl, target1, target2 {
       cx target2, target1;
       ccx ctrl, target1, target2;
       cx target2, target1;
   }

量子フーリエ変換のためのゲート
------------------------------

位相ゲートの一般化
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 一般的な位相ゲート
   gate p(lambda) q { U(0, 0, lambda) q; }
   
   // 制御位相ゲート
   gate cp(lambda) ctrl, target { ctrl @ p(lambda) ctrl, target; }

QFTでの使用例：

.. code-block:: qasm3

   def qft_3bit(qubit a, qubit b, qubit c) {
       h a;
       cp(π/2) a, b;
       cp(π/4) a, c;
       h b;
       cp(π/2) b, c;
       h c;
   }

エイリアスと互換性
------------------

OpenQASM 2.0互換エイリアス
~~~~~~~~~~~~~~~~~~~~~~~~~~

後方互換性のためのエイリアス：

.. code-block:: qasm3

   // OpenQASM 2.0スタイルのエイリアス
   gate cnot ctrl, target { cx ctrl, target; }
   gate ccnot ctrl1, ctrl2, target { ccx ctrl1, ctrl2, target; }

一般的なエイリアス
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // よく使われるエイリアス
   gate id q { U(0, 0, 0) q; }        // 恒等ゲート
   gate rccx ctrl1, ctrl2, target {   // 相対制御Toffoli
       u2(0, π) target;
       u1(π/4) target;
       cx ctrl2, target;
       u1(-π/4) target;
       cx ctrl1, target;
       u1(π/4) target;
       cx ctrl2, target;
       u1(-π/4) target;
       u2(0, π) target;
   }

カスタマイズと拡張
------------------

標準ライブラリの拡張
~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.0;
   include "stdgates.inc";
   
   // カスタムゲートの追加
   gate my_custom_gate(theta, phi) q {
       ry(theta) q;
       rz(phi) q;
   }
   
   // 標準ゲートとカスタムゲートの組み合わせ
   def my_algorithm(qubit[4] qubits) {
       h qubits[0];                    // 標準ライブラリ
       my_custom_gate(π/4, π/2) qubits[1];  // カスタムゲート
       cx qubits[0], qubits[1];        // 標準ライブラリ
   }

実装の柔軟性
~~~~~~~~~~~~

標準ライブラリのゲートはハードウェア固有の最適化が可能：

.. code-block:: qasm3

   // 概念的な例: ハードウェア最適化版
   defcal cx $0, $1 {
       // ハードウェア固有の実装
       pulse_sequence("cross_resonance", 20ns);
   }

実用的な例
----------

Bell状態の準備
~~~~~~~~~~~~~~~

.. code-block:: qasm3

   OPENQASM 3.0;
   include "stdgates.inc";
   
   qubit[2] q;
   bit[2] c;
   
   // Bell状態 |Φ+⟩ = (|00⟩ + |11⟩)/√2
   h q[0];
   cx q[0], q[1];
   
   c = measure q;

GHZ状態の準備
~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[3] q;
   
   // GHZ状態 |GHZ⟩ = (|000⟩ + |111⟩)/√2
   h q[0];
   cx q[0], q[1];
   cx q[1], q[2];

量子テレポーテーション
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def quantum_teleportation(qubit alice, qubit bob, qubit ancilla) -> bit[2] {
       // Bellペアの準備
       h ancilla;
       cx ancilla, bob;
       
       // Aliceの操作
       cx alice, ancilla;
       h alice;
       
       // 測定
       bit[2] classical_bits;
       classical_bits[0] = measure alice;
       classical_bits[1] = measure ancilla;
       
       // Bobの修正操作
       if (classical_bits[1]) x bob;
       if (classical_bits[0]) z bob;
       
       return classical_bits;
   }

最適化とコンパイル
------------------

ゲート分解の最適化
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 最適化前
   t q;
   t q;
   t q;
   t q;
   
   // 最適化後（コンパイラが自動実行）
   s q;  // T⁴ = S

回路の簡約
~~~~~~~~~~

.. code-block:: qasm3

   // 最適化前
   h q;
   h q;
   
   // 最適化後（恒等操作として除去）
   // 何も残らない

ハードウェア制約
----------------

ネイティブゲートセット
~~~~~~~~~~~~~~~~~~~~~~

多くの量子ハードウェアは限定されたネイティブゲートセットを持ちます：

.. code-block:: qasm3

   // 例: 超伝導量子ビットの一般的なネイティブゲート
   // - 単一量子ビット: RZ, SX, X
   // - 2量子ビット: CZ
   
   // Yゲートの分解例
   gate y q {
       rz(π) q;
       sx q;
       rz(π) q;
   }

トポロジー制約
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 直接結合されていない量子ビット間のCNOT
   // SWAPゲートによるルーティングが必要
   
   def distant_cnot(qubit a, qubit intermediate, qubit b) {
       swap a, intermediate;
       cx intermediate, b;
       swap a, intermediate;
   }

まとめ
------

OpenQASMの標準ライブラリは：

- **包括性**: 量子計算に必要な基本ゲートを網羅
- **標準化**: 業界標準の量子ゲート定義
- **互換性**: 既存のコードとの互換性維持
- **拡張性**: カスタムゲートとの組み合わせ

この標準ライブラリにより、移植性が高く効率的な量子プログラムの開発が可能になります。