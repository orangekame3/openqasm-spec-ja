ディレクティブと注釈
==================

OpenQASM 3.0では、プログラムに追加情報を提供し、コンパイラやランタイムシステムの動作を制御するためのディレクティブシステムを提供しています。これにより、パラメトリック回路や高度な最適化が可能になります。

概要
----

ディレクティブの種類
~~~~~~~~~~~~~~~~~~~~

OpenQASMでは2つの主要なディレクティブを提供：

1. **プラグマ（Pragma）**: プログラム全体またはファイルレベルでの指示
2. **アノテーション（Annotation）**: 特定の文や宣言への注釈

どちらも名前空間を使用して衝突を回避し、拡張可能な設計になっています。

用途と利点
~~~~~~~~~~

- **最適化ヒント**: コンパイラへの最適化指示
- **デバッグ情報**: 実行時の詳細情報提供
- **ハードウェア制約**: デバイス固有の制約表現
- **パラメトリック回路**: 実行時パラメータの制御

プラグマ（Pragma）
------------------

基本構文
~~~~~~~~

プラグマは``pragma``キーワードで始まり、名前空間を使用します：

.. code-block:: qasm3

   pragma namespace.directive_name option1 option2;

一般的なプラグマの例：

.. code-block:: qasm3

   // 最適化レベルの指定
   pragma optimization.level 2;
   
   // デバッグ情報の有効化
   pragma debug.enable true;
   
   // ターゲットハードウェアの指定
   pragma target.backend "ibm_quantum";

最適化制御
~~~~~~~~~~

.. code-block:: qasm3

   // 回路最適化の制御
   pragma optimization.gate_fusion true;
   pragma optimization.circuit_depth_reduction true;
   pragma optimization.qubit_mapping "sabre";
   
   qubit[5] q;
   
   // 最適化された回路
   for i in [0:4] {
       h q[i];
   }

ハードウェア固有設定
~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // ハードウェア制約の指定
   pragma hardware.max_circuit_depth 1000;
   pragma hardware.gate_time.x 20ns;
   pragma hardware.gate_time.cx 100ns;
   
   qubit[2] q;
   x q[0];          // 20ns
   cx q[0], q[1];   // 100ns

コンパイル制御
~~~~~~~~~~~~~~

.. code-block:: qasm3

   // コンパイル時の動作制御
   pragma compile.check_bounds true;
   pragma compile.inline_functions true;
   pragma compile.target_instruction_set "qiskit";

アノテーション（Annotation）
----------------------------

基本構文
~~~~~~~~

アノテーションは``@``記号で始まり、直後の文や宣言に適用されます：

.. code-block:: qasm3

   @namespace.annotation_name(parameters)
   statement;

文書化アノテーション
~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @doc.description("Bell状態を準備する関数")
   @doc.author("OpenQASM翻訳チーム")
   def bell_preparation(qubit ctrl, qubit target) {
       h ctrl;
       cx ctrl, target;
   }

最適化ヒント
~~~~~~~~~~~~

.. code-block:: qasm3

   @optimization.inline
   def small_rotation(qubit q) {
       ry(π/8) q;
   }
   
   @optimization.parallel
   def independent_operations(qubit[4] q) {
       h q[0];
       h q[1];
       h q[2];
       h q[3];
   }

デバッグ情報
~~~~~~~~~~~~

.. code-block:: qasm3

   @debug.trace("量子フーリエ変換開始")
   def qft_3bit(qubit a, qubit b, qubit c) {
       @debug.checkpoint("第1段階")
       h a;
       
       @debug.checkpoint("第2段階")
       ctrl @ s a, b;
       ctrl @ t a, c;
       
       @debug.checkpoint("完了")
       h b;
       ctrl @ s b, c;
       h c;
   }

入力/出力パラメータ
-------------------

input修飾子
~~~~~~~~~~~

``input``修飾子は実行時に値が提供される変数を宣言します：

