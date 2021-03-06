# MedRisk: SheHacks healthcare Hack

## Why?

We developed a Risk Assessment application given the CMS database from IBM for SheHacks 2018.

We created a webapp that features a machine learning model that assesses risks for Multiple conditions for each person of different demographics and historical conditions. We also analyzed the CMS database to create visualizations of risk assessments based on demographic parameters. We created a US heatmap visualization that differentiates risk assessment by color depthness based on geographical location. The idea is that these visualizations and analysis would allow clients (such as clinicians or insurance companies) to assess the risk of a patient before hand, given certain parameters available through the dataset. We also created visualizations for other parameters such as age group, ethnicity, and gender. Lastly, we created a tool that allows patients to search for doctors nearby, with access to the doctor’s detail information such as degree and specialization.

## How

We developed our tool using CMS dataset provided by IBM, which consists of historical medical claims in US with thousands of records. The tool itself is a web application developed using flask for the server side and backend code running HTML and CSS code for the front end. The tool consists of two parts: an analysis side and a predictive model. Using HighCharts, we created a US heatmap visualization that differentiates risk assessment by color depthness based on geographical location. It categorize risk assessment by conditions to provide easier-understanding information for insurance companies to determine risk. We also provide visualizations based on other categories such as ethnicity and gender.

We used IBM’s dataset to create our prediction model and visualizations. We learned juypter to analyze IBM’s database, and extracted demographics parameters to create an interactive heatmap of disease trends in each state in US. We also used bokeh visualization library for python to create interactive graphs for other parameters such as ethnicity and gender. Using sklearn and the pandas library, we created a logistic regression model to predict the possible diagnosis of a user based on demographic parameters. We chose the logistic regression model to assess risks for multiple conditions by predicting the likelihood of a patient with a certain disease to contract other diseases. We did this by looking at features such as age, gender, race and county. We created a UI to take as input a new patient’s information and show how likely he/she is to contract diseases, given that the patient already has a specific disease. We created the heatmap visualization using a python visualization library HighCharts. We developed other visualization using Bokeh.

## Where

The web application and the machine learning model can be found in the web folder. Run

```
pip install -r requirements.txt
```

to install the required libraries for the service.
