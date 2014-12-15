# mlbdb

## Requirements
This project was built with Python 2.7.5 and PostgreSQL 9.3.4. If you aren't already, make sure you are in the ```mlbdb``` directory. 

If you are using Python 2.x, pip install the following requirements file:
```
$ pip install -r requirements.txt # Python 2.7.5
```

If you are on a Windows machine and are unable to install ```psycopg2``` with the message 'error: Unable to find vcvarsall.bat,' you will need to install ```psycopg2``` directly as this is a known issue with installing ```psycopg2``` on Windows. To do so, run the following:

```
$ easy_install http://stickpeople.com/projects/python/win-psycopg/2.5.3/psycopg2-2.5.3.win32-py2.6-pg9.3.4-release.exe
```

For more details, see the [following link](http://stackoverflow.com/questions/5382801/where-can-i-download-binary-eggs-with-psycopg2-for-windows/5383266#5383266).

## Configuration
Update ```config.ini``` with your PostgreSQL credentials, particularly a username with database write access and its password. This config file will be leveraged by scripts later on in this writeup.

You will need to create a database called ```mlbdb```. Assuming that you already have PostgreSQL 9.3.4, the ```createdb``` wrapper statement should already be mapped for you. To create your ```mlbdb```, execute the following in command line:
```
$ createdb mlbdb -U [USERNAME]
```

## Instructions
#### Step 1: Staging the data
To parse ```leaderboard.html``` and store the batter leaderboard table's data in a database table, execute the following in command line:
```
$ python python/create.py
```
```create.py``` starts off with using the methods in ```parse.py``` to store the header row of the HTML table as well as the records in the table. Some cleansing needed to be done before continuing, such as removing the separator column between the 'Team' and 'PlayerId' fields and cleaning up the 'Player' field. 

Next, a PostgreSQL database connection is made and a cursor object is created given the information in ```config.ini``` (see the ```create_connection()``` method in ```database.py```). To create the table (via ```create_table()```), the schema, table name, and column names are all parameterized so that the methods can be reused later to create more tables automatically.

Regarding ```create_table()```, there is one important caveat though -- all columns are declared as varchar(50). This is *by design* -- when ingesting new table structures from external sources into our data warehouse, we want to be add these tables without needing to declare each column's data type. This saves us time when we want to create many many tables from multiple data sources, as we can reuse the same code. In a larger data warehouse, we would write these tables into a schema that we'll designate as the staging layer. As you'll see in Steps 2 and 3, we will make use of *control tables* to govern our data model and schema design for our foundation layer.

#### Step 2: Creating a control table
To create your control table, execute the following. This control table will be used to update columns' data types. Enter your password for [USERNAME] after execution:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/control_table.sql
```
Moving on to Step 2, we create a control table here called ```etlcolumns```. This table is at the column-level. For each column, we assigned a data type. This is where we govern how the structure of the table should look in the foundation layer. Since this exercise is with a smaller data warehouse, we simply execute the ```update.py``` script in Step 3 to alter columns in the target table ```battingleaders```. In a much larger data warehouse though, we would define a target schema (foundation) and target tables that are distinct from the source schema (staging).

#### Step 3: Using the control table to perform SQL operations
Next, execute the script to update data types for all columns:
```
$ python python/update.py
```
Continuing the discussion from the previous step, you can see how we can make use of control tables to automatically execute the same SQL operations, whether it's setting columns' data types, adding new columns, adding new tables, even aggregations and data transformations. The scripts that leverage these control tables can be written once, then only altered in the future for new features. And rather than spending time hard-coding schemas and table names into SQL scripts, we simply insert new records (or update existing records) in our control table as requests come in.

#### Step 4: Storing a history of wOBA constants
Let's also import wOBA constants for the past 15 seasons into our database. Create the wOBA constants table like so:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/wOBA_constants.sql
```
In Step 4, we add wOBA constants for multiple seasons into our data warehouse. Even though the batters data are only from the 2014 season, we want to keep a history of wOBA constants in case we want to calculate wOBA for player-seasons from previous seasons. By the way, these wOBA constants in the ```wOBA_constants.sql``` script are taken straight from [FanGraphs' Guts! page](http://www.fangraphs.com/guts.aspx).

#### Step 5: Calculating metrics and using CTEs
Now that we've updated the data types for the ```battingleaders``` table as well as created a ```woba_constants``` table, we can calculate wOBA for each player. Execute the following SQL script:
```
$ psql -d mlbdb -U [USERNAME] -a -f sql/calculate_wOBA.sql
```
In the final step, Step 5, we make use of a common table expression (CTE a.k.a. the WITH statement) to construct a query to calculate wOBA for all players in the ```battingleaders``` table. Note that the common table expression joins the ```woba_constants``` table on woba.season=2014 since we do not store the season attribute in ```battingleaders``` and all the batter-seasons are for the 2014 season anyway. Now we can calculate the wOBA numerator and wOBA denominator based on the formula from [FanGraphs](http://www.fangraphs.com/library/offense/woba/).

We calculate the wOBA numerator and denominator to demonstrate the usefulness of control tables in calculating hundreds of different metrics that are calculated in the same manner. In a larger data warehouse, we could have many counting statistics, rate statistics, and average statistics, all transformed in very similar manners based on the type of statistic. In a well-designed ETL process with control tables, we can create new metrics that are summed, grouped by, divided, multiplied, etc. more seamlessly by simply inserting a new record in the right control table and letting the ETL jobs take care of the rest. Even the wOBA numerator, which is simply a linear combination of constants and counting statistics, can be abstracted such that we need not calculate it by hard-coding SQL into a script as we did in ```calculate_wOBA.sql```.

Based on the resulting set, Andrew McCutchen, Victor Martinez, and Jose Abreu are the leaders in wOBA, while Ben Revere, Alcides Escobar, and Erick Aybar are at the bottom.