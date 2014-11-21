# mlbdb

## Introduction

For this exercise you will be writing Python code to parse HTML and insert it into a PostgreSQL database that you will create.

Upon completion you will deliver the following
* Python code that does the following:
 * downloads the [Leaderboard HTML](https://raw.githubusercontent.com/kruser/interview-developer/master/python/leaderboard.html) found in this repository
 * parses all stats for players and inserts it into a database table or tables

* SQL statements to:
 * Create the table or tables that your Python code needs
 * A query that ranks these same players according to their 2014 [wOBA](http://www.fangraphs.com/library/offense/woba/)

### Notes

* Your Python code can assume the tables it uses have already been created. That is, it doesn't need to 
automatically create the tables.
* Feel free to use any modules available via a ```pip install```. Include a ```requirements.txt``` file that
lists the dependencies.

## Requirements
Set up a virtual environment with Python 2.7
```$ pip install -r requirements.txt```

## Setup
To parse the HTML and store in a newly created table, execute the following in command line:
```
$ python create.py
```
To create your control table, execute the following. This control table will be used to update columns' data types. Enter your password for [USERNAME] after execution:
```
$ psql -d mlbdb -U [USERNAME] -a -f control_table.sql
```
Next, execute the script to update data types for all columns:
```
$ python update.py
```
Let's also import wOBA constants into our database. Create the wOBA constants table like so:
```
$ psql -d mlbdb -U [USERNAME] -a -f wOBA_constants.sql
```
Now that we've updated the data types, we can calculate wOBA for each player. Execute the following SQL script:
```
$ psql -d mlbdb -U [USERNAME] -a -f calculate_wOBA.sql
```

## Discussion
I'd like to discuss why I implemented the above methods the way I did.
...