.. code-block:: qasm3

   // パラメトリック量子回路
   input angle[32] theta;    // 実行時に提供される角度
   input int iterations;     // 実行時に提供される反復回数
   
   qubit q;
   
   // 変分回路
   for i in [0:iterations-1] {
       ry(theta) q;
       rz(theta/2) q;
   }

複数入力パラメータ
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   input angle[32] alpha;
   input angle[32] beta;
   input angle[32] gamma;
   
   qubit[3] q;
   
   // オイラー角による任意回転
   rz(alpha) q[0];
   ry(beta) q[0];
   rz(gamma) q[0];

output修飾子
~~~~~~~~~~~~

``output``修飾子は量子プロセスから返される値を宣言します：

.. code-block:: qasm3

   input int shots;
   output bit[5] results;
   output float success_rate;
   
   qubit[5] q;
   
   // Bell状態の準備と測定
   h q[0];
   for i in [1:4] {
       cx q[0], q[i];
   }
   
   results = measure q;
   success_rate = float(popcount(results)) / float(shots);

パラメトリック量子回路
----------------------

基本的なパラメトリック回路
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // 変分量子固有値ソルバー（VQE）のアンザッツ
   input angle[32][4] rotation_angles;  // 4つの回転角
   input int circuit_depth;             // 回路の深さ
   output bit[4] measurement_results;
   
   qubit[4] q;
   
   // パラメータ化された変分回路
   for layer in [0:circuit_depth-1] {
       // 回転層
       for i in [0:3] {
           ry(rotation_angles[i]) q[i];
       }
       
       // エンタングリング層
       for i in [0:2] {
           cx q[i], q[i+1];
       }
       cx q[3], q[0];  // 周期境界条件
   }
   
   measurement_results = measure q;

条件付きパラメトリック回路
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   input angle theta;
   input bool apply_correction;
   output bit result;
   
   qubit q;
   
   // 条件付き回転
   ry(theta) q;
   
   if (apply_correction) {
       rx(π) q;  // エラー修正回転
   }
   
   result = measure q;

動的パラメータ生成
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   input float base_frequency;
   input int num_steps;
   output bit[4] final_state;
   
   qubit[4] q;
   
   // 動的に生成される角度
   for step in [0:num_steps-1] {
       angle dynamic_angle = 2 * π * base_frequency * step / num_steps;
       
       for i in [0:3] {
           ry(dynamic_angle) q[i];
       }
   }
   
   final_state = measure q;

実用的な例
----------

量子近似最適化アルゴリズム（QAOA）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @doc.description("QAOA回路の実装")
   @optimization.target("quantum_annealer")
   
   input angle[32] beta;     // ミキサーパラメータ
   input angle[32] gamma;    // 問題パラメータ
   input int num_layers;     // QAOA層数
   output bit[4] solution;
   
   qubit[4] q;
   
   // 初期状態: 均等重ね合わせ
   h q;
   
   // QAOA層
   for layer in [0:num_layers-1] {
       @debug.trace("QAOA層実行中")
       
       // 問題ハミルトニアン
       for i in [0:2] {
           @optimization.parallel
           rzz(2*gamma) q[i], q[i+1];
       }
       rzz(2*gamma) q[3], q[0];
       
       // ミキサーハミルトニアン
       for i in [0:3] {
           rx(2*beta) q[i];
       }
   }
   
   solution = measure q;

アダプティブ量子アルゴリズム
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @doc.description("フィードバック制御付き量子回路")
   
   input angle initial_angle;
   input float convergence_threshold;
   output angle final_angle;
   output int iterations_used;
   
   qubit q;
   bit measurement;
   angle current_angle = initial_angle;
   int iteration = 0;
   float error = 1.0;
   
   // 適応的パラメータ調整
   while (error > convergence_threshold && iteration < 100) {
       @debug.checkpoint("反復開始")
       
       ry(current_angle) q;
       measurement = measure q;
       
       // フィードバックベースの調整
       if (measurement) {
           current_angle *= 0.9;  // 角度を減少
       } else {
           current_angle *= 1.1;  // 角度を増加
       }
       
       // 収束判定
       error = abs(current_angle - π/2);
       iteration += 1;
       
       reset q;
   }
   
   final_angle = current_angle;
   iterations_used = iteration;

