from flask import Flask, render_template, request
import main_functions_search as mf
import help_functions as hf
import re
import os
import sqlite3
from math import ceil


app = Flask(__name__)

#limit = 25
#offset = 0
#order_id = "id"
#asc_desc = "ASC"
#num = 0
user_num = 25
#page_num = 0
#pattern = ""
#user_pattern = ""
#results = []
#first_results = []
#next_results = []
#language = ""

# wraps searched pattern of lemmas in span elements to mark them with css
# calls 
def mark_pattern (pattern, results, language):
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
def submit_start (user_search, accent_sensitive, language, order_id, asc_desc, limit, offset):
    user_allowed = mf.prepare_language_characteristics(language_index=int(language), accent=accent_sensitive)
    check = mf.check_validity(search_string=user_search, allowed=user_allowed)

    if check:
        user_results = mf.connect_search_related_fcts(search_string=user_search, order_id=order_id, asc_desc=asc_desc, limit=limit, offset=offset)
        results = user_results[0]
        #user_pattern = user_results[1]
        pattern = user_results[2]
        
        if os.name == "nt":
            #todo path join
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
        cur.execute(count_command)
        number = cur.fetchall()
        for num in number:
            number = num[0]

        syllables = hf.syllabificate(results)
        marked_results = mark_pattern(pattern=pattern, language=language, results=results)
        results = marked_results
        results_tup = (results, syllables, number)
        return results_tup
    else:
        return "an unexpected error occurred"


# gets the next search results if click on next button
#def submit_next (direction):
#    global limit
#    global offset
#    global order_id
#    global asc_desc
#    global page_num
#    global user_num
#    global num
#    global pattern
#    global user_pattern
#    global results
#
#    if direction == "last":
#        if page_num == 1:
#            pass
#        else:
#            page_num -= 1
#            offset -= user_num
#    elif direction == "next":
#        if page_num == ceil(num / user_num):
#            pass
#        else:
#            page_num += 1
#            offset += user_num
#    
#    results = mf.phoneme_search(pattern, order_id, asc_desc, limit, offset)[0]
#    syllables = hf.syllabificate(results)
#    next_results = mark_pattern(pattern=pattern)
#    next_results = (next_results, syllables)
#
#    return next_results


@app.route('/')
def route_page():
    return render_template('welcome.html')


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/search/description')
def description():
    return render_template('description.html')


@app.route('/search_result', methods=['GET'])
def result_page():
    submit = request.args.get("submit-button")
    page_num = int(request.args.get("page-num")) if request.args.get("page-num") is not None else 0
    page = request.args.get("page") if request.args.get("page") is not None else 0
    download_status = ""
    order_id = ""

    print("page", page)

    # get search data
    user_search = request.args.get("search-input")
    language = request.args.get("choose-language")
    accent_sensitive = request.args.get("accent-sensitive")
    offset = int(request.args.get("offset")) if request.args.get("offset") is not None else 0

    asc_desc = "ASC"

    print("asc_desc_bool", asc_desc)
    print("offset", offset)
    reverse_checked = ""
    descending_checked = ""
    length_asc_checked = ""
    length_desc_checked = ""

    limit = 25

    print("submit", submit)

    if submit == "start":
        print("start")
        offset = 0
        page_num = 1
        order_id = "id"
        asc_desc = "ASC"

    elif page == "next" or page == "last":
        print("page", type(offset))
        if page == "last": 
            page_num -= 1
            offset -= 25
        elif page == "next":
            page_num += 1
            offset += 25
        asc_desc = "ASC"
        order_id = "id"

    reverse = request.args.get("reverse")
    descending = request.args.get("descending")
    length_asc = request.args.get("length-asc")
    length_desc = request.args.get("length-desc")

    if reverse == "true" or descending == "true":
        length_asc_checked = "disabled"
        length_desc_checked = "disabled"
        if reverse == "true":
            order_id = "id_reverse"
            reverse_checked = "checked"
        else: 
            order_id = "id"
            reverse_checked = ""

        if descending == "true":
            asc_desc = "DESC"
            descending_checked = "checked"
        else:
            asc_desc = "ASC"
            descending_checked = ""

    elif length_asc == "true" or length_desc == "true":
        reverse_checked = "disabled"
        descending_checked = "disabled"
        if length_asc == "true":
            length_desc_checked = "disabled"
            order_id = "id_length"
            asc_desc = "ASC"
            length_asc_checked = "checked"
            
        if length_desc == "true":
            length_asc_checked = "disabled"
            order_id = "id_length"
            asc_desc = "DESC"
            length_desc_checked = "checked"
    
    else:
        order_id = "id"
        asc_desc = "ASC"

    switch_html = \
    f"""
    <span>
        <label class="switch" for='reverse-check'>
            <input id='reverse-check' class='alphabet-check' type='checkbox' name='reverse' value='true' onChange='this.form.submit();' {reverse_checked}>
            <span class="slider"></span>
        </label>
        <span class="switch-label">sort reverse</span>
        </span>
    <span>
        <label class="switch" for='descending-check'>
            <input id='descending-check' class='alphabet-check' type='checkbox' name='descending' value='true' onChange='this.form.submit();' {descending_checked}>
            <span class="slider"></span>
        </label>
        <span class="switch-label">sort descending</span>
    </span>
    <h2>sort by word length</h2>
    <span>
        <label class="switch" for='length-asc'>
            <input id='length-asc' class='alphabet-check' type='checkbox' name='length-asc' value='true' onChange='this.form.submit();' {length_asc_checked}>
            <span class="slider"></span>
        </label>
        <span class="switch-label">ascending</span>
    </span>
    <span>
        <label class="switch" for='length-desc'>
            <input id='length-desc' class='alphabet-check' type='checkbox' name='length-desc' value='true' onChange='this.form.submit();' {length_desc_checked}>
            <span class="slider"></span>
        </label>
        <span class="switch-label">descending</span>
    </span>
    """

    print("offset2", offset)
    results = submit_start(user_search=user_search, accent_sensitive=accent_sensitive, language=language, order_id=order_id, asc_desc=asc_desc, limit=limit, offset=offset)
    print("pageNum", page_num)
    return render_template(
        'result.html',
        results=(results[0], results[1]),
        user_pattern=user_search,
        number=results[2],
        language=language,
        pages=f"<span id='pages'>{ceil(results[2]/25)}</span>",
        switch_html=switch_html,
        download=download_status,
        page_num=page_num,
        offset=offset,
        accent_sensitive=accent_sensitive
    )

    #elif submit == "next" or submit == "last":
    #    next_results = submit_next(direction=submit)
    #    submit = ""
