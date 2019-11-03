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

########## Define the figure

fig = go.Figure(go.Densitymapbox(lat=df['latitude'], lon=df['longitude'], z=df['fatalities'], radius=10))
fig.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lon=0,
                  mapbox_center_lat=0,
                  mapbox_zoom=1,
                 )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Terrorist attacks'),
    html.Div([
        dcc.Graph(id='figure-1', figure=fig),
        html.A('Code on Github', href='https://github.com/dwb217/dash-density-heatmap'),
        html.Br(),
        html.A('Source:', href='https://plot.ly/python/mapbox-density-heatmaps')
    ])
])



######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
