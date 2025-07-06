サブルーチン
============

OpenQASM 3.0では、コードの再利用性とモジュラリティを向上させるために、サブルーチン（関数）の定義と呼び出しをサポートしています。サブルーチンは量子操作と古典計算の両方を含むことができ、複雑な量子アルゴリズムの構造化に重要な役割を果たします。

基本構文
--------

サブルーチンの定義
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def function_name(parameters) -> return_type {
       // 関数本体
       return value;
   }

戻り値がない場合：

.. code-block:: text

   def function_name(parameters) {
       // 関数本体
   }

基本的な例
~~~~~~~~~~

.. code-block:: qasm3

   // 戻り値のないサブルーチン
   def bell_prep(qubit a, qubit b) {
       h a;
       ctrl @ x a, b;
   }
   
   // 戻り値のあるサブルーチン
   def xmeasure(qubit q) -> bit {
       h q;
       return measure q;
   }

引数の種類
----------

古典引数（値渡し）
~~~~~~~~~~~~~~~~~~

古典的なデータ型は値渡しで関数に渡されます：

.. code-block:: qasm3

   def classical_function(int n, float theta) -> float {
       return n * theta;
   }
   
   // 呼び出し例
   float result = classical_function(5, π/4);

量子引数（参照渡し）
~~~~~~~~~~~~~~~~~~

量子ビットは常に参照渡しで関数に渡されます：

.. code-block:: qasm3

   def apply_rotation(qubit q, angle theta) {
       rx(theta) q;
   }
   
   // 使用例
   qubit target;
   apply_rotation(target, π/2);

重要な制約：

- 各量子ビットは1つのサブルーチンに1回のみ渡すことができる
- 量子ビットは関数内で変更される（参照渡しのため）

配列パラメータ
--------------

配列の参照渡し
~~~~~~~~~~~~~~

配列は参照渡しで関数に渡され、``readonly``または``mutable``を指定します：

