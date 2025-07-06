古典計算
========

OpenQASM 3.0は、量子計算と古典計算を統合的に扱うための包括的な古典プログラミング機能を提供します。これにより、量子アルゴリズムにおける測定結果に基づく条件分岐や、複雑な古典的前処理・後処理が可能になります。

古典制御のレベル
----------------

OpenQASMでは2つのレベルの古典制御を提供します：

1. **低レベル制御**: 量子回路に直接埋め込まれた基本的な命令
2. **高レベル制御**: 複雑な計算を行う外部関数や高度な制御構造

低レベル古典命令
~~~~~~~~~~~~~~~~

量子回路実行中にリアルタイムで実行される基本的な操作：

.. code-block:: qasm3

   qubit q;
   bit c;
   
   // 測定と即座の条件分岐
   c = measure q;
   if (c) x q;  // 測定結果に基づく即座のゲート適用

高レベル古典命令
~~~~~~~~~~~~~~~~

より複雑な計算や制御フローを扱う命令：

.. code-block:: qasm3

   // 複雑な数値計算
   float result = sqrt(2.0) * cos(π/4);
   
   // 配列処理
   int[32][10] data;
   for i in [0:9] {
       data[i] = i * i;
   }

データ型と演算
--------------

算術演算
~~~~~~~~

基本的な算術演算子をサポート：

.. code-block:: qasm3

   int a = 10;
   int b = 3;
   
   int sum = a + b;         // 加算: 13
   int diff = a - b;        // 減算: 7
   int product = a * b;     // 乗算: 30
   int quotient = a / b;    // 除算: 3
   int remainder = a % b;   // 剰余: 1

浮動小数点演算：

.. code-block:: qasm3

   float x = 3.14;
   float y = 2.71;
   
   float result = x * y + 1.0;  // 10.5094

ビット演算
~~~~~~~~~~

ビットレベルの操作をサポート：

.. code-block:: qasm3

   bit[8] a = 0b10110011;
   bit[8] b = 0b11001100;
   
   bit[8] and_result = a & b;    // ビット積: 0b10000000
   bit[8] or_result = a | b;     // ビット和: 0b11111111
   bit[8] xor_result = a ^ b;    // 排他的論理和: 0b01111111
   bit[8] not_result = ~a;       // ビット反転: 0b01001100

シフト演算：

.. code-block:: qasm3

   bit[8] value = 0b00001111;
   bit[8] left_shift = value << 2;   // 0b00111100
   bit[8] right_shift = value >> 1;  // 0b00000111

比較演算
~~~~~~~~

値の比較を行う演算子：

.. code-block:: qasm3

   int x = 10;
   int y = 20;
   
   bool equal = (x == y);        // false
   bool not_equal = (x != y);    // true
   bool less = (x < y);          // true
   bool greater = (x > y);       // false
   bool less_equal = (x <= y);   // true
   bool greater_equal = (x >= y); // false

論理演算
~~~~~~~~

真偽値に対する論理演算：

.. code-block:: qasm3

   bool a = true;
   bool b = false;
   
   bool and_result = a && b;   // false
   bool or_result = a || b;    // true
   bool not_result = !a;       // false

制御構造
--------

条件分岐（if-else）
~~~~~~~~~~~~~~~~~~~

条件に基づく実行の分岐：

.. code-block:: qasm3

   bit c;
   qubit q;
   
   c = measure q;
   
   if (c) {
       x q;  // cが1の場合にXゲートを適用
   } else {
       h q;  // cが0の場合にHゲートを適用
   }

ネストした条件分岐も可能：

.. code-block:: qasm3

   int value = 15;
   
   if (value > 10) {
       if (value < 20) {
           // 10 < value < 20の場合の処理
       }
   }

forループ
~~~~~~~~~

指定された回数の繰り返し処理：

.. code-block:: qasm3

   qubit[5] qreg;
   
   // 範囲指定による繰り返し
   for i in [0:4] {
       h qreg[i];
   }
   
   // 配列の要素に対する繰り返し
   int[5] indices = {0, 2, 4, 1, 3};
   for idx in indices {
       x qreg[idx];
   }

ステップ指定も可能：

.. code-block:: qasm3

   // 2つおきの要素に対する処理
   for i in [0:2:8] {  // 0, 2, 4, 6, 8
       z qreg[i];
   }

whileループ
~~~~~~~~~~~

条件が満たされる間の繰り返し処理：

.. code-block:: qasm3

   int counter = 0;
   bit result = 0;
   qubit q;
   
   while (!result && counter < 10) {
       h q;
       result = measure q;
       counter += 1;
   }

