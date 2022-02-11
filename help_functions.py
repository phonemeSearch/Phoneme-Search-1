from re import search, finditer, sub
from os import path, getcwd
from json import dumps
from base64 import b64encode
from sqlite3 import connect
from flask import session


# data structures


path_help = getcwd()
path_help = path.join(path_help, "database", "PhonemeSearch.db")

languages = ["greek", "vedic", "latin", "armenian"]


def sql_fetch_entries(command, path, regex) -> list:
    connection = connect(path)
    cursor = connection.cursor()
    if regex:
         connection.create_function("REGEXP", 2, regexp)
    cursor.execute(command)
    entries = cursor.fetchall()
    connection.close()
    return entries


def open_file(path, filename, enc, mode, data):
    with open(file=path.join(path, filename), encoding=enc, mode=mode) as file:
        if mode == "r":
            data = file.read()
            return data
        elif mode == "w":
            file.write(data)


def get_allowed_con_vow(language):
    consonants = []
    vowels = []
    
    allowed = ["(", ")", "+"]
    if language == "armenian":
        allowed.extend("`")

    for kind in ["vowel", "consonant"]:
        cmd = f"SELECT grapheme FROM {language}_{kind}"
        kind_entries = sql_fetch_entries(cmd, path_help, False)
        if kind == "vowel":
            vowels.extend([grapheme[0] for grapheme in kind_entries])
        elif kind == "consonant":
            consonants.extend([grapheme[0] for grapheme in kind_entries])

    cmd = f"SELECT key FROM search_key_{language}"
    key_entries = sql_fetch_entries(cmd, path_help, False)
    allowed.extend([key[0] for key in key_entries])
    allowed.extend(vowels + consonants)
    
    return allowed, consonants, vowels


def get_ambiguous(language):
    accent = session["accent_sensitive"]
    if accent == "on":   
        greek_ambiguous = {
                            "σ": ["ς"],
                            "ρ": ["ῥ"],
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
                            "ρ": ["ῥ"],
                            "α": ["ά", "ά", "ᾶ", "ἀ", "ἁ", "ἂ","ἃ","ἇ","ἆ", "ἄ", "ἅ"],
                            "ο": ["ό", "ό", "ὀ", "ὁ", "ὂ", "ὃ", "ὄ", "ὅ"], 
                            "ε": ["έ", "ἐ", "ἑ", "ἒ", "ἓ", "ἔ", "ἕ"],
                            "η": ["ή", "ή", "ῆ", "ἠ", "ἡ", "ἦ", "ἧ", "ἢ", "ἣ", "ἤ", "ἥ"],
                            "ι": ["ῖ", "ί", "ί", "ἰ", "ἱ", "ἲ", "ἳ", "ἶ", "ἷ", "ἴ", "ἵ"],
                            "ω": ["ώ", "ώ", "ῶ", "ὠ", "ὡ", "ὢ", "ὣ", "ὦ", "ὧ", "ὤ", "ὥ"],
                            "ου": ["όυ","ού","οῦ","οὐ","οὑ","οὖ", "οὗ", "ού", "οὔ", "οὕ"],
                            "υ": ["ύ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ὔ", "ὕ"], 
                            "h": ["ἁ", "ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ", "οὔ", "οὕ"]
                            }  

        vedic_ambiguous = {
                            'a': ['á', 'à'],
                            'e': ['é', 'è'],
                            'i': ['ì', 'í'],
                            'o': ['ò'],
                            'u': ['ù', 'ú']
                            }
        
        latin_ambiguous = {}

        armenian_ambiguous = {}
    
    if language == "greek":
        ambiguous = greek_ambiguous

    elif language == "vedic":
        ambiguous = vedic_ambiguous
   
    elif language == "latin":
        ambiguous = latin_ambiguous

    elif language == "armenian":
        ambiguous = armenian_ambiguous
    
    return ambiguous


