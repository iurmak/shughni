def dictreading():
    verbs = []
    with open('verbs.txt', 'r', encoding='utf-8') as vdct:
        for line in vdct:
            line = line.replace('\n', '')
            verbs.append(line.split('\t'))
            n = len(verbs)
    for i in range(len(verbs)):
        for j in range(len(verbs[i])):
            if verbs[i][j].find(',') != -1:
                verbs[i][j] = verbs[i][j].split(',')
    return verbs

def instroka(verbs):
    stroka = input()
    stroka = stroka.replace(',', '')
    stroka = stroka.replace('.', '')
    stroka = stroka.replace('!', '')
    stroka = stroka.replace('?', '')
    words = stroka.split(' ')
    for word in words:
        for verb in verbs:
            for form in verb:
                if type(form) != 'str':
                    for varform in form:
                        if word == varform:
                            
                else:
                    formcomparison(form)

instroka(dictreading())