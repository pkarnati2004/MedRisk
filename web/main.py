from flask import Flask, render_template, request
import pandas as pd
import matplotlib
import numpy as np

from bokeh.plotting import figure, output_file, show, save
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.models import HoverTool
from bokeh.io import show, output_file
from bokeh.palettes import Spectral6

from train import run_model

import os

app = Flask(__name__)

disease_map = {
    "SP_CHF": " health failure",
    "SP_CHRNKIDN": " chronic kidney disease",
    "SP_CNCR": " cancer",
    "SP_COPD": " copd",
    "SP_DEPRESSN": " depression",
    "SP_DIABETES": " diabetes",
    "SP_ISCHMCHT": " ischemic heart disease",
    "SP_OSTEOPRS": " osteoporosis",
    "SP_RA_OA": " arthritis",
    "SP_STRKETIA": " stroke",
    "SP_ALZHDMTA": " alzheimers"
    }

race_map = {
        "white" : " Caucasian",
        "black" : " African American",
        "other" : " Others",
        "hispanic" : " Hispanic"
    }

race_num_map = {
        "white" : 1,
        "black" : 2,
        "other" : 3,
        "hispanic" : 5
    }

gender_num_map = {
    "male" : 1,
    "female" : 2
}

gender_value = "Cancer"
race_value = "white"

@app.route('/')
def hello_world():
    # return "hello world, welcome to SheHacks!!!!! Standalone page for index!!!!"
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    race = request.form['race']
    county = request.form['county']

    data = np.loadtxt('static/data/learn/coeff.txt')

    patient_data = [[int(county)], [int(race_num_map[race])], [int(gender_num_map[gender])], [int(age)]]

    # res = np.multiply(data, patient_data)
    res = np.dot(data, patient_data)

    print(res)

    keys = ["SP_ALZHDMTA", "SP_CHF", "SP_CHRNKIDN", "SP_CNCR", "SP_COPD", "SP_DEPRESSN", "SP_DIABETES", "SP_ISCHMCHT",
    "SP_OSTEOPRS", "SP_RA_OA", "SP_STRKETIA"]
    # print(keys)

    patient_map = {}
    for i in range(len(keys)):
        patient_map[keys[i]] = float(res[i])
    
    print(patient_map)

    # print(data)

    # return name + " " + age + gender + race + county
    return render_template('results.html',
                            az=float(res[0]),
                            hf=float(res[1]),
                            ckd=float(res[2]),
                            cnr=float(res[3]),
                            copd=float(res[4]),
                            depr=float(res[5]),
                            dbts=float(res[6]),
                            ihd=float(res[7]),
                            os=float(res[8]),
                            art=float(res[9]),
                            stk=float(res[10]))


@app.route('/company')
def company():

    output_file("gender.html", title="Gender Risk Analysis")
    data = pd.read_csv('static/data/gender.csv')

    p = figure(x_range=data['Gender'].values, plot_height=250, title="Gender Disease Trends for Alzhiemers")
    p.vbar(x=data['Gender'].values, top=data['SP_ALZHDMTA'].values, width=0.4)

    p.y_range.start = 0
    p.y_range.end=100
    save(p, filename="gender.html")
    os.rename("gender.html", "templates/gender.html")
    # show(p)
    script, div = components(p)
    # save(script, "genderScript.html")
    # save(div, "genderDiv.html")

    # return render_template('company.html', gender="gender.html")
    text_file = open("templates/genderScript.html", "w")
    text_file.write(script)
    text_file.close()

    text_file = open("templates/genderDiv.html", "w")
    text_file.write(div)
    text_file.close()

    return render_template('company.html', 
            gender_script="genderScript.html", 
            gender_div="genderDiv.html",
            gender_disease=gender_value,
            race_script="raceScript.html",
            race_div="raceDiv.html",
            race_disease=race_map[race_value])
    # return render_template('company.html')


@app.route('/company_gender', methods=['GET', 'POST'])
def company_gender():
    # print("HELLO")
    value = request.form.get('stateCon')
    # print(value)
    # return render_template('company.html', gender=value)

    output_file("gender.html", title="Gender Risk Analysis")
    data = pd.read_csv('static/data/gender.csv')

    p = figure(x_range=data['Gender'].values, plot_height=250, title="Gender disease trends for" + disease_map[value])
    p.vbar(x=data['Gender'].values, top=data[value].values, width=0.4)

    p.y_range.start = 0
    p.y_range.end=100
    save(p, filename="gender.html")
    os.rename("gender.html", "templates/gender.html")

    script, div = components(p)

    text_file = open("templates/genderScript.html", "w")
    text_file.write(script)
    text_file.close()

    text_file = open("templates/genderDiv.html", "w")
    text_file.write(div)
    text_file.close()

    gender_value = disease_map[value]

    return render_template('company.html', 
                gender_script="genderScript.html", 
                gender_div="genderDiv.html",
                gender_disease=gender_value,
                race_script="raceScript.html",
                race_div="raceDiv.html",
                race_disease=race_map[race_value])

## name, age, race, gender, county, current disease

@app.route('/company_race', methods=['GET', 'POST'])
def company_race():

    value = request.form.get('race')

    race_dict = create_company_dict()

    output_file("race.html", title="Race Risk Analysis")
    p = figure(x_range=list(disease_map.values()), plot_height=250, plot_width=1100, title="Race disease trends for " + race_map[value])
    p.vbar(x=list(disease_map.values()), top=race_dict[value], width=0.4)

    p.y_range.start = 0
    p.y_range.end=0.5
    save(p, filename="race.html")
    os.rename("race.html", "templates/race.html")

    script, div = components(p)

    text_file = open("templates/raceScript.html", "w")
    text_file.write(script)
    text_file.close()

    text_file = open("templates/raceDiv.html", "w")
    text_file.write(div)
    text_file.close()

    return render_template('company.html', 
                gender_script="genderScript.html", 
                gender_div="genderDiv.html",
                gender_disease=gender_value,
                race_script="raceScript.html",
                race_div="raceDiv.html",
                race_disease=race_map[value])


def create_company_dict():

    output_file("race.html", title="Race Risk Analysis")
    data = pd.read_csv('static/data/race_dis.csv')

    # data = data.T

    print(data['Race'])
    dataset = [data[key] for key in disease_map.keys()]
    print(dataset)

    race_dict = {
        "white" : [d[0] for d in dataset],
        "black" : [d[1] for d in dataset],
        "other" : [d[2] for d in dataset],
        "hispanic" : [d[3] for d in dataset]
    }

    print(race_dict)

    return race_dict


@app.route('/server')
def run():
    print("RUNNING")
    coefs = run_model()

    return ceofs

@app.route('/plotlib')
def plot():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("lines.html", title="line plot example")
    # os.rename("lines.html", "templates/lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)
    save(p, filename="lines.html")
    os.rename("lines.html", "templates/lines.html")

    return render_template('plot.html', script="lines.html")

@app.route('/plotsample')
def plotsample():
    output_file("bars.html", title="bar example")

    data = pd.read_csv('static/data/dummydata.csv')

    # fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    # print(data)
    # print(data['category'].values)
    # print(data['pie'].values)

    # p = figure(x_range=fruits, plot_height=250, title="Fruit Counts")
    p = figure(x_range=data['category'].values, plot_height=250, title="Pie")

    # p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)
    p.vbar(x=data['category'].values, top=data['pie'].values, width=0.4)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)
    return "hello"
    

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    gender = request.form['gender']
    race = request.form['race']
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        gender=gender,
        race=race)


if __name__ == "__main__":
    app.run(debug=True)