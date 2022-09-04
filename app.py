# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 20:16:24 2022

@author: admin

https://discuss.streamlit.io/t/include-an-existing-html-file-in-streamlit-app/5655/3
"""

import streamlit as st
import streamlit.components.v1 as components 

# >>> import plotly.express as px
# >>> fig = px.box(range(10))
# >>> fig.write_html('test.html')

st.header("test html import")

def uploader_cb():
    print("Dummy callback for file uploader")

# define: file variables with streamlit
htmlFile = st.file_uploader("html file for display", type = 'html', on_change = uploader_cb())
if htmlFile is None:
    st.stop()  
    
# source_code = htmlFile.getvalue()
# st.write(source_code)

# source_code = open(htmlFile, 'r', encoding='utf-8')
source_code = htmlFile.getvalue().decode('utf-8')
# source_code = htmlFile.read()
# source_code = open(htmlFile)
# st.write(source_code)
components.html(source_code, height=1000)
# components.iframe('file:///Z:/CAD/Autodesk/RVT/Dynamo/Dynamo%202_X/github/pyvista_streamlit/pyvista%20(5)/pyvista%20(5).html', height=1000)