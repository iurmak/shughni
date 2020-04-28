ЧТО УМЕЕТ ДЕЛАТЬ ПАРСЕР
* строит систему глагольных основ по словарю Карамшоева
* заполняет лакуны в системе по регулярным правилам
* конвертирует текст в экспедиционную орфографию
* предупреждает, если в тексте смешанная орфография
* распознаёт глаголы в тексте
* определяет и указывает формы настоящего и прошедшего времён, перфекта и плюсквамперфекта, а также инфинитива
** а также производных от них форм — причастий и отглагольных существительных
** а также стяжённых форм настоящего времени
* знает о существовании нерегулярных глаголов и умеет с ними разбираться
* знает о существовании клитик, которые присоединяются к концу глагола, и умеет с ними разбираться

ЧТО ОН БУДЕТ ДЕЛАТЬ В БУДУЩЕМ
* распознавать отрицательные и сослагательные формы (скоро)
* распознавать формы, от которых убежали клитики (скоро)
* выдавать результат по стандарту Universal Dependencies (скоро)
* иметь нормальную документацию (скоро)
* радовать глаз пользователя приятным графическим интерфейсом (возможно???)

=================================================

УСТРОЙСТВО ПАРСЕРА
Можно посмотреть код в parser.py, а можно — примерный майндмэп алгоритма в mindmap.png.

=================================================

ФАЙЛЫ
p.py — это основной файл программы. Его нужно запустить, чтобы начать программу.

ortho.txt — это данные для конвертации орфографии. Для каждого символа "неправильной" орфографии обозначен символ, на который его нужно заменить.

text.txt — это файл с текстом, в котором пользователь хочет распознать формы глаголов.

vocab.txt — это файл-словарик с основами шугнанских глаголов, которые знакомы программе.
    vocab (ver1).txt и vocab (ver2).txt — две версии vocab. Обе теоретически совместимы, но в них разные ошибки. В первой версии j (й) часто неправильно заменён на ǯ (джь), но там почищено много помарок распознавания Карамшоева. Во второй помарок распознавания почищено меньше, зато с j всё в порядке.

orthocorrupt.txt — это файл с данными о символах, которые не могут встречаться в тексте вместе; то есть если они встречаются, надо выдать предупреждение.

irreg.txt — это файл-словарик нерегулярных глаголов и их глоссирований
