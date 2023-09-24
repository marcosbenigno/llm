from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import re
import os
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
import openai
openai.api_key = ''
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



app.config.from_object('config.Config')

def searchScopus(query):
    
    search = ScopusSearch("TITLE-ABS-KEY(("+query+")) AND PUBYEAR > 2023", subscriber=False)

   
    bibtex_content = ""
    for entry in search.results:
        # Manually format a BibTeX entry
        #authors = " and ".join([f"{author['given-name']} {author['surname']}" for author in entry.author_info])
        bibtex_content += f"@article{{scopus_id_{entry.eid},\n"
        bibtex_content += f"  title = {{{entry.title}}},\n"
        #bibtex_content += f"  author = {{{authors}}},\n"
        bibtex_content += f"  journal = {{{entry.publicationName}}},\n"
        bibtex_content += f"  year = {{{entry.coverDate.split('-')[0]}}},\n"
        bibtex_content += f"  volume = {{{entry.volume}}},\n"
        bibtex_content += f"  pages = {{{entry.pageRange}}}\n"
        bibtex_content += "}}\n\n"
    return bibtex_content

def getJson(request):
    try: 
        if 'jsonFile' not in request.files:
            
            return jsonify({"error": "No file provided"})
        json_file = request.files['jsonFile']

          
        if json_file.filename == '':
            
            return jsonify({"error": "No selected file"})

        if not json_file.filename.endswith('.json'):
         
            return jsonify({"error": "Invalid file format. Expected .json"})
           
        json_data = json_file.read().decode('utf-8')

            
        parsed_data = json.loads(json_data)
        
        return parsed_data
    except Exception as e:
        return jsonify({"error": str(e)})
    
def format_list_to_string(lst):
    formatted_string = '\n'.join(['-' + item + '\n' for item in lst])
    return f'"{formatted_string}"'

def parse_bibtex(bib_string):
    
    entry_pattern = r'@\w+\s*{[^}]+}'
    
    
    bib_entries = re.findall(entry_pattern, bib_string, re.DOTALL)
    
    return bib_entries

def format_inclusion_exclusion(data):
    inclusion_items = "\n".join([f"- IC{n}: {item}" for n, item in enumerate(data["inclusion"], start=1)])
    exclusion_items = "\n".join([f"- EC{n}: {item}" for n, item in enumerate(data["exclusion"], start=1)])
    result = f"inclusion:\n{inclusion_items}\nexclusion:\n{exclusion_items}"
    return result

def getString(pico):
    formatted_items = ['(' + ' OR '.join([f'"{item}"' for item in values if item]) + ')' for key, values in pico.items() if any(values)]


    initial_string = ' AND '.join(formatted_items)
    prompt = "Each sentence surrounded by parentheses in the following string is independent and contains different terms. Add at least 2 and at most 5 synonyms (you choose) for each of these terms to each matching sentence. Each term must be enclosed in double quotes and must be separated by the OR operator. The result must be only a string like the input, and nothing more. Input string: \"" + initial_string + "\""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you will be objective in your answers, answering only what is asked"},
            {"role": "user", "content": prompt}])
    stringResult = completion.choices[0].message.content

    return stringResult

def getForm(rqs):
    initial_string = format_list_to_string(rqs)
    prompt = "I'm making a form to extract data from academic articles based on questions I want to ansewer. This form will be filled fo each article. Give me the fields I should put on a detaild form to help me to ansewer each question; one question can have more than one field on the form. Put outher suggested information on the list you think would generate interesting insights. List the fields name and nothing more; be objective and don't use any intoduction sentence on your ansewer. The ansewer should be a python dict with each key referring to a question and pointing to a list of strings, each string being one field of the form. The questions are the following:" + initial_string
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you will be objective in your answers, answering only what is asked and not making introductions"},
            {"role": "user", "content": prompt}])
    return completion.choices[0].message.content

def getSelection(criteria, bibString):
    criteria_string = format_inclusion_exclusion(criteria)
    bibItems = parse_bibtex(bibString)
    results = []
    for bibItem in bibItems:
        prompt = '''having this bib string: "'''+bibItem+'''"\n for each of the following criteria, tell me if the article applies to each the inclusion criteria (IC) and exclusion criteria (EC). it can be "ok", "maybe" or "do not apply". if IC criteria are met, result is "ok", if EC criteria is not met, result is "ok"; if IC and EC are not clear, result is "maybe". criteria expressed as follows: "'''+criteria_string+'''". return ONLY a dict with the format: {title: "", criterias: [{critetia:"", result:"",explanation:""}]}'''
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you will be objective in your answers, answering only what is asked and not making introductions"},
                {"role": "user", "content": prompt}])
        results.append(completion.choices[0].message.content)
    return "\n\n".join(results)

@app.route('/protocol/string', methods=['POST'])
def protocol_string():
    data = getJson(request)
    pico = data["pico"]
    searchString = getString(pico)
    print(searchString)
    return jsonify({"success": searchString})

@app.route('/protocol/form', methods=['POST'])
def protocol_form():
    data = getJson(request)
    rqs = data["rqs"]
    formString = getForm(rqs)
    print(formString)
    return jsonify({"success": formString})

@app.route('/protocol/selection', methods=['POST'])
def protocol_selection():
    data = getJson(request)
    print(data)
    bib = data["bib"]
    criteria = data["criteria"]
    selectionString = getSelection(criteria, bib)
    print(selectionString)
    return jsonify({"success": selectionString})


if __name__ == '__main__':
    app.run()
