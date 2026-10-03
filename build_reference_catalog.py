from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
names={x['id']:x['reference_file'] for x in json.loads((ROOT/'theories.json').read_text(encoding='utf8'))}
def parse(path):
 out=[];obj=None
 for line in path.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'^([A-Z][A-Z0-9])  - ?(.*)$',line)
  if not m:continue
  tag,val=m.groups()
  if tag=='TY':obj={'type':val,'authors':[],'keywords':[]};continue
  if obj is None:continue
  if tag=='ER':out.append(obj);obj=None;continue
  key={'AU':'authors','A1':'authors','KW':'keywords','TI':'title','T1':'title','PY':'year','Y1':'year','DO':'doi','UR':'url','JO':'journal','JF':'journal','PB':'publisher','VL':'volume','IS':'issue','SP':'first_page','EP':'last_page'}.get(tag)
  if key in ('authors','keywords'):obj[key].append(val)
  elif key and val and not obj.get(key):obj[key]=val
 return out
refs={k:parse(ROOT/'sources'/f) for k,f in names.items()}
(ROOT/'sources'/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf8')
print({k:len(v) for k,v in refs.items()})
