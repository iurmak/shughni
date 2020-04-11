#[0]* vrblemma, [1] praesstem, [2] praes3sg, [3] pastmasc, [4] pastfepl, [5] perfmasc/perf, [6] perffemn, [7] perfplur, [8] infinite/infinitiveMasc, [9]infinitiveFem (в будущем можем прикрутить [9] imperate, [10] causativ; пока не добавляем)
def cleaning(str): #deletes all the unneeded punctuation and lowers the string
    for punct in '=:;.,':
        str = str.replace(punct,'').lower()
    return str

with open('verbs0.txt', encoding='utf-8') as f:
    text = f.read()
text = text.split('\n')
res = []
result = []
while '' in text:
    text.remove('') # text — лист из словарных статей глаголов, где каждая статья — строка (пустые строки удалены)
for i in range(len(text)):
    b = text[i].split() #b — конкретная СС, рассплитенная по пробелам
    #print(b)
    if len(b) <= 4:
        continue
    else:
        sm = ['0','1','2','3','4','5','6','7','8','9'] #наш формат данных
        prom1 = [] #praesstem
        prom3 = [] #pastmasc или просто универсальная paststem
        prom4 = [] #PastStemFem
        switcher = 0
        if b[0].endswith(':') or b[0].endswith(';'): #если первое слово в СС кончается на : или ;, то в [1] идет только оно
            prom1.append(b[0])
        elif b[0].endswith(','): #добавляет все варианты для [1]
            prom1.append(b[0])
            for z in range(1,5):
                if b[z].endswith(',') and switcher == 0:
                    if b[z+1].startswith('Perf') or b[z+1].startswith('3Sg') or b[z+1].startswith('Inf') or b[z+1].startswith('ж.'):
                        switcher = 1
                    prom1.append(b[z])
                elif switcher == 0:
                    prom1.append(b[z])
                    if b[z+1] == 'ж.':
                        switcher = 1
        sm[1] = '/'.join(prom1)
        switcher = 0
        if len(prom1) > 1:
            find = b.index(prom1[-1])
        else:
            find = 0
        prom3.append(b[find+1])
        for z in range(1,4):
            if b[find+1+z].startswith('Per') or b[find+1+z].startswith('3Sg') or b[find+1+z].startswith('In'):
                switcher = 1
            if b[find+1+z].endswith(',') or b[find+1+z].endswith(';') or b[find+1+z].endswith(':') and switcher == 0:
                prom3.append(b[find+1+z])
            elif b[find+1+z] == 'ж.':
                switcher = 1
                prom4.append(b[find+2+z])
        sm[3] = '/'.join(prom3)
        if prom4 == []:
            pass
        else:
            sm[4] = '/'.join(prom4)
        if '3SgPraes' in b:
            t = b.index('3SgPraes')
            sm[2] = b[t+1]
        if 'PerfM' in b:
            t = b.index('PerfM')
            sm[5] = b[t+1]
        if 'Perf' in b:
            t = b.index('Perf')
            sm[5] = b[t+1]
        if 'PerfF' in b:
            t = b.index('PerfF')
            sm[6] = b[t+1]
        if 'PerfPl' in b:
            t = b.index('PerfPl')
            sm[7] = b[t+1]
        if 'Inf' in b:
            t = b.index('Inf')
            sm[8] = b[t+1]
        if 'InfM' in b:
            t = b.index('InfM')
            sm[8] = b[t+1]
        if 'InfF' in b:
            t = b.index('InfF')
            sm[9] = b[t+1]
        res.append(sm)
for i in res:
    i = '#'.join(i)
    i = cleaning(i)
    result.append(i)

with open('v_ordered.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))
