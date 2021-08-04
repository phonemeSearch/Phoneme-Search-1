import re
import os
import sys
import json
from base64 import b64encode
import sqlite3
import main_functions_search as mf 

# data structures

greek_search_info = \
    ("\n"
     "Single Phonemes:\n"
     "a:  α\n"
     "e:  ε\n"
     "ē:  η\n"
     "i:  ι\n"
     "o:  ο\n"
     "ō:  ω\n"
     "y:  υ\n"
     "u:  ου\n"
     "a:  ά\n"
     "e:  έ\n"
     "i:  ί\n"
     "o:  ό\n"
     "ō:  ώ\n"
     "y:  ύ\n"
     "u:  όυ\n"
     "ē:  ή\n"
     "i:  ι\n"
     "p:  π\n"
     "b:  β\n"
     "ph: φ\n"
     "t:  τ\n"
     "d:  δ\n"
     "th: θ\n"
     "k:  κ\n"
     "g:  γ\n"
     "kh: χ\n"
     "z:  ζ\n"
     "m:  μ\n"
     "n:  ν\n"
     "l:  λ\n"
     "r:  ρ\n"
     "s:  σ\n"
     "s:  ς\n"
     "ps: ψ\n"
     "p:  π\n"
     "b:  β\n"
     "ph: φ\n"
     "t:  τ\n"
     "d:  δ\n"
     "th: θ\n"
     "k:  κ\n"
     "g:  γ\n"
     "ks: ξ\n"
     "\n"
     "Phoneme classes:\n"
     "A: alveolar\n"
     "L: labial\n"
     "K: velar\n"
     "J: palatal\n"
     "G: laryngeal\n"
     "P: plosive\n"
     "R: approximant\n"
     "W: sonorant\n"
     "N: nasal\n"
     "F: fricative\n"
     ">: voiced\n"
     "#: aspirated\n"
     "<: voiceless\n"
     "%: not aspirated\n"
     "C: consonant\n"
     "V: vowel\n"
     "\n"
     "Wildcards:\n"
     "*: 0 or more characters\n"
     "|: marks end of lemma\n"
     "\n"
     "Input options:\n"
     "\n"
     "- 'a', 'b', 'kh', 'k': Lower case letters correspond to a single phoneme,\n"
     "  e.g.: 'a' = 'α', 'b' = 'β', 'kh' = 'χ', 'k' = 'κ' (full key above)\n"
     "\n"
     "- 'P+L+>', 'A': The capital letters correspond to phoneme classes (full key above). These classes \n"
     "  can be connected with '+', e.g. 'P+L+>' means plosive + labial + voiced.\n"
     "  You can choose one value of the features (manner, place, voice, aspiration) at the same time.\n"
     "  Thus, such connections could contain only up to four members, e.g. P+L+>+#.\n"
     "  'V' stands for vowel and C for consonant. These keys cannot be mixed with other ones.\n"
     "\n"
     "- '(abP+L)': If you want to allow a specific combination of phonemes at a certain place, you have to put\n"
     "   them in parenthesis. The same input rules as declared above apply within the brackets, too.\n")
vedic_search_info = \
    ("\n"
     "Key:\n"
     "\n"
     "Single phoneme input:\n"
     "The characters of the Latin transcription are used.\n"
     "\n"
     "Phoneme classes:\n"
     "A: alveolar\n"
     "L: labial\n"
     "K: velar\n"
     "J: palatal\n"
     "H: laryngeal\n"
     "X: retroflex\n"
     "P: plosive\n"
     "R: approximant\n"
     "W: glide\n"
     "N: nasal\n"
     "F: fricative\n"
     ">: voiced\n"
     "\"#: aspirated\"\n"
     "\"_: one_char\n"
     "<: voiceless\n"
     "%: non_aspirated\n"
     "V: vowel\n"
     "C: consonant\n"
     "\n"
     "Wildcards:\n"
     "*: 0 or more characters\n"
     "|: marks end of lemma\n"
     "\n"
     "Eingabemöglichkeiten:\n"
     "\n"
     "- 'a', 'b', 'kh', 'k': Lower case letters correspond to a single phoneme.\n"
     "\n"
     "- 'P+L+>', 'A': The capital letters correspond to phoneme classes (full key above). These classes \n"
     "  can be connected with '+', e.g. 'P+L+>' means plosive + labial + voiced.\n"
     "  You can choose one value of the features (manner, place, voice, aspiration) at the same time.\n"
     "  Thus, such connections could contain only up to four members, e.g. P+L+>+#.\n"
     "  'V' stands for vowel and 'C' for consonant. These keys cannot be mixed with other ones.\n"
     "\n"
     "- '(abP+L)': If you want to allow a specific combination of phonemes at a certain place, you have to put\n"
     "   them in parenthesis. The same input rules as declared above apply within the parenthesis, too.\n")
latin_search_info = ""
current_search_info = ""

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
    global current_search_info
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
                            "h": ["ἁ","ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]
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
        current_search_info = greek_search_info

    elif language == "vedic":
        digraphs = vedic_digraphs
        following_digraph = following_digraph_vedic
        ambiguous = vedic_ambiguous
        current_search_info = vedic_search_info
   
    elif language == "latin":
        digraphs = latin_digraphs
        following_digraph = following_digraph_latin
        ambiguous = latin_ambiguous
        current_search_info = latin_search_info

    elif language == "armenian":
        digraphs = armenian_digraphs
        following_digraph = following_digraph_armenian
        ambiguous = armenian_ambiguous
        current_search_info = ""

    prepare_path()


def prepare_path():
    global path
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    if os.name == "nt":
        path = os.path.join(path, r"database\PhonemeSearch.db")
        
    else:
        path = os.path.join(path, r"database/PhonemeSearch.db")


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

C = ["β", "γ","δ", "ζ", "θ", "τ", "κ", "ρ", "ς", "σ", "π", "μ", "ν", "ψ", "χ", "φ", "ξ", "λ"]


def syllabificate(results):
    #print(results)
    syllable_lem = []
    numCount = 0
    for lemma in results:
        numCount += 1

        #print("Nummer: ", numCount)
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
            #print(index, char)
            #print(syllables)
            if char in V:
                #print("Vow")
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
                #print("Point")
                #print(syllables)
                point = False
                syllables += char + "."

            elif char in C:
                #print("Cons")
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


def download(pattern, user_pattern, language):
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

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    if os.name == "nt":
        path_os = "\\static\\download"
    else:
        path_os = "/static/download"

    mf.save(save_path=path + path_os, file_name="search_results", results=results, pattern=user_pattern)