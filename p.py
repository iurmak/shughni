def orthoconv(text):
    with open('ortho.txt', 'r', encoding='utf-8') as file:
        ortho = file.readlines()
    for line in ortho:
        if not line.startswith('#'):
            bad, good = line.split(' ')
            while bad in text:
                good = good[0:len(good)-1]
                text = text.replace(bad, good)
                #print(bad+' > '+good)
    print('/Orthography converted.')
    return text

def textreading():
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    text = orthoconv(text.lower())
    i = 0
    while i >= 0:
        i = text.find('\n', i, len(text))
        if i >= 0:
            text = text[0:i]+' \n '+text[i+1:len(text)]
            i = i+2
    while text[0] == '\n':
        text = text[1:len(text)]
    while text[len(text)-2:len(text)-1] == '\n':
        text = text[0:len(text)-2]
    while '\t' in text:
        text = text.replace('\t', ' ')
    text = ' '+text+' '
    while '  ' in text:
        text = text.replace('  ', ' ')
    print('/Text read.')
    print(text)
    return text

def slash_n_delete(stroka):                                         #функция удаляет \n из концов строк в словаре глаголов (для systembuilding)
    if stroka.endswith('\n'):
        stroka = stroka[0:len(stroka)-1]
    return stroka

def regular(stroka):                                                #функция проверяет, является ли форма '0', то есть образуется ли регулярно (для systembuilding)
    null = False
    if stroka == '0':
        null = True
    return null

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

def make_praes3sg(praestem, deaf):                                  #функция образует форму презенса 3 л. ед. ч. из основы презенса (для derivation)
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

def make_pastmasc(praestem, deaf):                                  #функция образует основу претерита из основы презенса (для derivation)
    form = []
    for variation in praestem:
        if variation[len(variation)-2:len(variation)] == 'mb' or variation[len(variation)-2:len(variation)] == 'nb':
            praestem.append(variation[0:len(variation)-2])              #если основа оканч. на mb/nb, то появляется вариант без b
        if variation[len(variation)-1] in deaf:
            form.append(variation+'t')
        else:
            form.append(variation+'d')                                  #если основа оканч. на глухой, то присоединяется -t, иначе — на -d
    return form

def make_perfmasc(praestem, deaf):                                  #функция образует основу перфекта из основы презенса (для derivation)
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
                vocab.append(line)                                      #читаем файл vocab, в котором лежит список глагольных основ
    #for stroka in vocab:
        #stroka = orthoconv(stroka.lower())                             #конвертируем орфографию (ПОКА ЧТО НЕТ, ВСЁ МОЖЕТ ПОЕХАТЬ)
    
    for i in range(len(vocab)):
        vocab[i] = vocab[i].split('\t')
        vocab[i][len(vocab[i])-1] = slash_n_delete(vocab[i][len(vocab[i])-1])#делим vocab на основы по символам табуляции + удаляем '\n' в конце строки
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            vocab[i][j] = listen(vocab[i][j])                           #теперь vocab — это список глаголов, которые представлены списками основ, которые представлены списками вариаций
    
    vocab = derivation(vocab)                                           #ячейки с '1' заполняются регулярно образованными формами
    
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            if vocab[i][j][0] == '0':
                vocab[i][j] = vocab[i][j-1]                             #ячейки с '0' заполняются значениями слева
    #print(vocab)
    print('/System built.')
    return vocab

def spacedivision(text):                                            #функция находит пробелы в тексте и таким образом вычленяет слова (для verbdivision)
    iwords = []
    iword = -1
    while text.find(' ', iword+1, len(text)-1) > -1:
        iword = text.find(' ', iword+1, len(text)-1) + 1
        iwords.append(iword)                                            #iwords собирает номера тех символов текста, которые являются пробелами
    iwords.append(len(text))                                            #это нужно, чтобы при вычленении слов последнее слово включалось в список
    return iwords

