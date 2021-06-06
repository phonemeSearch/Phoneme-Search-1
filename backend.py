from flask import Flask, render_template, request, url_for
import main_files_search as mf
import re

app = Flask(__name__)


def mark_pattern (pattern, results):
    marked_list = []
    for result in results:
        count = 0
        matches = re.finditer(pattern, result)
        marked = result
        #print("-----------------------------------")
        for match in matches:
            count += 1
            #print(result)
            #print(match)
            #print(match.groups())
            group = match.group(0)
            if count % 2 == 0:
                marked = re.sub(f"{group}(?!\w?\/%)", f"%{group}/%", marked, 1)
            elif count % 2 != 0:
                marked = re.sub(f"{group}(?!\w?\/%)", f"§{group}/%", marked, 1)
        
        marked = re.sub("(?<!\/)%", "<span class='mark-even'>", marked)
        marked = re.sub("\/%", "</span>", marked)
        marked = re.sub("§", "<span class='mark-odd'>", marked)

        marked = "<div class=lemma>" + marked + "</div>"
        marked_list.append(marked)
    marked_list = sorted(marked_list)
    print(pattern)
    return marked_list
            
        

@app.route('/')
def route_page():
    return render_template('welcome.html')


@app.route('/search', methods=["POST", "GET"])
def search():
    return render_template('search.html')


@app.route('/search/description')
def description():
    return render_template('description.html')


@app.route('/search_result', methods=["POST", "GET"])
def result_page():
    if request.method == "POST":
        user_search = request.form['search-input']
        # user_search = request.args.get['search-input']
        language = request.form['choose-language']
        # language = request.args.get['choose-language']
        user_allowed = mf.prepare_language_characteristics(language_index=int(language))
        check = mf.check_validity(search_string=user_search, allowed=user_allowed)
        if check:
            user_results = mf.connect_search_related_fcts(search_string=user_search)
            pattern = user_results[2]
            marked_results = mark_pattern(pattern=pattern, results=user_results[0])
            return render_template('result.html', results=marked_results, user_pattern=user_results[1],
                                   num=len(user_results[0]))
        else:
            pass


if __name__ == '__main__':
    app.run(port=1337, debug=True)
