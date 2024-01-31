import math
import streamlit as st
import altair as alt              # for data visualtization
#import sklearn
#from sklearn.preprocessing import StandardScaler
#from sklearn.neighbors import NearestNeighbors
#from sklearn.neighbors import KNeighborsClassifier
from PIL import Image
import requests
#import plotly
import os
from zipfile import ZipFile, BadZipFile
import pickle
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
    .\n"
        
    st.header("Welcome to the customers' page.\n")
    ".\n"
    st.subheader("Please enter your ID to know the results of your demands. \n") 