.. code-block:: qasm3

   // 読み取り専用配列
   def sum_array(readonly array[int[32], #dim=1] arr) -> int[32] {
       int total = 0;
       for i in [0:sizeof(arr, 0)-1] {
           total += arr[i];
       }
       return total;
   }
   
   // 変更可能配列
   def zero_array(mutable array[int[32], #dim=1] arr) {
       for i in [0:sizeof(arr, 0)-1] {
           arr[i] = 0;
       }
   }

配列の次元指定
~~~~~~~~~~~~~~

配列パラメータでは次元数を明示的に指定します：

.. code-block:: qasm3

   // 1次元配列
   def process_vector(readonly array[float[64], #dim=1] vec) -> float[64] {
       // ベクトル処理
   }
   
   // 2次元配列（行列）
   def matrix_multiply(
       readonly array[float[64], #dim=2] a,
       readonly array[float[64], #dim=2] b,
       mutable array[float[64], #dim=2] result
   ) {
       // 行列乗算の実装
   }

sizeof関数
~~~~~~~~~~

``sizeof()``関数で配列の各次元のサイズを取得：

.. code-block:: qasm3

   def analyze_matrix(readonly array[int[32], #dim=2] matrix) {
       int rows = sizeof(matrix, 0);     // 行数
       int cols = sizeof(matrix, 1);     // 列数
       
       for i in [0:rows-1] {
           for j in [0:cols-1] {
               // matrix[i][j]にアクセス
           }
       }
   }

戻り値
------

単一戻り値
~~~~~~~~~~

サブルーチンは最大1つの古典的な値を返すことができます：

.. code-block:: qasm3

   def measure_parity(qubit a, qubit b) -> bit {
       bit result_a = measure a;
       bit result_b = measure b;
       return result_a ^ result_b;  // パリティを返す
   }

戻り値なし
~~~~~~~~~~

戻り値がない場合は``return``文を省略するか、空の``return``を使用：

.. code-block:: qasm3

   def prepare_state(qubit q, angle theta) {
       ry(theta) q;
       // 明示的なreturnは不要
   }
   
   def conditional_reset(qubit q, bit condition) {
       if (condition) {
           reset q;
           return;  // 早期リターン
       }
       h q;
   }

量子サブルーチンの例
--------------------

Bell状態の準備
~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def bell_state(qubit ctrl, qubit target) {
       h ctrl;
       ctrl @ x ctrl, target;
   }
   
   // 使用例
   qubit[2] qubits;
   bell_state(qubits[0], qubits[1]);

量子フーリエ変換
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def qft_3bit(qubit a, qubit b, qubit c) {
       // 3量子ビットQFT
       h a;
       ctrl @ s a, b;
       ctrl @ t a, c;
       h b;
       ctrl @ s b, c;
       h c;
       
       // ビット順序の交換
       swap a, c;
   }

測定ベースの操作
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def teleport_measure(qubit alice, qubit ancilla) -> bit[2] {
       ctrl @ x alice, ancilla;
       h alice;
       bit[2] results;
       results[0] = measure alice;
       results[1] = measure ancilla;
       return results;
   }

古典-量子統合
--------------

パラメータ化されたゲート
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def parameterized_circuit(qubit q, float theta, int repetitions) {
       for i in [0:repetitions-1] {
           ry(theta) q;
           rz(theta/2) q;
       }
   }

条件付き量子操作
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def conditional_gates(qubit q, bit[2] condition) {
       if (condition == 0b00) {
           // 何もしない
       } else if (condition == 0b01) {
           x q;
       } else if (condition == 0b10) {
           y q;
       } else {
           z q;
       }
   }

エラー処理と検証
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def error_syndrome(qubit[3] data, qubit[2] ancilla) -> bit[2] {
       // パリティチェック
       ctrl @ x data[0], ancilla[0];
       ctrl @ x data[1], ancilla[0];
       ctrl @ x data[1], ancilla[1];
       ctrl @ x data[2], ancilla[1];
       
       bit[2] syndrome;
       syndrome[0] = measure ancilla[0];
       syndrome[1] = measure ancilla[1];
       
       return syndrome;
   }

再帰的定義
----------

制限事項
~~~~~~~~

OpenQASMでは直接的な再帰は一般的にサポートされていませんが、反復的な実装が可能です：

.. code-block:: qasm3

   def power_of_gate(qubit q, int power) {
       for i in [0:power-1] {
           t q;
       }
   }

高階関数パターン
----------------

関数ポインタは直接サポートされていませんが、条件分岐で類似の効果を実現：

.. code-block:: qasm3

   def apply_gate(qubit q, int gate_type) {
       if (gate_type == 0) {
           x q;
       } else if (gate_type == 1) {
           y q;
       } else if (gate_type == 2) {
           z q;
       } else {
           h q;
       }
   }

実践的な例
----------

変分量子固有値ソルバー（VQE）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def vqe_ansatz(qubit[4] qubits, float[8] params) {
       // 初期状態の準備
       for i in [0:3] {
           ry(params[i]) qubits[i];
       }
       
       // エンタングリング層
       for i in [0:2] {
           ctrl @ x qubits[i], qubits[i+1];
       }
       ctrl @ x qubits[3], qubits[0];
       
       // 第2層の回転
       for i in [0:3] {
           ry(params[i+4]) qubits[i];
       }
   }

量子近似最適化アルゴリズム（QAOA）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def qaoa_layer(qubit[4] qubits, float beta, float gamma) {
       // 問題ハミルトニアン
       for i in [0:2] {
           rzz(2*gamma) qubits[i], qubits[i+1];
       }
       rzz(2*gamma) qubits[3], qubits[0];
       
       // ミキサーハミルトニアン
       for i in [0:3] {
           rx(2*beta) qubits[i];
       }
   }

スコープとローカル変数
----------------------

ローカル変数
~~~~~~~~~~~~

サブルーチン内で宣言された変数はローカルスコープを持ちます：

.. code-block:: qasm3

   def local_computation(int input) -> int {
       int local_var = input * 2;  // ローカル変数
       int another_var = local_var + 1;
       return another_var;
   }

パラメータシャドウイング
~~~~~~~~~~~~~~~~~~~~~~~~

ローカル変数はパラメータ名をシャドウすることはできません：

.. code-block:: qasm3

   def shadow_example(int param) -> int {
       // int param = 5;  // エラー: パラメータ名と重複
       int local_param = param + 1;  // 正常: 異なる名前
       return local_param;
   }

型安全性
--------

型チェック
~~~~~~~~~~

OpenQASMは強い型付けを採用し、型の不一致はコンパイル時エラーとなります：

.. code-block:: qasm3

   def type_safe_function(qubit q, int count) -> bit {
       // bit result = q;  // エラー: 型の不一致
       bit result = measure q;  // 正常
       return result;
   }

最適化とインライン化
--------------------

コンパイラ最適化
~~~~~~~~~~~~~~~~

コンパイラは以下の最適化を実行可能：

- **インライン展開**: 小さな関数の呼び出しを本体で置換
- **定数伝播**: 定数引数の最適化
- **デッドコード除去**: 使用されない計算の削除

.. code-block:: qasm3

   // インライン化される可能性の高い小さな関数
   def simple_rotation(qubit q) {
       ry(π/4) q;
   }

まとめ
------

OpenQASMのサブルーチンは：

- **モジュラリティ**: 複雑なアルゴリズムの構造化
- **再利用性**: 共通操作の関数化
- **型安全性**: コンパイル時の型チェック
- **量子-古典統合**: seamless な混合計算

これらの機能により、大規模で保守性の高い量子プログラムの開発が可能になります。