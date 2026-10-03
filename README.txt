いちみず会EBP関連用語ライブラリー v4（2026-10-03）

【構成】
- index.html：3タブ表示（行動経済学／心理学／犯罪予防理論）と分野横断検索
- words/：115用語の個別HTML（既存75件のURL・固定IDは維持）
- terms/：1用語1JSON。現在は115語（既存75＋心理学40）。※これが内容の正本
- glossary.json：個別JSONから再生成した一覧データ
- theories.json / theories/：犯罪予防理論4件のページ（既存スライドは未同梱）
- publish_library.py：termsの内容からHTMLを再生成するビルド用スクリプト
- vol1_tags.html：コラムVol.1の関連用語タグをそのまま使用するためのHTML
- portal_small_link.html：既存ポータルの小さな導線のHTML例
- google_sites_embed.html：Googleサイト用iframeの例
- 心理学40語_出典一覧.md：追加用語と確認水準

【収録数】
行動経済学タブ：75語
心理学タブ：72語（心理学新規40語・既存共通32語）
犯罪予防理論タブ：4件（スライド未配置）
ユニークな用語：115語。共通32語は複製せず1JSON管理。

【GitHub Pagesへの配置】
既存の ichimizu-behavior-glossary リポジトリの公開ブランチのルートにZIP展開内容を追加/上書きする。
index.html, words/, terms/ は対応する最新版で上書きし、theories/ と theories.json を追加する。
既にあるリポジトリ固有のファイルや既存スライドを削除しないよう、上書き前に現状を確認する。
公開URLを変更しないこと。既存のVol.1の個別用語リンクは以前と同じ固定パスを維持している。

【今後3枚スライドを掲載する方法】
theories/<theory-id>/slide1.png, slide2.png, slide3.png を配置してから
  python publish_library.py
でページを再生成する（.jpg, .jpeg, .webpも対応）。原画像がない段階では未掲載と表示。

【用語の追加・修正】
terms/<id>.json を編集・新規追加し、
  python publish_library.py
で全ページ再生成する。分類が複数にまたがるときは
  "library_tabs": ["behavioral_economics","psychology"]
のように同一IDに複数タブを指定する。
原著・レビュー・書籍の別と公開要旨／全文精査の違いをJSONに明記する。
※40語の作成時のみ用いた調査補助プログラムは更新作業には不要のため同梱していない。

【技術・公開上の注意】
単一のHTML/CSS/JSによる静的ページで、検索はブラウザ内で実行する（外部サービス不要）。
検索語が空のときタブ内を表示し、検索語があるときはタブに関係なく全分野を検索する。
各ページを読み込み、リンクが繋がるかブラウザのデスクトップ/スマホ表示で最終確認すること。
Googleサイト本体とGitHubへのコミットは未実施。
参考資料は主に出版社/公的学術機関の書誌・公開要旨により照合。全件の全文精読までは主張しない。
