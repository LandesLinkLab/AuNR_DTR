# SPP App Version 1.2

![TOC](https://user-images.githubusercontent.com/23239448/118331280-02501f00-b4ce-11eb-9baf-7b117e16adff.png)

This web-based GUI allows you to predict AuNR width and length using our trained decision-tree model.

Available on [HERE](https://goldnanorod-size-predictor.streamlit.app)

## **Reference**
When publishing results obtained with the SPP App, we ask you to cite the following paper:

    K. Shiratori and L. D. C. Biship, B. Ostovar, R. Baiyasi, Y.-Y. Cai, P. J. Rossky, C. F. Landes, and S. Link, J. Phys. Chem. C, 125, 19353-19361 (2021).

## **How to use**

![GUI1](https://user-images.githubusercontent.com/23239448/118331287-054b0f80-b4ce-11eb-93d4-59ea846eeeeb.png)

1.	Instruction for this GUI.
2.	Training data conditions: substrate and surrounding.
3.	File uploader for .csv file containing “E_res” and “Linewidth” as the first row. 
4.	Prediction button to obtain predicted width and length. 

![GUI2](https://user-images.githubusercontent.com/23239448/118331295-0714d300-b4ce-11eb-9003-4bf9515890bd.png)

3.	After uploading a file, data is displayed.
4-1.	After pressing “Prediction”, predicted sizes and statistical results are shown in this chart.  

![GUI3](https://user-images.githubusercontent.com/23239448/118331301-09772d00-b4ce-11eb-86bc-48f18f9312fc.png)

4-2.	Interactive scatter plot of predicted width and length.
4-3.	Option to download all predicted results in .csv file.

