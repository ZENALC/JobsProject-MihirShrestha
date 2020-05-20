# Old school project. Not updated anymore.

## Requirements: 
JSON, time, pytest, os, beautifulsoup4, dash, plotly, geopy,
requests, pytest, feedparser, pandas, pymongo

## Brief Summary: 
The code retrieves job postings from GitHub and StackOverFlow and dumps it to a 
file called 'json.txt', a database called "jobs.db", and a mongo database. There are also several tests in the Tests 
folder that ensure the code works as intended. As of sprint 4, a new GUI has been implemented where
it shows the locations in an interactive map. Filters can be now applied through the GUI to filter
through companies, job technologies, locations, and dates the jobs were missing.

# What is missing: 
The database still can contain outdated data as it does not delete non-existent, old records.
However, a simple deletion of the db file takes care of this issue. 

UPDATE: Github actions work fine now, and a more appropriate manner of dumping JSON data has been implemented.\
UPDATE: Functionality to save to an SQLITE3 database has been implemented.\
UPDATE: Functionality to display and filter the data in a GUI (dash) has been implemented.\
UPDATE: Functionality to save to a NoSQL database like MongoDB has been added.\
UPDATE: For my additional filter, I picked location. Albeit not as elegant as I'd like it to be, it
uses SQL and the LIKE command to find locations that match the text entered. I'll update this accordingly
for the extra credit problem within the next few days.\
UPDATE: Now, the program supports two location filters; if you want to locate NY jobs, you can just
type in NY, and it'll show you NY jobs (and other jobs that have "ny" as part of its location). Or, 
if you want to find jobs that are within a certain radius from Bridgewater, that functionality has
been implemented as well! Since the layout is not important for this project, it looks very simple,
but overall the logic and functionality should be pretty sound. 
