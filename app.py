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

def get_table_download_link(df_results):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df_results.to_csv(index=False)
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
    dt_model_width = joblib.load('joblib_width_gs.pkl')
    dt_model_length = joblib.load('joblib_length_gs.pkl')

    predicted_width = dt_model_width.predict(Exp_data)
    predicted_length = dt_model_length.predict(Exp_data)

    df_particle = pd.DataFrame({"Particle": range(1, len(Exp_data['E_res']) + 1)})
    df_e_res = pd.DataFrame({"E_res (eV)": Exp_data['E_res']})
    df_linewidth = pd.DataFrame({"Linewidth (eV)": Exp_data['Linewidth']})
    df_predicted_width = pd.DataFrame({"Predicted Width (nm)": predicted_width})
    df_predicted_length = pd.DataFrame({"Predicted Length (nm)": predicted_length})
    df_aspect_ratio = pd.DataFrame({"Aspect Ratio": predicted_length / predicted_width})
    df_input = pd.concat([df_e_res, df_linewidth], axis=1, sort=True)
    df_output = pd.concat([df_predicted_width, df_predicted_length], axis=1, sort=True)
    df_input_output = pd.concat([df_input, df_output], axis=1, sort=True)
    df_particle_input_output = pd.concat([df_particle, df_input_output], axis=1, sort=True)
    df_results = pd.concat([df_particle_input_output, df_aspect_ratio], axis=1, sort=True)

    df_mean_e_res = Exp_data['E_res'].mean()
    df_mean_linewidth = Exp_data['Linewidth'].mean()
    df_mean_predicted_width = predicted_width.mean()
    df_mean_predicted_length = predicted_length.mean()
    df_mean_aspect_ratio = (predicted_length / predicted_width).mean()

    df_std_e_res = Exp_data['E_res'].std()
    df_std_linewidth = Exp_data['Linewidth'].std()
    df_std_predicted_width = predicted_width.std()
    df_std_predicted_length = predicted_length.std()
    df_std_aspect_ratio = (predicted_length / predicted_width).std()

    column1 = ['Particle', 'E_res (eV)', 'Linewidth (eV)', 'Predicted Width (nm)', 'Predicted Length (nm)',
               'Aspect Ratio']
    list1 = [['Mean', df_mean_e_res, df_mean_linewidth, df_mean_predicted_width, df_mean_predicted_length, df_mean_aspect_ratio]]
    list2 = [['Std', df_std_e_res, df_std_linewidth, df_std_predicted_width, df_std_predicted_length, df_std_aspect_ratio]]
    df_mean = pd.DataFrame(data=list1, columns=column1)
    df_std = pd.DataFrame(data=list2, columns=column1)
    df_results = df_results.append(df_mean, ignore_index=True)
    df_results = df_results.append(df_std, ignore_index=True)

    st.write(df_results)

    fig = figure(
        title='Scatter plot',
        x_axis_label='Predicted Width (nm)',
        y_axis_label='Predicted Length (nm)')
    fig.scatter(predicted_width, predicted_length, size=5)
    st.bokeh_chart(fig, use_container_width=True)

    st.markdown(get_table_download_link(df_results), unsafe_allow_html=True)
