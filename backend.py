from flask import Flask, render_template, request
import main_functions_search as mf
import help_functions as hf
import re
import os
import sys
from math import ceil

import test

app = Flask(__name__)

begin = 0
end = 0
num = 0
user_num = 25
page_num = 0
pattern = ""
user_pattern = ""
results = []
first_results = []
next_results = []
language = ""
switch_html = hf.switch_html_start


# wraps searched pattern of lemmas in span elements to mark them with css
# calls 
def mark_pattern (pattern):
    global begin
    global end
    global results
    global language

    marked_list = []
    for index in range(begin, end):
        if index >= len(results):
            break
        matches = re.finditer(pattern, results[index])
        marked = results[index]
        for match in matches:

            group = match.group(0)
            if group in hf.digraphs:
                after = hf.join_digraph(group)
                mark_re = f"(?<!§){group}(?!({'|'.join(after)}))"
            elif group in hf.following_digraph:
                before = hf.follows_digraph(group)
                mark_re = f"(?<![{before}]){group}(?!\w?%)"
            else:
                mark_re = f"{group}(?!\w?%)"

            marked = re.sub(mark_re, f"§{group}%", marked, 1)
        
        print(marked)
        marked = re.sub("%", "</span>", marked)
        marked = re.sub("§", "<span class='pattern'>", marked)
        marked = f"<span class='lemma'>{marked}</span>"

        url = hf.built_url_to_dictionaries(language, results, index)

        marked = f"<a class='external-link' href='{url}'>{marked}<i class='fa fa-external-link'></i></a>"
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
    end = user_num
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
            begin -= user_num
            end -= user_num
    elif direction == "next":
        if page_num == ceil(num / user_num):
            pass
        else:
            page_num += 1
            begin += user_num
            end += user_num
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
    global switch_html

    submit = ""
    if request.method == 'POST':
        submit = request.form.get("submit-button")

        if submit == "start":
            page_num = 1
            #user_result_num = 25
            # get search data
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
            
            #results = test.translit(res=results)

            return render_template('result.html', results=first_results, user_pattern=user_pattern, num=num,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>", switch_html=switch_html)

        elif submit == "next" or submit == "last":
            next_results = submit_next(direction=submit)
            submit = ""

            return render_template('result.html', results=next_results, user_pattern=user_pattern, num=num,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>", switch_html=switch_html)

    elif request.method == 'GET':
        reversed = request.args.get("reverse")
        descending = request.args.get("descending")
        length = request.args.get("length-button")

        if length in ["length-ascending", "length-descending"]:
            print("in length")
            switch_html = hf.switch_html_start
            results = hf.length_sorting(results, length)

        else:
            res_html_tup = hf.sort_prepare(results, language, reversed, descending)
            results = res_html_tup[1]
            switch_html = res_html_tup[0]
        
        page_num = 1
        begin = 0
        end = user_num
        reversed_results = submit_next(direction="last")
        return render_template('result.html', results=reversed_results, user_pattern=user_pattern, num=num,
                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
                                reverse="true", switch_html=switch_html)


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True)