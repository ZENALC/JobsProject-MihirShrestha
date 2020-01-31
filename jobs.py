# Author: Mihir Shrestha
import requests
import time


# Main function that calls the retrieve_jobs() and dump_data() functions.
def main():
    jobs = retrieve_jobs()
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


# Simple function that dumps JSON data to a txt file.
def dump_data(jobs, file_name):
    with open(file_name, 'w') as openFile:
        for job in jobs:
            openFile.write(str(job))
    print("Successfully dumped JSON data to {}.".format(file_name))


if __name__ == "__main__":
    main()
