import sqlite3
from sqlite3.dbapi2 import connect
import help_functions as hf
import os
import sys
import re


# language specific information
language = ""
consonants = []
vowels = []
path_main = ""


# prepares check list for
def prepare_language_characteristics(language_index, accent) -> list:
    global path_main
    global language

    language_list = ["greek", "vedic"]
    language = language_list[language_index - 1]

    hf.get_language_info(language, accent)
    path_main = os.path.dirname(os.path.abspath(sys.argv[0]))
    path_main = os.path.join(path_main, r"database\PhonemeSearch.db")

    allowed = ["(", ")", "+"]

    for kind in ["vowel", "consonant"]:
        kind_entries = hf.sql_fetch_entries(command=f"SELECT grapheme FROM {language}_{kind}")
        if kind == "vowel":
            vowels.extend([grapheme[0] for grapheme in kind_entries])
        elif kind == "consonant":
            consonants.extend([grapheme[0] for grapheme in kind_entries])

    key_entries = hf.sql_fetch_entries(command=f"SELECT key FROM search_key_{language}")
    allowed.extend([key[0] for key in key_entries])

    allowed.extend(vowels + consonants)
    return allowed


# checks if user string is a valid input
# returns False if there are syntax related problems
# returns True if there are no syntax related problems
def check_validity(search_string, allowed) -> bool:
    # check whether user str contains not allowed chars
    # check if there are probably misspelled blanks
    false_input = []
    aspirated_greek = ["k", "p", "t"] # characters which can be followed by 'h' in Greek
    allowed_aspirated = []
    index = -1
    for char in search_string:
        index += 1
        if char == "h":
            if language == "greek":
                allowed_aspirated = aspirated_greek
                if search_string[index - 1] not in allowed_aspirated:
                    false_input.append("No allowed usage of 'h'!")
        elif char not in allowed:
            false_input.append(char)
        elif char == "|":
            if (search_string.index(char) == 0) or (search_string.index(char) == len(search_string)-1):
                pass
            else:
                false_input.append(char)
                print("no allowed usage of '|'!")
    if len(false_input) > 0:
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
    # print("grouped_list: ", grouped_list)
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
    # print("connect_list: ", connect_list)
    return connect_list


def convert_to_non_latin_alphabet(search) -> list:
    outer_group = []
    print("search in convert non l:", search)
    for grapheme in search:
        inner_group = []
        for latin_graph in grapheme:
            if latin_graph in ["^", "(\\w*?)", "$"]:
                inner_group.append(latin_graph)
                continue

            translit_sql_cmd = \
                f"SELECT grapheme_{language} FROM {language}_consonant WHERE grapheme = '{latin_graph}'"

            graph = hf.sql_fetch_entries(command=translit_sql_cmd)
            if len(graph) == 0:
                translit_sql_cmd = \
                    f"SELECT grapheme_{language} FROM {language}_vowel WHERE grapheme = '{latin_graph}'"
                graph = hf.sql_fetch_entries(command=translit_sql_cmd)
                print("graph", graph)
            graph = graph[0]
            inner_group.append(graph[0])
        outer_group.append(inner_group)
    search = outer_group
    return search


# as long as plus_true is True or cluster key is given sql-cmd is built
# captures list index out of range error to examine end of list
# if plus_true is False and there's no key or end of list sql-cmd is executed
def cluster_key_cmd(char, index, phoneme) -> tuple:
    # set select phonemes command
    select_phonemes_cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
    
    if char == "+":
        select_phonemes_cmd += " AND "
    
    else:
        try:
            follow_char = phoneme[index + 1]
            if follow_char == "+":
                plus_true = True
            else:
                plus_true = False
        except IndexError:
            plus_true = False

        select_value_kind_cmd = f"SELECT value, kind FROM search_key_{language} " \
                                f"WHERE key = '{char}'"
        # unclear section, write more comprehensible
        value_kind = hf.sql_fetch_entries(command=select_value_kind_cmd)
        value_kind = value_kind[0]
        current_value = value_kind[0]
        current_kind = value_kind[1]
        select_phonemes_cmd += f"{current_kind} = '{current_value}'"

        if plus_true is False:
            print(select_phonemes_cmd)
            phonemes = hf.sql_fetch_entries(command=select_phonemes_cmd)
            select_phonemes_cmd = f"SELECT grapheme FROM {language}_consonant WHERE "
            
            return phonemes
        

def convert_key_to_grapheme(connected) -> list:
    search = []
    group = []
    is_digraph = False
    connected_index = -1
    for phoneme in connected:
        connected_index += 1
        phoneme_index = -1
        length = len(phoneme) - 1
        for char in phoneme:
            phoneme_index += 1
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
            else:
                if char == "V":
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
                    
                    phoneme_cluster = cluster_key_cmd(char, phoneme_index, phoneme)
                    if phoneme_cluster:
                        for phoneme in phoneme_cluster:
                            group.append(phoneme[0])
                    
        group = list(set(group))
        group = hf.digraphs_to_begin(group)
        search.append(group)
        group = []

    if language in ["greek"]:
        search = convert_to_non_latin_alphabet(search=search)
    return search


