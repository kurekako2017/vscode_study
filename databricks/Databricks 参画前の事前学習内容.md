Databricks 参画前の事前学習内容

Databricksの実務経験がない場合でも、PL/SQLなどのSQL経験があれば、事前に基本的な概念と操作方法を押さえておくことで、現場へのキャッチアップがしやすくなります。

事前学習では、細かい技術仕様やSparkの内部処理まで深く理解する必要はなく、まずは以下の内容を一通り確認しておくことをおすすめします。

1. Databricksの基本概念

まず、Databricksがどのようなサービスで、どのようにデータ処理を行うものなのかを理解する。

* Databricksの概要
* Workspaceの基本概念
* Catalog / Schema / Tableの関係
* Data Lake / Lakehouseの基本的な考え方
* SQL Warehouse / Compute（Cluster）の概要

→ まずは「Databricks上でデータをどのように管理・処理するのか」を理解できれば十分です。

2. Notebookの基本操作【重点】

現場ではNotebookを使用してデータ処理やSQLの実行を行うケースが多いため、基本的な操作方法を確認しておく。

* Notebookの作成・編集
* Cellの作成・実行
* SQL / Python / PySparkの基本的な使い分け
* テーブルの参照・検索
* 実行結果の確認
* Notebookの保存・管理
* 簡単なデータ加工処理の実行

特に、実際にNotebookを操作しながら、SQLを記述してテーブルを参照するところまで経験しておくとよいです。

3. Databricks SQL【重点】

PL/SQLの経験を活かせる部分なので、まずはSQLを中心にキャッチアップする。

以下のような基本的なSQLについて、Databricks上で実行できるようにしておく。

* SELECT
* WHERE
* GROUP BY
* ORDER BY
* JOIN
* CASE WHEN
* サブクエリ
* CTE
* INSERT
* UPDATE
* MERGE
* CREATE TABLE / VIEW

また、DatabricksでのTable / View / Temporary Viewなどの違いについても、概要を理解しておく。

4. Bronze / Silver / Goldの理解【重点】

Databricksでよく使用されるデータレイヤーの考え方を理解する。

* Bronze：元データ・取り込み直後のデータ
* Silver：データのクレンジング・加工後のデータ
* Gold：業務・分析用途に合わせて加工されたデータ

例えば、

「BronzeからSilverへデータを加工する」

と言われた際に、どのような処理を指しているのかイメージできる程度まで理解しておく。

5. Spark / PySparkの基礎

Sparkについては、事前に深く勉強する必要はありません。

まずは以下のレベルを目標とする。

* Apache Sparkとは何か
* DatabricksとSparkの関係
* PySparkとは何か
* DataFrameとは何か
* DataFrameを使用した簡単なデータ抽出・加工

例えば、以下のような簡単なPySparkコードを見た際に、何をしている処理なのか理解できる程度で十分です。

df = spark.read.table("bronze.customer")
df.filter(df["status"] == "ACTIVE") \
  .select("customer_id", "name")

Sparkの内部構造、RDD、Shuffle、パーティション、Catalyst Optimizerなどの詳細については、現時点では優先度は低いです。

6. 実際に触ってみる

可能であれば、公式ドキュメントを読むだけではなく、実際にDatabricksの環境で以下を一通り操作してみる。

1. Notebookを作成
2. SQLを実行
3. Tableを参照
4. JOINなどのデータ加工を実施
5. 簡単なTable / Viewを作成
6. PythonまたはPySparkで簡単なデータ処理を実行
7. Bronze → Silver → Goldの流れを簡単に確認

7. 学習の優先順位

時間が限られている場合は、以下の順番で学習してください。

優先度：高

1. Databricksの基本概念
2. Notebookの基本操作
3. Databricks SQL
4. Bronze / Silver / Gold

優先度：中
5. Spark / PySparkの基礎
6. Table / View / Catalog / Schemaなどのデータ管理

優先度：低
7. Sparkの内部処理・アーキテクチャ
8. 高度なパフォーマンスチューニング

まずは「DatabricksでSQLを使ってデータを確認・加工できる」「Notebookの基本操作ができる」「Bronze / Silver / Goldの意味が分かる」という状態を目標にしてください。

PL/SQLの経験がある場合、SQL部分は既存の知識を活かせるため、Databricks特有の操作やデータ処理の考え方を中心にキャッチアップするのが効率的です。