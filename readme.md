Name: Mihir Shrestha

Requirements: JSON, requests, time, pytest, and os packages.

Brief Summary: The code retrieves job postings from GitHub and dumps it to a file called 'json.txt' and a database called "jobs.db". There is are also several tests in the Tests folder that ensures the code works as intended.

What is missing: The database still can contain outddated data as it does not delete non-existent, old records. 

UPDATE: Github actions work fine now, and a more appropriate manner of dumping JSON data has been implemented.
UPDATE: Functionality to save to an SQLITE3 database has been implemented.
