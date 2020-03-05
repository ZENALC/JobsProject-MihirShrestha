# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sqlite3
import pandas as pd

databaseConnection = sqlite3.connect('jobs.db')
df = pd.read_sql_query("SELECT * FROM jobs", databaseConnection)
databaseConnection.commit()
databaseConnection.close()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Jobs Map Filter"
app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),

    dcc.Graph(
        figure=go.Figure(data=go.Scattergeo(
            lon=df['geo_longitude'],
            lat=df['geo_latitude'],
            text=str(df['Description'])[:20],
            mode='markers',
        ))
    ),
    ]
)


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')])
def update_output_div(input_value):
    return 'You typed in "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
