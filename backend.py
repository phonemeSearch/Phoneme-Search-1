from flask import Flask, render_template, request, Response, session
import secrets
import main_functions_search as mf
import help_functions as hf
import os
from math import ceil


app = Flask(__name__)


app.secret_key = secrets.token_urlsafe(16)


limit = 25

# uses mf to get search results
def get_results(language, accent, user_pattern, order_id, asc_desc, limit, offset):

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
    global limit #change, only currently
    submit = request.args.get("submit-button")

    if submit == "start":

        [session.pop(key) for key in list(session.keys())]
        
        # static values
        session["user_pattern"] = request.args.get("search-input")
        language_i = int(request.args.get("choose-language"))-1
        session["language"] = hf.languages[language_i]
        session["accent_sensitive"] = request.args.get("accent-sensitive")
        session["allowed"] = hf.get_allowed_con_vow(session["language"])
        pattern = mf.get_pattern()
        session["pattern"] = pattern
        result_num = hf.get_result_number(session["language"], pattern)
        session["result_num"] = result_num
        pages = ceil(result_num/25)
        session["pages"] = pages
        # default values
        session["page_num"] = "1"
        session["offset"] = "0"
        session["order_id"] = "id"
        #session["order_check"] = None
        session["asc_desc"] = "ASC"
        file_name = ""
        reverse_checked = ""
        descending_checked = ""
        length_asc_checked = ""
        length_desc_checked = ""

    else:
        download = request.args.get("download")
        page_skip = request.args.get("skip-btn")
        user_page = request.args.get("user-page")
        reverse_check = request.args.get("reverse-check")
        descending_check = request.args.get("descending-check")
        lasc_check = request.args.get("lasc-check")
        ldesc_check = request.args.get("ldesc-check")

        print("session", session)
        print(download)
        print(page_skip)
        print(user_page)
        print(reverse_check, descending_check, lasc_check, ldesc_check)

        if download:
            if download == "xml":
                kind = "xml"
            elif download == "txt":
                kind = "txt"
            response = hf.download(pattern=session["pattern"], user_pattern=session["user_pattern"], language=session["language"], kind=kind)
            return Response(response[0], mimetype=f"{response[1]}", headers={"Content-Disposition": f"attatchment; filename={response[2]}"})

        else:
            file_name = ""

        if page_skip:
            page_num = int(session["page_num"])
            offset = int(session["offset"])
            pages = int(session["pages"])
            if page_skip == "last":
                page_num -= 1
                offset -= limit
            elif page_skip == "next":
                page_num += 1
                offset += limit
            if page_num >= pages or page_num < 1:    #prüfen
                pass
            else: 
                session["offset"] = offset
                session["page_num"] = page_num
        
        if user_page:
            offset = session["offset"]
            offset = (int(user_page)-1)*limit
            session["offset"] = offset
            session["page_num"] = user_page 

        order_id = ""
        asc_desc = ""

        reverse_checked = ""
        descending_checked = ""
        length_asc_checked = ""
        length_desc_checked = ""
        
        if reverse_check == "checked" or descending_check == "checked":
            length_asc_checked = "disabled"
            length_desc_checked = "disabled"
            if reverse_check == "checked":
                order_id = "id_reverse"
                reverse_checked = "checked"
            else: 
                order_id = "id"
                reverse_checked = ""

            if descending_check == "checked":
                asc_desc = "DESC"
                descending_checked = "checked"
            else:
                asc_desc = "ASC"
                descending_checked = ""

        elif lasc_check == "checked" or ldesc_check == "checked":
            reverse_checked = "disabled"
            descending_checked = "disabled"
            if lasc_check == "checked":
                length_desc_checked = "disabled"
                order_id = "id_length"
                asc_desc = "ASC"
                length_asc_checked = "checked"
                
            if ldesc_check == "checked":
                length_asc_checked = "disabled"
                order_id = "id_length"
                asc_desc = "DESC"
                length_desc_checked = "checked"
        
        else:
            order_id = "id"
            asc_desc = "ASC"

        session["order_id"] = order_id
        session["asc_desc"] = asc_desc

    results = get_results(   # returns tuple(results, transliteration, syllables, pattern, number of results) or False
        language=session["language"],
        accent=session["accent_sensitive"],
        user_pattern=session["user_pattern"],
        order_id=session["order_id"],
        asc_desc=session["asc_desc"],
        limit=limit,
        offset=session["offset"])
   
    if results is False:
        return render_template("error.html")

    result_num = session["result_num"]
    return render_template(
        'result.html',
        results=(results[0], results[1],results[2]), #imp
        user_pattern=session["user_pattern"], #imp
        number=session["result_num"], #imp
        language=session["language"], #imp
        pages=session["pages"], #imp
        file_name_download=file_name, #imp
        page_num=session["page_num"], #imp
        accent_sensitive=session["accent_sensitive"], #imp
        reverse_checked=reverse_checked,
        descending_checked=descending_checked,
        length_asc_checked=length_asc_checked,
        length_desc_checked=length_desc_checked
    )


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'), port=int(os.environ.get("PORT", 1337)), debug=True, threaded=True)
