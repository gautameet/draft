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
    st.write("Credit Score Dashboard")
    logo_path = "logo.png"
    try:
        logo = Image.open(logo_path)
        st.image(logo, width=250)
    except FileNotFoundError:
        st.error(f"Error: Logo file not found at {logo_path}")
