######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import numpy as np

#import gtd data

df = pd.read_csv('gtd.csv')
country_list=list(df['country'].value_counts().sort_index().index)

print(country_list)

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
