def everythingalright():                                            #функция определяет, все ли необходимые для работы программы файлы лежат в директории
    alright = False
    import os
    if os.path.isfile('./text.txt') and os.path.isfile('./vocab.txt') and os.path.isfile('./output.txt') and os.path.isfile('./ortho.txt') and os.path.isfile('./help.txt'):
        alright = True
    return alright

def orthoconv(text):                                                #функция конвертирует орфографию
    with open('ortho.txt', 'r', encoding='utf-8') as file:
        ortho = file.readlines()
    for line in ortho:
        if not line.startswith('#'):                                    #с решёточки начинаются служебные строки в файле ortho
            bad, good = line.split(' ')
            while bad in text:
                good = good[0:len(good)-1]
                text = text.replace(bad, good)                          #плохие символы заменяются на хорошие
                #print(bad+' > '+good)
    print('     /Orthography converted.')
    return text

def textreading(orthoneed):                                         #функция читает текст из файла text и чистит его
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.lower()                                                 #всё переводим в строчные
    if orthoneed:
        text = orthoconv(text)                                          #конвертируем орфографию (если нужно)
    i = 0
    while i >= 0:
        i = text.find('\n', i, len(text))
        if i >= 0:
            text = text[0:i]+' \n '+text[i+1:len(text)]
            i = i+2                                                     #добавляем пробелы до и после \n — это нужно для корректного деления на слова
    while text[0] == '\n':
        text = text[1:len(text)]
    while '\t' in text:
        text = text.replace('\t', ' ')
    text = ' '+text+' '
    while '  ' in text:
        text = text.replace('  ', ' ')                                  #убираем табуляции и лишние пробелы
    print('     /Text read.')
    #print(text)
    return text

def deleteidentical(spisok):                                        #функция удаляет одинаковые элементы списка
    n = []
    for i in spisok:
        if i not in n:
            n.append(i)
    return n

def slash_n_delete(stroka):                                         #функция удаляет \n из концов строк в словаре глаголов (для systembuilding)
    if stroka.endswith('\n'):
        stroka = stroka[0:len(stroka)-1]
    return stroka

def listen(stroka):                                                 #функция делает из строки список с этой строкой из вариантов основы (для systembuilding)
    if '/' in stroka:
        spisok = stroka.split('/')
    else:
        spisok = [stroka]
    return(spisok)

def derivation(vocab):                                              #коммутатор, выявляющий, какую форму нужно образовать, и перенаправляющий к нужной функции (для systembuilding)
    voiced = ('b', 'v', 'w', 'g', 'd', 'ð', 'ž', 'z', 'j', 'm', 'ʒ', 'č', 'ʁ', 'h', 'ǯ', 'ұ')
    deaf = ('θ', 'k', 'p', 's', 't', 'f', 'χ', 'ӿ', 'c', 'č', 'š', 'q', 'l', 'r', 'm', 'n')
    for i in range(len(vocab)):
        if vocab[i][2][0] == '1':
            vocab[i][2] = make_praes3sg(vocab[i][0], deaf)              #форма презенса 3 л. ед. ч. образуется из основы презенса
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
    #print('     /Vocabulary loaded.')
    return vocab

def spacedivision(text):                                            #функция находит пробелы в тексте и таким образом вычленяет слова (для verbdivision)
    iwords = []
    iword = -1
    while text.find(' ', iword+1, len(text)-1) > -1:
        iword = text.find(' ', iword+1, len(text)-1) + 1
        iwords.append(iword)                                            #iwords собирает номера тех символов текста, которые являются пробелами
    iwords.append(len(text))                                            #это нужно, чтобы при вычленении слов последнее слово включалось в список
    return iwords

def jification(stem):                                               #добавляет -j- в конец основы, если она оканчивается на гласный
    vowels = ('a', 'e', 'i', 'o', 'u', 'ā', 'ī', 'ō', 'ū', 'ɛ', 'ö')
    for vowel in vowels:
        if stem.endswith(vowel):
            stem = stem+'j'
            break
    return stem

def wordclean(word):                                                #очищает слово от лишних знаков
    word = word.replace('-', '')
    word = word.replace('=', '')
    word = word.replace(' ', '')
    return word

def isitpraestem(word, stem, y):                                    #функция проверяет, не является ли слово глагольной формой, образованной от praestem (для formdefinition)
    stem = jification(stem)
    attribute = False
    flexias = {'um': '1SG', 'i': '2SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL', 'ēn': '3PL'}
    for flexia in flexias:
        if word == stem+flexia:
            attribute = 'PRS-'+flexias[flexia]                          #attribute — строка с глоссированием слова
    if attribute == False:
        if word == stem+'īǯ':
            attribute = 'AGENT_NOUN'
    return attribute

