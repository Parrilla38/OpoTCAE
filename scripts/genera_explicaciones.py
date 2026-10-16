import json,hashlib,subprocess,sys,os,concurrent.futures as cf
P=json.load(open('/workspace/opotcae/data/parsed/preguntas.json'))
def k(p): return hashlib.sha1(json.dumps([p['enunciado'],sorted(p['opciones'].items()),p['correcta']],ensure_ascii=False).encode()).hexdigest()[:12]
U={}
for p in P:
  if p['correcta']: U.setdefault(k(p),p)
items=list(U.items()); B=40
batches=[items[i:i+B] for i in range(0,len(items),B)]
D='/workspace/opotcae_expl'
def run(i):
  out=f'{D}/b{i:03d}.json'
  if os.path.exists(out): return i,'skip'
  qs=[{'k':kk,'tema':p.get('tema_nombre'),'enunciado':p['enunciado'],'opciones':p['opciones'],'correcta':p['correcta']} for kk,p in batches[i]]
  prompt=("Eres profesor de oposiciones TCAE del SAS. Para cada pregunta escribe una explicación en español, 2-4 frases claras: por qué la opción correcta es la correcta y, si ayuda, por qué fallan las demás. La clave 'correcta' es la oficial: no la discutas. Cita ley o artículo solo si estás seguro; no inventes números. Devuelve SOLO un objeto JSON {k: explicación}, sin texto extra.\n"+json.dumps(qs,ensure_ascii=False))
  r=subprocess.run(['claude','-p',prompt,'--model','claude-sonnet-5-5','--effort','medium','--output-format','text'],capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=900)
  t=r.stdout.strip(); t=t[t.find('{'):t.rfind('}')+1]
  try: d=json.loads(t)
  except Exception as e: return i,'ERR '+r.stdout[:200]+r.stderr[:200]
  json.dump(d,open(out,'w'),ensure_ascii=False); return i,len(d)
with cf.ThreadPoolExecutor(3) as ex:
  for res in ex.map(run,range(len(batches))): print(res,flush=True)
json.dump({kk:p['id'] for kk,p in items},open(f'{D}/keys.json','w'))
