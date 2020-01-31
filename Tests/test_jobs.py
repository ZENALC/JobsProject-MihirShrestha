import jobs
import os.path


# Simple test function that checks if the function returns a list with over 200 items
def test_retrieve_jobs():
    result = jobs.retrieve_jobs()
    assert len(result) > 200


# Simple test function that checks if the function actually writes the JSON data by first checking
# if there is a file with the name specified. If it exists, then it is deleted. Then the dump function is called.
# Then it checks if the file exists and if it has content inside.
def test_dump_data():
    fileName = 'json.txt'
    if os.path.exists(fileName):
        os.remove(fileName)

    jobs.dump_data(jobs.retrieve_jobs(), fileName)
    assert os.path.exists(fileName)

    with open(fileName, 'r') as openFile:
        fileLines = openFile.readlines()
        assert len(fileLines) > 0


