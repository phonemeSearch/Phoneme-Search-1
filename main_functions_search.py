import sqlite3
from sqlite3.dbapi2 import connect
import help_functions as hf
import os
import sys


# language specific information
language = ""
consonants = []
vowels = []
path_main = ""
user_pattern = ""


def sql_fetch_entries(command) -> list:
    connection = sqlite3.connect(path_main)
    cursor = connection.cursor()
    cursor.execute(command)
    entries = cursor.fetchall()
    connection.close()
    return entries


# prepares check list
def prepare_language_characteristics(language_index, accent) -> list:
    global path_main
    global language

    language_list = ["greek", "vedic", "latin", "armenian"]
    language = language_list[language_index - 1]

    hf.get_language_info(language, accent)
    path_main = os.path.dirname(os.path.abspath(sys.argv[0]))
    path_main = os.path.join(path_main, "database", "PhonemeSearch.db")
    
    allowed = ["(", ")", "+"]
    if language == "armenian":
        allowed.extend("`")

    for kind in ["vowel", "consonant"]:
        kind_entries = sql_fetch_entries(command=f"SELECT grapheme FROM {language}_{kind}")
        if kind == "vowel":
            vowels.extend([grapheme[0] for grapheme in kind_entries])
        elif kind == "consonant":
            consonants.extend([grapheme[0] for grapheme in kind_entries])

    key_entries = sql_fetch_entries(command=f"SELECT key FROM search_key_{language}")
    allowed.extend([key[0] for key in key_entries])
    allowed.extend(vowels + consonants)
    
    return allowed

# checks if user string is a valid input
# returns False if there are syntax related problems
# returns True if there are no syntax related problems
def check_validity(search_string, allowed) -> bool:
    # check whether user str contains not allowed chars
    # check if there are probably misspelled blanks
    global user_pattern

    user_pattern = search_string
    false_input = []
    aspirated_greek = ["k", "p", "t"] # characters which can be followed by 'h' in Greek
    aspirated_armenian = ["k", "p", "t", "c", "č"] # characters which can be followed by '`' in Armenian
    allowed_aspirated = []
    index = -1

    for char in search_string:
        index += 1

        if language == "greek":
            if char == "h":
                allowed_aspirated = aspirated_greek
                if search_string[index - 1] not in allowed_aspirated and index != 0:
                    false_input.append("h")

        elif language == "latin":
            if char in [char for char in allowed if char != "u"]:
                if search_string[index - 1] == "q": 
                    false_input.append("q")

        elif language == "armenian":
            if char == "`":
                allowed_aspirated = aspirated_armenian
                if search_string[index - 1] not in allowed_aspirated:
                    false_input.append("`")

        if char not in allowed:
            false_input.append(char)

        elif char == "|":
            if (search_string.index(char) == 0) or (search_string.index(char) == len(search_string)-1):
                pass
            else:
                false_input.append(char)
                print("|")
                
    if len(false_input) > 0:
        print(false_input)
        return False
    else:
        return True


def convert_string_to_list(search) -> list:
    group = ""
    grouped_list = []
    grouped = False
    for char in search:
        if char == "(":
            grouped = True
        elif char == ")":
            grouped = False
        else:
            group += char
        if grouped is False:
            grouped_list.append(group)
            group = ""
    grouped_list.append("fill")
    return grouped_list


def connect_phoneme_groups(grouped_list) -> list:
    connect_list = []
    group_entry = ""
    index_count = -1
    is_digraph = False

    for group in grouped_list:
        index_count += 1
        if group == "fill":
            pass
        elif group == "+":
            group_entry += "+"
        elif is_digraph is True:
            is_digraph = False
        elif group == "*":
            connect_list.append(group)
        elif group == "|":
            connect_list.append(group)
        else:
            group_entry += group
            if grouped_list[index_count + 1] != "+":
                if group in hf.digraphs:
                    digraph_return = \
                        hf.handle_digraphs(digraph=group, current_list=grouped_list, count=index_count)
                    group_entry = digraph_return[0]
                    is_digraph = digraph_return[1]
                connect_list.append(group_entry)
                group_entry = ""
    return connect_list


def convert_to_non_latin_alphabet(search) -> list:
    outer_group = []
    for grapheme in search:
        inner_group = []
        for latin_graph in grapheme:
            if latin_graph in ["^", "(\\w*?)", "$", "h"]:
                inner_group.append(latin_graph)
                continue

            translit_sql_cmd = \
                f"SELECT grapheme_{language} FROM {language}_consonant WHERE grapheme = '{latin_graph}'"

            graph = sql_fetch_entries(command=translit_sql_cmd)
            if len(graph) == 0:
                translit_sql_cmd = \
                    f"SELECT grapheme_{language} FROM {language}_vowel WHERE grapheme = '{latin_graph}'"
                graph = sql_fetch_entries(command=translit_sql_cmd)
            graph = graph[0]
            inner_group.append(graph[0])
        outer_group.append(inner_group)
    search = outer_group
    return search


