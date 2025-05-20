"""
日本語のガウスフィルターチャットボット用ナレッジベース。
コードベース、概念、機能に関する情報を含みます。
"""

JA_KNOWLEDGE_BASE = {
    "project": {
        "name": "ガウスフィルター",
        "description": "OpenCVを使用して画像にガウスぼかしフィルターを適用するシンプルなC++アプリケーション。",
        "repository": "ashandrin/test_cpp",
        "files": ["gaussian_filter.cpp", "Makefile"]
    },
    
    "code_structure": {
        "gaussian_filter.cpp": "ガウスカーネル生成関数とメインアプリケーションロジックを含むメインソースファイル。",
        "Makefile": "g++を使用してアプリケーションをコンパイルし、OpenCVとリンクするビルド設定。"
    },
    
    "functions": {
        "createGaussianKernel": {
            "purpose": "画像のぼかしに使用する2Dガウスカーネルを作成します",
            "parameters": [
                {"name": "rows", "type": "int", "description": "カーネルの行数"},
                {"name": "cols", "type": "int", "description": "カーネルの列数"},
                {"name": "sigmaX", "type": "double", "description": "X方向の標準偏差"},
                {"name": "sigmaY", "type": "double", "description": "Y方向の標準偏差"}
            ],
            "return": {"type": "cv::Mat", "description": "正規化されたガウスカーネル"},
            "algorithm": "2Dガウス分布を表す値のマトリックスを作成します。各位置(x,y)の値は次の式で計算されます：exp(-(x^2/(2*sigmaX^2) + y^2/(2*sigmaY^2)))。その後、カーネルはすべての値の合計が1になるように正規化されます。"
        },
        "main": {
            "purpose": "ガウスフィルターで画像を処理するエントリーポイント",
            "parameters": [
                {"name": "argc", "type": "int", "description": "コマンドライン引数の数"},
                {"name": "argv", "type": "char**", "description": "コマンドライン引数の配列"}
            ],
            "return": {"type": "int", "description": "終了コード（成功の場合は0、エラーの場合は-1）"},
            "algorithm": "コマンドライン引数を解析し、入力画像を読み込み、ガウスカーネルを作成し、OpenCVのfilter2D関数を使用して画像に適用し、結果を保存します。"
        }
    },
    
    "concepts": {
        "gaussian_filter": "ガウス関数を使用して画像をぼかすフィルター。近くのピクセルが遠くのピクセルよりも大きな影響を持つ加重平均を適用することで、ノイズやディテールを減らします。",
        "kernel": "畳み込み演算に使用される小さなマトリックス。画像処理では、カーネルが各ピクセルとその周囲に適用され、新しい値を生成します。",
        "sigma": "ガウス分布の「広がり」を制御します。シグマ値が大きいほど、より広いベル曲線になり、よりぼかしが強くなります。",
        "convolution": "カーネルと画像を組み合わせる数学的演算。各カーネル値に対応する近傍のピクセル値を掛け、これらの積を合計します。",
        "filter2D": "指定されたカーネルを使用して畳み込み演算を適用するOpenCV関数。",
        "normalization": "フィルタリング後も画像の明るさを維持するために、値の合計が1になるように調整するプロセス。"
    },
    
    "usage": {
        "compilation": "リポジトリディレクトリで「make」を実行してアプリケーションをコンパイルします。",
        "execution": "「./gaussian_filter [入力パス] [出力パス]」を実行して画像を処理します。",
        "command_line_args": [
            {"name": "入力パス", "description": "入力画像へのパス（オプション、デフォルトはハードコードされたパス）"},
            {"name": "出力パス", "description": "出力画像のパス（オプション、デフォルトは現在のディレクトリの「output.jpg」）"}
        ],
        "examples": [
            {"command": "./gaussian_filter", "description": "デフォルト画像を処理します"},
            {"command": "./gaussian_filter input.jpg", "description": "input.jpgをデフォルトの出力パスで処理します"},
            {"command": "./gaussian_filter input.jpg blurred.jpg", "description": "input.jpgを処理し、blurred.jpgとして保存します"}
        ]
    },
    
    "dependencies": {
        "opencv": {
            "name": "OpenCV",
            "description": "オープンソースコンピュータビジョンライブラリ、画像処理操作に使用",
            "version": "4.x（Makefileで指定）",
            "components_used": [
                {"name": "imread", "purpose": "画像ファイルの読み込み"},
                {"name": "imwrite", "purpose": "画像ファイルの書き込み"},
                {"name": "filter2D", "purpose": "畳み込みフィルターの適用"}
            ]
        }
    }
}

JA_DETAILED_EXPLANATIONS = {
    "gaussian_kernel_algorithm": """
createGaussianKernel関数は、次の手順で2Dガウスカーネルを生成します：
1. 指定された寸法の空のマトリックスを作成します
2. カーネルの中心点を計算します
3. カーネル内の各位置(i,j)に対して：
   a. 中心からの距離(x,y)を計算します
   b. 2Dガウス公式を適用します： exp(-(x^2/(2*σ_x^2) + y^2/(2*σ_y^2)))
   c. 結果をカーネルに格納します
4. カーネル内のすべての値を合計します
5. すべての値を合計で割ることでカーネルを正規化します
6. 正規化されたカーネルを返します

これにより、中心が最高値を持ち、中心から離れるにつれて値が減少するベル型の分布が作成されます。
    """,
    
    "image_processing_pipeline": """
main関数は次の画像処理パイプラインを実装しています：
1. コマンドライン引数を解析して入力と出力のパスを取得します
2. OpenCVのimreadを使用して入力画像を読み込みます
3. 画像が正常に読み込まれたかどうかを確認します
4. ガウスカーネルを作成します（8x8、σ=1.5）
5. カーネルを適切な形式（CV_32F）に変換します
6. filter2Dを使用して画像にカーネルを適用します
7. 結果を出力パスに保存します
8. 成功または失敗をユーザーに報告します

filter2D関数は次の方法で畳み込みを実行します：
- 各ピクセルにカーネルを中心に配置します
- 各カーネル値に対応するピクセル値を掛けます
- これらの積を合計して新しいピクセル値を取得します
- 画像内のすべてのピクセルに対してこれを繰り返します
    """
}