def isitcontract(word, praesstems):                                 #функция проверяет, не является ли слово стяжённой формой 1 лица ед. числа praesstem (для verbfind)
    attributes = []
    vowels = ('a', 'e', 'i', 'o', 'u', 'ā', 'ī', 'ō', 'ū', 'ɛ', 'ö')
    for stem in praesstems:
        attribute = False
        ivowel = len(stem)-1
        for a in range(1,len(stem)):
            if stem[a] in vowels:
                ivowel = a

        ivowel = len(stem)-ivowel
        if word.endswith('m'):
            if stem[len(stem)-ivowel] == 'a':
                stem = stem[0:len(stem)-ivowel]+'ā'
            elif stem[len(stem)-ivowel] == 'i':
                stem = stem[0:len(stem)-ivowel]+'ī'
            elif stem[len(stem)-ivowel] == 'o':
                stem = stem[0:len(stem)-ivowel]+'ō'
            elif stem[len(stem)-ivowel] == 'u':
                stem = stem[0:len(stem)-ivowel]+'ū'
            if word == stem+'m':
                attribute = 'PRS.1SG'                                   #стяжённая форма 1 лица ед. ч.
        elif word.endswith('en') or word.endswith('et'):
            if ivowel <3:
                stem = stem[0:len(stem)-ivowel]
                if word == stem+'et':
                    attribute = 'PRS.2PL'                                   #стяжённая форма 2 лица мн. ч.
                if word == stem+'en':
                    attribute = 'PRS.3PL'                                   #стяжённая форма 3 лица мн. ч.
        if not attribute == False:
            attribute = isitnegative(word, stem)+attribute
            attributes.append(attribute)                                #возвращается attributes — список attribute
    return attributes

def isitpraes3sg(word, stem):                                       #функция проверяет, не является ли слово глагольной формой praes3sg (для formdefinition)
    attribute = False
    if word == stem:
        attribute = 'PRS.3SG'                                           #attribute — строка с глоссированием слова
    return attribute

def isitpasttnse(word, stem, y):                                    #функция проверяет, не является ли слово глагольной формой, образованной от pastmasc / pastfepl (для formdefinition)
    attribute = False
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL', 'ēn': '3PL'}
    for flexia in flexias:
        if word.endswith(stem+flexia):
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 4:
                    attribute = 'PST.PL-'+flexias[flexia]
                if y == 3:
                    attribute = 'PST.SG-'+flexias[flexia]
            else:
                if y == 4:
                    attribute = 'PST.F-'+flexias[flexia]
                if y == 3:
                    attribute = 'PST.M-'+flexias[flexia]                #attribute — строка с глоссированием слова
    return attribute

def isitperftnse(word, stem, y):                                    #функция проверяет, не является ли слово глагольной формой, образованной от perfmasc / perffemn / perfplur (для formdefinition)
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL', 'ēn': '3PL'}
    attribute = False
    for flexia in flexias:
        if word == stem+flexia:
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 7:
                    attribute = 'PRF.PL-'+flexias[flexia]
            else:
                if y == 6:
                    attribute = 'PRF.F-'+flexias[flexia]
                if y == 5:
                    attribute = 'PRF.M-'+flexias[flexia]
        if word == stem+'at'+flexia or word == stem+'it'+flexia:
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 7:
                    attribute = 'PST.PRF.PL-'+flexias[flexia]
            else:
                if y == 6:
                    attribute = 'PST.PRF.F-'+flexias[flexia]
                if y == 5:
                    attribute = 'PST.PRF.M-'+flexias[flexia]
    if attribute == False:
        if word == stem+'ak':
            if y == 5:
                attribute = 'PRF.PTCP.M'
            if y == 6:
                attribute = 'PRF.PTCP.F'
            if y == 7:
                attribute = 'PRF.PTCP.PL'
        if word == stem+'in':
            if y == 5:
                attribute = 'ADJ.PTCP.M'
            if y == 6:
                attribute = 'ADJ.PTCP.F'
            if y == 7:
                attribute = 'ADJ.PTCP.PL'
    return attribute

def isitinfinite(word, stem, y):                                       #функция проверяет, не является ли слово глагольной формой, образованной от infinite (для formdefinition)
    attribute = False
    if word == stem+'ow':
        attribute = 'INF-INF2'
    elif word == stem:
        attribute = 'INF'                                               #attribute — строка с глоссированием слова
    elif word == stem+'meǯ':
        attribute = 'FUT.PTCP'
    return attribute

def isitnegative(word, stem):                                       #функция проверяет, не является ли слово отрицательной или условной формой (для formdefinition)
    neg = ''
    if word.startswith('na'+stem):
        neg = 'NEG-'
    return neg

