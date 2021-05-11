import streamlit as st
import pandas as pd
import base64
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.model_selection import GridSearchCV
from PIL import Image
from bokeh.plotting import figure
import joblib
"""
# Gold Nanorods Size Prediction Ver. 1.0

Provided by Link (https://slink.rice.edu) and Landes (https://lrg.rice.edu) Research Group

**_Instruction_**:

1. Upload .csv file with first row "E_res" and "Linewidth" in eV.

"""

# To load csv image
path = "./data/"
image = Image.open(path + 'example.png')
st.image(image, caption='This is an example in Excel.')

"""
2. Hit the prediction button
"""

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction_output.csv">Click here to download the outcome in .csv file</a>'
    return href

st.text("Training data conditions: Substrate: Quartz(refractive index: 1.52), Surrounding: Air")

#  To input experimental data
st.header('Experimental Data Input')

uploaded_file = st.file_uploader("Choose your data", type="csv")

if uploaded_file:
    dataframe = pd.read_csv(uploaded_file)
    Exp_data = pd.DataFrame(dataframe)
    st.write(Exp_data)

if st.button("Prediction"):

    st.text('Predicted results')
    dt_w_model = joblib.load('joblib_width_gs.pkl')
    dt_l_model = joblib.load('joblib_length_gs.pkl')

    wexp_y_pred = dt_w_model.predict(Exp_data)
    lexp_y_pred = dt_l_model.predict(Exp_data)

    df_P = pd.DataFrame({"Particle": range(1, len(Exp_data['E_res']) + 1)})
    df_E = pd.DataFrame({"E_res (eV)": Exp_data['E_res']})
    df_L = pd.DataFrame({"Linewidth (eV)": Exp_data['Linewidth']})
    df_w = pd.DataFrame({"Predicted_Width (nm)": wexp_y_pred})
    df_l = pd.DataFrame({"Predicted_Length (nm)": lexp_y_pred})
    df_A = pd.DataFrame({"Aspect Ratio": lexp_y_pred / wexp_y_pred})
    DF1 = pd.concat([df_E, df_L], axis=1, sort=True)
    DF2 = pd.concat([df_w, df_l], axis=1, sort=True)
    dfff = pd.concat([DF1, DF2], axis=1, sort=True)
    dff = pd.concat([df_P, dfff], axis=1, sort=True)
    df = pd.concat([dff, df_A], axis=1, sort=True)

    Mean_df_E = Exp_data['E_res'].mean()
    Mean_df_L = Exp_data['Linewidth'].mean()
    Mean_df_w = wexp_y_pred.mean()
    Mean_df_l = lexp_y_pred.mean()
    Mean_df_A = (lexp_y_pred / wexp_y_pred).mean()

    Std_df_E = Exp_data['E_res'].std()
    Std_df_L = Exp_data['Linewidth'].std()
    Std_df_w = wexp_y_pred.std()
    Std_df_l = lexp_y_pred.std()
    Std_df_A = (lexp_y_pred / wexp_y_pred).std()

    column1 = ['Particle', 'E_res (eV)', 'Linewidth (eV)', 'Predicted_Width (nm)', 'Predicted_Length (nm)',
               'Aspect Ratio']
    list1 = [['Mean', Mean_df_E, Mean_df_L, Mean_df_w, Mean_df_l, Mean_df_A]]
    list2 = [['Std', Std_df_E, Std_df_L, Std_df_w, Std_df_l, Std_df_A]]
    df1 = pd.DataFrame(data=list1, columns=column1)
    df2 = pd.DataFrame(data=list2, columns=column1)
    df = df.append(df1, ignore_index=True)
    df = df.append(df2, ignore_index=True)

    st.write(df)

    p = figure(
        title='Scatter plot',
        x_axis_label='Predicted Width (nm)',
        y_axis_label='Predicted Length (nm)')

    p.scatter(wexp_y_pred, lexp_y_pred, size=5)
    st.bokeh_chart(p, use_container_width=True)

    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
