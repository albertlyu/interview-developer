#! /usr/bin/python
from bs4 import BeautifulSoup
import ConfigParser
import psycopg2

def get_html_from_path(path):
  """
  Get html given a file path. Returns a BeautifulSoup object.
  """
  html = open(path)
  soup = BeautifulSoup(html.read()).find("table", {"id": "battingLeaders"})
  return soup

def get_header_from_html(soup):
  """
  Get header of html table. Returns a list of header columns.
  """
  head = soup.find("thead")
  tr = head.find_all("tr")
  for row in tr:
    th = row.find_all("th")
    header = [i.string for i in th if i.string is not None]
    print(header)
  return(header)

def get_records_from_html(soup):
  """
  Get records of html table. Returns a list of records, where each record is a list.
  """
  # Get batter records
  body = soup.find("tbody")
  records = []
  #player_names = [i.string.replace('\n',' ').replace('\t','') for i in body.find_all("a")]
  tr = body.find_all("tr")
  for row in tr:
    td = row.find_all("td")
    player = [i.string.replace('\n',' ').replace('\t','') for i in row.find("a")]
    record = [i.string for i in td]
    record = [player[0] if i is None else i for i in record]
    del(record[3]) # Cleanse record by deleting separator element
    records.append(record) # Store records in list of lists
  print(records)
  return(records)

def create_connection():
  """
  Create PostgreSQL connection given configuration file.
  """
  config = ConfigParser.ConfigParser()
  config.read("config.ini")
  localhost = config.get('postgresql','localhost')
  database = config.get('postgresql','database')
  username = config.get('postgresql','username')
  password = config.get('postgresql','password')
  conn_string = "host='" + localhost + "' dbname='" + database + "' user='" + username + "' password='" + password + "'"
  print("Connecting to database...")
  conn = psycopg2.connect(conn_string)
  print("Connection established!")
  return(conn)

def create_table(cursor,table_schema,table_name,column_names):
  """
  Create table with column names of data type varchar(100) if it 
  doesn't exist, then execute on cursor object.
  """
  create_table = "CREATE TABLE IF NOT EXISTS " + table_schema + "." + table_name + ' ("' + '" varchar(50),"'.join(column_names) + '" varchar(50));'
  print(create_table)
  cursor.execute(create_table)
  print("Created " + table_schema + "." + table_name + " table")

def insert_records(cursor,table_schema,table_name,column_names,records):
  """
  Insert multiple records with one INSERT statement into table, then execute 
  on cursor object.
  """
  insert_base = "INSERT INTO " + table_schema + "." + table_name + ' ("' + '","'.join(column_names) + '") VALUES '
  insert_values = []
  for record in records:
    insert_value = "('" + "','".join(str(x).replace("'","''") for x in record) + "')"  
    insert_values.append(insert_value)
  insert_record = insert_base + ",".join(insert_values) + ";"
  if records != []:
    print(insert_record)
    cursor.execute(insert_record)
    print("Inserted " + str(len(records)) + " records into " + table_schema + "." + table_name)
  else:
    print("No records to insert into %s.%s" % (table_schema,table_name))

if __name__ == "__main__":
  # Parse HTML and store header and records
  path = "leaderboard.html"
  soup = get_html_from_path(path)
  header = get_header_from_html(soup)
  records = get_records_from_html(soup)

  # Create PostgreSQL database connection and a cursor object
  conn = create_connection()
  cursor = conn.cursor()

  # Initialize table information
  table_schema = 'public'
  table_name = 'battingLeaders'
  column_names = header

  # Create table and insert records
  create_table(cursor,table_schema,table_name,column_names)
  insert_records(cursor,table_schema,table_name,column_names,records)

  # Commit executions and close connection
  conn.commit()
  conn.close()