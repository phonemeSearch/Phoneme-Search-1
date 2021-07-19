from flask import Flask, render_template, request
import main_functions_search as mf
import help_functions as hf
import re
import os
import sqlite3
from math import ceil


app = Flask(__name__)

limit = 25
offset = 0
order_id = "id"
asc_desc = "ASC"
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
    global limit
    global offset
    global results
    global language

    marked_list = []
    for index in range(len(results)):
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

        marked = re.sub("%", "</span>", marked)
        marked = re.sub("§", "<span class='pattern'>", marked)
        marked = f"<span class='lemma'>{marked}</span>"

        url = hf.built_url_to_dictionaries(language, results, index)

        marked = f"<a class='external-link' href='{url}'>{marked}<i class='fa fa-external-link'></i></a>"
        marked = f"<div class='result'>{marked}</div>"
        marked_list.append(marked)
    return marked_list


# uses mf to get search results
def submit_start (user_search, accent_sensitive):
    global limit
    global offset
    global pattern
    global user_pattern
    global num
    global results
    global language

    user_allowed = mf.prepare_language_characteristics(language_index=int(language), accent=accent_sensitive)
    check = mf.check_validity(search_string=user_search, allowed=user_allowed)
    if check:
        user_results = mf.connect_search_related_fcts(search_string=user_search)
        results = user_results[0]
        user_pattern = user_results[1]
        pattern = user_results[2]
        
        if os.name == "nt":
            conn = sqlite3.connect("database\\PhonemeSearch.db")
        else:
            conn = sqlite3.connect("database/PhonemeSearch.db")
        
        if language == "1":
            lang = "greek"
        elif language == "2":
            lang = "vedic"
        elif language == "3":
            lang = "latin"

        cur = conn.cursor()
        conn.create_function("REGEXP", 2, hf.regexp)
        count_command = \
        f"SELECT COUNT(*) FROM {lang} WHERE lemma REGEXP '{pattern}'"
        print(count_command)
        cur.execute(count_command)
        number = cur.fetchall()
        for num in number:
            number = num[0]
        print(number)
        num = number

        syllables = hf.syllabificate(results)
        marked_results = mark_pattern(pattern=pattern)
        first_results = marked_results
        first_results = (first_results, syllables)
        return first_results
    else:
        return "an unexpected error occurred"


# gets the next search results if click on next button
def submit_next (direction):
    global limit
    global offset
    global order_id
    global asc_desc
    global page_num
    global user_num
    global num
    global pattern
    global user_pattern
    global results

    if direction == "last":
        if page_num == 1:
            pass
        else:
            page_num -= 1
            offset -= user_num
    elif direction == "next":
        if page_num == ceil(num / user_num):
            pass
        else:
            page_num += 1
            offset += user_num
    
    results = mf.phoneme_search(pattern, order_id, asc_desc, limit, offset)[0]
    syllables = hf.syllabificate(results)
    next_results = mark_pattern(pattern=pattern)
    next_results = (next_results, syllables)

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
    global limit
    global offset
    global order_id
    global asc_desc
    global next_results
    global first_results
    global language
    global results
    global switch_html
    global pattern

    submit = ""
    if request.method == 'POST':
        submit = request.form.get("submit-button")
        download_status = ""
        if submit == "start":
            page_num = 1
            # get search data
            user_search = request.form['search-input']
            language = request.form['choose-language']
            accent_sensitive = request.form.get('accent-sensitive')
            
            first_results = submit_start(user_search=user_search, accent_sensitive=accent_sensitive)

            return render_template('result.html', results=first_results, user_pattern=user_pattern, num=num, language=language,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
                                    switch_html=switch_html, download=download_status)

        elif submit == "next" or submit == "last":
            next_results = submit_next(direction=submit)
            submit = ""

            return render_template('result.html', results=next_results, user_pattern=user_pattern, num=num, language=language,
                                    page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
                                    switch_html=switch_html, download=download_status)

    elif request.method == 'GET':
        reversed = request.args.get("reverse")
        descending = request.args.get("descending")
        length = request.args.get("length-button")
        download = request.args.get("download")
        download_status = ""
        
        if download == "download-results":
            hf.download(pattern, user_pattern)
            reversed_results = (mark_pattern(pattern), hf.syllabificate(results))
            print(reversed_results)
            download_status = "<input id='download-status' type='checkbox' value='download' checked>"

        else:
            offset = 0
            if length in ["length-ascending", "length-descending"]:
                print("in length")

                switch_html = hf.switch_html_start
                order_id = "id_length"
                if length == "length-ascending":
                    asc_desc = "ASC"
                elif length == "length-descending":
                    asc_desc = "DESC"
                results = mf.phoneme_search(pattern, order_id, asc_desc, 25, offset)

            else:

                switch_html = hf.change_switch_status(reversed, descending)

                if reversed == "1":
                    order_id = "id_reverse"
                else:
                    order_id = "id"
                if descending == "1":
                    asc_desc = "DESC"
                else:
                    asc_desc = "ASC"

                results = mf.phoneme_search(pattern, order_id, asc_desc, 25, offset)

            page_num = 1
            reversed_results = submit_next(direction="last")
        return render_template('result.html', results=reversed_results, user_pattern=user_pattern, num=num, language=language,
                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
                                reverse="true", switch_html=switch_html, download=download_status)


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True)