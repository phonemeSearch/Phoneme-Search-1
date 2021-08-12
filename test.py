import sqlite3
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


conn = sqlite3.connect("database\\PhonemeSearch.db")
cur = conn.cursor()

cmd = "SELECT lemma FROM vedic"
cur.execute(cmd)
lemmas = cur.fetchall()
lemmas_list = [lemma[0] for lemma in lemmas]
conn.close()

"ē" #change to e
"ō" #change to o
"r̥" #change to ṛ, 
"ḷ" #is correct
"ṃ" #is correct
"ṅ ñ ṇ n m" #to ṃ

corr_list = []
for lemma in lemmas_list:
    index = -1
    change_dict = {"ē": "e", "ō": "o", "r̥": "ṛ"}
    for to_sub in change_dict:
        corr = change_dict[to_sub]
        #print(to_sub)
        lemma = re.sub(f"{to_sub}", f"{corr}", lemma)
    
    lemma = list(lemma)
    for char in lemma:
        index += 1
        try:
            if char == "ṅ" and char[index+1] in ["k","g","ṅ"]:
                lemma[index] = "ṃ"
            elif char == "ñ" and char[index+1] in ["c","j","ñ"]:
                lemma[index] = "ṃ"
            elif char == "ṇ" and char[index+1] in ["ṭ","ḍ","ṇ"]:
                lemma[index] = "ṃ"
            elif char == "n" and char[index+1] in ["t","d","n"]:
                lemma[index] = "ṃ"
            elif char == "m" and char[index+1] in ["p","b","m"]:
                lemma[index] = "ṃ"
        except:
            pass
    lemma = "".join(lemma)
    corr_list.append(lemma)

deva_list = []
for word in corr_list:
    deva = transliterate(word, sanscript.IAST, sanscript.DEVANAGARI)
    deva_list.append(deva)
print(len(deva_list))

char_list = []
for word in corr_list:
    word = set(list(word))
    char_list.extend(list(word))
print("char list", len(char_list))
char_list = list(set(char_list))

deva_char = []
for deva in deva_list:
    deva = set(list(deva))
    #print(deva)
    deva_char.extend(list(deva))

deva_char = list(set(deva_char))
print("deva char", len(deva_char))

false = []
for char in deva_char:
    if char in char_list:
        false.append(char)

print(false)