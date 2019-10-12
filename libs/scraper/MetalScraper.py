import sqlite3
import time

DB = 'db/bands.sqlite3'
CONN = sqlite3.connect(DB)

class MetalScraper:
  def __init__(self):    
    self.displaystart = self.getdisplaystart()
    self.displaylength = 200
    self.baseurl = "../../mock/api.json"
    # self.baseurl = "https://www.metal-archives.com/search/ajax-advanced/searching/bands/?iDisplayStart={self.displaystart}&iDisplayLength=200

  def scrape(self):
    queryParams = {
      'start': 'iDisplayStart=' + str(self.displaystart),
      'length': 'iDisplayLength=' + str(self.displaylength)
    }
    target = self.baseurl + '?' + "&".join(queryParams.values())
    # do scrape
    self.displaystart = int(self.displaystart) + int(self.displaylength)
    self.updatedisplaystart(self.displaystart)
    print(target)
    time.sleep(2)
    self.scrape()


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