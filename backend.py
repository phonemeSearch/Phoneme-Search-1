from flask import Flask, render_template, request
import main_functions_search as mf
import help_functions as hf
import re
import os
import sys
from math import ceil
import json
import base64


app = Flask(__name__)

begin = 0
end = 0
num = 0
page_num = 0
pattern = ""
user_pattern = ""
results = []
first_results = []
next_results = []
language = ""


# wraps searched pattern of lemmas in span elements to mark them with css
def mark_pattern (pattern):
    global begin
    global end
    global results
    global language

    print("marking ", pattern)

    marked_list = []
    for index in range(begin, end):
        if index >= len(results):
            break
        matches = re.finditer(pattern, results[index])
        marked = results[index]
        for match in matches:
            print("match", match.group(0))
            group = match.group(0)

            if group in hf.following_digraph:
                before = hf.follows_digraph(group)
                marked = re.sub(f"(?<![{before}]){group}(?!\w?%)", f"§{group}%", marked, 1)
            else:
                marked = re.sub(f"{group}(?!\w?%)", f"§{group}%", marked, 1)
        
        marked = re.sub("%", "</span>", marked)
        marked = re.sub("§", "<span class='pattern'>", marked)
        marked = f"<span class='lemma'>{marked}</span>"

        if language == "1":
            #url = f"https://lsj.gr/wiki/{results[index]}"
            url = f"https://logeion.uchicago.edu/{results[index]}"
        elif language == "2":
            lemma = results[index]

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
            encoded_jsn = base64.b64encode(bytes_json)
            str_code = encoded_jsn.decode("utf-8")
            url = f"https://vedaweb.uni-koeln.de/rigveda/results/{str_code}"

        marked = f"<a class='lsj-link' href='{url}'>{marked}<i class='fa fa-external-link'></i></a>"
        marked = f"<div class=result>{marked}</div>"
        marked_list.append(marked)
    return marked_list


# uses mf to get search results
def submit_start (user_search, accent_sensitive):
    global begin
    global end
    global pattern
    global user_pattern
    global num
    global results
    global language
    
    begin = 0
    end = 25
    user_allowed = mf.prepare_language_characteristics(language_index=int(language), accent=accent_sensitive)
    check = mf.check_validity(search_string=user_search, allowed=user_allowed)
    if check:
        user_results = mf.connect_search_related_fcts(search_string=user_search)
        results = user_results[0]
        pattern = user_results[2]
        user_pattern = user_results[1]
        num = len(user_results[0])

        marked_results = mark_pattern(pattern=pattern)
        first_results = [marked_results[index] for index in range(begin, end) if index < len(marked_results)]
        return first_results
    else:
        return "an unexpected error occurred"


# gets the next search results if click on next button
def submit_next (direction):
    global begin
    global end
    global page_num
    global num
    global pattern
    global user_pattern

    if direction == "last":
        if page_num == 1:
            pass
        else:
            page_num -= 1
            begin -= 25
            end -= 25
    elif direction == "next":
        if page_num == ceil(num / 25):
            pass
        else:
            page_num += 1
            begin += 25
            end += 25
    next_results = mark_pattern(pattern=pattern)

    return next_results


@app.route('/')
def route_page():
    return render_template('welcome.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('search.html')


@app.route('/search/description')
def description():
    return render_template('description.html')


@app.route('/search_result', methods=['POST', 'GET'])
def result_page():
    global page_num
    global begin
    global end
    global next_results
    global first_results
    global language
    global results

    submit = ""
    if request.method == 'POST':
        submit = request.form.get("submit-button")
        #submit = request.args.get("submit-button")
        print(submit)
        if submit == "start":
            page_num = 1
            user_search = request.form['search-input']
            language = request.form['choose-language']
            accent_sensitive = request.form.get('accent-sensitive')
            first_results = submit_start(user_search=user_search, accent_sensitive=accent_sensitive)
            
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
            if os.name == "nt":
                path_os = "\\static\\download"
            else:
                path_os = "/static/download"

            mf.save(save_path=path + path_os, file_name="search_results", results=results, pattern=user_pattern)
            
            return render_template('result.html', results=first_results, user_pattern=user_pattern, num=num,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/25)}</span>")

        elif submit == "next" or submit == "last":
            next_results = submit_next(direction=submit)
            submit = ""
            return render_template('result.html', results=next_results, user_pattern=user_pattern, num=num,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/25)}</span>")

    elif request.method == 'GET':
        reverse_button = request.args.get("reverse-button")
        descending_button = request.args.get("descending-button")
        length_button = request.args.get("length-button")
        if reverse_button == "reverse":
            results = hf.sort_reverse(results = results)
        elif reverse_button == "alphabetical":
            results = hf.sort_alphabetical(results = results)
        if descending_button == "descending":
            hf.sort_descending(results)
        elif descending_button == "ascending":
            hf.sort_ascending(results)
        elif length_button == "length-ascending":
            hf.sort_length_ascending(results)
        elif length_button == "length-descending":
            hf.sort_length_descending(results)

        page_num = 1
        begin = 0
        end = 25
        reversed_results = submit_next(direction="last")
        return render_template('result.html', results=reversed_results, user_pattern=user_pattern, num=num,
                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/25)}</span>",
                                reverse="true")

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True)