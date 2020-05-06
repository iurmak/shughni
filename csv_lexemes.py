import csv
praes_stem_and_lexeme = {}
with open('shughni_lexxemes.csv',encoding='UTF-8') as spisok_lexem_i_form_praes:
    csv_file = csv.reader(spisok_lexem_i_form_praes,delimiter=';',quotechar='?')
    for i in csv_file:
        praes_stem_and_lexeme[i[0]] = i[1]

what_for_we_have_a_gloss = praes_stem_and_lexeme.keys()

with open('vocab (ver2).txt', encoding='UTF-8') as where_to_add_lexemes:
    existing_database = where_to_add_lexemes.read()
    existing_database = existing_database.splitlines()
updated_database = existing_database

for cell_number in range(len(existing_database)):
    cell_to_check = existing_database[cell_number].replace('/',' ').replace('\t',' ')
    for candidate in what_for_we_have_a_gloss:
        if candidate in cell_to_check.split():
            if updated_database[cell_number].endswith(praes_stem_and_lexeme[candidate]):
                continue
            else:
                updated_database[cell_number] = existing_database[cell_number] + '\t' + praes_stem_and_lexeme[candidate]

with open('vocab_with_lexemes.txt','w',encoding='UTF-8') as f:
    for string in updated_database:
        f.write(string+'\r\n')
