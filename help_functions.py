import re
import os
import sys
import json
from base64 import b64encode
from icu import Locale, Collator
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
current_search_info = ""

subst = {"α": "άᾶἀἁἂἃἇἆ", "η":  "ήῆἠἡἦἧἢἣ", "ι":  "ῖίἰἱἲἳἶἷ", "ο":  "όὀὁὂὃ", "υ": "ύῦὐὑὒὓὖὗ", "ω": "ώῶὠὡὢὣὦὧ"}

digraphs = {}
following_digraph = []
ambiguous = {}
path = ""


def get_language_info(language, accent):
    global digraphs
    global following_digraph
    global ambiguous
    global current_search_info

    greek_digraphs = {"p": ["h", "s"], "k": ["h","s"], "t": ["h"]}
    following_digraph_greek = ["h", "s"]

    vedic_digraphs = {"p": ["h"], "b": ["h"], "k": ["h"], "t": ["h"], "d": ["h"], "g": ["h"], "ṭ": ["h"],
                        "ḍ": ["h"], "c": ["h"]}
    following_digraph_vedic = ["h"]

    if accent == "on":   
        greek_ambiguous = {"σ": ["ς"], "α": ["ἀ", "ἁ"],
                            "ο": ["ὀ", "ὁ"], "ε": ["ἐ", "ἑ"],
                            "η": ["ἠ", "ἡ"],
                            "ι": ["ἰ", "ἱ",],
                           "ω": ["ὠ", "ὡ"],
                           "ου": ["οὐ","οὑ"],  
                           "υ": ["ὐ", "ὑ"],
                           "h":["ἁ","ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]}
        vedic_ambiguous = {}
    else:
        greek_ambiguous = {"σ": ["ς"], "α": ["ά", "ᾶ", "ἀ", "ἁ", "ἂ","ἃ","ἇ","ἆ"],
                            "ο": ["ό", "ὀ", "ὁ", "ὂ", "ὃ"], "ε": ["έ", "ἐ", "ἑ", "ἒ", "ἓ"],
                            "η": ["ή", "ῆ", "ἠ", "ἡ", "ἦ", "ἧ", "ἢ", "ἣ"],
                            "ι": ["ῖ", "ί", "ἰ", "ἱ", "ἲ", "ἳ", "ἶ", "ἷ"],
                           "ω": ["ώ", "ῶ", "ὠ", "ὡ", "ὢ", "ὣ", "ὦ", "ὧ"],
                           "ου": ["όυ","ού","οῦ","οὐ","οὑ","οὖ", "οὗ"],  # partly not yet in database, database transskript of 'hou'
                           "υ": ["ύ", "ῦ", "ὐ", "ὑ", "ὒ", "ὓ", "ὖ", "ὗ"], 
                           "h":["ἁ", "ἃ","ἇ", "ὁ", "ὃ", "ἑ", "ἓ", "ἡ", "ἧ", "ἣ", "ἱ", "ἳ", "ἷ", "ὡ", "ὣ", "ὧ", "οὑ", "οὗ"]}  

        vedic_ambiguous = {'a': ['á', 'à', 'ā'], 'e': ['é', 'è'], 'i': ['ì', 'í', 'ī'], 'o': ['ò'],
                            'u': ['ù', 'ú']}

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
    if language == "1":
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

def sort_key(x, y):
    global subst

    if x == y:
        return 0
    
    for key_subst in subst:
        
        to_subst = subst.get(key_subst)

        x = re.sub(f"[{to_subst}]", f"{subst}", x)
        y = re.sub(f"[{to_subst}]", f"{subst}", y) 

    return 1 if x > y else -1


def reversing(to_reverse):
    reversed = [lemma[::-1] for lemma in to_reverse]
    return reversed


def sort_alphabetical(language, results, reverse_bool):
    print(language)
    if language == "1":
        lang_code = "el"
    elif language == "2":
        lang_code = "san"
    else:
        lang_code = "el"

    loc = Locale(f'{lang_code}')
    col = Collator.createInstance(loc)
    results_sorted = sorted(results, key=cmp_to_key(col.compare), reverse=reverse_bool)
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

def length_sorting(sorting):

    if sorting == "length_ascending":
        pass
    
    elif sorting == "length_descending":
        pass

#def sort_reverse(results):
 #   reversed = [lemma[::-1] for lemma in results]
  #  reversed.sort()
   # results = [lemma[::-1] for lemma in reversed]
    #return results


#def sort_descending(results):
 #   results.sort(reverse=True)


#def sort_ascending(results):
 #   if language == ""
  #  loc = Locale('el')  # 'el' is the locale code for Greek
   # col = Collator.createInstance(loc)
    #results_sorted = sorted(results, key=cmp_to_key(col.compare))
    #return results_sorted

#def sort_length_ascending(results):
 #   results.sort(key=len)


#def sort_length_descending(results):
 #   results.sort(key=len, reverse=True)
