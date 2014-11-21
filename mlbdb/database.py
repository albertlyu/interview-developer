#! /usr/bin/python
import ConfigParser
import psycopg2

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
