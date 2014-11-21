#! /usr/bin/python
from bs4 import BeautifulSoup

def get_batter_html(path):
  html = open(path)
  soup = BeautifulSoup(html.read()).find("table", {"id": "battingLeaders"})
  return soup

def parse_html(soup):
  head = soup.find("thead")
  body = soup.find("tbody")

  # Get header row names
  tr = head.find_all("tr")
  for row in tr:
    th = row.find_all("th")
    header_row = [i.string for i in th if i.string is not None]
    print(header_row)

  # Get batter records
  records = []
  #player_names = [i.string.replace('\n',' ').replace('\t','') for i in body.find_all("a")]
  tr = body.find_all("tr")
  for row in tr:
    td = row.find_all("td")
    player = [i.string.replace('\n',' ').replace('\t','') for i in row.find("a")]
    record = [i.string for i in td]
    record = [player[0] if i is None else i for i in record]
    records.append(record) # Store records in list of lists

  # Cleanse records by removing separator element
  for record in records:
    del(record[3]) # Delete separator element



if __name__ == "__main__":
  path = "python/leaderboard.html"
  soup = get_batter_html(path)
  parse_html(soup)