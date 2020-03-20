'''
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
'''

def orthoconv(text):                                                          #КОНВЕРТЕР ОРФОГРАФИИ
    with open('ortho.txt', 'r', encoding='utf-8') as file:                        #открывает файл с заменами символов
        ortho = file.readlines()
    for line in ortho:
        if not line.startswith('#'):                                              #так в файле начинаются служебные пометы
            bad, good = line.split(' ')
            while bad in text:
                good = good[0:len(good)-1]                                        #замена плохих символов хорошими
                text = text.replace(bad, good)
                print(bad+' > '+good)
    return text

with open('text.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    text = text.lower()
print(orthoconv(text))
