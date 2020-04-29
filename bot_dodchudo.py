from telebot import TeleBot
from time import time as t

bot = TeleBot("731258272:AAFI2pR1hNIjVqBczIdhJ-BThTfFvRC1SnQ")

def translit(word):
    eng = ['a', 'b', 'c', 'd', 'e', 'ê', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ā', 'ž', 'č', 'x̌', 'ů', 'ū', 'ī', 'ʒ', 'ɣ', 'ɣ̌', 'ǰ', 'š', 'q', 'ð', 'θ']
    rus = ['А', 'Б', 'Ц', 'Д', 'Е', 'Ê', 'Ф', 'Г', 'И', 'Ҷ', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'В', 'W', 'Х', 'Й', 'З', 'Ā', 'Ж', 'Ч', 'X̌','У̊', 'Ӯ', 'Ӣ', 'Ʒ', 'Ғ', 'Г̌', 'Ҷ', 'Ш', 'Қ', 'Ð', 'θ']
    alph = dict(zip(eng,rus))
    slovo = []
    gap = []
    for y in range(len(word)):
        if word[y] == '̌':
            slovo = slovo[:len(slovo)-1]
            slovo.append(word[y-1]+word[y])
            y-=1
        else:
            slovo.append(word[y])
    for z in range(len(slovo)):
        if slovo[z] in alph:
            gap.append(alph[slovo[z]])
    parole = ('').join(gap)
    return(parole)


def simplify(dirty):
    clean = ('').join(('').join((('').join(('').join(('').join(dirty.split('-')).split(',')).split('='))).split('(')).split(':'))
    return(clean)


def starts(a, given):
    d = {'А': 'А', 'Б': 'Б', 'Ц': 'Ц', 'Д': 'Д', 'Е': 'Е', 'Ê': 'Е', 'Ф': 'Ф', 'Г': 'Г', 'И': 'И', 'Ҷ': 'Ц', 'К': 'К', 'Л': 'Л', 'М': 'М', 'Н': 'Н', 'О': 'О', 'П': 'П', 'Р': 'Р', 'С': 'С', 'Т': 'Т', 'У': 'У', 'В': 'В', 'W': 'W', 'Х': 'Х', 'Й': 'Й', 'З': 'З', 'Ā': 'А', 'Ж': 'Ж', 'Ч': 'Ц', 'Х̌': 'Х', 'У̊': 'У', 'Ӯ': 'У', 'Ӣ': 'И', 'Ʒ': 'Ʒ', 'Ғ': 'Г', 'Г̌': 'Г', 'Ш': 'Ш', 'Қ': 'К', 'Ð': 'D', 'θ': 'θ'}
    if len(given) > len(a):
            return
    for x in range(len(given)):
            if not (a[x] == given[x] or a[x] in d and d[a[x]] == given[x]):
                    return
    return True


def onlycapital(word):
    return word.upper() == word


lines = []
lines0 = []
n = 0


def preProcess():
    t0 = t()
    global lines, lines0
    with open('/home/faniadaniel/Dodchudo/REREWRITTEN.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines0 = lines[:]
    for x in range(len(lines)):
        massiv = lines[x].split()
        newmass = []
        for y in range(len(massiv)):
            massiv[y] = simplify(massiv[y])
            if onlycapital(massiv[y]):
                newmass.append(massiv[y])
        lines[x] = newmass

    print("Done in {}".format(t() - t0))


@bot.message_handler(func=lambda x: True)
def main(mes):
    text = mes.text
    with open('log.txt', 'a') as f:
        print("Got message from id {} message id {}. Text: {}. Sent at {}. Now is {}".format(mes.chat.id, mes.message_id, text, mes.date, t()), file=f)
    global n
    t0 = t()
    if text == '/start':
        bot.reply_to(mes, 'Привет! Пиши латиницей шугнанские слова!')
    else:
        eng = ['a', 'b', 'c', 'd', 'e', 'ê', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ā', 'ž', 'č', 'x̌', 'ů', 'ū', 'ī', 'ʒ', 'ɣ', 'ɣ̌', 'ǰ', 'š', 'q', 'ð', 'θ']
        text = text.lower()
        helphim = lambda: bot.reply_to(mes, "Пиши, пожалуйста, слово, состоящее из латинских букв без h и диакритик, и ничего кроме этого! Я не такой стабильный, как ты думаешь")
        if not text:
            helphim()
        for x in text:
            if not x in eng:
                helphim()
                return
        giveout = []
        exacts = []
        parole = translit(text)
        print("parsed in {}".format(t() - t0))
        for i in range(len(lines)):
            article = lines[i]
            if (len(article) > 0):
                for each in article:
                    if starts(each, parole):
                        if len(each) == len(parole):
                            exacts.append(lines0[i])
                            break
                else:
                    for each in article:
                        if starts(each, parole):
                            giveout.append(lines0[i])
                            break
        print("answer ready in {}".format(t() - t0))
        if (len(giveout) == 0 and len(exacts) == 0):
            bot.reply_to(mes, "Sorry, found nothing")
            print("done in {}".format(t() - t0))
            return
        if len(giveout) == 0:
            ans = '\n'.join(exacts)
            for x in range((len(ans) + 3999) // 4000):
                bot.send_message(mes.chat.id, ans[x * 4000:(x + 1) * 4000])
        if len (giveout) > 0:
            ans = '\n'.join(exacts) + "\nYou can find full answer in attachment"
            for x in range((len(ans) + 3999) // 4000):
                bot.send_message(mes.chat.id, ans[x * 4000:(x + 1) * 4000])
            n += 1
            ilnum = n
            n %= 20
            with open('/home/faniadaniel/Dodchudo/fullgiveout{}.txt'.format(ilnum), 'w', encoding = 'utf-8') as g:
                g.write('\n'.join(giveout) + "\n\nThank you for using our bot.")
            with open("/home/faniadaniel/Dodchudo/fullgiveout{}.txt".format(ilnum), "rb") as f:
                bot.send_document(mes.chat.id, f)

        print("done in {}".format(t() - t0))

preProcess()
while True:
    try:
        bot.polling()
    except Exception as e:
        with open("log.txt", 'a') as f:
            print("Experienced {} at {}.".format(e, t()), file=f)
        print("Experienced {} at {}.".format(e, t()))
