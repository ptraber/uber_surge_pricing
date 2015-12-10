import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import json
from flask import Flask
from flask.ext.cors import CORS

def day_fix(string):
    if string == '1':
        return "Monday"
    elif string =='2':
        return "Tuesday"
    elif string =='3':
        return "Wednesday"
    elif string =='4':
        return 'Thursday'
    elif string == '5':
        return 'Friday'
    elif string == '6':
        return 'Saturday'
    elif string == '0':
        return 'Sunday'

def min_fix(string):
    num = int(string)
    return str(num - (num%10))

def weather_fix(string):
    if string == 'Light Rain':
        return 'Rain'
    elif string == 'ScatteredClouds':
        return 'Cloudy'
    elif string == 'Mostly Cloudy':
        return'Cloudy'
    elif string == 'Partly Cloudy':
        return'Cloudy'
    elif string =='Overcast':
        return'Clear'
    else:
        return string

from sklearn.externals import joblib

rf = joblib.load("RandomForestClassifier.pkl")
columns = joblib.load('columns.pkl')

app = Flask(__name__)
CORS(app)
app.debug = True
app.run()

@app.route('/<string>')
def predict(string):
    string = temp.replace('ride','').replace('=','').replace('city','').replace('temp','').replace('day','').replace('time','').replace('weather','').replace('%20',' ')
    cleaning = string.split("&")
    cleaning[3] = day_fix(cleaning[3])
    time = cleaning[4].split(':')
    time[1] = min_fix(time[1])
    cleaning[4] = time[0] + ':' + time[1]
    temperature = int(cleaning[2])
    cleaning[5] = weather_fix(cleaning[5])
    del cleaning[2]
    
    X = [0] * len(columns)
    X[14] = temperature
    X[11] = 1
    #X
    for i in cleaning:
        for k in range(len(columns)):
            if i in columns[k]:
                X[k] = 1

    if cleaning[0] == 'uberX':
        X[5] = 0
    
    prediction = rf.predict(X)
    prediction = rf.predict_proba(X)
    return_dict = {}
    return_dict['High Surge'] = round(prediction[0][0][1],3)
    return_dict['Low Surge'] = round(prediction[1][0][1],3)
    return_dict['Mid Surge'] = round(prediction[2][0][1],3)
    return_dict['No Surge'] = round(prediction[3][0][1],3)
    d = json.dumps(return_dict)
    return d

if __name__ == '__main__':
    app.run(host='0.0.0.0')