def get_digraphs(language):

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
                        "c": ["h"],
                        "a": ["u"],
                        "a": ["i"]
                    }

    following_digraph_vedic = ["h", "u", "I"]
    
    latin_digraphs = {
                        "q": ["u"]
                    }

    following_digraph_latin = ["u"]

    armenian_digraphs = {
                        "ո": ["ւ"],
                        "p": ["`"],
                        "t": ["`"],
                        "k": ["`"],
                        "c": ["`"],
                        "č": ["`"]
                        }

    following_digraph_armenian = ["ւ"]

    if language == "greek":
        digraphs = greek_digraphs
        following_digraph = following_digraph_greek

    elif language == "vedic":
        digraphs = vedic_digraphs
        following_digraph = following_digraph_vedic
   
    elif language == "latin":
        digraphs = latin_digraphs
        following_digraph = following_digraph_latin

    elif language == "armenian":
        digraphs = armenian_digraphs
        following_digraph = following_digraph_armenian

    #prepare_path()

    return digraphs, following_digraph


# functions for main_functions_search

# function for sqlite3 REGEXP
def regexp(expr, item):
    find = search(expr, item)
    return find is not None


def handle_digraphs(digraph, current_list, count):
    language = session["language"]
    digraph_out = ""
    digraph_out += digraph
    is_digraph = False
    following = get_digraphs(language)[0].get(digraph)
    for char in following:
        if current_list[count + 1] == char:
            is_digraph = True
            digraph_out += char
    return digraph_out, is_digraph


def handle_ambiguous_phonemes(ambiguous_char) -> str:
    language = session["language"]
    ambiguous_out = ""
    ambiguous_out += ambiguous_char
    ambiguous = get_ambiguous(language)
    for char in ambiguous.get(ambiguous_char):
        ambiguous_out += "|" + char
    return ambiguous_out


def join_digraph(char):
    language = session["language"]
    following = "".join(get_digraphs(language)[0].get(char))    
    return following


def follows_digraph(follow_char):
    language = session["language"]
    before = ""
    digraphs = get_digraphs(language)[0]
    for digraph in digraphs:
        for char in digraphs.get(digraph):
            if char == follow_char:
                before += digraph

    return before


def digraphs_to_begin(group):
    sorted_group = [phoneme for phoneme in group if len(phoneme) > 1]
    sorted_group.extend([phoneme for phoneme in group if phoneme not in sorted_group])
    return sorted_group


# functions for backend

# built url

def get_result_number(language, pattern):

    extract = "lemma"
    if language == "vedic":
        extract = "transliteration"
    count_command = \
    f"SELECT COUNT(*) FROM {language} WHERE {extract} REGEXP '{pattern}'"

    number = sql_fetch_entries(count_command, path_help, True)
    for num in number:
        number = num[0]
        
    return number


def built_url_to_dictionaries(language, results, index):
    lemma = results[index]
    if language == "greek" or language == "latin":
        url = f"https://logeion.uchicago.edu/{lemma}"
        alt_url = f"https://lsj.gr/wiki/{lemma}"
    
    elif language == "vedic":

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

        json_str = dumps(json_obj)
        bytes_json = bytes(json_str, "utf-8")
        encoded_jsn = b64encode(bytes_json)
        str_code = encoded_jsn.decode("utf-8")
        url = f"https://vedaweb.uni-koeln.de/rigveda/results/{str_code}"
        alt_url = None

    elif language == "armenian":
        url = f"http://www.nayiri.com/imagedDictionaryBrowser.jsp?dictionaryId=26&dt=HY_HY&query={lemma}"
        alt_url = f"https://calfa.fr/search?query={lemma}"
    
    return url, alt_url


# mark pattern
# wraps searched pattern of lemmas in span elements to mark them with css


