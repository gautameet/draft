import math
import streamlit as st
import altair as alt              # for data visualtization
#import sklearn
#from sklearn.preprocessing import StandardScaler
#from sklearn.neighbors import NearestNeighbors
#from sklearn.neighbors import KNeighborsClassifier
from PIL import Image
import requests
import matplotlib.pyplot as plt
#import plotly
import os
from zipfile import ZipFile, BadZipFile
import pickle
import sys
#import shap

# Features
feat = ['SK_ID_CURR','TARGET','DAYS_BIRTH','NAME_FAMILY_STATUS','CNT_CHILDREN',
        'DAYS_EMPLOYED','NAME_INCOME_TYPE','AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY']

# Nombre de ligne
num_rows = 100000





###
## Page configuration initialisation
st.set_page_config(
    page_title="Credit Score Dashboard",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded")
    
# Sidebar
with st.sidebar:
    st.title("Credit Score Dashboard")
    logo_path = "logo.png"
    try:
        logo = Image.open(logo_path)
        st.image(logo, width=250)
    except FileNotFoundError:
        st.error(f"Error: Logo file not found at {logo_path}")

 # Page selection
    page =  st.selectbox("Menu", ["Home", "Customer", "Customer portfolio"])
    
    st.markdown("-----")
        
    st.write("By: Amit GAUTAM")

if page == "Home":
    st.title("💵 Credit Score Dashboard - Customer Page")
    ".\n"
    #.\n"
        
    st.markdown("This is an interactive dashboard website which lets the clients to know about their credit demands\n"
                "approved ou refused. The predictions are calculted automatically with the help of machine learning algorithm.\n"
                                    
                "\nThis dashboard is composed of following pages :\n"
                "- **Customer**: to find out all the information related to the customer.\n")

if page == "Customer":
    st.title("💵 Welcome to the Customer Page")
    ".\n"
    ".\n"
        
    st.header("Welcome to the customers' page.\n")
    ".\n"
    st.subheader("Please enter your ID to know the results of your demands. \n")

    st.markdown("Your ID:")
    ID=st.number_input(" ", min_value=100002, max_value=456255)
    try:
        raw_app_id = get_data(raw_app, ID)
        with st.spinner('Custumer....'):
            st.writer('Customer .....')
            with st.container():
                col1, col2 = st.columns([1.5,2.5])      
                with col1:
                    st.write("#### Customer detail " + str(ID))
                    st.markdown("* **Status : " + str(id_raw_app['NAME_FAMILY_STATUS'].values[0]) + "**")
                    st.markdown("* **Number of children) : " + str(id_raw_app['CNT_CHILDREN'].values[0]) + "**")
                    st.markdown("* **Employment: " + str(id_raw_app['NAME_INCOME_TYPE'].values[0]) + "**")
                    st.markdown("* **Current Loan : " + str(id_raw_app['CREDIT'].values[0]) + "**")
                with col2:
                    fig = plt.figure(figsize=(2,2))
                    st.pyplot(radat_id_plot(ID,fig))
            st.markdown("-----")

            with st.container():
                    st.write("#### Similar type of Customers ")
                    try:
                        col3, col4 = st.columns([3,1])
                        with col3:
                            fig = plt.figure(figsize=(3,3))
                            st.pyplot(radat_knn_plot(ID,fig))
                        with col4:
                            N_knn, N_knn1 = get_stat_ID(ID)
                            st.markdown("* **Similar type of customers : " + str(N_knn) + "**")
                            st.markdown("* **Customer having payment problem : " + str(N_knn1) + "**")                
                            st.markdown("_(either " + str(N_knn1*100/N_knn) + "% clients with similar payment problems)_")
                    except:
                        st.info('**_No similar customer_**')
            st.markdown("-----")
            with st.container():
                st.write("#### Customer solvability prediction ")
                pred = st.button('Calculation')
                if pred:
                    with st.spinner('Calculation...'):
                        try:
                            prediction = requests.get("https://urd9pbjwdlnjfnaoncmtdw.streamlit.app/predict?ID=" + str(ID)).json()
                            if prediction["target"]==0:
                                st.write(':smiley:')
                                st.success('Client solvable _(Target = 0)_, prediction difficult level at **' + str(prediction["risk"] * 100) + '%**')
                            elif prediction["target"]==1:
                                st.write(':confused:')
                                st.error('Client non solvable _(Target = 1)_, prediction difficult level at **' + str(prediction["risk"] * 100) + '%**')  
                            st.write('**Interpretability**')
                            fig = plt.figure(figsize=(2,2))
                            st.pyplot(shap_id(ID))
                        except :
                            st.warning('programme error programme') 
                            st.write(':dizzy_face:')             
    
    except:
        st.warning('**_Customer not found_**')

# Customer portfolio analysis        
if page == 'Customer portfolio':
    st.header("💵 Welcome to Customer portfolio analysis")
    with st.spinner('Analysing...'):
        with st.container():            
            st.write("#### Customer Profile")
            col1, col2,col3 = st.columns(3)
            #plt.ioff()
            with col1:
                fig = plt.figure(figsize=(4,4))
                bins = (raw_app['AGE'].max()-raw_app['AGE'].min())//5
                pt = sns.histplot(data=raw_app, x='AGE', hue='TARGET',bins=bins,palette=['royalblue','red'],alpha=.5)
                plt.xlabel('AGE',fontsize=12)
                plt.ylabel('')
                plt.legend(['having difficulty','without difficulty'],loc='lower center',bbox_to_anchor=(0.5, -0.35),fancybox=True, shadow=True, ncol=5)
                st.pyplot(fig)

            with col2:
                fig = plt.figure(figsize=(3,3))                
                pt = sns.barplot(raw_app['NAME_FAMILY_STATUS'][raw_app['TARGET']==1],raw_app['CNT_CHILDREN'][raw_app['TARGET']==1],color='red',alpha=.5,ci=None,edgecolor='black')
                pt = sns.barplot(raw_app['NAME_FAMILY_STATUS'][raw_app['TARGET']==0],raw_app['CNT_CHILDREN'][raw_app['TARGET']==0],color='royalblue',alpha=.5,ci=None,edgecolor='black')
            #pt = sns.barplot(x='NAME_FAMILY_STATUS', y='CNT_CHILDREN', hue='TARGET', data=raw_app,palette=['royalblue','red'],alpha=.7)
                plt.setp(pt.get_xticklabels(),rotation=45,fontsize=7)
                plt.setp(pt.get_yticklabels(),fontsize=5)
                st.pyplot(fig)
            with col3:
                fig = plt.figure(figsize=(4.5,4.5))
                pt = sns.barplot(raw_app['NAME_INCOME_TYPE'][raw_app['TARGET']==1],raw_app['AMT_INCOME_TOTAL'][raw_app['TARGET']==1],color='red',alpha=.5,ci=None,edgecolor='black')
                pt = sns.barplot(raw_app['NAME_INCOME_TYPE'][raw_app['TARGET']==0],raw_app['AMT_INCOME_TOTAL'][raw_app['TARGET']==0],color='royalblue',alpha=.5,ci=None,edgecolor='black')
                #pt = sns.barplot(x='NAME_INCOME_TYPE', y='AMT_INCOME_TOTAL', hue='TARGET', data=raw_app,palette=['royalblue','red'],alpha=.7)
                plt.setp(pt.get_xticklabels(),rotation=45,fontsize=7)
                plt.setp(pt.get_yticklabels(),fontsize=7)
                st.pyplot(fig)
        
            st.markdown("-----")

        with st.container():
            st.write("#### Loan Payment")
            tg_n = np.array([len(raw_app[raw_app['TARGET']==1]),len(raw_app[raw_app['TARGET']==0]),len(raw_app[raw_app['TARGET'].isnull()])])            
            col4, col5 = st.columns(2)
            with col4:
                fig = plt.figure(figsize=(5,5))
                plt.pie(tg_n,labels=['having difficulty','without difficulty','No Loan outstanding'],colors=['red','royalblue','honeydew'],autopct=lambda x:str(round(x,2))+'%')
                st.pyplot(fig)
            with col5:
                df = raw_app[['TARGET','NAME_INCOME_TYPE','AMT_ANNUITY','AMT_CREDIT']]
                df['COUNT_TG'] = df['TARGET']
                tg_df = pd.concat((df.groupby(['TARGET','NAME_INCOME_TYPE']).mean()[['AMT_ANNUITY','AMT_CREDIT']],df.groupby(['TARGET','NAME_INCOME_TYPE']).count()[['COUNT_TG']]), axis = 1)
                tg_0 = tg_df.loc[0]
                tg_1 = tg_df.loc[1]
                fig = plt.figure(figsize=(2,2))                  
                pt = sns.scatterplot(tg_1['AMT_ANNUITY'],tg_1['AMT_CREDIT'],s=tg_1['COUNT_TG'].values/100,label='Avec Difficulté',color='red')
                pt = sns.scatterplot(tg_0['AMT_ANNUITY'],tg_0['AMT_CREDIT'],s=tg_0['COUNT_TG'].values/100,label='Sans Difficulté',color='royalblue',alpha=.3)
                plt.legend(loc='lower center',bbox_to_anchor=(0.5, -0.3),fancybox=True, shadow=True, ncol=5,fontsize=5)
                plt.xlabel('AMT_ANNUITY',fontsize=5)
                plt.ylabel('AMT_CREDIT',fontsize=5)
                plt.xlim([20000,40000])
                plt.ylim([400000,800000])
                plt.setp(pt.get_xticklabels(),fontsize=4)
                plt.setp(pt.get_yticklabels(),fontsize=4)                
                st.pyplot(fig)
            
        
