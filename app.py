
import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.model_selection import GridSearchCV, train_test_split

"""
# Gold Nanorods Size Prediction 

**_Instruction_**:

1. Upload .csv file whose first row "E_res" and "Linewidth"

2. Hit the prediction button 
"""

# To load training data
path = "./data/"

@st.cache
def load_data(nrows):
    data = pd.read_csv(path + 'SPP+.csv', nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Training data loading done! Substrate: Quartz Surrounding: Air")

if st.checkbox('Show all training data'):
    st.subheader('Training data')
    st.write(data)

#  To input experimental data
st.header('Experimental Data Input')

uploaded_file = st.file_uploader("Choose your data", type="csv")

if uploaded_file:
    dataframe = pd.read_csv(uploaded_file)
    Exp_data = pd.DataFrame(dataframe)

    st.write(Exp_data)

# arranging features from original dataset for model learning
x = data.drop(['Wavelength (nm)', 'Width (nm)', 'AspectRatio', 'Length (nm)', 'Linewidth (nm)', 'MaxCscat'], axis=1)
w_y = data['Width (nm)']
l_y = data['Length (nm)']

# parameters for GridSearchCV class
param_grid = {'max_depth': range(1, 31)}

# Initialize GridSearchCV class
wgs = GridSearchCV(estimator=DTR(),
                   param_grid=param_grid,
                   cv=10, scoring='neg_mean_squared_error')
lgs = GridSearchCV(estimator=DTR(),
                   param_grid=param_grid,
                   cv=10, scoring='neg_mean_squared_error')

wgs.fit(x, w_y)
lgs.fit(x, l_y)

st.header('Prediction')

if st.button("Prediction!!!"):

    wexp_y_pred = wgs.predict(Exp_data)
    lexp_y_pred = lgs.predict(Exp_data)

    st.dataframe(({"Predicted_Width": wexp_y_pred, "Predicted_Length": lexp_y_pred}))
