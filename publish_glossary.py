from pathlib import Path
import json,html,zipfile,shutil
src=Path(__file__).resolve().parent; out=src;out.mkdir(exist_ok=True)
(out/'terms').mkdir(exist_ok=True); (out/'words').mkdir(exist_ok=True)
if src != out:
 for f in (src/'terms').glob('*.json'): shutil.copy2(f,out/'terms'/f.name)
items=[json.loads(f.read_text()) for f in sorted((out/'terms').glob('*.json'))]; ids={x['id'] for x in items};assert len(ids)==len(items)==75
items.sort(key=lambda x:(x['cat'],x['ja']))
(out/'glossary.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
BASE='https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/'
def e(v): return html.escape(str(v),quote=True)
CSS='''*{box-sizing:border-box}body{margin:0;background:#fbfbf7;color:#2f322b;font:15px/1.8 -apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif}a{color:#5f6730}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #9f9a4e;outline-offset:2px}header{background:#34362d;color:white;padding:32px 18px}header .inner,main{max-width:980px;margin:auto}h1{margin:0;font-size:clamp(21px,3vw,28px)}.sub{margin:4px 0;color:#e0dfd1;font-size:13px}main{padding:24px 16px 60px}h2{font-size:19px;margin:25px 0 9px}.note,.muted{color:#656960;font-size:13px}.search{width:100%;padding:13px 15px;border-radius:9px;border:1px solid #b9bbae;background:white;font:inherit}.chips{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0}.chips button{border:1px solid #a6a68c;background:white;border-radius:24px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}.chips button[aria-pressed=true]{background:#a8a65d;color:#171b17}.letters{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0}.letters a{padding:4px 10px;background:#ededdf;border-radius:6px;text-decoration:none}.group{scroll-margin-top:12px;margin-top:23px}.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}.term{padding:11px 13px;border:1px solid #deded3;background:white;border-radius:8px;display:block;text-decoration:none;color:inherit}.term:hover{border-color:#92944e;background:#f7f7ee}.term strong{display:block;font-size:15px}.term small{color:#666a62}.pill{background:#f0efd9;border-radius:5px;padding:2px 6px;font-size:11px}.section{margin-top:20px;background:white;border:1px solid #e1e2d7;border-radius:10px;padding:15px 18px}.section h2{margin:0 0 6px;color:#555b33;font-size:15px}.section p{margin:0}.links{display:flex;gap:12px;flex-wrap:wrap}.links a{word-break:break-all}.back{margin:0 0 15px}footer{padding:20px;background:#eeeee6;text-align:center;font-size:12px;color:#56574b}.empty{padding:25px;text-align:center;color:#666}@media(max-width:600px){header{padding:24px 14px}.items{grid-template-columns:1fr}main{padding:18px 13px 45px}}'''
def wrap(title,body,inside=False):
 return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="空想EBP読本の行動経済学・行動科学用語集。原著と転用仮説を区別して紹介します。"><title>'+e(title)+'｜空想EBP読本 用語集</title><style>'+CSS+'</style></head><body><header><div class="inner"><h1>行動経済学・行動科学 用語集</h1><p class="sub">空想EBP読本｜研究の知見を、犯罪予防の問いにつなぐ</p></div></header><main>'+body+'</main><footer>用語の出典確認状況を明示しています。応用例は、特記がなければ未検証の仮説です。</footer></body></html>'
# detail pages
for x in items:
 sections=[('定義',x['original_definition']),('考え方・作用',x['explanation']),('犯罪予防への応用仮説',x['application_hypothesis']),('注意点・反証',x['limitations']),('研究上の位置づけ',x.get('concept_status','')),('原典確認上の留意点',x.get('origin_audit_note','')),('効果に関する根拠・留意点',x.get('evidence_note',''))]
 content='<p class="back"><a href="../">← 検索・索引へ戻る</a></p><p><span class="pill">'+e(x['cat'])+'</span> <span class="pill">'+({'source_checked':'関連出典を確認','related_sources_checked':'関連研究・総説まで確認','bibliography_confirmed':'原著書誌まで確認（本文精査は未了）','nonstandard_term':'標準用語としての原典未確立'}.get(x['verification_status'],'出典精査中'))+'</span></p><h1>'+e(x['ja'])+'</h1><p class="muted">'+e(x['en'])+' ｜ '+e(x.get('academic_domain',''))+'</p>'
 for label,value in sections:content+='<section class="section"><h2>'+label+'</h2><p>'+e(value or '記載なし')+'</p></section>'
 s=x.get('sources',[])
 content+='<section class="section"><h2>原典・参考文献</h2>'+ ('<div>'+''.join('<div style="margin-bottom:9px"><a target="_blank" rel="noopener noreferrer" href="'+e(r['url'])+'">'+e(r['title'])+'</a><br><small>'+e(r.get('role','資料の位置づけ：追加確認を要する'))+ (('｜'+e(r['verification_note'])) if r.get('verification_note') else '')+'</small></div>' for r in s if r.get('url'))+'</div>' if s else '<p class="note">個別の原典は確認作業中です。出典を推測して掲載していません。</p>')+'</section>'
 related=[z for z in x.get('related_terms',[]) if z in ids]
 if related:content+='<section class="section"><h2>関連用語</h2><div class="links">'+''.join('<a href="'+e(r)+'.html">'+e(next(y['ja'] for y in items if y['id']==r))+'</a>' for r in related)+'</div></section>'
 if x.get('articles'):content+='<section class="section"><h2>関連コラム</h2><div class="links">'+''.join('<a target="_blank" rel="noopener noreferrer" href="'+e(a['url'])+'">'+e(a['title'])+'</a>' for a in x['articles'])+'</div></section>'
 (out/'words'/f'{x["id"]}.html').write_text(wrap(x['ja'],content),encoding='utf8')
# search index, all data embedded offline + client-only dynamic
view=[{'id':x['id'],'ja':x['ja'],'en':x['en'],'cat':x['cat'],'short':x['original_definition']} for x in items]
jsdata=json.dumps(view,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
body='''<h2>用語を探す</h2><p class="note">日本語・英語・定義から検索できます。用語を選ぶと個別解説ページが開きます。</p><input id="q" class="search" type="search" placeholder="用語名・英語・説明を入力" aria-label="用語検索" autocomplete="off"><div id="filters" class="chips" role="group" aria-label="分類で絞り込む"></div><p id="counter" class="note" role="status"></p><div id="list"></div><p class="note">原典確認が完了していない用語は各ページで明示しています。収録数は研究精査に応じて更新します。</p>'''
js='''<script>const terms=__DATA__,cats=['すべて',...new Set(terms.map(t=>t.cat))];let selected='すべて';const q=document.getElementById('q'),list=document.getElementById('list'),filters=document.getElementById('filters'),counter=document.getElementById('counter');const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function update(){const s=q.value.normalize('NFKC').toLowerCase().trim();filters.innerHTML=cats.map(c=>'<button type="button" data-cat="'+esc(c)+'" aria-pressed="'+(c===selected)+'">'+esc(c)+'</button>').join('');const ts=terms.filter(t=>(selected==='すべて'||t.cat===selected)&&[t.ja,t.en,t.short,t.cat].join(' ').normalize('NFKC').toLowerCase().includes(s));counter.textContent=ts.length+' / '+terms.length+' 用語';if(!ts.length){list.innerHTML='<div class="empty">該当する用語がありません。</div>';return;}const cs=[...new Set(ts.map(t=>t.cat))];list.innerHTML=cs.map(cat=>'<section class="group"><h2>'+esc(cat)+'</h2><div class="items">'+ts.filter(t=>t.cat===cat).map(t=>'<a class="term" href="words/'+encodeURIComponent(t.id)+'.html"><strong>'+esc(t.ja)+'</strong><small>'+esc(t.en)+'</small></a>').join('')+'</div></section>').join('')}filters.addEventListener('click',e=>{let b=e.target.closest('button[data-cat]');if(b){selected=b.dataset.cat;update()}});q.addEventListener('input',update);update();</script>'''.replace('__DATA__',jsdata)
index=wrap('検索・索引',body).replace('</body>',js+'</body>');(out/'index.html').write_text(index,encoding='utf8')
# vol 1 tags + portal snippet
labels=['implementation-intentions','reminder','intention-behaviour-gap','friction-costs','implementation-fidelity']
assert all(i in ids for i in labels)
vol='<div style="font-family:sans-serif;font-size:14px;line-height:1.8"><b style="margin-right:8px;color:#34362d">関連用語</b> '+''.join(f'<a href="{BASE}words/{x}.html" target="_blank" rel="noopener" style="display:inline-block;margin:3px;padding:3px 10px;text-decoration:none;border:1px solid #a8a65d;border-radius:18px;color:#34362d;background:#f6f6ef">#{e(next(y["ja"] for y in items if y["id"]==x))}</a>' for x in labels)+'</div>'
(out/'vol1_tags.html').write_text(vol,encoding='utf8')
(out/'portal_small_link.html').write_text('<a href="'+BASE+'" target="_blank" rel="noopener noreferrer" style="color:#6d6e55;font-size:12px;text-decoration:underline;text-underline-offset:3px" aria-label="空想EBP読本の行動経済学・行動科学用語集を開く">行動経済学・行動科学 用語集 <span aria-hidden="true">↗</span></a>\n',encoding='utf8')
(out/'google_sites_embed.html').write_text('<iframe src="'+BASE+'" title="行動経済学・行動科学 用語集" style="width:100%;height:680px;border:0" loading="lazy"></iframe>\n',encoding='utf8')
# regen script for maintenance independent
build='''# 個別JSONを正本として更新する際は、このディレクトリの generate.py を実行してください。\n# UI構造の再生成は publish_glossary.py が必要です。\n'''
(out/'README.txt').write_text("""空想EBP読本｜用語集 v3.2（2026-10-03 原典・出典点検）

構成：index.html（検索）、words/（75解説）、terms/（1用語1JSON）、glossary.json（統合）、関連タグHTML。

更新：terms/*.json を修正→python publish_glossary.py を実行。

【重要な解釈】
「関連出典を確認」は、その用語を直接扱う研究や枠組み・専門レビューへの参照があることを示すのみ。
定義の提唱原著の全文確認、学術界の完全な合意、犯罪予防での介入効果の確立を意味しない。
書籍原著には書誌・出版社概要まで確認し本文が未精査の項目がある。
計画と実行の不一致は、定着した独立専門用語としての原典を確認できないため、明示している。

確認一覧：SOURCE_AUDIT_2026-10-03.md を参照。
固定URL・75用語のIDを維持。公開先URLはGitHub Pagesで公開するまで実在が保証されない。
""",encoding='utf8')
print('PUBLISHED',len(items),len(list((out/'words').glob('*.html'))))