def isitpraestem(word, stem):                                       #функция проверяет, не является ли слово глагольной формой, образованной от praestem (для formdefinition)
    word = word.replace('-', '')
    attribute = False
    flexias = {'um': '1SG', 'i': '2SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
    for flexia in flexias:
        if word.endswith(stem+flexia):
            attribute = '.PRS-'+flexias[flexia]                        #attribute — строка с глоссированием слова
    if attribute == False:
        if stem+'īǯ' in word:
            attribute = '-AGENT_NOUN'
    return attribute

def isitsg1c(word, praesstems):                                     #функция проверяет, не является ли слово стяжённой формой 1 лица ед. числа praesstem (для verbfind)
    attribute = False
    if attribute == False:
        for stem in praesstems:
            if word.endswith(stem[0:len(stem)-1]+'m'):
                attribute = '.PRS.1SG'
    if attribute == False:
        for stem in praesstems:
            vowels = ('a', 'e', 'i', 'o', 'u', 'ā', 'ī', 'ō', 'ū', 'ɛ', 'ö', 'ů')
            for a in range(len(stem)):
                if stem[a] in vowels:
                    ivowel = a
            ivowel = len(stem)-ivowel
            if stem[len(stem)-ivowel] == 'a':
                stem = stem[0:len(stem)-ivowel]+'ā'
            elif stem[len(stem)-ivowel] == 'i':
                stem = stem[0:len(stem)-ivowel]+'ī'
            elif stem[len(stem)-ivowel] == 'o':
                stem = stem[0:len(stem)-ivowel]+'ō'
            elif stem[len(stem)-ivowel] == 'u':
                stem = stem[0:len(stem)-ivowel]+'ū'
            if word.endswith(stem[0:len(stem)]+'m'):
                attribute = '.PRS.1SG'
    return attribute

def isitpraes3sg(word, stem):                                       #функция проверяет, не является ли слово глагольной формой praes3sg (для formdefinition)
    word = word.replace('-', '')
    if word.endswith(stem):
        attribute = '.PRS.3SG'                                           #attribute — строка с глоссированием слова
    else:
        attribute = False
    return attribute

def isitpasttnse(word, stem, y):                                    #функция проверяет, не является ли слово глагольной формой, образованной от pastmasc / pastfepl (для formdefinition)
    word = word.replace('-', '')
    word = word.replace('=', '')
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
    for flexia in flexias:
        if word.endswith(stem+flexia):
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 4:
                    attribute = '.PST.PL-'+flexias[flexia]
                if y == 3:
                    attribute = '.PST.SG-'+flexias[flexia]
            else:
                if y == 4:
                    attribute = '.PST.F-'+flexias[flexia]
                if y == 3:
                    attribute = '.PST.M-'+flexias[flexia]                #attribute — строка с глоссированием слова
        else:
            attribute = False
    return attribute

def isitperftnse(word, stem, y):
    word = word.replace('-', '')
    word = word.replace('=', '')
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
    for flexia in flexias:
        if word.endswith(stem+flexia):
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 4:
                    attribute = '.PST.PL-'+flexias[flexia]
                if y == 3:
                    attribute = '.PST.SG-'+flexias[flexia]
            else:
                if y == 4:
                    attribute = '.PST.F-'+flexias[flexia]
                if y == 3:
                    attribute = '.PST.M-'+flexias[flexia]                #attribute — строка с глоссированием слова
        else:
            attribute = False
    return attribute

'''
def isitinfinite(word, stem):
'''

def formdefinition(word, stem, y):                                  #коммутатор, выявляющий, какая из основ найдена в слове, и перенаправляющий к нужной функции (для verbdivision)
    if y == 1:
        attribute = isitpraestem(word, stem)
    if y == 2:
        attribute = isitpraes3sg(word, stem)
    if y == 3 or y == 4:
        attribute = isitpasttnse(word, stem, y)
    if y == 5 or y == 6 or y == 7:
        attribute = isitperftnse(word, stem, y)
    if y == 8:
        attribute = isitinfinite(word, stem)
    return attribute

def verbfind(text, vocab):                                          #основная функция для поиска глагольных форм в тексте
    iwords = spacedivision(text)                                        #iwords — список номеров символов текста, с которых начинаются слова
    glossfounds = []
    for a in range(len(iwords)-1):
        word = text[iwords[a]:iwords[a+1]]
        word = word.replace(' ', '')                                    #word — это слово, в отношении которого программа пытается понять, является ли оно глаголом
        
        glossfoundsinword = []
        for x in range(len(vocab)):   #для каждой леммы:
            for y in range(1, len(vocab[x])):   #для каждой основы:
                for z in range(len(vocab[x][y])):                       #залезаем в словарь и смотрим, не содержит ли word одну из глагольных основ / форм из словаря vocab
                    if vocab[x][y][z] in word:
                        attribute = formdefinition(word, vocab[x][y][z], y)                    
                        if not attribute == False:                      #attribute — строка с глоссированием слова
                            attribute = vocab[x][0][0].replace(' ', '_')+attribute
                            glossfoundsinword.append(attribute)         #glossfoundsinword собирает все данные по найденным свойствам глагола для одного word
            if word.endswith('m'):                                      #если слово оканчивается на 'm', возможно, это стяжённая форма 1 лица ед. числа презенса?
                attribute = isitsg1c(word, vocab[x][1])
                if not attribute == False:
                    attribute = vocab[x][0][0].replace(' ', '_')+attribute
                    glossfoundsinword.append(attribute)
        if not glossfoundsinword == []:
            glossfounds.append([word, iwords[a], iwords[a+1]-1, glossfoundsinword]) #glossfounds собирает все глоссирования глаголов в тексте
    print(glossfounds)
    print('/Verbs found.')

vocab = systembuilding()
text = textreading()
verbfind(text, vocab)
