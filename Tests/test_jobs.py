import jobs
import os.path
import random
import pytest
import sqlite3

databaseFileName = "jobs.db"
testFileName = "test.txt"


@pytest.fixture
def get_data():
    import jobs
    return jobs.retrieve_jobs()


# Simple test function that checks if the function returns a list with over 100 items and checks
# if the first item in the list is a dict.
def test_retrieve_jobs(get_data):
    assert len(get_data) > 100
    assert type(get_data[1]) is dict


# Simple test function that checks if the function actually writes the JSON data by first checking
# if there is a file with the name specified. If it exists, then it is deleted. Then the dump function is called.
# Then it checks if the file exists and if it has content that should be expected inside. In this case, I check
# if it has the title 'Full Stack Software Engineer - Rails' inside.
# UPDATE: It also picks a random one from the retrieved list now and checks if it exists in the .txt file.
def test_dump_data(get_data):
    testTitle = 'Full Stack Software Engineer - Rails'
    randomTestTitle = random.choice(get_data)['title']
    fileName = 'json.txt'

    if os.path.exists(fileName):
        os.remove(fileName)

    jobs.dump_data(get_data, fileName)
    assert os.path.exists(fileName)

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


# Simple function that checks if the function dump_data() handles illogical data correctly. If the data is
# invalid, the testFileName would never be created. So, we check if the function works by checking if the
# testFileName exists or not. If it exists, it does not work; it if does not, it works.
def test_bad_dump_data():
    jobs.dump_data(123, testFileName)
    jobs.dump_data('123', testFileName)
    jobs.dump_data((1, 2, 3, 4, 5), testFileName)
    jobs.dump_data(True, testFileName)
    assert not os.path.exists(testFileName)

    if os.path.exists(testFileName):
        os.remove(testFileName)


# Simple function where we enter some valid data and check if the file exists.
# The test passes if it exists, and fails if it doesn't exist. We also check if the data is in the file.
def test_good_dump_data():
    testData = {"name": "mihir", "gender": "male", "eyeColor": "black"}
    jobs.dump_data(testData, testFileName)
    assert os.path.exists(testFileName)

    match = False
    testItem = testData['name']

    with open(testFileName, 'r') as openFile:
        readFile = openFile.readlines()
        for line in readFile:
            if testItem in line:
                match = True

    assert match
    if os.path.exists(testFileName):
        os.remove(testFileName)


# Simple function that checks if a database is being created.
def test_open_db():
    # Checking to see if the database exists, so we can delete it to check
    # if the open_db function actually creates the database.
    if os.path.exists(databaseFileName):
        os.remove(databaseFileName)

    connection, cursor = jobs.open_db(databaseFileName)
    assert os.path.exists('jobs.db')
    jobs.close_db(connection)


# Simple function that checks if the correct columns are being created in a table. In this case, I know
# that the description column exists. So, I'll try to add the column. Of course, it should fail. So if
# it fails, the test passes, and if it doesn't fail and actually ends up adding the column,
# the test fails.
def test_create_table():
    # Checking to see if the database exists, so we can delete it to check
    # if the create_table function actually creates the database table with the appropriate columns.
    if os.path.exists(databaseFileName):
        os.remove(databaseFileName)

    connection, cursor = jobs.open_db(databaseFileName)
    jobs.create_table(connection, cursor)
    columnExists = False

    try:
        cursor.execute('ALTER TABLE jobs ADD COLUMN Description;')
    except sqlite3.OperationalError:
        columnExists = True

    assert columnExists
    jobs.close_db(connection)


# Simple test function that checks if the jobs are being saved to the database.
def test_save_to_database(get_data):
    # Checking to see if the database exists, so we can delete it to check
    # if the save_to_database function actually saves the data to a fresh, new database.
    if os.path.exists(databaseFileName):
        os.remove(databaseFileName)

    connection, cursor = jobs.open_db(databaseFileName)
    jobs.create_table(connection, cursor)
    jobs.save_to_database(get_data, connection, cursor)

    # Checking if the database has some values that should be expected there. In this case, I know
    # that there is a job where the title is 'Lead Data Acquisition Design Engineer'.
    # It also picks a random one from the retrieved list and checks if it exists in the database.
    testTitle1 = random.choice(get_data)['title']
    testTitle2 = "Lead Data Acquisition Design Engineer"
    cursor.execute("SELECT * FROM jobs WHERE jobs.Title = ?", (testTitle1,))
    assert cursor.fetchone()
    cursor.execute("SELECT * FROM jobs WHERE jobs.Title = ?", (testTitle2,))
    assert cursor.fetchone()

    jobs.close_db(connection)


# Simple test function that adds good new data to a database then checks if it exists in the database.
def test_add_to_database_with_good_data():
    # Adding good data to the database.
    additionalTestData = [
        {"id": "TESTID1",
         "type": "Full Time",
         "url": "test1.com",
         "created_at": "Sat Feb 01 12:53:40 UTC 2020",
         "company": "TESTCOMPANY",
         "company_url": "test1.com",
         "location": "Boston, MA",
         "title": "Senior Python/Django Developer ",
         "description": "Test Description",
         "how_to_apply": "Yes.",
         "company_logo": "test.png"}]

    # Checking if the new data is added to the database.
    connection, cursor = jobs.open_db(databaseFileName)
    jobs.save_to_database(additionalTestData, connection, cursor)
    cursor.execute("SELECT * FROM jobs WHERE jobs.id = 'TESTID1'")
    assert cursor.fetchone()
    jobs.close_db(connection)


# Simple test function that tries to add bad new data to a database then checks if it is updated accordingly.
def test_add_to_database_with_bad_data():
    # Adding bad data to the database.
    additionalTestData = {
            "id": "TESTID2",
            "type": "Part Time",
            "url": "test1.com"}
    connection, cursor = jobs.open_db(databaseFileName)

    # Checking if the new data is added to the database.
    jobs.save_to_database(additionalTestData, connection, cursor)
    cursor.execute("SELECT * FROM jobs WHERE jobs.id = 'TESTID2'")
    assert cursor.fetchone() is None

    # Throwing in some additional weird arguments to test the function.
    jobs.save_to_database(102391, connection, cursor)
    jobs.save_to_database('follow', connection, cursor)
    jobs.save_to_database(['break'], connection, cursor)
    jobs.save_to_database((1, 2, 3), connection, cursor)
    jobs.save_to_database('', connection, cursor)
    jobs.save_to_database([], connection, cursor)
    jobs.save_to_database([[]], connection, cursor)
    jobs.save_to_database([{'id': 'test23', "type": "full-time"}], connection, cursor)
    jobs.save_to_database({'id': 'test23', "type": "full-time"}, connection, cursor)


def test_add_to_database_SQL_injection():
    connection, cursor = jobs.open_db(databaseFileName)
    sqlInjectionDict = [
        {"id": "; DROP TABLE JOBS",
         "type": "; DROP TABLE JOBS",
         "url": "; DROP TABLE JOBS",
         "created_at": "; DROP TABLE JOBS",
         "company": "; DROP TABLE JOBS",
         "company_url": "; DROP TABLE JOBS",
         "location": "; DROP TABLE JOBS",
         "title": "; DROP TABLE JOBS",
         "description": "; DROP TABLE JOBS",
         "how_to_apply": "; DROP TABLE JOBS",
         "company_logo": "; DROP TABLE JOBS"}]
    jobs.save_to_database(sqlInjectionDict, connection, cursor)