import streamlit as st
import os
import pandas as pd
from functions import displayPDF, create_pdf, save_pdf 
import numpy as np
from num2words import num2words

st.set_page_config(layout="wide")

# get file
def set_data_df(filepath):
    csv = filepath
    df = pd.read_csv(csv, index_col=False)

    # important variables
    name = df['name'].astype('str')
    search_name = df['name'].astype('str').str.lower()
    month = df['month'].astype('str')
    search_month = df['month'].astype('str').str.lower()
    year = df['year'].astype('str')
    employee_id = df['id'].astype('str')
    designation = df['designation'].astype('str')
    date_of_leaving = df['date_of_leaving']
    net_salary = df['net_salary'].astype('str')
    incentive_pay = df['incentive_pay'].astype('str')

    options_month = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October",
                "November", "December"]
    options_name = df['name'].str.lower().str.capitalize().unique()



    df['date'] = month + '-' + year

    return df

in_data, unused, pdf_data = st.columns([3,1,8])

with in_data:
    uploaded_csv = st.file_uploader("Upload CSV here: ", accept_multiple_files=False, type = ['csv'] )
    # st.text(type(uploaded_csv))

    uploaded_csv_path = "CSVs/uploaded.csv"

    if uploaded_csv is not None:
        with open(uploaded_csv_path, "wb") as f:
            f.write(uploaded_csv.getbuffer())


    
    if (os.path.exists(uploaded_csv_path)) & (uploaded_csv is not None):
        csv = uploaded_csv_path
        df = pd.read_csv(csv, index_col=False)

        st.write(df)

        # important variables
        name = df['name'].astype('str')
        search_name = df['name'].astype('str').str.lower()
        month = df['month'].astype('str')
        search_month = df['month'].astype('str').str.lower()
        year = df['year'].astype('str')
        employee_id = df['id'].astype('str')
        designation = df['designation'].astype('str')
        date_of_leaving = df['date_of_leaving']
        net_salary = df['net_salary'].astype('str')
        incentive_pay = df['incentive_pay'].astype('str')

        options_month = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October",
                    "November", "December"]
        options_name = df['name'].str.lower().str.capitalize().unique()
        df['date'] = month + '-' + year





        def name_changed():
            st.session_state["name"] = f"{st.session_state['selected_name']}"

        selected_name = st.selectbox(
            "Employee Name",
            options_name,
            key="selected_name",  # Store value in session_state
            on_change=name_changed, # Call function when selection changes
            placeholder = "Choose Employee Name",
            index = None,
        )
        selected_name_changed = st.session_state.get("name", "Make a selection")
        dates_options = df['date'][search_name == selected_name_changed.lower()]
        selected_dates = st.multiselect('Choose Date(s)', options=dates_options)
    



        pdf_names = []
        for dates in selected_dates:
                data_in = pd.DataFrame()
                date_sep = dates.split('-')
                curr_month = date_sep[0]
                curr_year = date_sep[1]
                data_in = df[(search_name == selected_name_changed.lower()) & (search_month == curr_month.lower()) & (year == curr_year)]
                
                # st.text(type(data_in['name']))
                data_dic = {}
                for col in data_in.columns:
                    data_dic[f"{col}"] = data_in[col].iloc[0]
                data_in['gross_salary'] = float(data_in['net_salary']) + float(data_in['incentive_pay'])
                data_in['date_of_leaving'] = data_in['date_of_leaving'].fillna("-")
                data_dic['gross_salary'] = data_in['gross_salary'].iloc[0]
                data_dic['amount_in_words'] = num2words(data_in['gross_salary'].iloc[0]).title()

                pdf_name = create_pdf(data_dic)
                pdf_names.append(pdf_name)

        save_pdf(pdf_names)

    else:
         pass

# show pdf/s

file = "PDFs/output.pdf"

with pdf_data:
    if os.path.exists(file):
        displayPDF(file)
    else:
        file = "PDFs/test.pdf"
        displayPDF(file)


    

