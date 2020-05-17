def cleaning(str): #deletes all the unneeded punctuation and lowers the string
    for punct in '=:;.,()?':
        str = str.replace(punct,'').lower()
    return str

def extract(gloss,place,source,sample): #extracts verb forms from the verb lists and puts them in their places
    if gloss in source:
        n = source.index(gloss)
        if n == -1:
            pass
        else:
            sample[place] = source[n+1]
    return sample

def main():
    format = {0:('Praes','PraesM'),1:'PraesF',2:'3SgPraes',3:('Past','PastM'),4:'PastF',5:('PerfM','Perf'),6:'PerfF',7:'PerfPl',8:('Inf','InfM'),9:('InfF')} #our way of keeping verb lemmas (their forms)
    with open('verbs0.txt', encoding='utf-8') as f: #verbs0.txt is the txt where manually corrected verb entries are kept 
        text = f.read()
    text = text.split('\n')
    res = []
    result = []
    while '' in text:
        text.remove('') #text is the list of the dictionary entries of verbs; each entry is a string; all the empty terms have been deleted
    for i in range(len(text)):
        b = text[i].split() #b is the dictionary entry which was splitted by space
        sm = ['0','1','2','3','4','5','6','7','8','9']
        for pl, gl in format.items():
            if isinstance(gl,tuple):
                gl1,gl2 = gl
                sm = extract(gl1,pl,b,sm)
                sm = extract(gl2,pl,b,sm)
            else:
                sm = extract(gl,pl,b,sm)
        res.append(sm)

    for i in range(len(res)):
        for z in range(len(res[i])):
            if '(' and '/' in res[i][z]:
                spli = res[i][z].split('/')
                for p in range(len(spli)):
                    while '(' in spli[p]:
                        a = spli[p].replace('(','',1).replace(')','',1)
                        num = spli[p].find('(') + 1
                        spli[p] = spli[p][:num] + spli[p][num+1:]
                        b = spli[p].replace('(','',1).replace(')','',1)
                        c = [a,b]
                        spli[p] = '/'.join(c)
                res[i][z] = '/'.join(spli)
            elif '(' in res[i][z]:
                a = res[i][z].replace('(','',1).replace(')','',1)
                num = res[i][z].find('(') + 1
                res[i][z] = res[i][z][:num] + res[i][z][num+1:]
                b = res[i][z].replace('(','',1).replace(')','',1)
                c = [a,b]
                res[i][z] = '/'.join(c)

    for i in res:
        i = '#'.join(i)
        i = cleaning(i)
        result.append(i)

    for i in range(len(result)):
        result[i] = list(result[i])
        for z in range(len(result[i])):
            if z != len(result[i]) and result[i][z] == '/':
                if result[i][z+1] == '/':
                    result[i][z+1] = ''
                    result[i] = ''.join(result[i])
                    print(result[i])
        result[i] = ''.join(result[i])

    with open('v_ordered.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))

if __name__ == '__main__':
    main()
