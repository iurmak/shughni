'''
Привет!
Функции идут в более-менее хронологическом / логическом порядке. По большому счёту вся программа состоит из вложенных друг в друга функций.
Дополнительные, более мелкие функции технического характера описываются в самом начале, до 180 строки.

UPD: я так посмотрел и понял, что легче читать код «с конца», и по ходу движения искать в коде новые функции и узнавать, что они делают. В конце происходит самое важное, каркас, потом можно пролистывать вверх и узнавать, что происходит в вызванных функциях.
Я бы расположил иначе, но Python не умеет вызывать функцию, которая ниже в коде, поэтому приходится сначала описывать функции, а потом их вызывать :/
'''

import re

def deleteidentical(spisok):
    #функция удаляет одинаковые элементы списка
    
    #сначала проверяется, есть ли в списке элементы, которые отличаются только родом или числом, и удаляет их — это рудименты одинаковых основ глагола
    #например, для большинства основ презенса нет вариантов мужского и женского родов; на этом этапе глоссирования PRS.M-2SG и PRS.F-2SG
    #все подходящие элементы попадают в список n
    n = []
    for element in spisok:
        
        if '.M' in element:
            if element.replace('.M', '.F') in spisok:
                n.append(element.replace('.M', ''))
            else:
                n.append(element)
        elif '.F' in element:
            if not element.replace('.F', '') in n:
                n.append(element)
        elif '.PL' in element:
            if not element.replace('.PL', '') in n:
                n.append(element)
        else:
            n.append(element)
    
    #здесь проверяется, есть ли в списке одинаковые элементы
    #все подходящие элементы попадают в список q, который выводится из функции
    q = []
    for element in n:
        if element not in q:
            if not 'NEG-NEG' in element:
                q.append(element)
    
    return q

def unglue(text):
    #эта функция отделяет знаки препинания от предшествующих слов
    #например, строка 'A word, another word. Please!' превратится в 'A word , another word . Please !'
    #это нужно для нормального деления на слова
    
    signs = ('\.', '\,', '\!', '\?', '\:', '\-', '\;')
    for sign in signs:
        text = re.sub(sign+' ', ' '+sign[1:]+' ', text)
    return text

def glue(text):
    #эта функция присоединяет знаки препинания к предшествующим словам обратно
    #например, строка 'A word , another word . Please (please > IMP.SG) !' превратится в 'A word, another word. Please (please > IMP.SG)!'
    #это нужно для красивого отображения текста в аутпуте
    
    signs = ('\.', '\,', '\!', '\?', '\:', '\-', '\;')
    for sign in signs:
        text = re.sub(' '+sign, sign[1:], text)
    return text

def slash_n_delete(stroka):
    #функция удаляет \n из концов строк в словаре глаголов (для systembuilding)
    
    if stroka.endswith('\n'):
        stroka = stroka[0:len(stroka)-1]
    return stroka

def listen(stroka):
    #функция делает из строки список с этой строкой из вариантов основы (для systembuilding)
    
    if '/' in stroka:
        spisok = stroka.split('/')
    else:
        spisok = [stroka]
    return(spisok)

def setnumbers():
    #функция устанавливает глобальные константы, индексы глагольных основ, чтобы было удобнее достигать нужной ячейки в матрице словаря
    #каждая константа — индексы грамматической формы в словаре (начиная с 0)
    #теперь можно обращаться к стемам презенса не как vocab[i][0], а как vocab[i][praesmasc] — так интуитивнее, плюс всегда можно легко поменять нумерацию
    
    global praesmasc
    global praesfemn
    global praes3sg
    global pastmasc
    global pastfepl
    global perfmasc
    global perffemn
    global perfplur
    global infimasc
    global infifemn
    global lemma
    praesmasc = 0
    praesfemn = 1
    praes3sg = 2
    pastmasc = 3
    pastfepl = 4
    perfmasc = 5
    perffemn = 6
    perfplur = 7
    infimasc = 8
    infifemn = 9
    lemma = 10
    
    #индекс -1 зарезервирован для стяжённых форм
    global contracted
    contracted = -1

