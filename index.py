import random
import urllib.request
import sqlite3
from libs.RandomBand import RandomBand
from libs.scraper.MetalScraper import MetalScraper
from bs4 import BeautifulSoup

USER_AGENTS = user_agent_list = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
LOCAL = True

def get_maximum_id():
    
    if(LOCAL):
        home_url = 'mock/home.html'
        enc = 'utf-8'
        with open(home_url, 'r', encoding=enc) as f:
            data = f.read()
    """ 
    else:
        user_agent = random.choice(USER_AGENTS)
        request = urllib.request.Request(band_url)
        request.add_header('User-Agent', user_agent)
        data = urllib.request.urlopen(request).read()
    """
    soup = BeautifulSoup(data, 'html.parser')
    latest_url = soup.find('div', {'id': 'additionBands'}).find('a')['href']
    latest_url = latest_url.split('/')
    max_value = latest_url.pop()

    return max_value

def get_file(bandId = 0):
    
    if(LOCAL):
        bandUrl = 'mock/3540321652.html'
        enc = 'utf-8'
        with open(bandUrl, 'r', encoding=enc) as f:
            data = f.read()
    else:
        bandUrl = 'https://www.metal-archives.com/band/view/id/' + bandId
        user_agent = random.choice(USER_AGENTS)
        request = urllib.request.Request(bandUrl)
        request.add_header('User-Agent', user_agent)
        data = urllib.request.urlopen(request).read()

    return data

def get_band_stats(soup):
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

def cache_band_logo(logo_url):
    filename = logo_url.split('/')
    filename = 'cache/' + filename.pop()

    user_agent = random.choice(USER_AGENTS)
    request = urllib.request.Request(logo_url)
    request.add_header('User-Agent', user_agent)
    data = urllib.request.urlopen(request).read()

    f = open(filename, 'wb')
    f.write(data)
    f.close()
    
    return filename

# From https://github.com/alikoneko/metal-scraper/
def save(band):
    placeholder = ", ".join(["?"] * len(band))
    fields = ','.join(band.keys())
    values = band.values()
    #print(fields)
    #print(values)
    sql = "INSERT INTO `{table}` ({columns}) VALUES ({values})".format(table="maBands", columns=fields, values=placeholder)
    #print(sql)
    conn = sqlite3.connect('db/bands.sqlite3')
    cur = conn.cursor()
    cur.execute(sql, list(values))
    conn.commit()
    return cur.lastrowid

def run():

    metalscraper = MetalScraper
    print(metalscraper)
    #print(band_id)

    #get_maximum_id()

    """
    html = get_file()
    soup = BeautifulSoup(html, 'html.parser')
    band = {}

    band_url = soup.find("input", {"name":"origin"}).get('value')
    band_url = band_url.split('/')
    band["ma_id"] = band_url.pop()
    name_div = soup.find("h1", {"class":"band_name"})
    band["name"] = name_div.find("a").get_text() if name_div else None
    logo_div = soup.find("a", {"id":"logo"})
    band["live_logo_url"] = logo_div["href"] if logo_div else None
    band["cached_logo_url"] = cache_band_logo(band["live_logo_url"])
    stats = get_band_stats(soup)
    band.update(stats)
    #save(band)
    """

if __name__ == "__main__":
    run()
    pass
