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


def orthoconv(text):
    with open('ortho.txt', 'r', encoding='utf-8') as file:
        ortho = file.readlines()
    for line in ortho:
        if not line.startswith('#'):
            bad, good = line.split(' ')
            while bad in text:
                good = good[0:len(good)-1]
                text = text.replace(bad, good)
                print(bad+' > '+good)
    return text

with open('text.txt', 'r', encoding='utf-8') as file:
    text = file.read()
text = text.lower()
text = orthoconv(text)

'''

def slash_n_delete(stroka):                                         #функция удаляет \n из концов строк в словаре глаголов (для systembuilding)
    if stroka.endswith('\n'):
        stroka = stroka[0:len(stroka)-1]
    return stroka

def listen(stroka):                                                 #функция делает из строки список с этой строкой (для systembuilding)
    if ',' in stroka:
        spisok = stroka.split(',')
    else:
        spisok = [stroka]
    return(spisok)

def derivation(vocab):                                              #коммутатор, выявляющий, какую форму нужно образовать, и перенаправляющий к нужной функции (для systembuilding)
    voiced = ('b', 'v', 'w', 'g', 'd', 'ð', 'ž', 'z', 'j', 'm', 'ʒ', 'č', 'ʁ', 'h', 'ǯ', 'γ')
    deaf = ('θ', 'k', 'p', 's', 't', 'f', 'χ', 'ӿ', 'c', 'č', 'š', 'q', 'l', 'r', 'm', 'n')
    for i in range(len(vocab)):
        if vocab[i][2][0] == '1':
            vocab[i][2] = make_praes3sg(vocab[i][1], deaf)              #форма презенса 3 л. ед. ч. образуется из основы презенса
        if vocab[i][3][0] == '1':
            vocab[i][3] = make_pastmasc(vocab[i][1], deaf)              #основа претерита образуется из основы презенса
        if vocab[i][5][0] == '1':
            vocab[i][5] = make_perfmasc(vocab[i][1], deaf)              #основа перфекта образуется из основы презенса
        if vocab[i][8][0] == '1':
            vocab[i][8] = vocab[i][3]                                   #основа инфинитива совпадает с основой претерита
    return(vocab)

def make_praes3sg(praestem, deaf):                                  #функция образует форму презенса 3 л. ед. ч. из основы презенса
    form = []
    for variation in praestem:
        if variation[len(variation)-2:len(variation)] == 'mb' or variation[len(variation)-2:len(variation)] == 'nb':
            variation = variation[0:len(variation)-2]                   #если основа оканч. на mb/nb, то b удаляется
        if variation[len(variation)-1] == 'ʒ':
            variation = variation[0:len(variation)-1]+'z'               #если основа оканч. на ʒ, то она заменяется на z
        if variation[len(variation)-1] == 'c':
            variation = variation[0:len(variation)-1]+'s'               #если основа оканч. на c, то она заменяется на s
        if variation[len(variation)-1] in deaf:
            form.append(variation+'t')
        else:
            form.append(variation+'d')                                  #если основа оканч. на глухой, то присоединяется -t, иначе — на -d
    return form

def make_pastmasc(praestem, deaf):                                  #функция образует основу претерита из основы презенса
    form = []
    for variation in praestem:
        if variation[len(variation)-2:len(variation)] == 'mb' or variation[len(variation)-2:len(variation)] == 'nb':
            praestem.append(variation[0:len(variation)-2])              #если основа оканч. на mb/nb, то появляется вариант без b
        if variation[len(variation)-1] in deaf:
            form.append(variation+'t')
        else:
            form.append(variation+'d')                                  #если основа оканч. на глухой, то присоединяется -t, иначе — на -d
    return form

def make_perfmasc(praestem, deaf):                                  #функция образует основу перфекта из основы презенса
    form = []
    for variation in praestem:
        if variation[len(variation)-1] in deaf:
            form.append(variation+'č')
        else:
            form.append(variation+'ǯ')                                  #если основа оканч. на глухой, то присоединяется -t, иначе — на -d
    return form

def systembuilding():                                               #основная функция для сборки словаря из файла с исключениями и образования регулярных форм
    vocab = []
    with open('vocab.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                vocab.append(line)                                      #читаем файл verbs, в котором лежит список глагольных основ
    #for stroka in vocab:
        #stroka = orthoconv(stroka.lower())                             #конвертируем орфографию (ПОКА ЧТО НЕТ, ВСЁ МОЖЕТ ПОЕХАТЬ)
    
    for i in range(len(vocab)):
        vocab[i] = vocab[i].split('\t')
        vocab[i][len(vocab[i])-1] = slash_n_delete(vocab[i][len(vocab[i])-1]) #делим verbs на основы по символам табуляции + удаляем '\n' в конце строки
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            vocab[i][j] = listen(vocab[i][j])                           #теперь vocab — это список глаголов, которые представлены списками основ, которые представлены списками вариаций
    
    vocab = derivation(vocab)                                           #ячейки с '1' заполняются регулярно образованными формами
    
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            if vocab[i][j][0] == '0':
                vocab[i][j] = vocab[i][j-1]                             #ячейки с '0' заполняются значениями слева
    #print(vocab)

systembuilding()
