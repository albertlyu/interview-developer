#! /usr/bin/python
import database as db

if __name__ == "__main__":
  # Create PostgreSQL database connection and a cursor object
  conn = db.create_connection()
  cursor = conn.cursor()

  # Query control table
  query = "SELECT * FROM public.etlcolumns;"
  cursor.execute(query)
  rows = cursor.fetchall()

  # Update data types for columns in control table
  for row in rows:
    table_schema = row[0]
    table_name = row[1]
    column_name = '"' + row[2] + '"'
    data_type = row[3]
    update_column = 'ALTER TABLE %s.%s ALTER COLUMN %s SET DATA TYPE %s USING (%s::%s);' % (table_schema,table_name,column_name,data_type,column_name,data_type)
    print(update_column)
    cursor.execute(update_column)

  # Commit executions and close connection
  conn.commit()
  conn.close()