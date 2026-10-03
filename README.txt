いちみず会EBP関連用語ライブラリー V5 — GitHub Pages配置用（2026-10-03）

■ 更新内容
・従来115用語を維持（元のwords/<id>.htmlへのURLは変更しない）。
・検索は全分野横断。行動経済学／心理学／犯罪予防理論・EBPの3タブを設置。
・RAT、PMT、CPTED、EBPの実際の3枚スライドを掲載。画像3枚・PDF原本をそれぞれ同梱。
・合理的選択理論はスライド未完成につき今回は公開一覧に掲載しない。今後追加できる構造。
・原典・関連文献は添付RISをそれぞれ保持し、ページごとに参照一覧とRISダウンロードを設置。
・EBPは犯罪予防理論と混同しないよう「EBPの基礎資料」分類。
・PMTに関する用語（脅威評価／対処評価／自己効力感）からスライドへリンク。

■ GitHub Pagesへの反映方法
1. リポジトリ ebp2ichimizu-cell/ichimizu-behavior-glossary の公開ブランチを開く。
2. 本ZIPを展開し、ZIP内のフォルダではなく「中身すべて」を公開リポジトリのルートに配置・上書きする。
3. 特に index.html、terms/、words/、theories/、sources/ と各JSONをまとめてアップロードする。
4. GitHub Actions等でPages公開を確認。既存のコラムVol.1リンクが引き続き開くことを確認する。
5. GitHub Pagesの想定URL: https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/
   ※既存サイトの実URLが違う場合、publish_library.py内BASEも修正して再生成する。

■ 既存リンクとの互換性
・words/以下の115語のID・公開パスは従来どおり。
・Vol.1関連用語タグ用コード vol1_tags.html、および portal_small_link.html も含む。
・新たな理論URLは theories/<id>/ 形式。

■ 更新の手順
・用語追加・修正: terms/<id>.jsonを更新。
・理論の追加: theories.jsonに登録し、theories/<id>/slide1.png～slide3.pngを配置。
・参考文献RISの更新: sources/内RISを差し替え、下記の再生成コマンドを実行。
    python build_reference_catalog.py
    python publish_library.py
・3枚スライド原本PDFの閲覧リンクは theories/<id>/slides.pdf 。
・GitHub Pagesは静的ファイル配信のため、変更時に再生成したHTMLをコミットする。

■ 掲載に際しての注意
・スライドはユーザー提供PDFから作成し、文面と図は変更していない。
・各理論ページの文献一覧はRISの登録書誌情報であり、原著本文と個別主張の照合済みを意味しない。
・今回のPDF・RISは利用者提供ファイルであり、Zotero内の最新変更とは自動同期されない。
・Googleサイトへの埋め込みではiframeが制限される場合があるため、URL埋め込み方式も利用可能。
・GitHubへの公開操作自体は未実施。
