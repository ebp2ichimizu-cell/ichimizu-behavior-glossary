# Ver.5 参考文献HTML版の差し替え手順

## 今回の成果物

- `ichimizu-v5-references-patch.zip`：今回の変更・追加ファイルのみ。現在のサイトへの反映はこちらを推奨。
- `ichimizu-v5-references-full.zip`：GitHubから取得した現在のサイトに今回の変更を適用した一式。RIS・PDF・画像・既存用語ページを含みます。

対象リポジトリ：https://github.com/ebp2ichimizu-cell/ichimizu-behavior-glossary

取得時の既定ブランチ：`main`。取得スナップショット：`991bb89`、確認日：2026-10-03。
リポジトリのREADME.txtにVer.5と記載されている配置済みデータを使用しました。
前のChatGPTチャットの添付ZIPはこの作業環境では取得できず、別途アップロードされたV5 ZIPとの同一性は確認していません。
書誌情報はGitHubの `sources/` にある元RISから直接生成しています。

## GitHubへの配置

1. 上記リポジトリの `main` を開きます。作業前の状態を残すため、必要ならGitHubの「Code → Download ZIP」でバックアップします。
2. `ichimizu-v5-references-patch.zip` を展開します。
3. 展開したフォルダそのものではなく、その**中身**をリポジトリのルート（既存の `index.html` がある階層）へ配置します。
4. 同名ファイルを上書きし、追加ファイルを保存してコミットします。フォルダ全体の削除・置換は不要です。
5. GitHub Pagesの公開処理完了後、下記のURLを開いて確認してください。

### 上書きするファイル（5ファイル）

```text
index.html
theories/routine-activity-theory/index.html
theories/protection-motivation-theory/index.html
theories/cpted/index.html
theories/ebp/index.html
```

### 追加するファイル（7ファイル）

```text
references/index.html
theories/routine-activity-theory/references.html
theories/protection-motivation-theory/references.html
theories/cpted/references.html
theories/ebp/references.html
build_readable_references.cjs
UPLOAD_GUIDE.md
```

`terms/`、`words/`、`sources/`、各JSON、スライド画像・PDFは変更していません。今回の差分ZIPにこれらは含めていません。
全体ZIPには取得時点の既存ファイルをそのまま含めています。以後GitHub側で別の変更をした場合は、全体ZIPで上書きせず差分ZIPを使ってください。

## 配置後の文献ページURL

以下は今回追加するページの公開後URLです。この作業ではGitHubへのアップロードは行っていません。

| ページ | URL | 元RISの登録件数 |
|---|---|---:|
| 総合一覧 | https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/references/index.html | 4分野 |
| RAT | https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/theories/routine-activity-theory/references.html | 13 |
| PMT | https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/theories/protection-motivation-theory/references.html | 19 |
| CPTED | https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/theories/cpted/references.html | 23 |
| EBP | https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/theories/ebp/references.html | 18 |

合計73登録。分野間の重複を除いた論文数という意味ではありません。
既存の `theories/各ID/` でも同じ書誌情報が折りたたまずに表示されます。

## 表示内容と出典

- 全著者、年、タイトル、雑誌名、収録書・資料名、編者、出版社・機関、出版地、巻号、ページ、版、ISBN/ISSN、DOI、URLを元RISの登録範囲で表示。
- 著者・年・タイトル・DOIが未登録の場合はその旨を明記。他の未登録項目は省略。
- DOIリンクは元RISのDOフィールドから `https://doi.org/` を使用して作成。URLは元RISのURフィールドを使用。
- 「元RISの登録項目を見る」で、キーワードなどを含む各レコードの登録値も確認可能。
- 元RIS全ファイルはバイト単位で変更せず保持。Zotero等への取り込み用ダウンロードリンクを継続。
- 文献情報・効果量・研究結果を外部情報や推測で補完していません。論文本文の転載ではありません。

## 確認した内容

- 更新・追加した10 HTMLページを画面幅320 / 375 / 768 / 1440pxで確認。横はみ出し・JavaScript実行エラーなし。
- 各理論ページ・文献専用ページにある全73登録の主要書誌項目を元RISと照合。
- 対象10ページ内の内部リンク、RISダウンロード先、画像・PDF参照先、文献欄へのページ内リンクの存在を確認。
- トップページの検索から理論ページ、文献欄、専用一覧へ移動できることを確認。
- JavaScript無効でも文献一覧を読めることを確認。
- `sources/`・`terms/`・`words/` の236ファイル、およびスライドPDF・画像が取得時の内容と一致することを確認。
- 外部DOI・出版社等のリンクは元RISから引き継ぎました。全リンク先の応答・本文閲覧可否は今回一括検証していません。

## 今後RISを更新する場合

GitHub上の正式な管理データを更新したうえで、既存手順の末尾に今回のHTML生成を追加します。

```text
python build_reference_catalog.py
python publish_library.py
node build_readable_references.cjs
```

最後のコマンドにはNode.jsが必要です。追加ライブラリのインストールは不要です。閲覧者やGitHub PagesではNode.jsもPythonも不要です。
今回追加した生成処理は元RIS・terms・wordsを書き換えず、文献HTMLとトップページの導線だけを更新します。
既存の `publish_library.py` だけを実行すると旧表示に戻るため、必ず最後のコマンドまで実行して生成HTMLを配置してください。
文献HTMLだけ再生成する場合は最後のコマンドのみで構いません。

旧README.txtの「中身すべてを更新する」という説明は元のV5全体更新用です。今回の参考文献表示の更新は本書の差分配置手順に従ってください。
