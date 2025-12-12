from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     


@app.route("/contact/")
def contact_page():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def tawarano_graph():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits_graph():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    
    # Extraction des minutes de chaque commit
    minutes_list = []
    for commit_entry in data:
        date_string = commit_entry.get("commit", {}).get("author", {}).get("date")
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_object.minute)
    
    return render_template("commits.html", minutes_list=minutes_list)
  
if __name__ == "__main__":
  app.run(debug=True)
