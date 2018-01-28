from flask import Flask, render_template, request
import pandas as pd
import matplotlib
from bokeh.plotting import figure, output_file, show, save
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.models import HoverTool
from bokeh.io import show, output_file
from bokeh.palettes import Spectral6

import os

app = Flask(__name__)

disease_map = {
    "health_failure": "SP_CHF",
    "chronic_kidney_disease": "SP_CHRNKIDN",
    "cancer": "SP_CNCR",
    "copd": "SP_COPD",
    "depression": "SP_DEPRESSN",
    "diabetes": "SP_DIABETES",
    "ischemic_heart_disease": "SP_ISCHMCHT",
    "osteoporosis": "SP_OSTEOPRS",
    "arthritis" : "SP_RA_OA",
    "stroke": "SP_STRKETIA",
    "alzheimers": "SP_ALZHDMTA"
    }


@app.route('/')
def hello_world():
    # return "hello world, welcome to SheHacks!!!!! Standalone page for index!!!!"
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('index.html')

@app.route('/company')
def show():
    return render_template('company.html')

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

    # show the results
    # show(p)
    # html = file_html(p, CDN, "myplot")
    # save(html)
    # script, div = components(p)
    # show(p)

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