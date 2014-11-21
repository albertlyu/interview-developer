#! /usr/bin/python
import database as db
import parse as p

if __name__ == "__main__":
  # Parse HTML and store header and records
  path = "leaderboard.html"
  soup = p.get_html_from_path(path)
  header = p.get_header_from_html(soup)
  records = p.get_records_from_html(soup)

  # Create PostgreSQL database connection and a cursor object
  conn = db.create_connection()
  cursor = conn.cursor()

  # Initialize table information
  table_schema = 'public'
  table_name = 'battingLeaders'
  column_names = header

  # Create table and insert records
  db.create_table(cursor,table_schema,table_name,column_names)
  db.insert_records(cursor,table_schema,table_name,column_names,records)

  # Commit executions and close connection
  conn.commit()
  conn.close()