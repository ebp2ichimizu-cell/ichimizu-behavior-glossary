// Node.js built-ins only. Run after publish_library.py when rebuilding V5.
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const theories = JSON.parse(fs.readFileSync(path.join(root, 'theories.json'), 'utf8'));
const e = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const write = (p, s) => { fs.mkdirSync(path.dirname(path.join(root,p)), {recursive:true}); fs.writeFileSync(path.join(root,p), s); };
function parseRIS(text) {
  const records = []; let record = null, last = null;
  for (const line of text.replace(/^\uFEFF/, '').split(/\r?\n/)) {
    const match = line.match(/^([A-Z][A-Z0-9])\s{2}- ?(.*)$/);
    if (!match) {
      if (line.trim() && record && last) record[last][record[last].length-1] += '\n' + line.trim();
      continue;
    }
    const [,tag,value] = match;
    if (tag === 'TY') { if(record) throw Error('Unclosed RIS record'); record = {}; }
    if (!record) { if(line.trim()) throw Error('RIS field outside record'); continue; }
    if (tag === 'ER') { records.push(record); record = null; last = null; continue; }
    (record[tag] ||= []).push(value); last = tag;
  }
  if (record) throw Error('Missing ER in RIS');
  return records;
}
const first = (r, ...tags) => tags.flatMap(t => r[t] || []).find(v => v.trim()) || '';
const values = (r, ...tags) => tags.flatMap(t => r[t] || []).filter(Boolean).join(' / ');
function safeURL(value) { try { const u = new URL(value); return ['https:','http:'].includes(u.protocol) ? u.href : ''; } catch { return ''; } }
function link(url, label) { return '<a href="'+e(url)+'" target="_blank" rel="noopener noreferrer">'+e(label)+'</a>'; }
const note = '元RISに登録された書誌情報を表示しています。未登録の項目は推測で補完していません。リンク先は文献情報や本文の提供ページです。本文の閲覧には契約・購入が必要な場合があります。';
const css = '.bibliography{padding-left:1.6em}.bibliography>li{padding:16px 0;border-bottom:1px solid #dfe0d7;overflow-wrap:anywhere}.bibliography h3{font-size:16px;line-height:1.65;margin:0 0 10px}.bib-meta{margin:0}.bib-meta div{display:grid;grid-template-columns:7em minmax(0,1fr);gap:10px;margin:5px 0}.bib-meta dt{font-weight:600;color:#535d31}.bib-meta dd{margin:0;white-space:pre-line}.ref-nav{display:flex;flex-wrap:wrap;gap:8px}.ref-nav a,.ref-actions a{display:inline-block;padding:8px 10px}.bibliography details{margin-top:10px}.bibliography pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}.refs .ref-actions{margin:12px 0}.reference-top{scroll-margin-top:20px}@media(max-width:480px){.bib-meta div{grid-template-columns:1fr;gap:0}.panel.refs{padding:14px}.bibliography{padding-left:1.3em}}';
function list(records) {
  return '<ol class="bibliography">' + records.map((r,i) => {
    const row = (label, value) => value ? '<div><dt>'+e(label)+'</dt><dd>'+e(value)+'</dd></div>' : '';
    const doi = first(r,'DO');
    const doiURL = doi ? safeURL(/^https?:\/\//i.test(doi) ? doi : 'https://doi.org/'+doi.replace(/^doi:\s*/i,'')) : '';
    const urls = [...new Set((r.UR || []).map(safeURL).filter(Boolean))];
    const raw = Object.entries(r).flatMap(([tag,vs]) => vs.map(v => tag+'  - '+v)).join('\n')+'\nER  -';
    return '<li id="reference-'+(i+1)+'"><h3>'+e(first(r,'TI','T1') || 'タイトル：元RISに記載なし')+'</h3><dl class="bib-meta">'
      + row('著者', values(r,'AU','A1') || '元RISに記載なし')
      + row('年', first(r,'PY','Y1') || '元RISに記載なし')
      + row('雑誌名', first(r,'JO','JF','JA'))
      + row('収録書・資料名', values(r,'T2','BT'))
      + row('編者', values(r,'A2','ED'))
      + row('出版社・機関', values(r,'PB')) + row('出版地', values(r,'CY'))
      + row('巻', values(r,'VL')) + row('号', values(r,'IS'))
      + row('ページ', first(r,'SP') + (first(r,'EP') ? '–'+first(r,'EP') : ''))
      + row('版', values(r,'ET')) + row('ISBN / ISSN', values(r,'SN'))
      + '<div><dt>DOI</dt><dd>'+(doiURL ? link(doiURL,doi) : e(doi || '元RISに記載なし'))+'</dd></div>'
      + (urls.length ? '<div><dt>URL</dt><dd>'+urls.map(u=>link(u,u)).join('<br>')+'</dd></div>' : '')
      + '</dl><details><summary>元RISの登録項目を見る</summary><pre>'+e(raw)+'</pre></details></li>';
  }).join('') + '</ol>';
}
const template = read('theories/'+theories[0].id+'/index.html');
const originalCSS = template.match(/<style>([\s\S]*?)<\/style>/)[1].split('/* readable-references */')[0];
const site = 'いちみず会EBP関連用語ライブラリー';
function frame(title,body) {
  return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'｜'+site+'</title><style>'+originalCSS+'/* readable-references */'+css+'</style></head><body><header><div class="inner"><h1>'+site+'</h1><p class="sub">参考文献一覧</p></div></header><main>'+body+'</main><footer>書誌情報の出典：各ページに記載した元RIS。原著本文・個別の主張との照合は行っていません。</footer></body></html>';
}
const report = [];
for (const t of theories) {
  const records = parseRIS(read('sources/'+t.reference_file));
  const ris = '../../sources/'+encodeURIComponent(t.reference_file);
  const bibliography = list(records);
  const section = '<section class="panel refs reference-top" id="references"><h2>参考文献（'+records.length+'件）</h2><p class="note">'+note+'</p><p class="ref-actions"><a href="references.html">文献一覧を専用ページで読む</a> <a href="../../references/index.html">全分野の参考文献へ</a> <a href="'+ris+'" download>RISを保存（Zotero等向け）</a></p>'+bibliography+'</section>';
  const p = 'theories/'+t.id+'/index.html';
  let page = read(p);
  if (!/<section class="panel refs[^\"]*"/.test(page)) throw Error('Reference section not found: '+p);
  page = page.replace(/<section class="panel refs[^\"]*"[^>]*>[\s\S]*?<\/section>/, section);
  if (!page.includes('/* readable-references */')) page = page.replace('</style>','/* readable-references */'+css+'</style>');
  if (!page.includes('class="reference-jump"')) page = page.replace('<section class="panel">','<p class="reference-jump"><a href="#references">参考文献（'+records.length+'件）を読む ↓</a></p><section class="panel">');
  write(p,page);
  const nav = '<nav class="ref-nav" aria-label="文献の分野">'+theories.map(x=>'<a href="../'+e(x.id)+'/references.html"'+(x.id===t.id?' aria-current="page"':'')+'>'+e(x.ja)+'</a>').join('')+'</nav>';
  write('theories/'+t.id+'/references.html',frame(t.ja+'の参考文献','<p class="back"><a href="index.html">← '+e(t.ja)+'の解説・スライドへ</a> ｜ <a href="../../references/index.html">参考文献の総合一覧へ</a></p>'+nav+'<h2>'+e(t.ja)+'の参考文献（'+records.length+'件）</h2><p class="muted">'+e(t.en)+'</p><p class="note">'+note+'</p><p class="download"><a href="'+ris+'" download>RISを保存（Zotero等向け）</a></p><p class="note">出典ファイル：'+e(t.reference_file)+'</p>'+bibliography));
  report.push({id:t.id,name:t.ja,file:t.reference_file,count:records.length});
}
write('references/index.html',frame('参考文献の総合一覧','<p class="back"><a href="../index.html">← 検索・索引へ戻る</a></p><h2>参考文献の総合一覧</h2><p>'+note+'</p><div class="cards">'+report.map(t=>'<a class="theory" href="../theories/'+e(t.id)+'/references.html"><strong>'+e(t.name)+'</strong><br>'+t.count+'件の参考文献を読む</a>').join('')+'</div><p class="note">件数は各RISの登録件数です。分野間で重複する文献を含む場合があります。</p>'));
let home = read('index.html');
if (!home.includes('href="references/index.html"')) home = home.replace('<main>','<main><p class="back"><a href="references/index.html">RAT・PMT・CPTED・EBPの参考文献を読む</a></p>');
write('index.html',home);
console.log(JSON.stringify(report,null,2));
