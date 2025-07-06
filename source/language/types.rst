型システム
========

OpenQASM 3.0は、量子計算と古典計算の両方をサポートする包括的な型システムを提供します。

識別子
------

識別子は変数、関数、および他のプログラム要素の名前です。

識別子の規則
~~~~~~~~~~~~

- **開始文字**: 文字（a-z、A-Z）、アンダースコア（_）、またはUnicode文字
- **継続文字**: 文字、数字、アンダースコアが使用可能
- **大文字小文字**: 区別されます（``myVar`` と ``myvar`` は異なる識別子）

.. code-block:: qasm3

   // 有効な識別子の例
   my_variable
   _temp
   Variable1
   π  // Unicode文字も使用可能

予約識別子
~~~~~~~~~~

以下の識別子は言語によって予約されており、上書きできません：

- ``qubit``、``bit``、``int``、``uint``、``float``、``angle``、``bool``、``duration``
- ``input``、``output``、``const``
- ``if``、``else``、``for``、``while``、``break``、``continue``

型の分類
--------

OpenQASMの型は以下のカテゴリに分類されます：

量子型
~~~~~~

**qubit**
  量子ビットを表す基本的な量子型です。

.. code-block:: qasm3

   qubit q;           // 単一量子ビット
   qubit[5] qreg;     // 5つの量子ビットの配列

量子ビットには2つの種類があります：

- **仮想量子ビット**: プログラム内で宣言される論理的な量子ビット
- **物理量子ビット**: ハードウェア上の実際の量子ビット（``$[番号]``で参照）

.. code-block:: qasm3

   // 物理量子ビットの直接参照
   x $[0];  // 物理量子ビット0にXゲートを適用

古典スカラー型
~~~~~~~~~~~~~~

**bit**
  単一のビット値（0または1）を格納します。

.. code-block:: qasm3

   bit b = 0;
   bit[8] byte_val;  // 8ビットのビット配列

**bool**
  真偽値（``true``または``false``）を格納します。

.. code-block:: qasm3

   bool flag = true;
   bool result = (x > 5);

**int / uint**
  符号付き/符号なし整数を格納します。

.. code-block:: qasm3

   int[32] signed_int = -42;
   uint[16] unsigned_int = 65535;

**float**
  浮動小数点数を格納します。

.. code-block:: qasm3

   float[64] pi = 3.14159265359;
   float theta = 1.57;  // デフォルトサイズ

**complex**
  複素数を格納します。

.. code-block:: qasm3

   complex[float[64]] z = 1.0 + 2.0im;

**angle**
  角度を効率的に表現する特殊な型です。

.. code-block:: qasm3

   angle[32] theta = π/4;
   angle phi = 1.57;

配列型
~~~~~~

すべての型は配列として宣言できます（最大7次元まで）。

.. code-block:: qasm3

   int[32][10] int_array;        // 10要素の配列
   float[64][3][3] matrix;       // 3x3行列
   qubit[5] quantum_register;    // 量子ビット配列

配列の特徴：

- **静的サイズ**: サイズはコンパイル時に決定
- **負のインデックス**: ``array[-1]``は最後の要素を参照
- **範囲アクセス**: ``array[1:3]``でスライスアクセス可能

特殊型
~~~~~~

**duration**
  時間の長さを表します。

.. code-block:: qasm3

   duration d = 100ns;
   duration[32] delay_time = 1.5μs;

**stretch**
  可変の非負の持続時間を表します。

.. code-block:: qasm3

   stretch s;  // 実行時に決定される時間

型変換
------

OpenQASMは明示的および暗黙的な型変換をサポートします。

暗黙的型変換
~~~~~~~~~~~~

安全な型変換は自動的に行われます：

.. code-block:: qasm3

   int[32] i = 42;
   float[64] f = i;  // intからfloatへの自動変換

明示的型変換
~~~~~~~~~~~~

キャスト演算子を使用して明示的に型変換を行います：

.. code-block:: qasm3

   float[32] f = 3.14;
   int[16] i = int[16](f);  // floatからintへの明示的変換

.. note::
   精度の損失が発生する可能性がある変換については、実装依存の動作となります。

型安全性
--------

OpenQASMは強い型付けを採用しており、型の不一致はコンパイル時エラーとなります：

.. code-block:: qasm3

   qubit q;
   bit b;
   // q = b;  // エラー: 量子型と古典型は互換性がない

定数修飾子
----------

``const``修飾子を使用して定数を宣言できます：

.. code-block:: qasm3

   const int N = 5;
   const float π = 3.14159265359;
   
   qubit[N] qreg;  // 定数を配列サイズに使用

入出力修飾子
~~~~~~~~~~~~

サブルーチンのパラメータに対して入出力の性質を指定できます：

.. code-block:: qasm3

   def measure_all(input qubit[5] q, output bit[5] result) {
       for i in [0:4] {
           result[i] = measure q[i];
       }
   }

まとめ
------

OpenQASMの型システムは：

- 量子計算と古典計算の明確な分離
- 型安全性の保証
- 効率的なハードウェア制御
- 高レベルプログラミングの抽象化

これらの特徴により、量子アルゴリズムの正確で効率的な記述が可能になります。