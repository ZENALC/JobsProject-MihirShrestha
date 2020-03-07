Name: Mihir Shrestha

Requirements: JSON, time, pytest, os, beautifulsoup4, dash, plotly, geopy,
requests, pytest, feedparser, pandas

Brief Summary: The code retrieves job postings from GitHub and StackOverFlow and dumps it to a 
file called 'json.txt' and a database called "jobs.db". There are also several tests in the Tests 
folder that ensure the code works as intended. As of sprint 4, a new GUI has been implemented where
it shows the locations in an interactive map. Filters can be now applied through the GUI to filter
through companies, job technologies, locations, and dates the jobs were missing.

What is missing: The database still can contain outddated data as it does not delete non-existent, old records.
However, a simple deletion of the db file takes care of this issue. 

UPDATE: Github actions work fine now, and a more appropriate manner of dumping JSON data has been implemented.
UPDATE: Functionality to save to an SQLITE3 database has been implemented.
UPDATE: Functionality to display and filter the data in a GUI (dash) has been implemented.

For my additional filter, I picked location. Albeit not as elegant as I'd like it to be, it
uses SQL and the LIKE command to find locations that match the text entered. I'll update this accordingly
for the extra credit problem within the next few days. 