def spacedivision(text):
    #функция находит пробелы в тексте и таким образом вычленяет токены (для verbdivision
    
    #iwords собирает номера тех символов текста, которые являются пробелами
    iwords = []
    iword = -1
    while text.find(' ', iword+1, len(text)-1) > -1:
        iword = text.find(' ', iword+1, len(text)-1)
        
        #добавим +1, тогда iword будет номером не пробела, а следующего за ним токена
        iword = iword + 1
        iwords.append(iword)
    
    #добавим в качестве последнего iwords конец текста, чтобы программа «заметила» последнее слово в тексте
    iwords.append(len(text))
    
    return iwords

def jification(stem):
    #добавляет -j- в конец основы, если она оканчивается на гласный
    #это нужно, чтобы парсер распознавал naxtijum, a naxtium не распознавал
    
    vowels = ('a', 'e', 'i', 'o', 'u', 'ā', 'ī', 'ō', 'ū', 'ɛ', 'ö')
    for vowel in vowels:
        if stem.endswith(vowel):
            stem = stem+'j'
            break
    
    return stem

def wordclean(word):
    #очищает токен от лишнего
    
    word = word.lower()
    
    #если конец токена отделяется дефисом или «равно» и не известен как личное окончание, то это может быть клитика, которую надо удалить
    verbendings = ('um', 'jum', 'i', 'ji', 'd', 't', 'ām', 'jām', 'et', 'jet', 'en', 'jen', 'īǯ', 'jīǯ', 'meǯ', 'ak', 'jak', 'in', 'jin', 'ow', 'jow')
    if '-' in word or '=' in word:
        iclitic = max(word.rfind('-'), word.rfind('='))+1
        clitic = word[iclitic:len(word)]
        if not clitic in verbendings:
            word = word[0:iclitic-1]
    
    #нужно удалить знаки препинания, которые могли затеряться в токене
    word = re.sub('\-', '', word)
    word = re.sub('\—', '', word)
    word = re.sub('\=', '', word)
    word = re.sub('\ ', '', word)
    word = re.sub('\.', '', word)
    word = re.sub('\,', '', word)
    word = re.sub('\?', '', word)
    word = re.sub('\!', '', word)
    word = re.sub('\:', '', word)
    
    return word

def realword(word):
    #проверяем, является ли токен настоящим словом (состоящим из символов), или пустой строкой
    
    wordness = True
    
    if word == '':
        wordness = False
    
    return wordness






def everythingalright():
    #если некоторых критически важных для работы программы файлов не хватает, то просим пользователя скачать полную версию со всеми файлами с гитхаба
    
    alright = False
    import os
    if os.path.isfile('./text.txt') and os.path.isfile('./vocab.txt') and os.path.isfile('./ortho.txt') and os.path.isfile('./help.txt'):
        alright = True
    return alright

def orthoconv(text):
    #конвертируем орфографию
    
    '''
    if not orthochecker(text) == True:
        print('In your text we have found symbols that shouldn't appear in one txt. These are: ')
        print('     /'+orthochecker(text))
        print('Either our parser doesn't support your writing system or your text is corrupted. Please keep in mind that the results of parsing can thus be unsatisfying.')
    '''
    
    with open('ortho.txt', 'r', encoding='utf-8') as file:
        ortho = file.readlines()
    goodlist = []
    for line in ortho:
        
        #с решёточки начинаются служебные строки в файле ortho
        if not line.startswith('#'):
            bad, good = line.split(' ')
            while bad in text:
                
                #все плохие символы заменяются на хорошие
                good = good[0:len(good)-1]
                text = text.replace(bad, good)
                #print(bad+' > '+good)
    
    return text

def orthochecker(text):
    #функция должна проверят, насколько последовательна орфография в исходном тексте, и если непоследовательна, выдавать предупреждение
    #но пока что она в разработке :)
    
    orthoright = ''
    
    '''
    with open('orthocorrupt.txt', 'r', encoding='utf-8') as file:
        ortho = file.readlines()
    for line in ortho:
        a, b = line.split(' ')
        if a in text and b in text:
            orthoright = orthoright+'{'+a+', '+b+'} '
    '''
    
    if orthoright == '':
        orthoright = True
    return orthoright

