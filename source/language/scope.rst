スコープとシンボル管理
====================

OpenQASM 3.0では、変数やシンボルの可視性と生存期間を制御するために、階層的なスコープシステムを採用しています。このシステムは量子計算の特殊な要件を考慮しながら、プログラムの構造化と安全性を提供します。

スコープの概要
--------------

スコープは名前空間の境界を定義し、シンボル（変数、関数、ゲートなど）の可視性を制御します。OpenQASMには以下のスコープの種類があります：

1. **グローバルスコープ**: プログラム全体で有効
2. **サブルーチン/ゲートスコープ**: 関数やゲート定義内
3. **ローカルブロックスコープ**: 制御構造内
4. **校正スコープ**: defcal定義内

グローバルスコープ
------------------

グローバルスコープの特徴
~~~~~~~~~~~~~~~~~~~~~~~~

グローバルスコープはプログラムの最上位レベルで、以下の要素を含みます：

.. code-block:: qasm3

   // グローバルスコープでの宣言
   qubit[5] global_qubits;           // 量子ビット配列
   bit[5] global_bits;              // 古典ビット配列
   const int CIRCUIT_DEPTH = 10;    // グローバル定数
   
   // グローバル関数定義
   def global_function(qubit q) -> bit {
       return measure q;
   }
   
   // グローバルゲート定義
   gate custom_gate q {
       h q;
   }

グローバル変数の特徴：

- プログラム実行全体を通じて存在
- 他のスコープから参照可能（制限あり）
- 量子ビットは必ずグローバルスコープで宣言

量子ビットのグローバル性
~~~~~~~~~~~~~~~~~~~~~~~~

すべての量子ビットはグローバルスコープで宣言される必要があります：

.. code-block:: qasm3

   qubit[3] qreg;  // グローバル量子ビット
   
   def local_function() {
       // qubit local_q;  // エラー: 量子ビットはグローバルでのみ宣言可能
       h qreg[0];  // グローバル量子ビットへのアクセスは可能
   }

サブルーチン/ゲートスコープ
---------------------------

関数スコープ
~~~~~~~~~~~~

関数内では独立したスコープが作成されます：

.. code-block:: qasm3

   const int GLOBAL_CONST = 42;
   int global_var = 10;
   
   def my_function(int param) -> int {
       int local_var = param * 2;      // ローカル変数
       int another_var = GLOBAL_CONST; // グローバル定数は参照可能
       // int wrong = global_var;      // エラー: 非const変数は参照不可
       
       return local_var + another_var;
   }

ゲートスコープ
~~~~~~~~~~~~~~

ゲート定義内でも独立したスコープが存在します：

.. code-block:: qasm3

   gate parameterized_gate(theta) q {
       // theta: ゲートパラメータ（ローカル）
       // q: 量子ビットパラメータ（ローカル）
       ry(theta) q;
       
       // ゲート内でのローカル計算は制限される
   }

パラメータとローカル変数
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   def complex_function(int n, float theta) -> float {
       // パラメータ: n, theta
       float local_result = 0.0;    // ローカル変数
       
       for i in [0:n-1] {           // iもローカルスコープ
           local_result += sin(theta * i);
       }
       
       return local_result;
   }

ローカルブロックスコープ
------------------------

制御構造内のスコープ
~~~~~~~~~~~~~~~~~~~~

制御構造（if、for、whileなど）は独自のスコープを作成します：

.. code-block:: qasm3

   int global_counter = 0;
   
   if (global_counter < 10) {
       int local_temp = global_counter * 2;  // ifブロック内のローカル変数
       global_counter = local_temp;          // グローバル変数の変更
       
       if (local_temp > 5) {                 // ネストしたスコープ
           int nested_var = local_temp + 1;  // さらに内側のローカル変数
       }
       // nested_varはここでは利用不可
   }
   // local_tempはここでは利用不可

forループのスコープ
~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   for i in [0:4] {
       int loop_var = i * i;    // ループスコープ内のローカル変数
       
       for j in [0:2] {         // ネストしたループ
           int inner_var = i + j;
       }
       // inner_varはここでは利用不可
   }
   // i, loop_varはここでは利用不可

whileループのスコープ
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   int counter = 0;
   
   while (counter < 10) {
       int step = counter + 1;   // whileブロック内のローカル変数
       counter = step;
       
       if (step == 5) {
           int special = step * 2; // 条件ブロック内のローカル変数
           break;
       }
   }

シンボルの可視性ルール
----------------------

スコープチェーン
~~~~~~~~~~~~~~~~

内側のスコープは外側のスコープのシンボルにアクセス可能ですが、制限があります：

.. code-block:: qasm3

   const int CONSTANT = 100;    // グローバル定数
   int variable = 50;           // グローバル変数
   
   def access_test(int param) -> int {
       // CONSTANT: アクセス可能（定数）
       // variable: アクセス不可（非const変数）
       // param: アクセス可能（パラメータ）
       
       int local = param + CONSTANT;
       
       if (local > 150) {
           // CONSTANT: アクセス可能
           // param: アクセス可能
           // local: アクセス可能
           int nested = local - param;
           return nested;
       }
       
       return local;
   }