def formdefinition(word, stem, y):                                  #коммутатор, выявляющий, какая из основ найдена в слове, и перенаправляющий к нужной функции (для verbdivision)
    if y == 0 or y == 1:
        attribute = isitpraestem(word, stem, y)
    if y == 2:
        attribute = isitpraes3sg(word, stem)
    if y == 3 or y == 4:
        attribute = isitpasttnse(word, stem, y)
    if y == 5 or y == 6 or y == 7:
        attribute = isitperftnse(word, stem, y)
    if y == 8 or y == 9:
        attribute = isitinfinite(word, stem, y)
    if not attribute == False:
        attribute = isitnegative(word, stem)+attribute
    return attribute

def nedostatochny_stem(stems):
    nedost = False
    if '-' in stems:
        nedost = True
    return nedost

def verbfind(text, vocab):                                          #основная функция для поиска глагольных форм в тексте
    iwords = spacedivision(text)                                        #iwords — список номеров символов текста, с которых начинаются слова
    glossboxes = []
    for a in range(len(iwords)-1):
        word = text[iwords[a]:iwords[a+1]]
        word = word.replace(' ', '')                                    #word — это слово, в отношении которого программа пытается понять, является ли оно глаголом
        #print(word)
        
        glossfoundsinword = []
        for x in range(len(vocab)):   #для каждой леммы:
            for y in range(1, len(vocab[x])):   #для каждой основы:
                if not nedostatochny_stem(vocab[x][y]):                 #так обозначаются отсутствующие (недостаточные) основы, которых нет в языке

                    for z in range(len(vocab[x][y])):                   #залезаем в словарь и смотрим, не содержит ли word одну из глагольных основ / форм из словаря vocab
                        wordnew = wordclean(word)
                        if vocab[x][y][z] in wordnew:
                            attribute = formdefinition(wordnew, vocab[x][y][z], y)
                            if not attribute == False:                  #attribute — строка с глоссированием слова
                                attribute = vocab[x][y][0]+' > '+attribute
                                glossfoundsinword.append(attribute)     #glossfoundsinword собирает все данные по найденным свойствам глагола для одного word
            if word.endswith('m') or word.endswith('n') or word.endswith('t'):
                if not nedostatochny_stem(vocab[x][0]):
                    wordnew = wordclean(word)
                    if not isitcontract(wordnew, vocab[x][0]) == []:           #если слово оканчивается на m, t или n, возможно, это стяжённая форма презенса?
                        for attribute in isitcontract(wordnew, vocab[x][0]):
                            attribute = vocab[x][0][0]+' > '+attribute
                        glossfoundsinword.append(attribute)
        if not glossfoundsinword == []:
            glossfoundsinword = deleteidentical(glossfoundsinword)
            glossboxes.append([word, iwords[a], iwords[a+1]-1, glossfoundsinword])
    print(glossboxes)                                                  #glossboxes собирает все глоссирования глаголов в тексте в список "боксов" (слово, номер первого символа, номер пробела после слова, глоссирование)
    print('     /Verbs found.')
    return glossboxes

def output(text, glossboxes):
    glossboxes.reverse()
    for glossbox in glossboxes:
        allglossesline = '('
        for gloss in glossbox[3]:
            allglossesline = allglossesline+gloss+', '
        allglossesline = allglossesline[0:len(allglossesline)-2]+')'
        text = text[0:glossbox[2]+1]+allglossesline+text[glossbox[2]:len(text)]
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)

def interface():
    vocab = systembuilding()
    exit = False
    print('> > > Hello! You are using Shugni language verb parser. Fill the file text.txt in the same directory with the text you want to parse. It is preferable to avoid using punctuation and mark each sentence with a new line. Type in HELP for documentation.')
    while exit == False:
        print('> > > Does your text need convertion of the orthography? Type A and press Enter if so, else just press Enter, and the program will run.')
        orthoneed = input()
        if orthoneed.upper() == 'A' or orthoneed.upper() == 'А':
            orthoneed = True
        else:
            orthoneed = False
        text = textreading(orthoneed)
        glossboxes = verbfind(text, vocab)
        output(text, glossboxes)
        print('''> > > You can find your text parsed in the file output.txt. Type X and press Enter if you want to stop the program. Else, edit text.txt to parse another text.
''')
        exit = input()
        if exit.upper() == 'X' or exit.upper() == 'Х':
            exit = True
        else:
            exit = False

if everythingalright():
    interface()
else:
    print('Sadly, it seems some of the files necessary for the parser are missing. Please download the latest version of the parser from here: https://github.com/iurmak/shughni .')
