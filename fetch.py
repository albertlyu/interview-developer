#! /usr/bin/python
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup

BASE_URL = "http://gd2.mlb.com/components/game/mlb/"

# Get HTML of front office employees from url
def get_list(url):
  html = urlopen(url)
  soup = BeautifulSoup(html.read()).find("ul", {"li": "mc"})
  return soup

def fetch_gids(dates):  
  """
  Return a list of gids for a range of dates, inclusive.
  """
  gids = []
  for date in dates:
    YYYY = str(date.year)
    MM = str(date.month)
    DD = str(date.day)
    day_url = BASE_URL + "year_%s/month_%s/day_%s/" % (YYYY,MM,DD)
    #end here

if __name__ == "__main__":
  try:
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    dates = [start_date + timedelta(days=x) for x in range((end_date-start_date).days+1)]
  except IndexError:
    print("I need a start and end date ('YYYY-MM-DD').")
    sys.exit()