シャドウイング
~~~~~~~~~~~~~~

内側のスコープで同名の変数を宣言すると、外側の変数が隠される：

.. code-block:: qasm3

   int value = 10;  // グローバル変数
   
   def shadow_example() -> int {
       int value = 20;  // ローカル変数（グローバルをシャドウ）
       
       if (true) {
           int value = 30;  // さらに内側でシャドウ
           return value;    // 30を返す
       }
       
       return value;  // この行には到達しない
   }

量子ビットのスコープ規則
------------------------

量子ビットの可視性
~~~~~~~~~~~~~~~~~~

量子ビットはグローバルに宣言されますが、関数への引数として渡す必要があります：

.. code-block:: qasm3

   qubit[3] qreg;  // グローバル量子ビット
   
   def quantum_operation(qubit q) {
       h q;  // 引数として渡された量子ビットを操作
   }
   
   // 使用例
   quantum_operation(qreg[0]);

量子ビットのエイリアス
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit[5] main_register;
   
   def multi_qubit_gate(qubit ctrl, qubit target) {
       ctrl @ x ctrl, target;
   }
   
   // エイリアシング: 同じ量子ビットを複数回渡すことは不可
   // multi_qubit_gate(main_register[0], main_register[0]);  // エラー

変数の生存期間
--------------

自動変数
~~~~~~~~

ローカル変数は自動的に管理されます：

.. code-block:: qasm3

   def lifetime_example() -> int {
       int local_var = 42;    // スコープ開始時に作成
       
       if (local_var > 40) {
           int inner_var = local_var * 2;  // 内側スコープで作成
           // inner_var: ここで有効
       }  // inner_var: ここで破棄
       
       return local_var;      // local_var: まだ有効
   }  // local_var: ここで破棄

定数の生存期間
~~~~~~~~~~~~~~

定数は宣言されたスコープの全体で有効です：

.. code-block:: qasm3

   def constant_scope() {
       const int LOCAL_CONST = 100;
       
       for i in [0:9] {
           int value = LOCAL_CONST + i;  // LOCAL_CONSTは参照可能
       }
   }

名前解決
--------

名前解決の優先順位
~~~~~~~~~~~~~~~~~~

シンボルの名前解決は以下の順序で行われます：

1. 現在のスコープのローカル変数
2. 外側のスコープの変数（内側から外側へ）
3. 関数パラメータ
4. グローバル定数
5. 組み込みシンボル

.. code-block:: qasm3

   const int GLOBAL = 1;
   
   def resolution_example(int GLOBAL) -> int {  // パラメータでシャドウ
       int local = GLOBAL + 10;  // パラメータのGLOBALを使用
       
       {
           int GLOBAL = 100;      // さらにシャドウ
           local += GLOBAL;       // ローカルのGLOBALを使用（100）
       }
       
       return local;  // パラメータのGLOBALを使用
   }

前方宣言
~~~~~~~~

OpenQASMでは使用前に宣言が必要です：

.. code-block:: qasm3

   // 正しい順序
   def helper_function() -> int {
       return 42;
   }
   
   def main_function() -> int {
       return helper_function();  // helper_functionは既に定義済み
   }

スコープとコンパイル最適化
--------------------------

レキシカルスコープ
~~~~~~~~~~~~~~~~~~

OpenQASMはレキシカルスコープを採用し、コンパイル時に変数の可視性が決定されます：

.. code-block:: qasm3

   int outer = 10;
   
   def lexical_example() -> int {
       return outer;  // コンパイル時エラー: 非const変数への参照
   }

最適化の影響
~~~~~~~~~~~~

スコープ規則により、コンパイラは以下の最適化を実行可能：

- **変数の早期解放**: スコープ終了時の自動メモリ管理
- **定数伝播**: 定数の値をコンパイル時に展開
- **デッドコード除去**: 使用されない変数の除去

.. code-block:: qasm3

   def optimizable_function(int n) -> int {
       const int FACTOR = 2;     // コンパイル時定数
       int temp = n * FACTOR;    // FACTOR=2として最適化可能
       int unused = 100;         // 使用されない変数（除去可能）
       
       return temp;
   }

実践的なスコープ管理
--------------------

良いスコープ設計
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 良い例: 明確なスコープ分離
   def calculate_probability(qubit q, int shots) -> float {
       int success_count = 0;
       
       for shot in [0:shots-1] {
           bit result = measure q;    // ループスコープ内での宣言
           if (result) {
               success_count += 1;
           }
           reset q;
       }
       
       return float(success_count) / float(shots);
   }

避けるべきパターン
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 避けるべき例: 不必要なシャドウイング
   int data = 100;
   
   def confusing_function(int data) -> int {  // パラメータ名の衝突
       int data = data * 2;  // エラー: 同じスコープでの再宣言
       return data;
   }

まとめ
------

OpenQASMのスコープシステムは：

- **階層的構造**: ネストしたスコープの明確な管理
- **量子特有の制約**: 量子ビットのグローバル性
- **安全性**: コンパイル時の名前解決とエラー検出
- **最適化**: 効率的なメモリ管理と実行

適切なスコープ管理により、保守性が高く効率的な量子プログラムを作成できます。