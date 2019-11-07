######### Import libraries #######
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import numpy as np

########## import gtd data
df = pd.read_csv('gtd.csv')

########### define variables
total_attacks = df['eventid'].value_counts()
group_list = list(df['group'].value_counts().sort_index().index)
country_list = list(df['country'].value_counts().sort_index().index)


########## manipulate data
df['newdate'] = pd.to_datetime(df['date'])
df['year'] = df['newdate'].dt.year
df['year'] = df['year'].astype(int)

year_attacks = df.groupby(['year'])['eventid'].count()
year_totals = df.groupby(['year'])['eventid'].count()

########## Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Terrorism'


######### layout

app.layout = html.Div(children=[
    html.H1('Terrorist Attacks: 2002-2018'),
#     html.Br(),
#     html.H5("This dataset comes from the University of Maryland's Global Terrorism Database. It identifies 116,912 attacks since 2002."),
#     html.Br(),
    html.H3('Filter by group'),
    dcc.Dropdown(
        id='dropdown_groups',
        options=[{'label': i, 'value': i} for i in group_list],
        value='Islamic State of Iraq and the Levant (ISIL)'
    ),
    dcc.Graph(id='group-display'),
    html.Br(),
    html.H3('Filter by year'),
    dcc.Slider(
        id='slider',
        min=2002,
        max=2018,
        step=1,
        marks={i:str(i) for i in range(2002,2019)},
        value=2002
    ),
    html.Br(),
    dcc.Graph(id='year-display'),
    html.Br(),
    html.A('Code on Github', href='https://github.com/dwb217/gtd-map'),
    html.Br(),
    html.A('Source:', href='https://www.start.umd.edu/data-tools/global-terrorism-database-gtd')
])

######### app callback 1 map by group

@app.callback(dash.dependencies.Output('group-display', 'figure'),
              [dash.dependencies.Input('dropdown_groups', 'value')])
def group_picker(group_id):
    group_df=df[df['group']==group_id]
    fig = go.Figure(go.Densitymapbox(lat=group_df['latitude'], lon=group_df['longitude'], z=total_attacks, radius=7))
    fig.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lon=0,
                  mapbox_center_lat=0,
                  mapbox_zoom=1,
                 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


########## app callback 2 map by year slider

@app.callback(dash.dependencies.Output('year-display', 'figure'),
              [dash.dependencies.Input('slider', 'value')])
def year_picker(year_id):
    year_df=df[df['year']==year_id]
    fig1 = go.Figure(go.Densitymapbox(lat=year_df['latitude'], lon=year_df['longitude'], z=total_attacks, radius=3))
    fig1.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lon=0,
                  mapbox_center_lat=0,
                  mapbox_zoom=1,
                 )
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig1

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
