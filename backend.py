from flask import Flask, render_template, request, url_for
import main_files_search as mf

app = Flask(__name__)


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
            return render_template('result.html', results=user_results[0], pattern=user_results[1],
                                   num=len(user_results[0]))
        else:
            pass


if __name__ == '__main__':
    app.run(port=1337, debug=True)
