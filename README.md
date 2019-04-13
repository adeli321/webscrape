# webscrape

A few simple scripts utilizing Python's BeautifulSoup and Requests modules to scrape 4 pages of data from Indeed at a time.
At the moment the only jobs being searched are 'Junior Data Engineer' and 'Data Engineer'.
The script stores various information about each job in a local Postgres database.

To replicate yourself:
  1. Install Postgres locally
  2. Run Command
    a. CREATE TABLE job_listings(title VARCHAR(100), company VARCHAR(40), 
        location VARCHAR(50), summary VARCHAR(7000), timestamp TIMESTAMP);
  3. Edit db_config dictionary (user and database name) in script to match your local instance
  4. Run script!
