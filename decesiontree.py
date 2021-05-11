import pandas as pd
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.model_selection import GridSearchCV
import joblib

path = "/Users/katsuyashiratori/Documents/Python/SPP/Input/"

# loading original dataset
data = pd.read_csv(path + 'SPP+.csv')
# arranging features from original dataset for model learning
x = data.drop(['Wavelength (nm)', 'Width (nm)', 'AspectRatio', 'Length (nm)', 'Linewidth (nm)', 'MaxCscat'], axis=1)
w_y = data['Width (nm)']
l_y = data['Length (nm)']

# parameters for GridSearchCV class
param_grid = {'max_depth': range(1, 31)}

# Initialize GridSearchCV class
width_gs = GridSearchCV(estimator=DTR(),
                   param_grid=param_grid,
                   cv=10, scoring='neg_mean_squared_error')
length_gs = GridSearchCV(estimator=DTR(),
                   param_grid=param_grid,
                   cv=10, scoring='neg_mean_squared_error')

width_gs.fit(x, w_y)
length_gs.fit(x, l_y)

joblib_width_file = "joblib_width_gs.pkl"
joblib.dump(width_gs, joblib_width_file)

joblib_length_file = "joblib_length_gs.pkl"
joblib.dump(length_gs, joblib_length_file)