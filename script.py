import collections
with open('2tmk.txt', encoding='utf-8') as f:
    text = f.read()

fin = []
gl = []
txt = text.split()

for i in txt:
    if i.isupper():
        fin.append(i.lower())
d = collections.Counter(fin)

for i in range(len(txt)):
    if txt[i] == 'гл.':
        art = txt[i+1]
        gl.append(art.lower())


for i in gl:
    if i in fin:
        d[i] = 'гл.'

print(d)
