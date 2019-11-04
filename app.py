######### Import your libraries #######
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
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
total_attacks = df['eventid'].value_counts()
group_name = df['group']
group_list = list(df['group'].value_counts().sort_index().index)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Terrorism'

########## Define the figure

fig = go.Figure(go.Densitymapbox(lat=df['latitude'], lon=df['longitude'], z=total_attacks, radius=5))
fig.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lon=0,
                  mapbox_center_lat=0,
                  mapbox_zoom=1,
                 )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Terrorist Attacks: 2002-2018'),
    dcc.Graph(id='figure-1', figure=fig),
    html.Br(),
    html.H3('Filter by group:'),
    html.Br(),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in group_list]
    ),
    dcc.Graphic(id='group-display'),
    html.Br(),            
    html.A('Code on Github', href='https://github.com/dwb217/gtd-map'),
    html.Br(),
    html.A('Source:', href='https://www.start.umd.edu/data-tools/global-terrorism-database-gtd')
])

### app callback #1

@app.callback(dash.dependencies.Output('group_display', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def group_picker(group_id):
    group_df=df[df['group']==group_id]
    fig = go.Figure(go.Densitymapbox(lat=group_df['latitude'], lon=group_df['longitude'], z=total_attacks, radius=5))
    fig.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lon=0,
                  mapbox_center_lat=0,
                  mapbox_zoom=1,
                 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
  

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
