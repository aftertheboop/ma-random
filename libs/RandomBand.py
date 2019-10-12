import random
import time
import urllib.request
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from libs.scraper.ScraperHelper import ScraperHelper

DB = 'db/bands.sqlite3'
CONN = sqlite3.connect(DB)

class RandomBand:
  def __init__(self):
    self.target = 'https://www.metal-archives.com/band/view/id/'

  def get(self):
    randomband = self.getrandomband()    
    if(randomband['played'] == 1):
      band = self.getband(randomband['id'])
    else:
      self.scrapeband(randomband['id'], randomband['ma_id'])
      band = self.getband(randomband['id'])
      
    return band

  def getband(self, id):
    cur = CONN.cursor()
    sql = "SELECT * FROM maBands WHERE id = " + str(id) + " LIMIT 1;"
    cur.execute(sql)
    row = cur.fetchone()
    return row
    
  def getrandomband(self):
    cur = CONN.cursor()
    sql = "SELECT id, ma_id, played FROM maBands ORDER BY RANDOM() LIMIT 1"
    cur.execute(sql)
    row = cur.fetchone()
    #print(row)
    return {
      'id': row[0],
      'ma_id': row[1],
      'played': row[2]
    }
  
  def scrapeband(self, id, maid):
    maurl = self.target + str(maid)
    #maurl = 'http://localhost/ma-test/1.html'
    scraperhelper = ScraperHelper()
    html = scraperhelper.get(maurl)    
    soup = BeautifulSoup(html, 'html.parser')
    band = {}
    name_div = soup.find("h1", {"class":"band_name"})
    band["name"] = name_div.find("a").get_text() if name_div else None
    logo_div = soup.find("a", {"id":"logo"})
    band["live_logo_url"] = logo_div["href"] if logo_div else None
    band["cached_logo_url"] = self.cache_band_logo(band["live_logo_url"])
    band["played"] = 1
    stats = self.get_band_stats(soup)
    band.update(stats)
    self.save(id, band)

  def cache_band_logo(self, logo_url):
    if not logo_url:
      return ''
    logo_url = logo_url.split('?')[0]
    filename = logo_url.split('/')
    filename = 'cache/' + filename.pop()
    scraperhelper = ScraperHelper()
    data = scraperhelper.get(logo_url)
    f = open(filename, 'wb')
    f.write(data)
    f.close()
    return filename

  # From https://github.com/alikoneko/metal-scraper/
  def get_band_stats(self, soup):
      dts = soup.find_all("dt")
      stats_keys = []
      for key in dts:
          stats_keys.append(key.get_text().lower().replace(" ", "_").strip(":"))
      dds = soup.find_all("dd")
      stats_values = []
      for value in dds:
          stats_values.append(value.get_text().lower().replace(
              "\n", " ").replace("\t", " ").strip())
      band_stats = dict(zip(stats_keys, stats_values))
      return band_stats

  def save(self, id, band):
    items = band.items()
    update = []
    for item in items:
      update.append(str(item[0]) + "=\"" + str(item[1]) + "\"")

    sql = "UPDATE maBands SET " + ', '.join(update) + " WHERE id = " + str(id) + ";"

    cur = CONN.cursor()
    cur.execute(sql)
    CONN.commit()
    
    """
    placeholder = ", ".join(["?"] * len(band))
    fields = ','.join(band.keys())
    values = band.values()
    #print(fields)
    #print(values)
    sql = "UPDATE maBands "
    sql = "INSERT INTO `{table}` ({columns}) VALUES ({values})".format(table="maBands", columns=fields, values=placeholder)
    #print(sql)
    conn = sqlite3.connect('db/bands.sqlite3')
    cur = conn.cursor()
    cur.execute(sql, list(values))
    conn.commit()
    return cur.lastrowid
    """

"""
class RandomBand:
    def get(self):
        lastupdateddate = float(self.getlastupdateddate())
        now = float(time.time())
        timediff = now - lastupdateddate
        # if the last update is over a day ago, update the max value
        max = int(self.getmax())

        if not max:
            max = int(self.insertmax())
        
        if timediff > 86400:
            max = int(self.updatemax())

        self.getrandomband(max)

    def getrandomband(self, max):
        randombandid = self.getrandombandid(max)

    def getrandombandid(self, max):
        return random.randint(1, max)

    def getmax(self):
        cur = CONN.cursor()
        sql = "SELECT value FROM options WHERE key = 'max_id' LIMIT 1;"
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            max = self.insertmax()
        else:
            max = row[0]
        return max
        
    def insertmax(self):
        max = self.getmaxfromhomepage()
        cur = CONN.cursor()
        sql = "INSERT INTO options (key, value) VALUES (?,?)"
        values = ['max_id', max]
        cur.execute(sql, values)
        CONN.commit()
        return max        
        
    def updatemax(self):
        max = self.getmaxfromhomepage()
        self.updatemax(max)
        self.updatelastupdateddate()
        return max

    def updatemax(self, max):
        cur = CONN.cursor()
        sql = "UPDATE options SET value = ? WHERE key = ? LIMIT 1;"
        values = ['max_id', max]
        cur.execute(sql, values)
        CONN.commit()
        return max        

    def getmaxfromhomepage(self):
        if(LOCAL):
            home_url = 'mock/home.html'
            enc = 'utf-8'
            with open(home_url, 'r', encoding=enc) as f:
                data = f.read()
        else:
            print('???')
        
        soup = BeautifulSoup(data, 'html.parser')
        latest_url = soup.find('div', {'id': 'additionBands'}).find('a')['href']
        latest_url = latest_url.split('/')
        max_value = latest_url.pop()

        return max_value

    def getlastupdateddate(self):
        # Get the last DB update value
        cur = CONN.cursor()
        sql = "SELECT value FROM options WHERE key = 'max_last_updated' LIMIT 1;"
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            timestamp = self.insertlastupdateddate()
        else:
            timestamp = row[0]

        return timestamp

    def insertlastupdateddate(self):
        cur = CONN.cursor()
        currenttimestamp = time.time()
        sql = "INSERT INTO options (key, value) VALUES (?,?)"
        values = ['max_last_updated', currenttimestamp]
        cur.execute(sql, values)
        CONN.commit()
        return currenttimestamp    

    def updatelastupdateddate(self):
        cur = CONN.cursor()
        currenttimestamp = time.time()
        sql = "UPDATE options SET value = ? WHERE key = ?"
        values = ['max_last_updated', currenttimestamp]
        cur.execute(sql, values)
        CONN.commit()
        return currenttimestamp
"""