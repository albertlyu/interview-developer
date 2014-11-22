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
This project was built with Python 2.7.5 and PostgreSQL 9.3.4. If you aren't already, make sure you are in the ```mlbdb``` directory. 

If you are using Python 2.x, pip install the following requirements file:
```
$ pip install -r requirements.txt # Python 2.7.5
```

## Configuration
Update ```config.ini``` with your PostgreSQL credentials, particularly a username with database write access and its password. This config file will be leveraged by scripts later on in this writeup.

You will need to create a database called ```mlbdb```. Assuming that you already have PostgreSQL 9.3.4, the ```createdb``` wrapper statement should already be mapped for you. To create your ```mlbdb```, execute the following in command line:
```
$ createdb mlbdb -U [USERNAME]
```

## Instructions
1. To parse ```leaderboard.html``` and store the batter leaderboard table's data in a database table, execute the following in command line:
```
$ python python/create.py
```
2. To create your control table, execute the following. This control table will be used to update columns' data types. Enter your password for [USERNAME] after execution:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/control_table.sql
```
3. Next, execute the script to update data types for all columns:
```
$ python python/update.py
```
4. Let's also import wOBA constants for the past 15 seasons into our database. Create the wOBA constants table like so:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/wOBA_constants.sql
```
5. Now that we've updated the data types for the ```battingleaders``` table as well as created a ```woba_constants``` table, we can calculate wOBA for each player. Execute the following SQL script:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/calculate_wOBA.sql
```

## Discussion
I'd like to discuss why I implemented the above methods the way I did.
...