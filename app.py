import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sqlite3
import pandas as pd
from datetime import datetime as dt
import jobs
import os
from geopy import distance
from geopy import Point

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


# Query that returns a new data frame from an SQL argument
def query(arg="SELECT * FROM jobs"):
    databaseConnection = sqlite3.connect('jobs.db')
    try:
        newDataFrame = pd.read_sql_query(arg, databaseConnection)
    except pd.io.sql.DatabaseError:
        newDataFrame = None
    databaseConnection.close()
    return newDataFrame


def query_by_distance(dataFrame, radius):
    queryList = dataFrame.to_dict('records')
    newList = []
    bridgeWaterLatitude = 41.9904
    bridgeWaterLongitude = 70.9751

    for row in queryList:
        latitude = row['geo_latitude']
        longitude = row['geo_longitude']
        if latitude is None or longitude is None:
            continue
        if is_inside_radius(bridgeWaterLatitude, bridgeWaterLongitude,
                            abs(float(latitude)), abs(float(longitude)), radius):
            newList.append(row)
    return pd.DataFrame(newList)


# Function that returns more details about a job and/or more jobs if they exist at the same coordinate.
def return_more_job_information(lon, lat):
    totalString = []
    temp_data_frame = query("SELECT * FROM JOBS WHERE JOBS.GEO_LONGITUDE = '{}' "
                            "AND JOBS.GEO_LATITUDE = '{}'".format(lon, lat))
    titles = temp_data_frame["Title"]
    descriptions = temp_data_frame['Description']
    datesPosted = temp_data_frame['Created_at']
    for index in range(len(titles)):
        totalString += [index + 1, ") ", "Date posted: ", datesPosted[index], html.Br(), "Title: ", titles[index],
                        html.Br(),
                        "Description: ", descriptions[index], html.Br(), html.Br()]
    return totalString


# Function that returns a new map box figure each there a new query is posed.
def return_figure(data_frame):
    figure = go.Figure(data=go.Scattermapbox(
        lon=data_frame['geo_longitude'],
        lat=data_frame['geo_latitude'],
        text="Job Description: " + data_frame['Description'].str.slice(0, 75) + "</br>"
             + data_frame['Description'].str.slice(75, 150) + "..."
             + "</br>Location: " + data_frame['Location']
             + "</br>Job Title: " + data_frame['Title']
             + "</br>Company: " + data_frame['Company']
             + "</br>Click on data and scroll down for more details and jobs at this location!",
        mode='markers',
    ))

    figure.update_layout(
        mapbox_style="open-street-map",
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'zoom': 1})

    return figure


def is_inside_radius(latitude1, longitude1, latitude2, longitude2, radius):
    if latitude1 is not None and longitude1 is not None and latitude2 is not None and longitude2 is not None:
        point1 = Point(latitude1, longitude1)
        point2 = Point(latitude2, longitude2)
        result = distance.distance(point1, point2).miles

        if result <= radius:
            return True
    return False


# Just a simple function that checks if a table named jobs already exists. If it exists,
# then a prompt is given out whether or not to run jobs.main()
def check_if_exists():
    found = False
    if query("SELECT geo_longitude, geo_latitude FROM JOBS") is not None:
        found = True
    else:
        if os.path.exists("jobs.db"):
            os.remove("jobs.db")

    answer = ''
    if found:
        while answer.lower() not in ['y', 'n']:
            answer = input("Database found before initialization. Would you like to skip finding jobs? Y or N>>")
    if found and answer == 'n' or not found:
        print("Initializing data from jobs...")
        jobs.main()


# Callback function for filtering data.
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='locationInput', component_property='value'),
     Input(component_id='locationByDistanceInput', component_property='value'),
     Input(component_id='techInput', component_property='value'),
     Input(component_id='companyInput', component_property='value'),
     Input(component_id='datePick', component_property='start_date'),
     Input(component_id='datePick', component_property='end_date')])
def update_output_div(map_input, location_by_distance_input, tech_input, company_input, start_date, end_date):
    temporaryDF = query("SELECT * FROM jobs WHERE UPPER(jobs.description) "
                        "LIKE '%{}%' AND UPPER(jobs.location) LIKE '%{}%' AND "
                        "julianday('{}') <= julianday(jobs.Created_At) AND "
                        "julianday('{}') >= julianday(jobs.Created_At) AND "
                        "UPPER(jobs.Company)  LIKE '%{}%';".format(
                         tech_input.upper(), map_input.upper(), start_date, end_date, company_input.upper()))

    if location_by_distance_input is not None and location_by_distance_input != '':
        secondTempDF = query_by_distance(temporaryDF, float(location_by_distance_input))
        if secondTempDF.empty:
            # Running an extremely weird and unefficent code to retrieve an empty dataframe with columns.
            temporaryDF = query("SELECT * FROM JOBS WHERE JOBS.LOCATION = 'IJADIJAIDJA';")
        else:
            temporaryDF = secondTempDF
    return return_figure(temporaryDF)


# Callback function for retrieving more information on jobs.
@app.callback(
    Output('additionalInfo', 'children'),
    [Input('map', 'clickData')])
def display_click_data(click_data):
    if click_data is not None:
        moreData = click_data['points'][0]
        lon, lat = moreData['lon'], moreData['lat']
        return return_more_job_information(lon, lat)
    else:
        return "No data selected. Please make sure to click on a data point to view more jobs in that area."


if __name__ == '__main__':
    app.title = "Jobs Map Filter"
    check_if_exists()
    app.layout = html.Div([
        html.H5(
            children='Welcome to the job seeking tool.',
            style={
                'textAlign': 'center',
            }
        ),

        html.Label(children='Filter Location - eg. Boston, MA'),
        dcc.Input(id='locationInput', value='', type='text'),

        html.Label(children='Filter Distance in Miles from Bridgewater'),
        dcc.Input(id='locationByDistanceInput', value='', type='number'),

        html.Label(children='Filter Job Technology - eg. Python'),
        dcc.Input(id='techInput', value='', type='text'),

        html.Label(children='Filter Job Company - eg. Facebook'),
        dcc.Input(id='companyInput', value='', type='text'),

        html.Label('Filter jobs by date.'),
        dcc.DatePickerRange(
            id="datePick",
            start_date=dt(2020, 1, 1),
            end_date=dt.today(),
            display_format='MMM Do, YYYY',
            start_date_placeholder_text='Start Period',
            end_date_placeholder_text="End Period",
        ),

        html.Br(),

        dcc.Graph(
            id="map",
            figure=return_figure(query()),
        ),

        html.H4(children="More Details"),
        html.Label(id="additionalInfo", children="No data selected. Please make sure to click on a "
                                                 "data point to view more jobs in that area.")

    ])
    app.run_server(debug=True, use_reloader=False)
