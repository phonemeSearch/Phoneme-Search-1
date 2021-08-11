import re
import os
import sys
import json
from base64 import b64encode
import sqlite3
import main_functions_search as mf


# data structures

#subst = {"α": "άᾶἀἁἂἃἇἆ", "η":  "ήῆἠἡἦἧἢἣ", "ι":  "ῖίἰἱἲἳἶἷ", "ο":  "όὀὁὂὃ", "υ": "ύῦὐὑὒὓὖὗ", "ω": "ώῶὠὡὢὣὦὧ"}

digraphs = {}
following_digraph = []
ambiguous = {}
path = ""
lang = ""

def get_language_info(language, accent):
    global digraphs
    global following_digraph
    global ambiguous
    global lang

    lang = language

    greek_digraphs = {
                        "p": ["h", "s"],
                        "k": ["h","s"],
                        "t": ["h"],
                        "ο": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"],
                        "ό": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"],
                        "ὀ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"],
                        "ὁ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"],
                        "ὂ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"],
                        "ὃ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"]
                    }

    following_digraph_greek = ["h", "s", "υ", "υ" "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ", "ὔ", "ὕ"]

    vedic_digraphs = {
                        "p": ["h"],
                        "b": ["h"],
                        "k": ["h"],
                        "t": ["h"],
                        "d": ["h"],
                        "g": ["h"],
                        "ṭ": ["h"],
                        "ḍ": ["h"],
                        "c": ["h"]
                    }

    following_digraph_vedic = ["h"]
    
    latin_digraphs = {
                        "q": ["u"]
                    }

    following_digraph_latin = ["u"]

    armenian_digraphs = {"ո": ["ւ"]}
    following_digraph_armenian = ["ւ"]

    if accent == "on":   
        greek_ambiguous = {
                            "σ": ["ς"],
                            "α": ["ἀ", "ἁ"],
                            "ά": ["ἄ", "ἅ", "ἇ", "ἆ", "ᾶ"],
                            "ο": ["ὀ", "ὁ"],
                            "ό": ["ὄ", "ὅ"],
                            "ε": ["ἐ", "ἑ"],
                            "έ": ["ἔ", "ἕ"],
                            "η": ["ἠ", "ἡ"],
                            "ή": ["ἤ", "ἥ", "ἦ", "ἧ", "ῆ"],
                            "ι": ["ἰ", "ἱ"],
                            "ί": ["ἶ", "ἷ", "ἴ", "ἵ", "ῖ"],
                            "ω": ["ὠ", "ὡ"],
                            "ώ": ["ῶ", "ὤ", "ὥ", "ὦ", "ὧ"],
                            "ου": ["οὐ","οὑ"],  
                            "υ": ["ὐ", "ὑ", "υ"],
                            "h": ["ἁ", "ἃ", "ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]
                        }

        vedic_ambiguous = {}

        latin_ambiguous = {}

        armenian_ambiguous = {}

    else:
        greek_ambiguous = {
                            "σ": ["ς"],
                            "α": ["ά", "ά", "ᾶ", "ἀ", "ἁ", "ἂ","ἃ","ἇ","ἆ", "ἄ", "ἅ"],
                            "ο": ["ό", "ό", "ὀ", "ὁ", "ὂ", "ὃ", "ὄ", "ὅ"], 
                            "ε": ["έ", "ἐ", "ἑ", "ἒ", "ἓ", "ἔ", "ἕ"],
                            "η": ["ή", "ή", "ῆ", "ἠ", "ἡ", "ἦ", "ἧ", "ἢ", "ἣ", "ἤ", "ἥ"],
                            "ι": ["ῖ", "ί", "ί", "ἰ", "ἱ", "ἲ", "ἳ", "ἶ", "ἷ", "ἴ", "ἵ"],
                            "ω": ["ώ", "ώ", "ῶ", "ὠ", "ὡ", "ὢ", "ὣ", "ὦ", "ὧ", "ὤ", "ὥ"],
                            "ου": ["όυ","ού","οῦ","οὐ","οὑ","οὖ", "οὗ", "ού", "οὔ", "οὕ"],  # partly not yet in database, database transskript of 'hou'
                            "υ": ["ύ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ὔ", "ὕ"], 
                            "h": ["ἁ", "ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ", "οὔ", "οὕ"]
                            }  

        vedic_ambiguous = {
                            'a': ['á', 'à', 'ā'],
                            'e': ['é', 'è'],
                            'i': ['ì', 'í', 'ī'],
                            'o': ['ò'],
                            'u': ['ù', 'ú']
                            }
        
        latin_ambiguous = {}

        armenian_ambiguous = {}

    if language == "greek":
        digraphs = greek_digraphs
        following_digraph = following_digraph_greek
        ambiguous = greek_ambiguous

    elif language == "vedic":
        digraphs = vedic_digraphs
        following_digraph = following_digraph_vedic
        ambiguous = vedic_ambiguous
   
    elif language == "latin":
        digraphs = latin_digraphs
        following_digraph = following_digraph_latin
        ambiguous = latin_ambiguous

    elif language == "armenian":
        digraphs = armenian_digraphs
        following_digraph = following_digraph_armenian
        ambiguous = armenian_ambiguous

    prepare_path()


def prepare_path():
    global path
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(path, "database", "PhonemeSearch.db")


# functions for main_functions_search

# function for sqlite3 REGEXP
def regexp(expr, item):
    find = re.search(expr, item)
    return find is not None


def handle_digraphs(digraph, current_list, count):
    digraph_out = ""
    digraph_out += digraph
    is_digraph = False
    following = digraphs.get(digraph)
    for char in following:
        if current_list[count + 1] == char:
            is_digraph = True
            digraph_out += char
    return digraph_out, is_digraph


def handle_ambiguous_phonemes(ambiguous_char) -> str:
    ambiguous_out = ""
    ambiguous_out += ambiguous_char
    for char in ambiguous.get(ambiguous_char):
        ambiguous_out += "|" + char
    return ambiguous_out


def join_digraph(char):
    following = "".join(digraphs.get(char))    
    return following


def follows_digraph(follow_char):
    before = ""
    for digraph in digraphs:
        for char in digraphs.get(digraph):
            if char == follow_char:
                before += digraph

    return before


def digraphs_to_begin(group):
    sorted_group = [phoneme for phoneme in group if len(phoneme) > 1]
    sorted_group.extend([phoneme for phoneme in group if phoneme not in sorted_group])
    return sorted_group


# built url

def built_url_to_dictionaries(language, results, index):
    lemma = results[index]
    if language == "1" or language == "3":
        #url = f"https://lsj.gr/wiki/{results[index]}"
        url = f"https://logeion.uchicago.edu/{lemma}"
    
    elif language == "2":

        json_obj = {
            "input": f"{lemma}",
            "field": "version_",
            "regex": False,
            "sortBy": None,
            "sortOrder": None,
            "size": 10,
            "from": 0,
            "mode": "quick",
            "accents": False
        }

        json_str = json.dumps(json_obj)
        bytes_json = bytes(json_str, "utf-8")
        encoded_jsn = b64encode(bytes_json)
        str_code = encoded_jsn.decode("utf-8")
        url = f"https://vedaweb.uni-koeln.de/rigveda/results/{str_code}"
    
    elif language == "4":
        url = ""

    return url


# mark pattern
# wraps searched pattern of lemmas in span elements to mark them with css

def mark_pattern (pattern, results, language, xml):
    marked_list = []
    for index in range(len(results)):
        matches = re.finditer(pattern, results[index])
        marked = results[index]
        for match in matches:

            group = match.group(0)
            if group in digraphs:
                after = join_digraph(group)
                mark_re = f"(?<!§){group}(?!({'|'.join(after)}))"
            elif group in following_digraph:
                before = follows_digraph(group)
                mark_re = f"(?<![{before}]){group}(?!\w?%)"
            else:
                mark_re = f"{group}(?!\w?%)"

            marked = re.sub(mark_re, f"§{group}%", marked, 1)

        marked = re.sub("%", "</span>", marked)
        marked = re.sub("§", "<span class='pattern'>", marked)
        marked = f"<span class='word'>{marked}</span>"
        
        if xml is False:
            url = built_url_to_dictionaries(language, results, index)
            marked = f"<a class='external-link' href='{url}'>{marked}<i class='fa fa-external-link'></i></a>"

        marked = f"<div class='result'>{marked}</div>"
        marked_list.append(marked)
    return marked_list


# order functions

# alphabetical sorting

def change_switch_status(reverse_status, descending_status):

    if reverse_status == "1":
        checked_reverse = "checked"
    else:
        checked_reverse = ""

    if descending_status == "1":
        checked_descending = "checked"
    else:
        checked_descending = ""

    switch_html = f"""
                <label for='reverse-check'>
                    <input id='reverse-check' class='alphabet-check' type='checkbox' name='reverse' value='1' onChange='this.form.submit();' {checked_reverse}>
                    sort reverse
                </label>
                <label for='descending-check'>
                    <input id='descending-check' class='alphabet-check' type='checkbox' name='descending' value='1' onChange='this.form.submit();' {checked_descending}>
                    sort descending
                </label>"""

    return switch_html


# length sorting

def length_sorting(results, sorting):
    if sorting == "length-ascending":
        results.sort(key=len)
    
    elif sorting == "length-descending":
        results.sort(key=len, reverse=True)

    return results


# syllablificate

def add_syl(syl):
    syl += "."
    return syl


def cut(word:str, place:int):
    place = place * (-1)
    syl = word[place:-1] + word[-1]
    syl_add = add_syl(syl)
    word = word.removesuffix(syl)
    #print(word)
    return word, syl_add


def syllabificate_armenian(results):
    V = ['ի', 'u', 'ե', 'ո', 'ը', 'է', 'ա', 'օ']

    C = [
        'պ', 'բ', 'փ', 'տ', 'դ', 'թ', 'կ',
        'գ', 'ք', 'մ', 'ն', 'ռ', 'ր', 'ս',
        'զ', 'շ', 'ժ', 'խ', 'հ', 'ֆ', 'վ',
        'ւ', 'յ', 'լ', 'ղ', 'ծ', 'ձ', 'ց',
        'ճ', 'ջ', 'չ'
        ]

    F = ['ս', 'զ', 'շ', 'ժ', 'խ', 'հ', 'ֆ']

    P = ['պ', 'բ', 'փ', 'տ', 'դ', 'թ', 'կ', 'գ', 'ք']

    # stop, fricatives, affricates
    T = [
        'պ', 'բ', 'փ', 'տ', 'դ', 'թ', 'կ', 'գ', 'ք', 'ծ', 'ձ',
        'ց', 'ճ', 'ջ', 'չ', 'ս', 'զ', 'շ', 'ժ', 'խ', 'հ', 'ֆ'
        ]

    N = ['մ', 'ն']

    W = ['վ', 'ւ', 'յ']

    R = ['ռ', 'ր', 'լ', 'ղ', 'մ', 'ն', 'վ', 'ւ', 'յ'] # r, glide, lateral, nasal

    L = ['ռ', 'ր', 'լ', 'ղ']

    A = ['ծ', 'ձ', 'ց', 'ճ', 'ջ', 'չ']

    syllab_results = []
    for word in results:
        word  = re.sub("ու", "u", word)
        syllab = []
        #print("syllab", syllab)
        i = 0
        while len(word) > 0:
            i += 1
            if i == 100:
                print(word, "except")
                raise IndexError
            #print("in loop", syllab)
            try:
                if word[-4] in C and word[-3] in V and word[-2] in C and word[-1] in C:
                    if word[-2] in W:
                        if word[-1] in N or word[-1] in L:
                            pass #match
                            word_syl = cut(word=word, place=4)
                            word = word_syl[0]
                            syllab.append(word_syl[1])
                            continue
                        else:
                            pass #no match
                    elif word[-2] in R and word[-1] in T:
                        #match
                        word_syl = cut(word=word, place=4)
                        word = word_syl[0]
                        syllab.append(word_syl[1])
                        continue
                    elif word[-2] in F:
                        if word[-1] in P or word[-1] in A:
                            #match
                            word_syl = cut(word=word, place=4)
                            word = word_syl[0]
                            syllab.append(word_syl[1])
                            continue
                        else:
                            pass #no match
                    elif word[-2] in L and word[-1] in N:
                        #match
                        word_syl = cut(word=word, place=4)
                        word = word_syl[0]
                        syllab.append(word_syl[1])
                        continue
                    else:
                        pass #no match
                if word[-4] in C and word[-3] in 'ե' and word[-2] in 'ա' and word[-1] in C:
                    #match
                    word_syl = cut(word=word, place=4)
                    word = word_syl[0]    
                    syllab.append(word_syl[1])
                    continue
            except IndexError:
                pass

            try:
                if word[-3] in C and word[-2] in V and word[-1] in C:
                    #match
                    word_syl = cut(word=word, place=3)
                    word = word_syl[0]
                    syllab.append(word_syl[1])
                    continue
            except IndexError:
                pass

            try:
                if word[-2] in C and word[-1] in V:
                    #match
                    word_syl = cut(word=word, place=2)
                    word = word_syl[0]
                    syllab.append(word_syl[1])
                    continue
            except IndexError:
                pass

            # 2. Stufe
            try:
                if word[-3] in V and word[-2] in C and word[-1] in C:
                    if word[-2] in W:
                        if word[-1] in N or word[-1] in L:
                            #match
                            word_syl = cut(word=word, place=3)
                            word = word_syl[0]
                            syllab.append(word_syl[1])
                            continue
                        else:
                            #no match
                            pass
                    elif word[-2] in F:
                        if word[-1] in P or word[-1] in A:
                            #match
                            word_syl = cut(word=word, place=3)
                            word = word_syl[0]
                            syllab.append(word_syl[1])
                            continue
                    elif word[-2] in R and word[-1] in T:
                        #match
                        word_syl = cut(word=word, place=3)
                        word = word_syl[0]
                        syllab.append(word_syl[1])
                        continue
                    elif word[-2] in L and word[-1] in N:
                        #match
                        word_syl = cut(word=word, place=3)
                        word = word_syl[0]
                        syllab.append(word_syl[1])
                        continue
            except IndexError:
                pass

            try:
                if word[-2] in V and word[-1] in C:
                    #match
                    word_syl = cut(word=word, place=2)
                    word = word_syl[0]
                    syllab.append(word_syl[1])
                    continue
            except IndexError:
                pass

            # 3. Stufe
            try:
                if word[-2] in C and word[-1] in C:
                    #match
                    word_syl = cut(word, 2)
                    word = word_syl[0]
                    syllab.append(word_syl[1])
                    continue
            except IndexError:
                pass
            
            # rest match
            if word[-1] in C or word[-1] in V:
                word_syl = cut(word=word, place=1)
                word = word_syl[0]
                syllab.append(word_syl[1])

        syllab_str = "".join(reversed(syllab))
        syllab_str  = re.sub("u", "ու", syllab_str)
        syllab_results.append("<div class='syllable-lemma'>" + syllab_str.removesuffix(".") + "</div>")

    return syllab_results

def syllabificate_greek(results):
    V = [
        "α", "ά", "ά", "ᾶ", "ἀ", "ἁ", "ἂ","ἃ","ἇ","ἆ", "ἄ", "ἅ",
        "ο", "ό", "ό", "ὀ", "ὁ", "ὂ", "ὃ", "ὄ", "ὅ",
        "ε", "έ", "έ", "ἐ", "ἑ", "ἒ", "ἓ", "ἔ", "ἕ",
        "η", "ή", "ή", "ῆ", "ἠ", "ἡ", "ἦ", "ἧ", "ἢ", "ἣ","ἤ","ἥ",
        "ι", "ῖ", "ί", "ί", "ἰ", "ἱ", "ἲ", "ἳ", "ἶ", "ἷ","ἴ","ἵ",
        "ω", "ώ", "ώ", "ῶ", "ὠ", "ὡ", "ὢ", "ὣ", "ὦ", "ὧ","ὤ","ὥ",
        "υ", "ύ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ","ὔ","ὕ",
        "u", "ú", "ù", "ò", "o", "ó", "ü", "q", "w"
        ]

    C = [
        "β", "γ","δ", "ζ", "θ", "τ", "κ", "ρ", "ς", "σ", "π", "μ", "ν",
        "ψ", "χ", "φ", "ξ", "λ"
        ]

    syllable_lem = []
    numCount = 0
    for lemma in results:
        numCount += 1

        lemma = re.sub(("ου"), "u", lemma)
        lemma = re.sub(("όυ"), "ú", lemma)
        lemma = re.sub(("ού"), "ù", lemma)
        lemma = re.sub(("οῦ"), "o", lemma)
        lemma = re.sub(("οὐ"), "ó", lemma)
        lemma = re.sub(("οὑ"), "ò", lemma)
        lemma = re.sub(("οὖ"), "ü", lemma)
        lemma = re.sub(("οὗ"), "q", lemma)
        lemma = re.sub(("ού"), "w", lemma)
        index = 0
        point = False
        syllables = ""
        
        for char in lemma:
            if char in V:
                pass
            try:
                lemma[index+1]
                try:
                    lemma[index+2]
                except IndexError:
                    if point:
                        char += "."
                    syllables += char + lemma[index+1]
                    break
            except IndexError:
                syllables += char
                break

            if point:
                point = False
                syllables += char + "."

            elif char in C:
                syllables += char
            elif char in V:
                if lemma[index+1] in V and lemma[index+2] in V:
                    #print("in: --VVV--")
                    syllables += char + "."
                elif lemma[index+1] in V and lemma[index+2] in C:
                    #print("in: --VVC--")
                    point = True
                    syllables += char
                elif lemma[index+1] in C and lemma[index+2] in V:
                    #print("in: --VCV--")
                    syllables += char + "."
        
                elif lemma[index+1] in C and lemma[index+2] in C:
                    #print("in: --VCC--")
                    point = True
                    syllables += char

            index += 1

        syllables = re.sub(("u"), "ου", syllables)
        syllables = re.sub(("ú"), "όυ", syllables)
        syllables = re.sub(("ù"), "ού", syllables)
        syllables = re.sub(("o"), "οῦ", syllables)
        syllables = re.sub(("ó"), "οὐ", syllables)
        syllables = re.sub(("ò"), "οὑ", syllables)
        syllables = re.sub(("ü"), "οὖ", syllables)
        syllables = re.sub(("q"), "οὗ", syllables)
        syllables = re.sub(("w"), "ού", syllables)

        syllable_lem.append("<div class='syllable-lemma'>" + syllables + "</div>")
        
    return syllable_lem


# if any download button is pressed function is called
# gets all possible results from DB and saves them into txt resp xml file

def download(pattern, user_pattern, language, kind):
    languages = ["greek", "vedic", "latin", "armenian"]
    language = languages[language-1]
    search_command = \
    f"SELECT lemma FROM {language} WHERE lemma REGEXP '{pattern}' "
    
    if os.name == "nt":
        connection = sqlite3.connect("database\\PhonemeSearch.db")
    else:
        connection = sqlite3.connect("database/PhonemeSearch.db")
        
    cursor = connection.cursor()
    connection.create_function("REGEXP", 2, regexp)
    print(search_command)
    cursor.execute(search_command)
    results = cursor.fetchall()
    connection.close()
    results = [result[0] for result in results]

    # format string
    num_str = str(len(results))
    if kind == "txt":
        response_str = "\nnumber of results: " + num_str
        response_str += "\nsearch pattern: " + results[3] + "\n\n"
        response_str += "\n".join(results)
        mimetype = "text/plain"
        filename = f"{language}_{user_pattern}_{num_str}.txt"
    elif kind == "xml":
        response_str = mark_pattern(pattern, results, language, xml="True")
        response_str = "".join(response_str)
        response_str = f"<results language='{language}' pattern='{user_pattern}' number='{num_str}'>{response_str}</results>"
        mimetype = "application/xml"
        filename = f"{language}_{user_pattern}_{str(len(results))}.xml"
    return (response_str, mimetype, filename)
