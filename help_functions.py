import re
import os
import sys
import json
from base64 import b64encode
from icu import Locale, Collator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, transliterate
from functools import cmp_to_key


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

subst = {"α": "άᾶἀἁἂἃἇἆ", "η":  "ήῆἠἡἦἧἢἣ", "ι":  "ῖίἰἱἲἳἶἷ", "ο":  "όὀὁὂὃ", "υ": "ύῦὐὑὒὓὖὗ", "ω": "ώῶὠὡὢὣὦὧ"}

switch_html_start = """
<label for='reverse-check'>
    sort reverse
    <input id='reverse-check' class='alphabet-check' type='checkbox' name='reverse' value='1' onChange='this.form.submit();'>
</label>
<label for='descending-check'>
    sort descending
    <input id='descending-check' class='alphabet-check' type='checkbox' name='descending' value='1' onChange='this.form.submit();'>
</label>
"""

digraphs = {}
following_digraph = []
ambiguous = {}
path = ""


def get_language_info(language, accent):
    global digraphs
    global following_digraph
    global ambiguous
    global current_search_info

    greek_digraphs = {
                        "p": ["h", "s"],
                        "k": ["h","s"],
                        "t": ["h"],
                        "ο": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"],
                        "ό": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"],
                        "ὀ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"],
                        "ὁ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"],
                        "ὂ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"],
                        "ὃ": ["υ", "υ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"]
                    }

    following_digraph_greek = ["h", "s", "υ", "υ" "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ", "ύ"]

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

    if accent == "on":   
        greek_ambiguous = {
                            "σ": ["ς"],
                            "α": ["ἀ", "ἁ"],
                            "ο": ["ὀ", "ὁ"],
                            "ε": ["ἐ", "ἑ"],
                            "η": ["ἠ", "ἡ"],
                            "ι": ["ἰ", "ἱ"],
                            "ω": ["ὠ", "ὡ"],
                            "ου": ["οὐ","οὑ"],  
                            "υ": ["ὐ", "ὑ", "υ"],
                            "h": ["ἁ","ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]
                        }

        vedic_ambiguous = {}

        latin_ambiguous = {}

    else:
        greek_ambiguous = {
                            "σ": ["ς"],
                            "α": ["ά", "ά", "ᾶ", "ἀ", "ἁ", "ἂ","ἃ","ἇ","ἆ"],
                            "ο": ["ό", "ό", "ὀ", "ὁ", "ὂ", "ὃ"], 
                            "ε": ["έ", "ἐ", "ἑ", "ἒ", "ἓ"],
                            "η": ["ή", "ή", "ῆ", "ἠ", "ἡ", "ἦ", "ἧ", "ἢ", "ἣ"],
                            "ι": ["ῖ", "ί", "ί", "ἰ", "ἱ", "ἲ", "ἳ", "ἶ", "ἷ"],
                            "ω": ["ώ", "ώ", "ῶ", "ὠ", "ὡ", "ὢ", "ὣ", "ὦ", "ὧ"],
                            "ου": ["όυ","ού","οῦ","οὐ","οὑ","οὖ", "οὗ", "ού"],  # partly not yet in database, database transskript of 'hou'
                            "υ": ["ύ", "ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ"], 
                            "h": ["ἁ", "ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]
                            }  

        vedic_ambiguous = {
                            'a': ['á', 'à', 'ā'],
                            'e': ['é', 'è'],
                            'i': ['ì', 'í', 'ī'],
                            'o': ['ò'],
                            'u': ['ù', 'ú']
                            }
        
        latin_ambiguous = {}

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


def handle_digraphs(digraph, current_list, count) -> tuple[str, bool]:
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
    
    return url


# order functions

# alphabetical sorting

def convert_to_devanagari(results):
    
    deva_results = []
    change = {"è": "e", "á": "a", "à": "a", "é": "e", "ē": "e", "ō": "o", "í": "i", "ó": "o", "ú": "u", "ṛ": "r̥", "ṝ": "r̥̄", "l̥": "ḷ", "l̥̄":"ḹ", "ṁ": "ṃ"}
    for lemma in results:
        for char in change:
            change_to = change.get(char)
            lemma = re.sub(f"{char}", f"{change_to}", lemma)
        deva_results.append(transliterate(lemma, sanscript.IAST, sanscript.DEVANAGARI))
    
    return deva_results


def convert_to_roman(results):
    
    roman_results = []
    for lemma in results:
        roman_results.append(transliterate(lemma, sanscript.DEVANAGARI, sanscript.IAST))
    
    return roman_results


def reversing(to_reverse):
    reversed = [lemma[::-1] for lemma in to_reverse]
    return reversed


def sort_alphabetical(language, results, reverse_bool):
    if language == "1" or language == "greek":
        lang_code = "el"
    elif language == "2" or language == "vedic":
        # lang_code = "san"
        # results = convert_to_devanagari(results)
        results.sort(reverse=reverse_bool)
        return results
    elif language == "3" or language == "latin":
        # lang_code = ""
        results.sort(reverse=reverse_bool)
        return results

    loc = Locale(f'{lang_code}')
    col = Collator.createInstance(loc)
    results_sorted = sorted(results, key=cmp_to_key(col.compare), reverse=reverse_bool)
    
    if language == "2" or language == "vedic":
        results_sorted = convert_to_roman(results_sorted)

    return results_sorted


def sort_prepare(results, language, reverse_status, descending_status):
    print(reverse_status, descending_status)
    reverse_bool = False

    if reverse_status == "1":
        checked_reverse = "checked"
        results = reversing(results)
    else:
        checked_reverse = ""

    if descending_status == "1":
        checked_descending = "checked"
        reverse_bool = True
    else:
        checked_descending = ""

    switch_html = f"""
                <label for='reverse-check'>
                    sort reverse
                    <input id='reverse-check' class='alphabet-check' type='checkbox' name='reverse' value='1' onChange='this.form.submit();' {checked_reverse}>
                </label>
                <label for='descending-check'>
                    sort descending
                    <input id='descending-check' class='alphabet-check' type='checkbox' name='descending' value='1' onChange='this.form.submit();' {checked_descending}>
                </label>"""
        
    sorted_results = sort_alphabetical(language, results, reverse_bool)
    
    if reverse_status == "1":
        results = reversing(sorted_results)
    else:
        results = sorted_results
    
    return switch_html, results

    #elif sorting == "ascending":
     #   sort_alphabetical(language, results, reverse_bool=False)


# length sorting

def length_sorting(results, sorting):
    if sorting == "length-ascending":
        results.sort(key=len)
    
    elif sorting == "length-descending":
        results.sort(key=len, reverse=True)

    return results
