import jobs
import os.path
import random
import sqlite3


# Simple test function that checks if the function returns a list with over 100 items.
def test_retrieve_jobs():
    result = jobs.retrieve_jobs()
    assert len(result) > 100


# Simple test function that checks if the function actually writes the JSON data by first checking
# if there is a file with the name specified. If it exists, then it is deleted. Then the dump function is called.
# Then it checks if the file exists and if it has content that should be expected inside. In this case, I check
# if it has the title 'Full Stack Software Engineer - Rails' inside.
# UPDATE: It picks a random one from the retrieved list now and checks if it exists in the .txt file.
def test_dump_data():
    retrievedJobs = jobs.retrieve_jobs()
    testTitle = 'Full Stack Software Engineer - Rails'
    fileName = 'json.txt'
    if os.path.exists(fileName):
        os.remove(fileName)

    jobs.dump_data(retrievedJobs, fileName)
    assert os.path.exists(fileName)

    randomTestTitle = random.choice(retrievedJobs)['title']

    with open(fileName, 'r') as openFile:
        fileLines = openFile.readlines()
        assert len(fileLines) > 0
        match = False
        randomMatch = False
        for fileLine in fileLines:
            if testTitle in fileLine:
                match = True
            if randomTestTitle in fileLine:
                randomMatch = True
            if match and randomMatch:
                break
        assert match and randomMatch


# Simple function that checks if a database is being created.
def test_open_db():
    # Checking to see if the database exists, so we can delete it to check
    # if the open_db function actually creates the database table.
    databaseFileName = 'jobs.db'
    if os.path.exists(databaseFileName):
        os.remove(databaseFileName)

    connection, cursor = jobs.open_db(databaseFileName)
    assert os.path.exists('jobs.db')
    jobs.close_db(connection)


# Simple function that checks if the correct columns are being created in a table. In this case, I know
# that the description column exists. So, I'll try to add the column. Of course, it should fail. So if it fails,
# the test passes, and if it doesn't fail and actually ends up adding the column, the test fails.
def test_create_table():
    databaseFileName = 'jobs.db'
    connection, cursor = jobs.open_db(databaseFileName)
    jobs.create_table(connection, cursor)
    columnExists = False

    try:
        cursor.execute('ALTER TABLE jobs ADD COLUMN Description;')
    except sqlite3.OperationalError:
        columnExists = True

    assert columnExists


# Simple test function that checks if the jobs are being saved to the database.
# def test_save_to_database():
#
#     databaseFileName = 'jobs.db'
#     tableName = 'jobs'
#     retrievedJobs = jobs.retrieve_jobs()
#
#
#     connection, cursor = jobs.open_db(databaseFileName)
#
#     jobs.create_table(tableName, connection, cursor)
#
#
#     # Checking if the database has some values that should be expected there. In this case, I know
#     # that there is a job where the title is 'Lead Data Acquisition Design Engineer'.
#     # UPDATE: It also picks a random one from the retrieved list now and checks if it exists in the database.
#     testTitle1 = random.choice(retrievedJobs)['title']
#     testTitle2 = "Lead Data Acquisition Design Engineer"
#     connection = sqlite3.connect('jobs.db')
#     cursor = connection.cursor()
#
#     cursor.execute("SELECT * FROM jobs WHERE jobs.Title = ?", (testTitle1,))
#     assert cursor.fetchone()
#     cursor.execute("SELECT * FROM jobs WHERE jobs.Title = ?", (testTitle2,))
#     assert cursor.fetchone()
#
#     connection.close()


# Simple test function that adds good new data to a database then checks if it exists in the database.
# def test_add_to_database_with_good_data():
#     # Adding good data to the database.
#     additionalTestData = [
#         {"id": "TESTID1",
#          "type": "Full Time",
#          "url": "test1.com",
#          "created_at": "Sat Feb 01 12:53:40 UTC 2020",
#          "company": "TESTCOMPANY",
#          "company_url": "test1.com",
#          "location": "Boston, MA",
#          "title": "Senior Python/Django Developer ",
#          "description": "Test Description",
#          "how_to_apply": "Yes.",
#          "company_logo": "test.png"}]
#
#     # Checking if the new data is added to the database.
#     jobs.save_to_database(additionalTestData)
#     connection = sqlite3.connect('jobs.db')
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM jobs WHERE jobs.id = 'TESTID1'")
#     assert cursor.fetchone()
#     connection.close()


# Simple test function that tries to add bad new data to a database then checks if it is updated accordingly.
# def test_add_to_database_with_bad_data():
#     # Adding bad data to the database.
#     additionalTestData = {
#             "id": "TESTID2",
#             "type": "Part Time",
#             "url": "test1.com"}
#
#     # Checking if the new data is added to the database.
#     jobs.save_to_database(additionalTestData)
#     connection = sqlite3.connect('jobs.db')
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM jobs WHERE jobs.id = 'TESTID2'")
#     assert cursor.fetchone() is None
#     connection.close()
#
#     # Throwing in some additional weird arguments to test the function.
#     jobs.save_to_database(102391)
#     jobs.save_to_database('follow')
#     jobs.save_to_database(['break'])
#     jobs.save_to_database((1, 2, 3))
#     jobs.save_to_database('')
#     jobs.save_to_database([])
#     jobs.save_to_database([[]])
#     jobs.save_to_database([{'id': 'test23', "type": "full-time"}])
