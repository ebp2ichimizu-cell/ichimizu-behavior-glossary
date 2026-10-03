from pathlib import Path
import json,html,unicodedata,os
ROOT=Path(__file__).resolve().parent
items=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'terms').glob('*.json'))]
assert len(items)==len({t['id'] for t in items})
byid={t['id']:t for t in items}
theories=json.loads((ROOT/'theories.json').read_text(encoding='utf-8'))
assert len(theories)==len({t['id'] for t in theories})
BASE='https://ebp2ichimizu-cell.github.io/ichimizu-behavior-glossary/'
site='いちみず会EBP関連用語ライブラリー'
for t in items:
 for k in ['id','ja','en','original_definition','explanation','application_hypothesis','limitations','library_tabs']:
  assert t.get(k), (t['id'],k)
 assert all(z in ['behavioral_economics','psychology'] for z in t['library_tabs'])
for t in theories:assert all(t.get(k) for k in ['id','ja','en','short'])
# supplementary data are generated from canonical 1-term-1-JSON, no duplicate definitions
items.sort(key=lambda t:t['ja'])
(ROOT/'glossary.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'words').mkdir(exist_ok=True)
(ROOT/'theories').mkdir(exist_ok=True)
def e(s):return html.escape(str(s),quote=True)
CSS='''*{box-sizing:border-box}body{margin:0;background:#f9faf6;color:#30332e;font:15px/1.85 -apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif}a{color:#58662f}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #afad5f;outline-offset:2px}header{background:#34362e;color:#fff;padding:32px 18px}header .inner,main{max-width:1050px;margin:auto}h1{font-size:clamp(21px,3vw,29px);line-height:1.5;margin:0}.sub{margin:4px 0;color:#e4e4d5;font-size:13px}main{padding:22px 16px 64px}h2{font-size:19px;margin:20px 0 10px}p{overflow-wrap:anywhere}.muted,.note{color:#60675e;font-size:13px}.tabs{display:flex;flex-wrap:wrap;border-bottom:2px solid #b3b49b;gap:7px;margin:8px 0 20px}.tabs button{appearance:none;border:1px solid #d3d5c9;border-bottom:0;padding:10px 16px;border-radius:9px 9px 0 0;cursor:pointer;background:#efefe7;color:#323529;font:inherit;font-weight:600}.tabs button[aria-selected=true]{background:#a6a45a;border-color:#a6a45a;color:#181c10}.search{display:block;width:100%;border:1px solid #b9bbae;border-radius:8px;padding:12px 14px;font:inherit;background:#fff}.chips{display:flex;flex-wrap:wrap;gap:7px;margin:11px 0}.chips button{font:inherit;font-size:13px;cursor:pointer;border:1px solid #a6a98e;border-radius:22px;padding:6px 11px;background:#fff}.chips button[aria-pressed=true]{background:#a6a45a;color:#171b10}.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}.term{display:block;border:1px solid #dfe0d7;background:#fff;border-radius:9px;padding:12px 14px;text-decoration:none;color:inherit;min-height:95px}.term strong{display:block;font-size:15px}.term small{display:block;color:#656b61;font-size:12px;line-height:1.5}.term .hint{color:#62675c;font-size:12px;margin:6px 0 0}.term:hover{border-color:#92944e;background:#f8f8ed}.group{margin:20px 0 24px}.group h2{border-left:4px solid #a6a45a;padding-left:10px;margin:0 0 10px}.pill{display:inline-block;background:#eae8d3;border-radius:5px;padding:2px 8px;font-size:12px;margin:3px 4px 3px 0}.panel{background:#fff;border:1px solid #e1e2d7;border-radius:10px;padding:16px 19px;margin:18px 0}.panel h2{font-size:16px;color:#535d31;margin:0 0 8px}.panel p{margin:0}.back{margin:0 0 16px}.links{display:flex;gap:8px;flex-wrap:wrap}.links a{border:1px solid #d1d3c1;padding:4px 10px;border-radius:14px;text-decoration:none}.source{margin-bottom:13px;padding-bottom:10px;border-bottom:1px solid #efefed}.source small{color:#61645b}.theory{display:block;text-decoration:none;background:#fff;border:1px solid #dadbd0;border-radius:10px;padding:13px 15px;color:inherit}.theory small{color:#555b51}.theory .pending{font-size:12px;color:#706e50}.slide{margin:15px auto 20px;text-align:center}.slide img{display:block;max-width:100%;height:auto;border:1px solid #d6d6c9}.download{margin:12px 0;padding:11px;background:#f2f3ea;border-radius:9px}.download a{margin-right:16px}.refs summary{font-weight:600;cursor:pointer}.refs li{margin:9px 0;overflow-wrap:anywhere}.empty{color:#6a6c63;padding:22px;border:1px dashed #ccc;border-radius:10px;text-align:center}footer{background:#eeeee7;padding:19px 12px;text-align:center;font-size:12px;color:#55594e}@media(max-width:600px){header{padding:24px 14px}.tabs button{padding:9px 10px;font-size:13px}.cards{grid-template-columns:1fr}main{padding:16px 13px 42px}}'''
def frame(title,body,script=''):
 return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="行動経済学、心理学、犯罪予防理論・EBPを横断検索。定義・出典・応用仮説を整理。"><title>'+e(title)+'｜'+site+'</title><style>'+CSS+'</style></head><body><header><div class="inner"><h1>'+site+'</h1><p class="sub">行動経済学・心理学・犯罪予防理論・EBPをつなぐ参照資料</p></div></header><main>'+body+'</main><footer>原著の内容・研究者の解釈・犯罪予防への応用仮説は区別して掲載しています。未掲載資料は掲載準備中と表示します。</footer>'+script+'</body></html>'
for t in items:
 pills=''.join('<span class="pill">'+e({'behavioral_economics':'行動経済学','psychology':'心理学'}[tab])+'</span>' for tab in t['library_tabs'])
 c='<p class="back"><a href="../">← 検索・索引へ戻る</a></p>'+pills+'<h2>'+e(t['ja'])+'</h2><p class="muted">'+e(t['en'])+'</p>'
 for label,key in [('定義','original_definition'),('考え方・作用','explanation'),('犯罪予防への応用仮説','application_hypothesis'),('成立条件・注意点','limitations'),('根拠について','evidence_note')]:
  if t.get(key):c+='<section class="panel"><h2>'+e(label)+'</h2><p>'+e(t[key])+'</p></section>'
 sources=t.get('sources',[])
 c+='<section class="panel"><h2>原典・参考文献</h2>'
 for s in sources:
  c+='<div class="source"><a href="'+e(s.get('url','#'))+'" target="_blank" rel="noopener noreferrer">'+e(s.get('title','資料'))+'</a><br><small>'+e(s.get('verification_note',''))+'</small></div>'
 c+='</section><section class="panel"><h2>確認状況</h2><p>'+e(t.get('origin_audit_note') or '原著全体の再精読は実施していない場合があります。出典に示す確認範囲を参照。')+'</p></section>'
 rel=[z for z in t.get('related_terms',[]) if z in byid and z!=t['id']]
 if rel:c+='<section class="panel"><h2>関連用語</h2><div class="links">'+''.join('<a href="'+e(z)+'.html">'+e(byid[z]['ja'])+'</a>' for z in rel)+'</div></section>'
 if t['id'] in ['threat-appraisal','coping-appraisal','self-efficacy']:
  c+='<section class="panel"><h2>関連理論</h2><a href="../theories/protection-motivation-theory/">防護動機理論（3枚スライド）</a></section>'
 if t.get('articles'):
  c+='<section class="panel"><h2>関連コラム</h2>'+''.join('<div><a href="'+e(a['url'])+'">'+e(a['title'])+'</a></div>' for a in t['articles'])+'</section>'
 (ROOT/'words'/(t['id']+'.html')).write_text(frame(t['ja'],c),encoding='utf-8')
# Theory and EBP pages: user-supplied 3-page slide PDFs and their RIS bibliographies.
REFS=json.loads((ROOT/'sources'/'references.json').read_text(encoding='utf-8'))
for t in theories:
 d=ROOT/'theories'/t['id']; d.mkdir(parents=True,exist_ok=True)
 slides=[]
 for n in range(1,4):
  hits=[ext for ext in ['png','jpg','jpeg','webp'] if (d/(f'slide{n}.'+ext)).is_file()]
  if hits:slides.append((n,'slide'+str(n)+'.'+hits[0]))
 status='掲載済み（3枚）' if len(slides)==3 else ('一部掲載済み' if slides else 'スライド未配置')
 c='<p class="back"><a href="../../">← 検索・索引へ戻る</a></p><h2>'+e(t['ja'])+'</h2><p class="muted">'+e(t['en'])+'</p><section class="panel"><p>'+e(t['short'])+'</p><p class="note">'+e(status)+'。理論・研究成果と防犯実務への応用を区別してお読みください。</p></section>'
 if (d/'slides.pdf').is_file():
  c+='<div class="download"><a href="slides.pdf" target="_blank" rel="noopener noreferrer">3枚スライドPDFを見る・保存</a></div>'
 for n,file in slides:
  c+='<section class="slide"><h2>スライド '+str(n)+'</h2><a href="'+e(file)+'" target="_blank" rel="noopener noreferrer" title="別タブで拡大"><img src="'+e(file)+'" alt="'+e(t['ja'])+' スライド'+str(n)+'" loading="lazy"></a></section>'
 if len(slides)!=3:c+='<div class="empty">3枚スライドの原本はまだ掲載されていません。</div>'
 refs=REFS.get(t['id'],[])
 if refs:
  c+='<section class="panel refs"><h2>参考文献</h2><p class="note">添付RISに登録された文献の書誌情報です。各研究の原著全文やスライド中の記述との個別照合が完了したことを意味しません。</p>'
  c+='<details><summary>文献 '+str(len(refs))+' 件を表示</summary><ol>'
  for r in refs:
   author=', '.join(r.get('authors',[])[:3])+(' ほか' if len(r.get('authors',[]))>3 else '')
   label=(author+' ('+str(r.get('year','年不詳'))+'). '+r.get('title','書名・論文名不詳')).strip()
   url=r.get('url','')
   if not url and r.get('doi'):url='https://doi.org/'+r['doi']
   c+='<li>'+(('<a href="'+e(url)+'" target="_blank" rel="noopener noreferrer">'+e(label)+'</a>') if url.startswith(('https://','http://')) else e(label))+'</li>'
  c+='</ol></details><p class="download"><a href="../../sources/'+e(t['reference_file'])+'" download>参考文献データ（RIS）を保存</a></p></section>'
 c+='<p class="note">関連する概念については、上部の検索・索引から行動経済学・心理学の用語も横断検索できます。</p>'
 (d/'index.html').write_text(frame(t['ja'],c),encoding='utf-8')
 t['slide_status']='published' if len(slides)==3 else ('partial' if slides else 'pending')
# search: across all tabs if query nonempty; no duplicates in results
view=[{'id':t['id'],'ja':t['ja'],'en':t['en'],'category':t['cat'],'short':t['original_definition'],'tabs':t['library_tabs'],'kind':'term'} for t in items]
view += [{'id':t['id'],'ja':t['ja'],'en':t['en'],'category':('EBPの基礎資料' if t['id']=='ebp' else '犯罪予防理論'),'short':t['short'],'tabs':['crime_theory'],'kind':'theory','slide_status':t['slide_status']} for t in theories]
jsonjs=json.dumps(view,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
body='''<nav id="tabs" class="tabs" role="tablist" aria-label="分野の切替"><button data-tab="behavioral_economics" role="tab" aria-selected="true">行動経済学</button><button data-tab="psychology" role="tab" aria-selected="false">心理学</button><button data-tab="crime_theory" role="tab" aria-selected="false">犯罪予防理論・EBP</button></nav><label for="q"><strong>用語を横断検索</strong></label><p class="note">検索語を入力すると、選択中のタブに関係なく全分野から探します。用語を選ぶと個別解説ページが開きます。</p><input id="q" class="search" type="search" placeholder="用語・英語・説明を検索" autocomplete="off"><p id="hint" role="status" class="note"></p><div id="filters" class="chips"></div><div id="results"></div>'''
script='''<script>const TERMS=__TERMS__;
const TAB_NAMES={behavioral_economics:'行動経済学',psychology:'心理学',crime_theory:'犯罪予防理論'};
const $=id=>document.getElementById(id), q=$('q'),hint=$('hint'),res=$('results'),filters=$('filters'),tabbar=$('tabs');
let selected='behavioral_economics',cat='すべて';
function norm(v){return String(v||'').normalize('NFKC').toLowerCase().replace(/\\s+/g,' ').trim()}
function esc(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function page(t){return t.kind==='theory'?'theories/'+encodeURIComponent(t.id)+'/':'words/'+encodeURIComponent(t.id)+'.html'}
function render(){let s=norm(q.value);document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.tab===selected)));
let base=TERMS.filter(t=>s?[t.ja,t.en,t.short,t.category,...t.tabs.map(x=>TAB_NAMES[x])].some(x=>norm(x).includes(s)):t.tabs.includes(selected));
let cats=['すべて',...new Set(base.map(t=>t.category))];if(!cats.includes(cat))cat='すべて';
filters.innerHTML=cats.map(c=>'<button type="button" data-cat="'+esc(c)+'" aria-pressed="'+String(cat===c)+'">'+esc(c)+'</button>').join('');
let matching=base.filter(t=>cat==='すべて'||t.category===cat),all=TERMS.length;
hint.textContent=(s?'横断検索：':'表示分野：'+TAB_NAMES[selected]+'／')+matching.length+' 件（登録用語 '+TERMS.filter(t=>t.kind==='term').length+' 語、理論・基礎資料 '+TERMS.filter(t=>t.kind==='theory').length+' 件）';
if(!matching.length){res.innerHTML='<div class="empty">該当する項目はありません。</div>';return;}
res.innerHTML=[...new Set(matching.map(t=>t.category))].map(c=>'<section class="group"><h2>'+esc(c)+'</h2><div class="cards">'+matching.filter(t=>t.category===c).sort((a,b)=>a.ja.localeCompare(b.ja,'ja')).map(t=>'<a class="term" href="'+page(t)+'"><strong>'+esc(t.ja)+'</strong><small>'+esc(t.en)+'</small><p class="hint">'+esc(t.short)+'</p>'+(t.kind==='theory'&&t.slide_status!=='published'?'<small>3枚スライド：掲載準備中</small>':'')+'</a>').join('')+'</div></section>').join('');}
tabbar.addEventListener('click',e=>{let b=e.target.closest('button[data-tab]');if(!b)return;selected=b.dataset.tab;cat='すべて';render()});
filters.addEventListener('click',e=>{let b=e.target.closest('button[data-cat]');if(!b)return;cat=b.dataset.cat;render()});
q.addEventListener('input',()=>{cat='すべて';render()});
const p=new URLSearchParams(location.search);if(p.has('q'))q.value=p.get('q');if(p.has('tab')&&TAB_NAMES[p.get('tab')])selected=p.get('tab');render();</script>'''.replace('__TERMS__',jsonjs)
(ROOT/'index.html').write_text(frame('検索・索引',body,script),encoding='utf-8')
(ROOT/'google_sites_embed.html').write_text('<iframe title="'+site+'" src="'+BASE+'" style="width:100%;height:780px;border:0" loading="lazy"></iframe>\n',encoding='utf-8')
(ROOT/'portal_small_link.html').write_text('<a href="'+BASE+'" target="_blank" rel="noopener noreferrer" style="font-size:12px;color:#74755d;text-decoration:underline;text-underline-offset:3px">'+site+' ↗</a>\n',encoding='utf-8')
labels=['implementation-intentions','reminder','intention-behaviour-gap','friction-costs','implementation-fidelity']
assert all(x in byid for x in labels)
vol='<div style="background:#171717;border:1px solid #303030;padding:14px;border-radius:12px;font-family:sans-serif;line-height:1.8;color:#fff"><strong>関連用語</strong><div style="display:flex;flex-wrap:wrap;gap:8px;margin:10px 0">'+''.join('<a href="'+BASE+'words/'+x+'.html" target="_blank" rel="noopener noreferrer" style="display:inline-block;border:1px solid #a6a45a;border-radius:24px;padding:5px 11px;color:#fff;text-decoration:none;font-size:13px">#'+e(byid[x]['ja'])+'</a>' for x in labels)+'</div><small style="color:#b8b8b8">各タグから個別用語の説明を開きます。</small></div>'
(ROOT/'vol1_tags.html').write_text(vol,encoding='utf-8')
print('BUILD:',len(items),'terms',len(theories),'theory entries',len(list((ROOT/'words').glob('*.html'))),'pages')
