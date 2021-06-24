from flask import Flask, render_template, request
import main_files_search as mf
import re
import os
import sys
from math import ceil

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

def sort_reverse():
    global results
    reversed = [lemma[::-1] for lemma in results]
    reversed.sort()
    results = [lemma[::-1] for lemma in reversed]


def sort_alphabetical():
    global results
    alphabetical = [lemma for lemma in results]
    alphabetical.sort()
    results = [lemma for lemma in alphabetical]


def sort_descending():
    print("descending")
    global results
    results.sort(reverse=True)


def sort_ascending():
    global results
    results.sort()


def sort_length_ascending():
    global results
    results.sort(key=len)


def sort_length_descending():
    global results
    results.sort(key=len, reverse=True)


# wraps searched pattern of lemmas in span elements to mark them with css
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
            marked = re.sub(f"{group}(?!\w?%)", f"§{group}%", marked, 1)
        
        marked = re.sub("%", "</span>", marked)
        marked = re.sub("§", "<span class='pattern'>", marked)
        marked = f"<span class='lemma'>{marked}</span>"

        if language == "1":
            #get_link = f"https://lsj.gr/wiki/{results[index]}"
            get_link = f"https://logeion.uchicago.edu/{results[index]}"
            marked = f"<a class='lsj-link' href='{get_link}'>{marked}<i class='fa fa-external-link'></i></a>"
        elif language == "2":
            pass

        #marked = f"<a class='lsj-link' href='{get_link}'>{marked}<i class='fa fa-external-link'></i></a>"
        
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
    #print(next_results)
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

    submit = ""
    if request.method == 'POST':
        submit = request.form.get("submit-button")
        print(submit)
        if submit == "start":
            page_num = 1
            user_search = request.form['search-input']
            language = request.form['choose-language']
            accent_sensitive = request.form.get('accent-sensitive')
            first_results = submit_start(user_search=user_search, accent_sensitive=accent_sensitive)
            
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
            mf.save(save_path=path + "\\static\\download\\", file_name="search_results", results=results, pattern=user_pattern)
            
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
            sort_reverse()
        elif reverse_button == "alphabetical":
            sort_alphabetical()
        if descending_button == "descending":
            sort_descending()
        elif descending_button == "ascending":
            sort_ascending()
        elif length_button == "length-ascending":
            sort_length_ascending()
        elif length_button == "length-descending":
            sort_length_descending()

        page_num = 1
        begin = 0
        end = 25
        reversed_results = submit_next(direction="last")
        return render_template('result.html', results=reversed_results, user_pattern=user_pattern, num=num,
                                page_num=f"<span id='page-num'>{page_num}</span>", pages=f"<span id='pages'>{ceil(num/25)}</span>",
                                reverse="true")

if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True)