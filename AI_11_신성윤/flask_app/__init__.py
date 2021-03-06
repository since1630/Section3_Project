from distutils.log import debug
from flask import Flask , render_template , jsonify , request, redirect, url_for
import pickle
import numpy as np
import pandas as pd
import joblib

model_kospi = pickle.load(open('flask_app/model/model_kospi.pkl','rb'))
model_kosdaq= pickle.load(open('flask_app/model/model_kosdaq.pkl','rb'))

def create_app():

    app = Flask(__name__)


    @app.route('/')
    def index():

        # y_pred_kospi = model_kospi.predict([[4000]])
        # y_pred_kosdaq = model_kosdaq.predict([[5000]])

        return render_template('index.html')




    @app.route('/predict', methods=['POST'])
    def predict():
        if request.method == 'POST':

            data1 = request.form['koribor_3month']
            data2 = request.form['economic_growth_rate']
            data3 = request.form['base_inflation']
            data4 = request.form['interest_rate']

            arr = [[data1,data2,data3,data4]]
            pred_kospi = np.round(model_kospi.predict(arr)[0], 2)
            
            pred_kosdaq = np.round(model_kosdaq.predict(arr)[0], 2)
            

            return render_template('predict.html', data_kospi=pred_kospi , data_kosdaq=pred_kosdaq)

    return app

app = create_app()


if __name__ == '__main__':    
    app.run(debug=True)
