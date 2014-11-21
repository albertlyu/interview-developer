#! /usr/bin/python
from bs4 import BeautifulSoup

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