import help_functions as hf
import os
import sys
from flask import session


# language specific information
languages = ["greek", "vedic", "latin", "armenian"]
path_main = os.path.dirname(os.path.abspath(sys.argv[0]))
path_main = os.path.join(path_main, "database", "PhonemeSearch.db")


# checks if user string is a valid input
# returns False if there are syntax related problems
# returns True if there are no syntax related problems
def check_validity(language, user_pattern, allowed) -> bool:
    # check whether user str contains not allowed chars
    # check if there are probably misspelled blanks

    false_input = []
    aspirated_greek = ["k", "p", "t"] # characters which can be followed by 'h' in Greek
    aspirated_armenian = ["k", "p", "t", "c", "č"] # characters which can be followed by '`' in Armenian
    allowed_aspirated = []
    index = -1

    for char in user_pattern:
        index += 1
        print(language)
        if language == "greek":
            allowed_aspirated = aspirated_greek
            print(allowed_aspirated)
            if char == "h":
                if user_pattern[index - 1] not in allowed_aspirated and index != 0:
                    false_input.append("h")

        elif language == "latin":
            if char in [char for char in allowed if char != "u"]:
                if user_pattern[index - 1] == "q": 
                    false_input.append("q")

        elif language == "armenian":
            if char == "`":
                allowed_aspirated = aspirated_armenian
                if user_pattern[index - 1] not in allowed_aspirated:
                    false_input.append("`")

        if char not in allowed:
            false_input.append(char)

        elif char == "|":
            if (user_pattern.index(char) == 0) or (user_pattern.index(char) == len(user_pattern)-1):
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


def connect_phoneme_groups(language, accent, grouped_list) -> list:
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
                if group in hf.get_digraphs(language)[0]:
                    digraph_return = \
                        hf.handle_digraphs(digraph=group, current_list=grouped_list, count=index_count)
                    group_entry = digraph_return[0]
                    is_digraph = digraph_return[1]
                connect_list.append(group_entry)
                group_entry = ""
    return connect_list


def convert_to_non_latin_alphabet(language, search) -> list:
    outer_group = []
    for grapheme in search:
        inner_group = []
        for latin_graph in grapheme:
            if latin_graph in ["^", "(\\w*?)", "$", "h"]:
                inner_group.append(latin_graph)
                continue

            translit_sql_cmd = \
                f"SELECT grapheme_{language} FROM {language}_consonant WHERE grapheme = '{latin_graph}'"

            graph = hf.sql_fetch_entries(translit_sql_cmd, path_main, False)
            if len(graph) == 0:
                translit_sql_cmd = \
                    f"SELECT grapheme_{language} FROM {language}_vowel WHERE grapheme = '{latin_graph}'"
                graph = hf.sql_fetch_entries(translit_sql_cmd, path_main, False)
            graph = graph[0]
            inner_group.append(graph[0])
        outer_group.append(inner_group)
    search = outer_group
    return search


# as long as plus_true is True or cluster key is given sql-cmd is built
# captures list index out of range error to examine end of list
# if plus_true is False and there's no key or end of list sql-cmd is executed
def cluster_key_cmd(language, char):
    if char == "+":
        cmd_part = " AND "
        #return cmd_part

    else:
        select_value_kind_cmd = f"SELECT value, kind FROM search_key_{language} " \
                                f"WHERE key = '{char}'"
        
        value_kind = hf.sql_fetch_entries(select_value_kind_cmd, path_main, False)
        value_kind = value_kind[0]
        
        current_value = value_kind[0]
        current_kind = value_kind[1]
        cmd_part = f"{current_kind} = '{current_value}'"

        #select_phonemes_cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
    return cmd_part


def add_cluster(group, cmd):
    phoneme_cluster = hf.sql_fetch_entries(cmd, path_main, False)
    for phoneme in phoneme_cluster:
        group.append(phoneme[0])
    return group

def convert_key_to_grapheme(language, connected) -> list:
    search = []
    group = []
    con_vow = hf.get_allowed_con_vow(language)
    consonants = con_vow[1]
    vowels = con_vow[2]
    cluster_end = False
    cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
    is_digraph = False
    connected_index = -1

    for phoneme in connected:
        connected_index += 1
        phoneme_index = -1
        length = len(phoneme) - 1
        for char in phoneme:
            phoneme_index += 1
            if cluster_end:
                cmd = f"SELECT grapheme FROM {language}_consonant WHERE "

            if is_digraph is True:
                is_digraph = False
            elif char in consonants or char in vowels:
                if phoneme_index == length:
                    pass
                elif char in hf.get_digraphs(language)[0]:
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
                cmd += cluster_key_cmd(language, char)
                try:
                    if phoneme[phoneme_index + 1] != "+" and char != "+":
                        group = add_cluster(group, cmd)
                        cluster_end = True
                except IndexError:
                        group = add_cluster(group, cmd)
                        cluster_end = True
                
        group = list(set(group))
        group = hf.digraphs_to_begin(group)
        search.append(group)
        group = []

    if language in ["greek", "armenian"]:
        search = convert_to_non_latin_alphabet(language, search)
    return search


# uses regex
def build_regex(language, accent, grapheme_string) -> str:
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

                if char[0] in hf.get_ambiguous(language):
                    pattern_part = hf.handle_ambiguous_phonemes(ambiguous_char=char)
                    pattern_part = f"({pattern_part})"

                if char[0] in hf.get_digraphs(language)[0]:
                  
                    try:
                        char[1]
                    except IndexError:
                        pattern_part += f"(?![{hf.join_digraph(char)}])"
                        
                
                # checks if char can be part of digraph to construct lookahead 
                elif char in hf.get_digraphs(language)[1]:
                    before = hf.follows_digraph(follow_char=char)
                    pattern_part = f"(?<![{before}])" + char
                    
                pattern += pattern_part
                pattern_part = ""
                if index + 1 < len(grapheme):
                    pattern += "|"

            pattern += ")"
        
    return pattern


# sql regex search
def phoneme_search(language, pattern, user_pattern, order_id, asc_desc, limit, offset):
    
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

    results = hf.sql_fetch_entries(search_command, path_main, True)

    if language in ["armenian", "greek"]:
        results = [(result[0], result[1]) for result in results]
    elif language in ["vedic"]:
        results = [(result[1], result[0]) for result in results]
    else:
        results = [(result[0], "") for result in results]
    
    return results, user_pattern, pattern


def get_pattern():
    language = session["language"]
    accent = session["accent_sensitive"]
    user_pattern = session["user_pattern"]
    
    converted = (convert_string_to_list(search=user_pattern))
    connected_list = connect_phoneme_groups(language, accent ,converted)
    grapheme_list = convert_key_to_grapheme(language, connected_list)
    regex_pattern = build_regex(language, accent, grapheme_list)
    return regex_pattern


def connect_search_related_fcts(language, accent, user_pattern, order_id, asc_desc, limit, offset):
    #language = session["language"]
    #accent = session["accent"]
    #user_pattern = session["user_pattern"]
    #order_id = session["order_id"]
    #limit = session["limit"]
    #offset = session["offset"]

    converted = (convert_string_to_list(search=user_pattern))
    connected_list = connect_phoneme_groups(language, accent ,converted)
    grapheme_list = convert_key_to_grapheme(language, connected_list)
    regex_pattern = build_regex(language, accent, grapheme_list)
    results = phoneme_search(language, regex_pattern, user_pattern, order_id, asc_desc, limit, offset)
    return results  # tuple(results, user_pattern, pattern, number)
