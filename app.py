import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sqlite3
import pandas as pd
from datetime import datetime as dt


def query(arg="SELECT * FROM jobs"):
    databaseConnection = sqlite3.connect('jobs.db')
    newDataFrame = pd.read_sql_query(arg, databaseConnection)
    databaseConnection.close()
    return newDataFrame


def return_figure(data_frame):
    figure = go.Figure(data=go.Scattermapbox(
        lon=data_frame['geo_longitude'],
        lat=data_frame['geo_latitude'],
        text="Job Description: " + data_frame['Description'].str.slice(0, 75) + "</br>"
             + data_frame['Description'].str.slice(75, 170) + "..."
             + "</br>Location: " + data_frame['Location']
             + "</br>Job Title: " + data_frame['Title']
             + "</br>Company: " + data_frame['Company'],
        mode='markers',
    ))

    figure.update_layout(
        mapbox_style="open-street-map",
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'zoom': 1})

    return figure


df = query()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Jobs Map Filter"
app.layout = html.Div([
    html.Label('Filter Location'),
    dcc.Input(id='locationInput', value='', type='text'),
    html.Div(id='my-div1'),

    html.Label('Filter Job Technology'),
    dcc.Input(id='techInput', value='', type='text'),
    html.Div(id='my-div2'),

    html.Label('Filter Job Company'),
    dcc.Input(id='companyInput', value='', type='text'),
    html.Div(id='my-div3'),

    html.Label('Pick your date.'),
    dcc.DatePickerRange(
        id="datePick",
        start_date=dt(2020, 1, 1),
        end_date=dt.today(),
        display_format='MMM Do, YYYY',
        start_date_placeholder_text='Start Period',
        end_date_placeholder_text="End Period",
    ),

    dcc.Graph(
        id="map",
        figure=return_figure(df),
    )],

)


@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='locationInput', component_property='value'),
     Input(component_id='techInput', component_property='value'),
     Input(component_id='companyInput', component_property='value'),
     Input(component_id='datePick', component_property='start_date'),
     Input(component_id='datePick', component_property='end_date')])
def update_output_div(map_input, tech_input, company_input, start_date, end_date):
    temporaryDF = query("SELECT * FROM jobs WHERE UPPER(jobs.description) "
                        "LIKE '%{}%' AND UPPER(jobs.location) LIKE '%{}%' AND "
                        "julianday('{}') <= julianday(jobs.Created_At) AND "
                        "julianday('{}') >= julianday(jobs.Created_At) AND "
                        "UPPER(jobs.Company)  LIKE '%{}%';".format(
                         tech_input.upper(), map_input.upper(), start_date, end_date, company_input.upper()))
    return return_figure(temporaryDF)


if __name__ == '__main__':
    app.run_server(debug=True)