#
    #    return render_template('result.html', results=next_results, user_pattern=user_pattern, num=num, language=language,
    #                            page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
    #                            switch_html=switch_html, download=download_status)
    #global page_num
    #global limit
    #global offset
    #global order_id
    #global asc_desc
    #global next_results
    #global first_results
    #global language
    #global results
    #global switch_html
    #global pattern

    #submit = ""
    #if request.method == 'POST':
    #    submit = request.form.get("submit-button")
    #    download_status = ""
    #    if submit == "start":
    #        page_num = 1
    #        # get search data
    #        user_search = request.form['search-input']
    #        language = request.form['choose-language']
    #        accent_sensitive = request.form.get('accent-sensitive')
    #        
    #        first_results = submit_start(user_search=user_search, accent_sensitive=accent_sensitive)
#
    #        return render_template('result.html', results=first_results, user_pattern=user_pattern, num=num, language=language,
    #                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
    #                                switch_html=switch_html, download=download_status)
#
    #    elif submit == "next" or submit == "last":
    #        next_results = submit_next(direction=submit)
    #        submit = ""
#
    #        return render_template('result.html', results=next_results, user_pattern=user_pattern, num=num, language=language,
    #                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
    #                                switch_html=switch_html, download=download_status)
#
    #elif request.method == 'GET':
    #    reversed = request.args.get("reverse")
    #    descending = request.args.get("descending")
    #    length = request.args.get("length-button")
    #    download = request.args.get("download")
    #    download_status = ""
    #    
    #    if download == "download-results":
    #        hf.download(pattern, user_pattern)
    #        reversed_results = (mark_pattern(pattern), hf.syllabificate(results))
    #        download_status = "<input id='download-status' type='checkbox' value='download' checked>"
#
    #    else:
    #        offset = 0
    #        if length in ["length-ascending", "length-descending"]:
#
    #            switch_html = hf.switch_html_start
    #            order_id = "id_length"
    #            if length == "length-ascending":
    #                asc_desc = "ASC"
    #            elif length == "length-descending":
    #                asc_desc = "DESC"
    #            results = mf.phoneme_search(pattern, order_id, asc_desc, 25, offset)
#
    #        else:
#
    #            switch_html = hf.change_switch_status(reversed, descending)
#
    #            if reversed == "1":
    #                order_id = "id_reverse"
    #            else:
    #                order_id = "id"
    #            if descending == "1":
    #                asc_desc = "DESC"
    #            else:
    #                asc_desc = "ASC"
#
    #            results = mf.phoneme_search(pattern, order_id, asc_desc, 25, offset)
#
    #        page_num = 1
    #        reversed_results = submit_next(direction="last")
    #    return render_template('result.html', results=reversed_results, user_pattern=user_pattern, num=num, language=language,
    #                            page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/user_num)}</span>",
    #                            reverse="true", switch_html=switch_html, download=download_status)
#

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True)
