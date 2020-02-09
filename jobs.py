# Author: Mihir Shrestha
from requests import get
from time import sleep
import json
import sqlite3
from typing import Tuple, List, Dict


# Main function that calls the retrieve_jobs(), open_db(), create_table_jobs(),
# save_to_database(), and dump_data() functions.
def main():
    # nice job on sprint one - benign comment to test github actions
    WRITE_TO_FILE = True
    UPDATE_DATABASE = True
    jobs = retrieve_jobs()

    if UPDATE_DATABASE:
        databaseName = 'jobs.db'
        connection, cursor = open_db(databaseName)
        create_table(connection, cursor)
        save_to_database(jobs, connection, cursor)
        close_db(connection)

    if WRITE_TO_FILE:
        fileName = "json.txt"
        dump_data(jobs, fileName)


# Function that retrieves the jobs from GitHub. It has a sleep function implemented,
# so that the program doesn't shoot all the requests at once to GitHub. It also checks
# if it received a 200 response code or not and reports the code back to the user if it is not 200.
# UPDATE: It is now not hard-coded to go up to 5 pages, it keeps looping through until the number
# of jobs is less than 50. Also, a new failCounter has been implemented to reduce the risks for
# an infinite loop. With the failCounter, if one page fails 3 times, then all the following pages' data will
# also not be retrieved.
def retrieve_jobs() -> List[Dict]:
    missedList = []
    jsonData = []

    endOfJobs = False
    num = 1
    failCounter = 0
    # The failCounter is implemented because if GitHub is down or the page does not exist,
    # the loop would never break.

    while not endOfJobs:
        url = "https://jobs.github.com/positions.json?page=" + str(num)
        response = get(url)
        if response.status_code == 200:
            newJsonData = response.json()
            jsonData += newJsonData
            if len(newJsonData) < 50:
                endOfJobs = True
            if num in missedList:
                missedList.remove(num)
                failCounter = 0
        else:
            print("Received response: {} for page {}.".format(response.status_code, num))
            if num not in missedList:
                missedList.append(num)
            failCounter += 1
            if failCounter == 3:
                break
            # Code will try to get data from the page again for 3 attempts. It first sleeps again
            # for a half of a second to give GitHub an idea that we are friendly.
            # If it fails 3 times, it finally breaks out of the loop.
            sleep(.5)
            continue
        sleep(.5)
        num += 1

    if len(missedList) > 0:
        print("Missed data for pages {}.".format(str(missedList)[1:-1]))
    else:
        print("Successfully retrieved data from all pages.")

    return jsonData


# Simple function that dumps JSON data to a .txt file.
def dump_data(jobs: list, file_name: str):
    if not (type(jobs) is list or type(jobs) is dict):
        print("Illegal type of data. {} is of type {}. Please enter a list or dictionary.".format(jobs, type(jobs)))
        return None
    if type(jobs) is dict:
        jobs = [jobs]
    with open(file_name, 'w') as openFile:
        for job in jobs:
            json.dump(job, openFile)
    print("Successfully dumped JSON data to {}.".format(file_name))


# Simple function that dumps data to its corresponding column in the database.
def save_to_database(jobs: list, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    if not (type(jobs) is list or type(jobs) is dict):
        print("Illegal type of data. {} is of type {}. Please enter a list or dictionary.".format(jobs, type(jobs)))
        return None
    if type(jobs) is dict:
        jobs = [jobs]
    for job in jobs:
        if len(job) != 11:
            print("Incorrect number of arguments. Insertion failed.")
            return None
        try:
            cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", [job['id'],
                                                                                          job['type'],
                                                                                          job['url'],
                                                                                          job['created_at'],
                                                                                          job['company'],
                                                                                          job['company_url'],
                                                                                          job['location'],
                                                                                          job['title'],
                                                                                          job['description'],
                                                                                          job['how_to_apply'],
                                                                                          job['company_logo']
                                                                                          ])
        except sqlite3.IntegrityError:
            print("Data already exists in the table.")
    commit_db(connection)
    print("Successfully stored all new JSON data to jobs.db.")


# Simple function that creates a connection with a filename given and returns a connection and cursor.
def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(filename)  # Connects to an existing database or creates a new one.
    cursor = connection.cursor()  # We are now ready to read/write data.
    return connection, cursor


# Simple function that closes a database.
def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


# Simple function that commits changes to a database.
def commit_db(connection: sqlite3.Connection):
    connection.commit()


# Simple function that creates the initial table jobs with its respective columns.
def create_table(connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
                       id TEXT PRIMARY KEY,
                       Position_Type TEXT NOT NULL,
                       URL TEXT NOT NULL,
                       Created_at TEXT NOT NULL,
                       Company TEXT NOT NULL,
                       Company_URL TEXT,
                       Location TEXT NOT NULL,
                       Title TEXT NOT NULL,
                       Description TEXT NOT NULL,
                       How_To_Apply TEXT NOT NULL,
                       Company_Logo TEXT
                        );''')
    commit_db(connection)


if __name__ == "__main__":
    main()