# uses regex
def build_regex(grapheme_string) -> str:
    print("amb", hf.ambiguous)
    pattern = ""
    # iterate over list with grapheme groups single and multi
    for grapheme in grapheme_string:
        # pick regex escape characters
        if "\\" in grapheme:
            pattern += grapheme
        
        # handling of multigraphemes
        elif len(grapheme) > 1:
            index = 0
            pattern += "("

            # iterate over grapheme
            for char in grapheme:
                index += 1

                if char in hf.ambiguous:
                    pattern += hf.handle_ambiguous_phonemes(ambiguous_char=char)

                elif char in hf.digraphs:
                    if index == len(grapheme):
                        pattern += char + f"(?![{hf.join_digraph(char)}])" 
                    elif grapheme[index] in hf.digraphs.get(char):
                        pass
                    else:
                        pattern += char + f"(?![{hf.join_digraph(char)}])"
                #elif char == "ου":
                 #   pattern += "ου|όυ|ού|οῦ"  # verallgemeinern
                else:
                    pattern += char
                if index < len(grapheme):
                    pattern += "|"

            pattern += ")"
        
        # handling of single graphemes
        else:
            if grapheme[0] in hf.ambiguous:
                amb_grapheme = "("
                amb_grapheme += hf.handle_ambiguous_phonemes(ambiguous_char=grapheme[0])
                amb_grapheme += ")"
                grapheme = amb_grapheme

            elif grapheme[0] in hf.digraphs:
                grapheme[0] += f"(?![{hf.join_digraph(grapheme[0])}])"
            
            # to specific, own category like non search language digraph
            elif grapheme[0] == "ου":
                grapheme = "(ου|όυ|ού)"

            pattern += "".join(grapheme)
    
    return pattern


# sql regex search
def phoneme_search(grapheme_list) -> tuple[list, str, str]:
    pattern = build_regex(grapheme_list)
    user_pattern = re.sub(r"(\\w\*\?)", "*", pattern)
    user_pattern = re.sub(r"\^", "|", user_pattern)
    user_pattern = re.sub(r"\$", "|", user_pattern)
    
    print("regex pattern:", pattern)
    
    # sql access
    search_command = f"SELECT lemma FROM {language} WHERE lemma REGEXP '{pattern}'"
    connection = sqlite3.connect(path_main)
    cursor = connection.cursor()
    print(search_command)
    connection.create_function("REGEXP", 2, hf.regexp)
    cursor.execute(search_command)
    results = cursor.fetchall()
    connection.close()

    results = [result[0] for result in results]
    print("res ", results[0:20])
    results.sort()

    return results, user_pattern, pattern


def save(save_path, file_name, results, pattern):
    file = open(save_path + f"\\{file_name}.txt", "w", encoding="utf-8")
    file.write("\nnumber of results: " + str(len(results)))
    file.write("\nsearch pattern: " + pattern + "\n\n")
    file.write("\n".join(results))
    file.close() 


def save_result(results, pattern) -> str:
    file_name = ""
    exists = True
    save_path = path_main.removesuffix("\\database\\PhonemeSearch.db")
    save_path = save_path + f"\\saved searches\\{language}"
    while exists:
        if os.path.exists(save_path) == False:
            print(save_path)
            os.makedirs(save_path)
            
        try:
            file_name = input("Please set a file name.\n""input: ")
            file_exists = open(save_path + f"\\{file_name}.txt", encoding="utf-8")
            overwrite = input("File already exists. Do you want to overwrite it?\n"
                                "1) yes\n"
                                "any key) no\n")
            if overwrite == "1":
                exists = False
            file_exists.close()
        except FileNotFoundError:
            exists = False

    save(save_path=save_path, file_name=file_name, results=results, pattern=pattern)
    return f"Search saved as {file_name}.txt."


def connect_search_related_fcts(search_string) -> tuple[list, str]:
    in_list = (convert_string_to_list(search=search_string))
    connected_list = connect_phoneme_groups(in_list)
    grapheme_list = convert_key_to_grapheme(connected=connected_list)
    results = phoneme_search(grapheme_list=grapheme_list)
    return results


# user gives search, decides whether to save it or not
# use of functions
# only used in local version
def main_menu():
    user_string = []
    user_input_check = False
    allowed = []
    while user_input_check is False:
        user_language = input("In which language would you like to search?"
                              "\n"
                              "1) Greek"
                              "\n"
                              "2) Vedic"
                              "\n"
                              "input: ")
        if user_language in ["1", "2"]:
            user_language = int(user_language)
            user_input_check = True
            allowed = prepare_language_characteristics(language_index=user_language, accent="off")
        else:
            print("\nFalse input. Please try again.\n")

    user_input_check = False
    false_input = ""
    while user_input_check is False:
        if false_input:
            print(false_input)
        print(hf.current_search_info)
        user_string = input("Look for input options and search key above."
                            "\n"
                            "input: ")
        check = check_validity(search_string=user_string, allowed=allowed)
        # calls check_validity function which checks user string
        # if check_validity returns None: not handled
        if check is True:
            user_input_check = True
        else:
            false_input = "\nWrong input. Please try again.\n"
            user_input_check = False

    res_pat = connect_search_related_fcts(search_string=user_string)
    print(res_pat[1], res_pat[2])
    #print("result: ", res_pat[0])
    print("number of lemmata found: ", len(res_pat[0]))
    save_input = input("Do you want to save your search in a txt-File?\n"
                       "1) yes\n"
                       "any key) no\n")
    if save_input == "1":
        save_result(results=res_pat[0], pattern=res_pat[1])


if __name__ == "__main__":
    new_search = True
    while new_search:
        main_menu()
        user_new_search = input("Another search?\n"
                                "1) yes\n"
                                "any key) no\n")
        if user_new_search == "1":
            new_search = True
        else:
            new_search = False