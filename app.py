import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sqlite3
import pandas as pd


def query(arg="SELECT * FROM jobs"):
    databaseConnection = sqlite3.connect('jobs.db')
    newDataFrame = pd.read_sql_query(arg, databaseConnection)
    databaseConnection.close()
    return newDataFrame


def returnFigure(dataFrame):
    return go.Figure(data=go.Scattergeo(
        lon=dataFrame['geo_longitude'],
        lat=dataFrame['geo_latitude'],
        text=dataFrame['Company'] + " located at " + dataFrame['Location'],
        mode='markers',
    ))


df = query()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Jobs Map Filter"
app.layout = html.Div([
    html.Label('Filter Location'),
    dcc.Input(id='locationInput', value='World', type='text'),
    html.Div(id='my-div'),

    html.Label('Filter Job Technology'),
    dcc.Input(id='techInput', value='', type='text'),
    html.Div(id='my-div2'),

    html.Label('Age of Posting'),
    dcc.Input(id='ageInput', value='', type='text'),
    html.Div(id='my-div3'),

    dcc.Graph(
        id="map",
        figure=returnFigure(df)
    ),
    ]
)


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='locationInput', component_property='value'),
     Input(component_id='techInput', component_property='value')])
def update_output_div(mapInput, techInput):
    if len(mapInput) == 0 or mapInput == "World":
        return returnFigure(df)

    temporaryDF = query("SELECT * FROM jobs WHERE UPPER(jobs.description) "
                        "LIKE '%{}%' AND UPPER(jobs.location) LIKE '%{}%';".format(
                         techInput.upper(), mapInput.upper()))
    return returnFigure(temporaryDF)


if __name__ == '__main__':
    app.run_server(debug=True)
