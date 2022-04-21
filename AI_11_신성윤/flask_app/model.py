from sklearn.metrics import mean_absolute_error , r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

df = pd.read_csv('./macro_economic_csv.csv')
df['time'] = df['time'].astype('str')
df = df.fillna(method='bfill')

df_kospi = df.drop('kosdaq_value', axis=1)
df_kospi

df_kosdaq = df.drop('kospi_value', axis=1)
df_kosdaq

X_features_kospi = df_kospi[['koribor_3month','economic_growth_rate','base_inflation','interest_rate']]
y_target_kospi = df_kospi['kospi_value']

X_features_kosdaq = df_kosdaq[['koribor_3month','economic_growth_rate','base_inflation','interest_rate']]
y_target_kosdaq = df_kosdaq['kosdaq_value']

X_train_kospi, X_test_kospi , y_train_kospi, y_test_kospi = train_test_split(X_features_kospi, y_target_kospi, test_size=0.2, random_state=1)
X_train_kosdaq, X_test_kosdaq , y_train_kosdaq, y_test_kosdaq = train_test_split(X_features_kosdaq, y_target_kosdaq, test_size=0.2, random_state=1)

model_1 = LinearRegression()
model_2 = LinearRegression()

model_1.fit(X_train_kospi, y_train_kospi)
y_pred_kospi = model_1.predict(X_test_kospi)

model_2.fit(X_train_kosdaq, y_train_kosdaq)
y_pred_kosdaq = model_2.predict(X_test_kosdaq)

pickle.dump(model_1, open('/model/model_kospi.pkl','wb'))
pickle.dump(model_2, open('/model/model_kosdaq.pkl','wb'))