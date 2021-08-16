from flask import Flask, render_template, request, Response#, session
import main_functions_search as mf
import help_functions as hf
import os
from math import ceil


app = Flask(__name__)


# uses mf to get search results
def get_results(language_str_i, accent, user_pattern, order_id, asc_desc, limit, offset):

    #language = hf.languages[int(language)-1]
    language = hf.languages[int(language_str_i)-1]

    allowed = hf.get_allowed_con_vow(language=language)[0]
    check = mf.check_validity(language, user_pattern=user_pattern, allowed=allowed)

    if check:
        user_results = mf.connect_search_related_fcts(language, accent, user_pattern=user_pattern, order_id=order_id, asc_desc=asc_desc, limit=limit, offset=offset)
        results = [word[0] for word in user_results[0]]
        transliteration = [word[1] for word in user_results[0]]
        pattern = user_results[2]
    
        number = hf.get_result_number(language, pattern)

        if language == "armenian":
            syllables = hf.syllabificate_armenian(results)
        else:
            syllables = hf.syllabificate_greek(results)

        marked_results = hf.mark_pattern(pattern=pattern, language=language, results=results, xml=False)
        results = marked_results

        return results, transliteration, syllables, pattern, number
    
    else:
        return False


@app.route('/')
def route_page():
    return render_template('welcome.html')


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/description')
def description():
    return render_template('description.html')


@app.route('/search/results', methods=['GET'])
def result_page():
    submit = request.args.get("submit-button")
    download = request.args.get("download-input")
    page_num = int(request.args.get("page-num")) if request.args.get("page-num") is not None else 0
    page = request.args.get("page-skip") if request.args.get("page-skip") is not None else 0
    user_pattern = request.args.get("search-input")
    language = request.args.get("choose-language")
    accent_sensitive = request.args.get("accent-sensitive")
    offset = int(request.args.get("offset")) if request.args.get("offset") is not None else 0

    order_id = "" 

    # get search data
    asc_desc = "ASC"
    reverse_checked = ""
    descending_checked = ""
    length_asc_checked = ""
    length_desc_checked = ""
    limit = 25

    # download, page_num, page(pageskip), order_id, user_pattern, language,accent_sensitiive, offset, reverse, descending, length_asc, length_desc 

    if submit == "start":
        print("start")
        offset = 0
        page_num = 1
        order_id = "id"
        asc_desc = "ASC"

    elif page == "next" or page == "last":
        if page == "last":
            if page_num == 1:
                pass
            else:
                page_num -= 1
                offset -= 25
        elif page == "next":
            page_num += 1
            offset += 25
        
        asc_desc = "ASC"
        order_id = "id"


    # eigene Funktion
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
        <span class="switch-label">reverse</span>
        </span>
    <span>
        <label class="switch" for='descending-check'>
            <input id='descending-check' class='alphabet-check' type='checkbox' name='descending' value='true' onChange='this.form.submit();' {descending_checked}>
            <span class="slider"></span>
        </label>
        <span class="switch-label">descending</span>
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

    results = get_results(   # returns tuple(results, transliteration, syllables, pattern, number of results) or False
        language_str_i=language,
        accent=accent_sensitive,
        user_pattern=user_pattern,
        order_id=order_id,
        asc_desc=asc_desc,
        limit=limit,
        offset=offset)
   
    if results is False:
        return render_template("error.html")

    if page_num > ceil(results[4]/25):
        page_num -= 1
        offset -= 25
    print(download)
    if download == "xml" or download == "txt":
        if download == "txt":
            kind = "txt"
        elif download == "xml":
            kind = "xml"

        response = hf.download(pattern=results[3], user_pattern=user_pattern, language=int(language), kind=kind)
        return Response(response[0], mimetype=f"{response[1]}", headers={"Content-Disposition": f"attatchment; filename={response[2]}"})

    else:
        file_name = ""
        
    return render_template(
        'result.html',
        results=(results[0], results[1],results[2]),
        user_pattern=user_pattern,
        number=results[4],
        language=language,
        pages=f"{ceil(results[4]/25)}",
        switch_html=switch_html,
        download="false",
        file_name_download=file_name,
        page_num=page_num,
        offset=offset,
        page_skip="false",
        accent_sensitive=accent_sensitive
    )


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True, threaded=True)
