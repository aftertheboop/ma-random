import random
import time
import urllib.request
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

DB = 'db/bands.sqlite3'
CONN = sqlite3.connect(DB)
LOCAL = True

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