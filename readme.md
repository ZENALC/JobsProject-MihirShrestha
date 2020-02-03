Name: Mihir Shrestha

Requirements: JSON, requirements, time, and os packages.

Brief Summary: The code retrieves job postings from GitHub and dumps it to a file called 'json.txt'. There is also a test in the Tests folder that ensures the code works as intended.

What is missing: In GitHub actions, GitHub cannot find the jobs package for some reason, so it fails to perform the test. I don't know why it does this. The code also just reads the file as is and does not convert it back to a dictionary. This way, theoretically, if a job title like 'Developer' were to be tested with, it could also pass due to 'Developer' being in a description, and not necessarily a job title. Need to fix this in a later patch.

UPDATE: Github actions work fine now, and a more appropriate manner of dumping JSON data has been implemented.
UPDATE: Functionality to save to an SQLITE3 database has been implemented.