def mark_pattern (pattern, results, language, xml):
    language = session["language"]

    if xml is False:
        tags = ["span class='pattern'", "span", "span class='word'", "span"]
    else:
        tags = ["pattern", "pattern", "word", "word"]
        
    #tags = []
    marked_list = []
    for index in range(len(results)):
        matches = finditer(pattern, results[index])
        marked = results[index]
        for match in matches:

            group = match.group(0)
            if group in get_digraphs(language)[0]:
                after = join_digraph(group)
                mark_re = f"(?<!§){group}(?!({'|'.join(after)}))"
            elif group in get_digraphs(language)[1]:
                before = follows_digraph(group)
                mark_re = f"(?<![{before}]){group}(?!\w?%)"
            else:
                mark_re = f"{group}(?!\w?%)"

            marked = sub(mark_re, f"§{group}%", marked, 1)

        marked = sub("%", f"</{tags[1]}>", marked)
        marked = sub("§", f"<{tags[0]}>", marked)
        marked = f"<{tags[2]}>{marked}</{tags[3]}>"
        
        if xml is False:
            url = built_url_to_dictionaries(language, results, index)
            main_url = url[0]
            #alt_url = url[1]
            alt = ""

            marked = f"<a class='external-link' href='{main_url}'>{marked}<i class='fa fa-external-link'></i></a>{alt}"
            marked = f"<span class='original'>{marked}</span>"
            
        marked_list.append(marked)
    return marked_list


# order functions

# syllablificate

def add_syl(syl):
    syl += "."
    return syl


def cut(word:str, place:int):
    place = place * (-1)
    syl = word[place:-1] + word[-1]
    syl_add = add_syl(syl)
    word = word.removesuffix(syl)

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
        word  = sub("ու", "u", word)
        syllab = []
        #print("syllab", syllab)
        i = 0
        while len(word) > 0:
            i += 1
            if i == 100:
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
        syllab_str  = sub("u", "ու", syllab_str)
        syllab_results.append(syllab_str.removesuffix("."))

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

        lemma = sub(("ου"), "u", lemma)
        lemma = sub(("όυ"), "ú", lemma)
        lemma = sub(("ού"), "ù", lemma)
        lemma = sub(("οῦ"), "o", lemma)
        lemma = sub(("οὐ"), "ó", lemma)
        lemma = sub(("οὑ"), "ò", lemma)
        lemma = sub(("οὖ"), "ü", lemma)
        lemma = sub(("οὗ"), "q", lemma)
        lemma = sub(("ού"), "w", lemma)
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

        syllables = sub(("u"), "ου", syllables)
        syllables = sub(("ú"), "όυ", syllables)
        syllables = sub(("ù"), "ού", syllables)
        syllables = sub(("o"), "οῦ", syllables)
        syllables = sub(("ó"), "οὐ", syllables)
        syllables = sub(("ò"), "οὑ", syllables)
        syllables = sub(("ü"), "οὖ", syllables)
        syllables = sub(("q"), "οὗ", syllables)
        syllables = sub(("w"), "ού", syllables)

        syllable_lem.append(syllables)
        
    return syllable_lem


def syllabificate_vedic(results):
    return []


def syllabificate_latin(results):
    return []



def syllabificate(language, results):
    #unvisible = ""
    if language == "greek":
        syl_results = syllabificate_greek(results)
    elif language == "vedic":
        syl_results = syllabificate_vedic(results)
        #unvisible = "hidden"
    elif language == "latin":
        syl_results = syllabificate_latin(results)
        #unvisible = "hidden"
    elif language == "armenian":
        syl_results = syllabificate_armenian(results)
     
    return syl_results

# if any download button is pressed function is called
# gets all possible results from DB and saves them into txt resp xml file

def download(pattern, user_pattern, language, kind):
    
    extract = "lemma"
    if language in ["vedic"]:
        extract = "transliteration"

    search_command = \
    f"SELECT lemma FROM {language} WHERE {extract} REGEXP '{pattern}' "
    
    connection = connect(path.join("database", "PhonemeSearch.db"))    
    cursor = connection.cursor()
    connection.create_function("REGEXP", 2, regexp)
    
    cursor.execute(search_command)
    results = cursor.fetchall()
    connection.close()
    results = [result[0] for result in results]

    # format string
    num_str = str(len(results))
    if num_str == "0":
        response_str = "no results"
        mimetype = "text/plain"
        filename = f"{language}_{user_pattern}_{str(len(results))}.txt"
    elif kind == "txt":
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