ハードウェア最適化
------------------

デバイス固有アノテーション
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @hardware.target("superconducting")
   @hardware.topology("heavy_hex")
   
   input angle[32] rotation_parameter;
   
   qubit[7] q;  // Heavy-hexトポロジーに適した配置
   
   @hardware.native_gate
   def native_rx(angle theta, qubit target) {
       // ハードウェアネイティブな実装
       U(theta, -π/2, π/2) target;
   }
   
   // トポロジーを考慮した回路
   native_rx(rotation_parameter) q[0];
   @hardware.swap_route(q[0], q[6])
   cx q[0], q[6];

エラー軽減アノテーション
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @error_mitigation.technique("zero_noise_extrapolation")
   @error_mitigation.noise_levels([1.0, 1.5, 2.0])
   
   input angle theta;
   output bit corrected_result;
   
   qubit q;
   
   @error_mitigation.critical_gate
   ry(theta) q;
   
   corrected_result = measure q;

コンパイル時処理
----------------

メタプログラミング
~~~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   @compile.generate_variants(["theta = π/4", "theta = π/2", "theta = π"])
   def parameterized_preparation(angle theta, qubit q) {
       ry(theta) q;
   }

最適化制御
~~~~~~~~~~

.. code-block:: qasm3

   @optimization.preserve_structure
   def critical_sequence(qubit[3] q) {
       // この順序を保持する必要がある重要なゲート列
       barrier q;
       h q[0];
       cx q[0], q[1];
       cx q[1], q[2];
       barrier q;
   }

名前空間管理
------------

カスタム名前空間
~~~~~~~~~~~~~~~~

.. code-block:: qasm3

   // カスタム名前空間の使用例
   pragma mycompany.optimization.level 3;
   pragma mycompany.hardware.backend "custom_processor";
   
   @mycompany.circuit.version("1.2.0")
   @mycompany.license("MIT")
   def proprietary_algorithm(qubit[8] q) {
       // 独自アルゴリズムの実装
   }

標準名前空間
~~~~~~~~~~~~

.. code-block:: qasm3

   // 標準的な名前空間の例
   pragma qiskit.optimization.level 2;
   pragma cirq.device "sycamore";
   pragma braket.shots 1000;
   
   @ibm.error_mitigation.readout_correction
   qubit[5] q;
   
   @google.hardware.native
   def sqrt_x(qubit q) {
       // Google固有のsqrt(X)ゲート
   }

実行時考慮事項
--------------

パラメータ検証
~~~~~~~~~~~~~~

.. code-block:: qasm3

   input angle theta;
   input int repetitions;
   
   // 実行時パラメータの検証
   @runtime.validate("0 <= theta <= 2*π")
   @runtime.validate("repetitions > 0")
   
   qubit q;
   
   for i in [0:repetitions-1] {
       ry(theta) q;
   }

動的最適化
~~~~~~~~~~

.. code-block:: qasm3

   @runtime.adaptive_optimization
   input angle[32][100] parameter_sweep;
   output float[100] energy_values;
   
   qubit[4] q;
   
   // 実行時最適化が適用される
   for i in [0:99] {
       // VQE回路
       for j in [0:3] {
           ry(parameter_sweep[i][j]) q[j];
       }
       
       // エネルギー測定（概念的）
       energy_values[i] = measure_energy(q);
       reset q;
   }

まとめ
------

OpenQASMのディレクティブと注釈システムは：

- **拡張性**: 名前空間による衝突回避
- **柔軟性**: パラメトリック回路の効率的実装
- **最適化**: コンパイラへの詳細な制御指示
- **移植性**: ハードウェア固有の最適化情報
- **デバッグ**: 実行時の詳細な情報提供

これらの機能により、高度で効率的な量子プログラムの開発が可能になります。