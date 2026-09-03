import json, re, os
shell = open('shell.html', encoding='utf-8').read()

chmap = [
 ('ch01',1),('ch02',1),('ch03',1),('ch04',1),('ch05',1),('ch06',1),
 ('ch07',1),('ch08',1),('ch09',1),('ch10',1),('ch11',1),
 ('p2ch01',2),('p2ch02',2),('p2ch03',2),('p2ch04',2),('p2ch05',2),
]
chapters=[]
for key,part in chmap:
    d=json.load(open(f'data/{key}.json',encoding='utf-8'))
    ch=d['ch']
    no=re.search(r'CHAPTER (\d+)',ch).group(1)
    title=re.sub(r'^(\[Part 2\] )?CHAPTER \d+\s*','',ch)
    cid=('p1c' if part==1 else 'p2c')+no
    chapters.append({"id":cid,"part":part,"no":no,"title":title,
                     "src":d['src'].replace('표준교재 ',''),"qs":d['qs']})

mocks=[]
for i,key in enumerate(['mock1','mock2'],1):
    d=json.load(open(f'data/{key}.json',encoding='utf-8'))
    qs=[{k:v for k,v in q.items() if k!='e'} for q in d['qs']]
    mocks.append({"id":f"mock{i}","title":d['ch'],"mock":True,"qs":qs})

data = "const DATA = " + json.dumps({"chapters":chapters,"mocks":mocks},
        ensure_ascii=False, separators=(',',':')) + ";"
out = shell.replace('__DATA__', data)
open('index.html','w',encoding='utf-8').write(out)
n=sum(len(c['qs']) for c in chapters); m=sum(len(x['qs']) for x in mocks)
print(f"index.html  {len(out)//1024}KB  · 챕터 {len(chapters)}개 {n}문항 · 모의고사 {len(mocks)}회 {m}문항")
