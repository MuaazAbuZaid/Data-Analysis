# importing neede libraries
import streamlit as st
import sys

# Directing to MEDA file path to be able to import it
# sys.path.append( 'D:\Moaaz\Programming\Epsilon_Data_Science_Diploma\Mid_Project' ) # Path of MEDA file
import MEDA as md

# Title
st.markdown(" <center>  <h1> Superstore Dataset </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

# Link of Data
st.markdown('<a href="https://www.kaggle.com/datasets/vivek468/superstore-dataset-final"> <center> Link to Dataset  </center> </a> ', unsafe_allow_html=True)

# Load data
df = md.df_source

# Show data
st.write(df)