# as long as plus_true is True or cluster key is given sql-cmd is built
# captures list index out of range error to examine end of list
# if plus_true is False and there's no key or end of list sql-cmd is executed
def cluster_key_cmd(char):
    if char == "+":
        cmd_part = " AND "
        #return cmd_part

    else:
        select_value_kind_cmd = f"SELECT value, kind FROM search_key_{language} " \
                                f"WHERE key = '{char}'"
        
        value_kind = sql_fetch_entries(command=select_value_kind_cmd)
        print(value_kind)
        value_kind = value_kind[0]
        
        current_value = value_kind[0]
        current_kind = value_kind[1]
        cmd_part = f"{current_kind} = '{current_value}'"
        print(cmd_part)

        #select_phonemes_cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
    return cmd_part


def convert_key_to_grapheme(connected) -> list:
    search = []
    group = []
    cluster = False
    cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
    is_digraph = False
    connected_index = -1
    for phoneme in connected:
        print(cmd)
        connected_index += 1
        phoneme_index = -1
        length = len(phoneme) - 1
        for char in phoneme:
            phoneme_index += 1
            if char in ["|", "V", "C", "h", "`"] or char in consonants or char in vowels:
                if cluster is True:
                    phoneme_cluster = sql_fetch_entries(cmd)
                    for phoneme in phoneme_cluster:
                        group.append(phoneme[0])
                    cluster = False
                    cmd = f"SELECT grapheme FROM {language}_consonant WHERE "

                if is_digraph is True:
                    is_digraph = False
                elif char in consonants or char in vowels:
                    if phoneme_index == length:
                        pass
                    elif char in hf.digraphs:
                        digraph_return = \
                            hf.handle_digraphs(digraph=char, current_list=phoneme, count=phoneme_index)
                        char = digraph_return[0]
                        is_digraph = digraph_return[1]  #bool
                    group.append(char)
                
                # special characters
                elif char == "h":
                    group.append(char)
                elif char == "V":
                    for vow in vowels:
                        group.append(vow)
                elif char == "C":
                    for con in consonants:
                        group.append(con)
                elif char == "*":
                    group.append("(\\w*?)")
                elif char == "|":
                    if connected_index == 0:
                        group.append("^")
                    else:
                        group.append("$")
            else:
                print(char)  
                cmd += cluster_key_cmd(char)
                cluster = True      
        
        if cluster is True:
            phoneme_cluster = sql_fetch_entries(cmd)
            for phoneme in phoneme_cluster:
                group.append(phoneme[0])
            print(phoneme_cluster)
            cluster = False
            cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
        group = list(set(group))
        group = hf.digraphs_to_begin(group)
        search.append(group)
        group = []

    if language in ["greek", "armenian"]:
        search = convert_to_non_latin_alphabet(search=search)
    return search


# uses regex
def build_regex(grapheme_string) -> str:
    pattern = ""
    # iterate over list with grapheme groups single and multi
    for grapheme in grapheme_string:
        # pick regex escape characters
        if "\\" in grapheme:
            pattern += grapheme
        
        # handling of multigraphemes (in groups)
        else: #len grapheme > 1
            index = 0
            pattern += "("

            # iterate over grapheme
            index = -1
            for char in grapheme:
                index += 1

                pattern_part = char

                if char[0] in hf.ambiguous:
                    pattern_part = hf.handle_ambiguous_phonemes(ambiguous_char=char)
                    pattern_part = f"({pattern_part})"

                if char[0] in hf.digraphs:
                  
                    try:
                        char[1]
                    except IndexError:
                        pattern_part += f"(?![{hf.join_digraph(char)}])"
                        
                
                # checks if char can be part of digraph to construct lookahead 
                elif char in hf.following_digraph:
                    before = hf.follows_digraph(follow_char=char)
                    pattern_part = f"(?<![{before}])" + char
                    
                pattern += pattern_part
                pattern_part = ""
                if index + 1 < len(grapheme):
                    pattern += "|"

            pattern += ")"
        
    return pattern


# sql regex search
def phoneme_search(pattern, order_id, asc_desc, limit, offset):
    global user_pattern
    
    selection = "lemma"
    extract = "lemma"
    # sql access
    if language in ["armenian", "vedic", "greek"]:
        selection = "lemma, transliteration"
    if language in ["vedic"]:
        extract = "transliteration"
         
    search_command = \
    f"SELECT {selection} FROM {language} WHERE {extract} REGEXP '{pattern}' " \
    f"ORDER BY {order_id} {asc_desc} " \
    f"LIMIT {limit} OFFSET {offset}"

    connection = sqlite3.connect(path_main)
    cursor = connection.cursor()
    connection.create_function("REGEXP", 2, hf.regexp)

    cursor.execute(search_command)
    results = cursor.fetchall()
    
    connection.close()

    if language in ["armenian", "greek"]:
        results = [(result[0], result[1]) for result in results]
    elif language in ["vedic"]:
        results = [(result[1], result[0]) for result in results]
    else:
        results = [(result[0], "") for result in results]
    print(results)
    return results, user_pattern, pattern


def connect_search_related_fcts(search_string, order_id, asc_desc, limit, offset):
    in_list = (convert_string_to_list(search=search_string))
    connected_list = connect_phoneme_groups(in_list)
    grapheme_list = convert_key_to_grapheme(connected=connected_list)
    regex_pattern = build_regex(grapheme_list)
    results = phoneme_search(regex_pattern, order_id, asc_desc, limit, offset)
    return results  # tuple(results, user_pattern, pattern, number)