def textreading(orthoneed):
    #эта функция читает текст
    
    #берём текст пользователя из файла
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    
    #отдаём текст конвертеру, если необходимо
    if orthoneed:
        text = orthoconv(text)
    
    #наводим порядок, разделяя все токены и знаки между ними одиночными пробелами
    text = re.sub('\n', ' \n ', text)
    text = ' '+text+' '
    text = unglue(text)
    text = re.sub('  ', ' ', text)
    
    print('     /Text read.')
    #print(text)
    return text

def derivation(vocab):
    #это коммутатор, который принимает на вход словарь, выявляет, какую форму нужно образовать, и перенаправляет к нужной функции (для systembuilding)
    
    #нам понадобятся списки глухих и звонких согласных
    voiced = ('b', 'v', 'g', 'd', 'ð', 'ž', 'z', 'ʒ', 'ʁ', 'ǯ', 'ұ')
    deaf = ('θ', 'k', 'p', 's', 't', 'f', 'χ', 'ӿ', 'c', 'č', 'š', 'q')
    
    #теперь если значение какой-то ячейки матрицы словаря равно 1, то мы перенаправляем программу в нужную функцию
    for i in range(len(vocab)):
        if vocab[i][praes3sg][0] == '1':
            vocab[i][2] = make_praes3sg(vocab[i][0], deaf, voiced)      #форма презенса 3 л. ед. ч. образуется из основы презенса
        if vocab[i][3][0] == '1':
            vocab[i][3] = make_pastmasc(vocab[i][1], deaf)              #основа претерита образуется из основы презенса
        if vocab[i][5][0] == '1':
            vocab[i][5] = make_perfmasc(vocab[i][1], deaf)              #основа перфекта образуется из основы презенса
        if vocab[i][8][0] == '1':
            vocab[i][8] = vocab[i][3]                                   #основа инфинитива совпадает с основой претерита
    
    #возвращаем vocab — полный словарь с формами
    return(vocab)

def make_praes3sg(praestem, deaf, voiced):
    #функция образует форму презенса 3 л. ед. ч. из основы презенса (для derivation)
    
    form = []
    for variation in praestem:
        
        #если основа оканч. на mb/nb, то b удаляется
        if variation[len(variation)-2:len(variation)] == 'mb' or variation[len(variation)-2:len(variation)] == 'nb':
            variation = variation[0:len(variation)-2]
        
        #если основа оканч. на ʒ, то она заменяется на z
        if variation[len(variation)-1] == 'ʒ':
            variation = variation[0:len(variation)-1]+'z'
        
        #если основа оканч. на c, то она заменяется на s
        if variation[len(variation)-1] == 'c':
            variation = variation[0:len(variation)-1]+'s'
        
        #если основа оканч. на глухой, то присоединяется -t, иначе — -d
        if not variation[len(variation)-1] in deaf:
            if not variation.endswith('d'):
                form.append(variation+'d')
        if not variation[len(variation)-1] in voiced:
            if not variation.endswith('t'):
                form.append(variation+'t')
    
    return form

def make_pastmasc(praestem, deaf):
    #функция образует основу претерита из основы презенса (для derivation)
    
    form = []
    for variation in praestem:
        
        #если основа оканч. на mb/nb, то появляется вариант без b
        if variation[len(variation)-2:len(variation)] == 'mb' or variation[len(variation)-2:len(variation)] == 'nb':
            praestem.append(variation[0:len(variation)-2])
        
         #если основа оканч. на глухой, то присоединяется -t, иначе — -d
        if variation[len(variation)-1] in deaf:
            form.append(variation+'t')
        else:
            form.append(variation+'d')
    
    return form

def make_perfmasc(praestem, deaf):
    #функция образует основу перфекта из основы презенса (для derivation)
    
    form = []
    for variation in praestem:
        
        #если основа оканч. на глухой, то присоединяется -č, иначе — -ǯ
        if variation[len(variation)-1] in deaf:
            form.append(variation+'č')
        else:
            form.append(variation+'ǯ')
    
    return form

