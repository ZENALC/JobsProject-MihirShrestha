# Author: Mihir Shrestha
import requests
import time
import json
import sqlite3


# Main function that calls the retrieve_jobs(), save_to_database() and dump_data() functions.
def main():
    WRITE_TO_FILE = True
    UPDATE_DATABASE = True
    jobs = retrieve_jobs()

    if UPDATE_DATABASE:
        save_to_database(jobs)

    if WRITE_TO_FILE:
        fileName = "json.txt"
        dump_data(jobs, fileName)


# Function that retrieves the jobs from GitHub. It has a sleep function implemented,
# so that the program doesn't shoot all the requests at once to GitHub. It also checks
# if it received a 200 response code or not and reports the code back to the user if it is not 200.
def retrieve_jobs():
    missedList = []
    jsonData = []
    for num in range(1, 6):
        url = "https://jobs.github.com/positions.json?page=" + str(num)
        response = requests.get(url)
        if response.status_code == 200:
            newJsonData = response.json()
            jsonData += newJsonData
        else:
            print("Received response: {} for page {}.".format(response.status_code, num))
            missedList.append(num)
        time.sleep(1)
    if len(missedList) > 0:
        print("Missed data for pages {}.".format(str(missedList)[1:-1]))
    else:
        print("Successfully retrieved data from all pages.")
    return jsonData


# Simple function that dumps JSON data to a .txt file.
def dump_data(jobs, file_name):
    with open(file_name, 'w') as openFile:
        for job in jobs:
            json.dump(job, openFile)
    print("Successfully dumped JSON data to {}.".format(file_name))


# Simple function that dumps data to its corresponding column in the jobs.db database.
def save_to_database(jobs):
    if not (type(jobs) is list or type(jobs) is dict):
        return None
    if type(jobs) is dict:
        jobs = [jobs]
    connection = sqlite3.connect('jobs.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
                   id TEXT PRIMARY KEY,
                   Position_Type TEXT,
                   URL TEXT,
                   Created_at TEXT,
                   Company TEXT,
                   Company_URL TEXT,
                   Location TEXT,
                   Title TEXT,
                   Description TEXT,
                   How_To_Apply TEXT,
                   Company_Logo TEXT
                    )''')
    for job in jobs:
        if len(job) != 11:
            return None
        try:
            cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [job['id'],
                                                                                         job['type'],
                                                                                         job['url'],
                                                                                         job['created_at'],
                                                                                         job['company'],
                                                                                         job['company_url'],
                                                                                         job['location'],
                                                                                         job['title'],
                                                                                         job['description'],
                                                                                         job['how_to_apply'],
                                                                                         job['company_logo'],
                                                                                         ])
        except sqlite3.IntegrityError:
            print("Insertion failed.")
        connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