switch文
~~~~~~~~

多分岐の条件処理：

.. code-block:: qasm3

   int state = 2;
   qubit q;
   
   switch (state) {
       case 0: {
           x q;
           break;
       }
       case 1: {
           y q;
           break;
       }
       case 2: {
           z q;
           break;
       }
       default: {
           h q;
       }
   }

ループ制御
~~~~~~~~~~

``break``と``continue``文：

.. code-block:: qasm3

   for i in [0:9] {
       if (i == 3) {
           continue;  // i=3をスキップ
       }
       if (i == 7) {
           break;     // i=7でループを終了
       }
       // 処理
   }

外部関数
--------

``extern``キーワードで外部関数を宣言：

.. code-block:: qasm3

   // 外部関数の宣言
   extern real_function(angle) -> float;
   extern complex_sqrt(complex[float[64]]) -> complex[float[64]];
   
   // 使用例
   angle theta = π/4;
   float result = real_function(theta);

外部関数の特徴：

- コンパイル時に型とサイズが既知である必要
- 量子計算と並行して実行可能
- 複雑な数値計算やアルゴリズムの実装に使用

配列操作
--------

配列の宣言と初期化
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 配列の宣言
   int[32][10] array;
   
   // 初期化リストによる配列の初期化
   int[5] fibonacci = {1, 1, 2, 3, 5};
   
   // 多次元配列
   float[64][3][3] matrix = {
       {1.0, 0.0, 0.0},
       {0.0, 1.0, 0.0},
       {0.0, 0.0, 1.0}
   };

配列のスライス
~~~~~~~~~~~~~~

.. code-block:: qasm3

   int[10] data = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
   
   // スライスによる部分配列の取得
   int[3] subset = data[2:4];    // {2, 3, 4}
   int[5] step_slice = data[0:2:8]; // {0, 2, 4, 6, 8}

文字列と文字定数
----------------

文字列リテラル：

.. code-block:: qasm3

   // 文字列の使用（主にアノテーションで）
   @description("Bell state preparation")
   gate bell_prep a, b {
       h a;
       ctrl @ x a, b;
   }

演算子の優先順位
----------------

演算子の優先順位（高から低）：

1. ``()`` - 括弧
2. ``!``, ``~``, 単項``-``, 単項``+`` - 単項演算子
3. ``**`` - べき乗
4. ``*``, ``/``, ``%`` - 乗除算
5. ``+``, ``-`` - 加減算
6. ``<<``, ``>>`` - ビットシフト
7. ``<``, ``>``, ``<=``, ``>=`` - 比較
8. ``==``, ``!=`` - 等価性
9. ``&`` - ビット積
10. ``^`` - 排他的論理和
11. ``|`` - ビット和
12. ``&&`` - 論理積
13. ``||`` - 論理和

型変換と代入
------------

暗黙的型変換
~~~~~~~~~~~~

.. code-block:: qasm3

   int i = 42;
   float f = i;      // intからfloatへの自動変換
   complex c = f;    // floatからcomplexへの自動変換

明示的型変換
~~~~~~~~~~~~

.. code-block:: qasm3

   float f = 3.14;
   int i = int(f);   // 明示的キャスト: 3

代入演算子
~~~~~~~~~~

.. code-block:: qasm3

   int a = 10;
   a += 5;    // a = a + 5 と等価
   a -= 3;    // a = a - 3 と等価
   a *= 2;    // a = a * 2 と等価
   a /= 4;    // a = a / 4 と等価

実行時の考慮事項
----------------

量子-古典混合実行
~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   qubit q;
   bit c;
   int counter = 0;
   
   // 量子操作と古典処理の混合
   repeat {
       h q;
       c = measure q;
       counter += 1;
   } until (c || counter >= 100);

リアルタイム制約
~~~~~~~~~~~~~~~~

低レベル古典命令は量子デコヒーレンス時間内に実行される必要があります：

.. code-block:: qasm3

   qubit q;
   bit[2] syndrome;
   
   // 高速なエラー修正
   syndrome[0] = measure ancilla[0];
   syndrome[1] = measure ancilla[1];
   
   if (syndrome == 0b01) x q;      // 即座の修正
   else if (syndrome == 0b10) z q;

まとめ
------

OpenQASMの古典計算機能は：

- **統合性**: 量子計算との seamless な統合
- **表現力**: 豊富な制御構造と演算子
- **効率性**: リアルタイム実行とコンパイル時最適化
- **拡張性**: 外部関数による機能拡張

これらの機能により、複雑な量子アルゴリズムの実装と制御が可能になります。