def systembuilding():
    #начинается основная функция для сборки словаря
    
    setnumbers()
    
    #vocab — это матрица словаря
    vocab = []
    
    #читаем файл vocab.txt, в котором лежит список глагольных основ
    with open('vocab.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                vocab.append(line)
    
    #делим vocab на основы по символам табуляции + удаляем '\n' в конце строки
    for i in range(len(vocab)):
        vocab[i] = vocab[i].split('\t')
        vocab[i][len(vocab[i])-1] = slash_n_delete(vocab[i][len(vocab[i])-1])
    
    #реорганизуем vocab как список (словарь) списков (лексем), состоящих из списков (разных форм), состоящих из списков (разных вариаций одной формы)
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            vocab[i][j] = listen(vocab[i][j])
    
    #ячейки с '1' заполняются регулярно образованными формами — так, например, происходит с отсутствующими формами претерита
    vocab = derivation(vocab)
    
    #ячейки с '0' заполняются ближайшими значениями слева — так, например, происходит с совпадающими формами женского рода / множественного числа
    for i in range(len(vocab)):
        for j in range(len(vocab[i])):
            if vocab[i][j][0] == '0':
                vocab[i][j] = vocab[i][j-1]
    
    #теперь vocab — список (словарь) списков (лексем), состоящих из списков (разных форм), состоящих из списков (разных вариаций одной формы)
    #у каждой формы есть свой индекс (например, 0 для стема презенса, 5 для женского стема перфекта, 10 для леммы, и т.д.)
    
    #print(vocab)
    print('     /Vocabulary loaded.')
    
    return vocab

def isitpraestem(word, stem, y):
    #функция проверяет, не является ли слово глагольной формой, образованной от praestem (для formdefinition)
    
    #определяем род стема
    if y == praesmasc:
        gender = 'M'
    if y == praesfemn:
        gender = 'F'
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #добавим к концу стема -j-, если он оканчивается на гласный
    stem = jification(stem)
    
    #проверяем, не является ли слово формой 3 лица ед. ч. презенса
    if word.endswith('d') or word.endswith('t'):
        flexias = ('d', 't')
        for flexia in flexias:
            if word == stem+flexia:
                attribute = 'PRS.'+gender+'-'+'3SG'
    
    #проверяем, не является ли слово одной из других форм презенса
    if attribute == False:
        flexias = {'um': '1SG', 'i': '2SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
        for flexia in flexias:
            if word == stem+flexia:
                attribute = 'PRS.'+gender+'-'+flexias[flexia]
    
    #проверяем, не является ли слово отглагольным существительным
    if attribute == False:
        if word == stem+'īǯ':
            attribute = 'AGENT_NOUN'
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def isitpraes3sg(word, stem):
    #функция проверяет, не является ли слово глагольной формой praes3sg (для formdefinition)
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #проверяем, не является ли слово формой 3 лица ед. ч. презенса
    if word == stem:
        attribute = 'PRS.3SG'
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def isitpasttnse(word, stem, y):
    #функция проверяет, не является ли слово глагольной формой, образованной от pastmasc / pastfepl (для formdefinition)
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #нам понадобятся окончания-клитики
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
    
    #добавим к концу стема -j-, если он оканчивается на гласный
    stem = jification(stem)
    
    #проверяем, не является ли слово формой претерита
    for flexia in flexias:
        if word.endswith(stem+flexia):
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == 4:
                    attribute = 'PST.PL-'+flexias[flexia]
                if y == pastmasc:
                    attribute = 'PST.SG-'+flexias[flexia]
            else:
                if y == pastfepl:
                    attribute = 'PST.F-'+flexias[flexia]
                if y == pastmasc:
                    attribute = 'PST.M-'+flexias[flexia]
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def isitperftnse(word, stem, y):
    #функция проверяет, не является ли слово глагольной формой, образованной от perfmasc / perffemn / perfplur (для formdefinition)
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #определяем род стема
    if y == perfmasc:
        gender = 'M'
    if y == perffemn:
        gender = 'F'
    if y == perfplur:
        gender = 'PL'
    
    #добавим к концу стема -j-, если он оканчивается на гласный
    stem = jification(stem)
    
    #нам понадобятся окончания-клитики
    flexias = {'um': '1SG', 'at': '2SG', 'i': '3SG', '': '3SG', 'ām': '1PL', 'et': '2PL', 'en': '3PL'}
    
    #проверяем, не является ли слово одной из форм
    for flexia in flexias:
        
        #перфект
        if word == stem+flexia:
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == perfplur:
                    attribute = 'PRF.PL-'+flexias[flexia]
            else:
                if y == perfmasc or y == perffemn:
                    attribute = 'PRF.'+gender+'-'+flexias[flexia]
        
        #плюсквамперфект
        if word == stem+'at'+flexia or word == stem+'it'+flexia:
            if flexias[flexia] == '1PL' or flexias[flexia] == '2PL' or flexias[flexia] == '3PL':
                if y == perfplur:
                    attribute = 'PST.PRF.PL-'+flexias[flexia]
            else:
                if y == perfmasc or y == perffemn:
                    attribute = 'PST.PRF.'+gender+'-'+flexias[flexia]
    
    #если ничего не найдено, ищем соответствия среди причастий
    if attribute == False:
        
        #перфектное причастие
        if word == stem+'ak':
            attribute = 'PRF.PTCP.'+gender
        
        #тупа причастие
        if word == stem+'in':
            attribute = 'ADJ.PTCP.'+gender
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def isitinfinite(word, stem, y):
    #функция проверяет, не является ли слово глагольной формой, образованной от infinite (для formdefinition)
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #определяем род стема
    if y == infimasc:
        gender = 'M'
    if y == infifemn:
        gender = 'F'
    
    #если это необходимо, добавим к концу стема -j-, если он оканчивается на гласный
    #а затем проверим, не является ли слово одной из форм
    
    #инфинитив-2 (супин)
    if word == jification(stem)+'ow':
        attribute = 'INF2.'+gender
    
    #инфинитив-1
    elif word == jification(stem):
        attribute = 'INF.'+gender
    
    #причастие будущего времени
    elif word == stem+'meǯ':
        attribute = 'FUT.PTCP.'+gender
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def isitcontract(word, stem):
    #функция проверяет, не является ли слово стяжённой формой praesstem (для verbfind)
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    
    #нам понадобится список гласных
    vowels = ('a', 'e', 'i', 'o', 'u', 'ā', 'ī', 'ō', 'ū', 'ɛ', 'ö')
    
    #определяем местоположение ближайшего к концу слова гласного в стеме
    #например, для стема naxti значение ivowel будет равно 1 (первый символ с конца), а для стема kafc — 3 (третий символ с конца)
    #ivowel нужен, чтобы определить, возможна ли вообще стяжённая форма, и какие фонемы «стягиваются»
    ivowel = len(stem)-1
    for a in range(1,len(stem)):
        if stem[a] in vowels:
            ivowel = a
    ivowel = len(stem)-ivowel
    
    #если ivowel равен 1 или 2 (то есть не более одного согласного после последнего гласного в стеме)
    #то проверяем, не является ли слово одной из стяжённых форм презенса
    if ivowel <= 2:
        
        #стяжённая форма 1 лица ед. ч.
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
                attribute = 'PRS.1SG'
        
        #стяжённая форма 2 лица мн. ч.
        elif word.endswith('et'):
            stem = stem[0:len(stem)-ivowel]
            if word == stem+'et':
                attribute = 'PRS.2PL'
        
        #стяжённая форма 3 лица мн. ч.
        elif word.endswith('en'):
            stem = stem[0:len(stem)-ivowel]
            if word == stem+'en':
                attribute = 'PRS.3PL'
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def formdefinition(word, stem, y):
    #это коммутатор, который выявляет, какая из основ найдена в слове, и перенаправляет программу к нужной функции (для verbfind)
    #на вход принимается слово (токен текста) word, предполагаемая основа stem и индекс этой основы в матрице словаря y
    
    #attributes — список глоссирований, который является результатом работы formdefinition
    #здесь нужен именно список, потому что найденных глоссирований может быть больше одного
    attributes = []
    
    #если переданный индекс y равен индексу одного из стемов, идём к этому стему
    #сначала проверяем на обычные формы
    if word.startswith(stem):
        if y == praesmasc or y == praesfemn:
            attributes.append(isitpraestem(word, stem, y))
        elif y == praes3sg:
            attributes.append(isitpraes3sg(word, stem))
        elif y == pastmasc or y == pastfepl:
            attributes.append(isitpasttnse(word, stem, y))
        elif y == perfmasc or y == perffemn or y == perfplur:
            attributes.append(isitperftnse(word, stem, y))
        elif y == infimasc or y == infifemn:
            attributes.append(isitinfinite(word, stem, y))
    
    #проверяем на стяжённые формы
    if y == contracted:
        attributes.append(isitcontract(word, stem))
    
    #проверяем на отрицательные и условные формы
    #если слово начинается на -ma- или -na-, а при удалении этих приставок найденная основа остаётся внутри слова
    #то вызываем formdefinition ещё раз, но уже для слова без приставки (ДА!!! РЕКУРСИЯ!!! КРУТО ПРАВДА???)
    #например, naxtijum не пройдёт, потому что стем naxti не сохраняется, если убрать -na-
    #а вот navuðǰ пройдёт, потому что без -na- перфектный стем vuðǰ сохраняется, и formdefinition вызовется уже для vuðǰ, чтобы определить его форму
    if word.startswith('ma') or word.startswith('na'):
        
        #если без приставки стем не сохраняется, мы предполагаем, что это стяжённая форма, и присваиваем индекс contracted
        if not word[2:].startswith(stem):
            if word.endswith('m') or word.endswith('et') or word.endswith('en'):
                y = contracted
        
        #вызываем formdefinition
        if word[2:].startswith(stem) or y == contracted:
            neg_attributes = formdefinition(word[2:], stem, y)
            for neg_attribute in neg_attributes:
                if word.startswith('ma'):
                    attributes.append('SUB-'+neg_attribute)
                if word.startswith('na'):
                    attributes.append('NEG-'+neg_attribute)
    
    #все пустые (то есть False) глоссирования удаляем
    for element in attributes:
        if element == False:
            attributes.pop(element)
    
    #возвращаем глоссирования (пустой список, если ничего не найдено)
    return attributes

def nedostatochny_stem(stems):
    
    #функция определяет, не является ли глагол недостаточным, то есть не имеющим некоторых форм (тогда на их месте стоит дефис)
    nedost = False
    if '-' in stems or '—' in stems or '−' in stems:
        nedost = True
    
    #возвращается True (глагол недостаточный) или False (все формы есть)
    return nedost

def irreg(word, stroki):
    #функция определяет, не является ли слово нерегулярным глаголом, форма которого добывается отдельно
    #stroki — строчки файла irreg.txt, в которых записаны нерегулярные глаголы таким образом: 'форма'+'\t'+'глоссирование'
    
    irregulars = {}
    for line in stroki:
        a, b = line.split('\t')
        b = b.replace('\n', '')
        irregulars[a] = b
    
    #по умолчанию значение глоссирования — False, что сигнализирует о том, что формам этого стема токен не соответствует
    attribute = False
    for irrform in irregulars:
        if irrform == word:
            attribute = irregulars[irrform]
    
    #возвращаем глоссирование (False, если ничего не найдено)
    return attribute

def verbfind(text, vocab):
    #это основная функция для поиска глагольных форм в тексте
    
    #читаем все нерегулярные глаголы из отдельного файла irreg.txt, помещаем его строчки в irregularwordlines
    with open('irreg.txt', 'r', encoding='utf-8') as f:
        irregularwordlines = f.readlines()
    
    #iwords — список номеров символов текста, с которых начинаются слова, плюс номер конца текста (в тексте 'First second' iwords = [0, 6, 12]
    iwords = spacedivision(text)
    
    #glossboxes — список, который собирает все найденные в тексте глоссирования
    glossboxes = []
    
    #приступим к поиску основ
    for a in range(len(iwords)-1):
        
        #word — это фрагмент строки от одного iwords до другого
        #например, при первой итерации цикла для текста 'First second' word будет 'First '
        word = text[iwords[a]:iwords[a+1]]
        
        #уберём в word возможные висящие сзади пробелы
        word = re.sub(' ', '', word)
        
        #очистим слово от мусора — пробелов и висящих в начале и конце знаках препинаний — и будем использовать его для определения формы
        wordnew = wordclean(word)
        
        #если то, что осталось после очистки — нормальное слово, а не пустая строка, то продолжаем
        if realword(wordnew):
            
            #glossfoundsinword — переменная, которая для каждой итерации цикла собирает найденные в токене глоссирования, а потом пакует их и передаёт в glossboxes
            glossfoundsinword = []
            
            #для каждой лексемы в словаре:
            for x in range(len(vocab)):
                
                #для каждого индекса стема в лексеме:
                for y in range(len(vocab[x])):
                    
                    #если этот стем недостаточный, не трогаем его
                    if not nedostatochny_stem(vocab[x][y]):
                        
                        #для каждой вариации стема:
                        for z in range(len(vocab[x][y])):
                            
                            #если мы нашли наш стем в токене
                            if vocab[x][y][z] in wordnew:
                                
                                #отправляем токен, стем и его индекс на поиск формы и получаем attributes — глоссирование
                                attributes = formdefinition(wordnew, vocab[x][y][z], y)
                                
                                #если какие-то глоссирования нашлись, т.е. список не пустой:
                                if not attributes == []:
                                    for attribute in attributes:
                                        
                                        #если можно указать лемму, то указываем её
                                        if vocab[x][lemma][0] != '—':
                                            attribute = vocab[x][lemma][0]+' > '+attribute
                                        
                                        #складываем все глоссирования в glossfoundsinword
                                        glossfoundsinword.append(attribute)
                
                #стяжённые формы не получится найти поиском соответствия, так как корень там не представлен полностью
                #поэтому стяжённые формы ищутся особым способом
                #сначала проверим, что токен вообще может быть такой формой: он должен оканчиваться на одно из окончаний -m-, -en- или -et-
                if wordnew.endswith('m') or wordnew.endswith('en') or wordnew.endswith('et'):
                    
                    #если этот стем недостаточный, не трогаем его
                    if not nedostatochny_stem(vocab[x][0]):
                        
                        #для каждой вариации стема:
                        for stem in vocab[x][0]:
                            
                            #проверим ещё, присутствует ли в токене «стяжённый» стем
                            if stem[0:len(stem)-2] in wordnew:
                                
                                #отправляем токен, стем и его индекс на поиск формы и получаем attributes — глоссирование
                                attributes = formdefinition(wordnew, stem, contracted)
                                
                                #если какие-то глоссирования нашлись, т.е. список не пустой:
                                if not attributes == []:
                                    for attribute in attributes:
                                        
                                        #если можно указать лемму, то указываем её
                                        if vocab[x][lemma][0] != '—':
                                            attribute = vocab[x][lemma][0]+' > '+attribute
                                        
                                        #складываем все глоссирования в glossfoundsinword
                                        glossfoundsinword.append(attribute)
                
                #если ни обычных, ни стяжённых форм не нашлось, то это может быть нерегулярный глагол
                if glossfoundsinword == []:
                    
                    #отправляем токен и словарик нерегулярных глаголов на поиск формы и получаем attributes — глоссирование
                    attribute = irreg(wordnew, irregularwordlines)
                    if not attribute == False:
                        glossfoundsinword.append(attribute)
            
            #если в итоге список найденных глоссирований не пустой:
            if not glossfoundsinword == []:
                
                #удаляем повторящиеся глоссирования
                glossfoundsinword = deleteidentical(glossfoundsinword)
                
                #складываем всё в glossboxes: токен, номер его начала и номер пробела после него, затем глоссирование
                glossboxes.append([word, iwords[a], iwords[a+1]-1, glossfoundsinword])
    
    print(glossboxes)
    print('     /Verbs found.')
    
    #возвращаем glossboxes — список «боксов», т.е. списков с глоссированиями
    return glossboxes

def output(text, glossboxes):
    #функция выводит текст с тегами глоссирований в файл output.txt
    
    #перевернём список «боксов», чтобы начинать вставлять глоссирования в текст с конца, а не с начала
    #таким образом мы не перепутаем номера символов в тексте, потому что сделанные изменения не будут влиять на предыдущие символы
    glossboxes.reverse()
    
    #вставляем каждое глоссирование в текст
    for glossbox in glossboxes:
        
        #начинаем строчку, которая будет представлять глоссирование, со скобочки
        allglossesline = '('
        
        #добавляем все глоссирования через запятую
        for gloss in glossbox[3]:
            allglossesline = allglossesline+gloss+', '
        
        #убираем последнюю запятую и закрываем скобочку
        allglossesline = allglossesline[0:len(allglossesline)-2]+')'
        
        #вставляем строчку с глоссированиями в текст на указанное в «боксе» место пробела после токена
        text = text[0:glossbox[2]+1]+allglossesline+text[glossbox[2]:len(text)]
    
    #приклеиваем все знаки препинания обратно к словам (собственно вся операция по отклеиванию и приклеиванию была нужна, чтобы скобочки с глоссированиями красиво обрамлялись знаками препинания, типа: 'glagol (PRS-1SG)!', а не 'glagol! (PRS-1SG)'
    text = glue(text)
    
    #все лишние пробелы, которые мы добавили, чтобы разделить на токены, тоже убираем
    text = re.sub('\n ', '\n', text)
    text = re.sub(' \n', '\n', text)
    if text.startswith(' '):
        text = text[1:len(text)]
    if text.endswith(' '):
        text = text[:len(text)-1]
    
    #записываем изменённый текст с глоссированиями в файл
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)

def interface():
    #это «интерфейс» — основная функция всего, которая запускает парсер и осуществляет взаимодействие с пользователем
    
    #построим словарь с помощью специальной функции
    vocab = systembuilding()
    
    #по умолчанию считаем, что пользователь не хочет выходить из программы
    exit = False
    
    #поздороваемся, у нас же вежливый парсер
    print('> > > Hello! You are using Shughni language verb parser. Fill the file text.txt in the same directory with the text you want to parse. It is preferable to avoid using punctuation and mark each sentence with a new line. Type in HELP for documentation.')
    
    #начинаем userloop, который будет удерживать программу и не прекратится, пока пользователь не захочет выйти
    while exit == False:
        
        #спрашиваем, надо ли конвертировать в орфографию
        print('> > > Does your text need convertion of the orthography? Type A and press Enter if so, else just press Enter, and the program will run.')
        orthoneed = input()
        if orthoneed.upper() == 'A' or orthoneed.upper() == 'А' or orthoneed.upper() == 'Ф':
            orthoneed = True
        else:
            orthoneed = False
        
        #читаем текст, держа в уме, нужно ли конвертировать орфографию
        text = textreading(orthoneed)
        
        #ищем глаголы в тексте и складываем глоссирования в glossboxes
        glossboxes = verbfind(text, vocab)
        
        #добавляем glossboxes в текст и выводим его
        output(text, glossboxes)
        
        #хвалимся пользователю, что молодцы, и спрашиваем, свободен ли Добби
        print('''> > > You can find your text parsed in the file output.txt. Type X and press Enter if you want to stop the program. Else, edit text.txt and press Enter to parse another text.
''')
        exit = input()
        if exit.upper() == 'X' or exit.upper() == 'Х' or exit.upper() == '[' or exit.upper() == '{':
            exit = True
        else:
            exit = False

#если все файлы программы на месте, запускаем «интерфейс»
if everythingalright():
    interface()
else:
    print('Sadly, it seems some of the files necessary for the parser are missing. Please download the latest version of the parser from here: https://github.com/iurmak/shughni .')
    exit = input()

#спасибо что дочитали ;)
