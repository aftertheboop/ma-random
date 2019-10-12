import sqlite3
import time
import re
from .ScraperHelper import ScraperHelper

DB = 'db/bands.sqlite3'
CONN = sqlite3.connect(DB)

class MetalScraper:
  def __init__(self):    
    self.displaystart = self.getdisplaystart()
    self.displaylength = 200
    #self.baseurl = "http://localhost/ma-test/search.json"
    self.baseurl = "https://www.metal-archives.com/search/ajax-advanced/searching/bands/"

  def scrape(self):
    queryParams = {
      'start': 'iDisplayStart=' + str(self.displaystart),
      'length': 'iDisplayLength=' + str(self.displaylength)
    }
    target = self.baseurl + '?' + "&".join(queryParams.values())
    # do scrape
    response = self.consume(target)

    if response['aaData']:
      self.process(response['aaData'])
      print(target)
      # scrape complete
      self.displaystart = int(self.displaystart) + int(self.displaylength)
      self.updatedisplaystart(self.displaystart)
      # naptime
      time.sleep(2)
      self.scrape()

  def process(self, data):
    for item in data:
      match = re.search(r'<a href=".*/(\d+)">(.*)<\/a>.*', item[0])
      name = match.group(2)
      ma_id = match.group(1)
      self.savetodb(ma_id, name)

  def savetodb(self, id, name):
    bandid = self.getbandbymaid(id)
    if not bandid:
      self.insertband(id, name)

  def insertband(self, id, name):
    cur = CONN.cursor()
    sql = "INSERT INTO maBands (ma_id, name) VALUES (?, ?);"
    values = [id, name]
    cur.execute(sql, values)
    CONN.commit()
    
  def getbandbymaid(self, maid):
    cur = CONN.cursor()
    sql = "SELECT id FROM maBands WHERE ma_id = ? LIMIT 1;"
    values = [maid]
    cur.execute(sql, values)
    row = cur.fetchone()
    if not row:
      return False
    else:
      return row[0]

  def consume(self, target):
    helper = ScraperHelper()
    rawdata = helper.get(target)
    parseddata = helper.parse(rawdata)
    return parseddata

  def getdisplaystart(self):
    cur = CONN.cursor()
    sql = "SELECT value FROM options WHERE key = 'display_start' LIMIT 1;"
    cur.execute(sql)
    row = cur.fetchone()
    if not row:
      displaystart = self.updatedisplaystart(0)
    else :
      displaystart = row[0]
    return displaystart

  def updatedisplaystart(self, displaystart):
    if (displaystart == 0):
      self.insertdisplaystart(0)
    else :
      cur = CONN.cursor()
      sql = "UPDATE options SET value = ? WHERE key = ?;"
      values = [str(displaystart), 'display_start']
      cur.execute(sql, values)
      CONN.commit()
      return displaystart

  def insertdisplaystart(self, displaystart):
    cur = CONN.cursor()
    sql = "INSERT INTO options (key, value) VALUES (?, ?);"
    values = ['display_start', displaystart]
    cur.execute(sql, values)
    CONN.commit()
    return int(displaystart)