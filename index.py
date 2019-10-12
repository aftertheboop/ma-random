import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from libs.RandomBand import RandomBand

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/api': {
              'status': 200,
              'content-type': 'text/json'
            },
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
          self.respond(paths[self.path])
        else:
          self.respond({'status': 500})

    def handle_http(self, status_code, path):
      self.send_response(status_code)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      content = ''
      if(path == '/api'):
        randomband = RandomBand()
        band = randomband.get()
        content = str(band)

      """
        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        <p>You accessed path: {}</p>
        </body></html>
        '''.format(path)
        """
      return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

"""
def get_maximum_id():
    
    if(LOCAL):
        home_url = 'mock/home.html'
        enc = 'utf-8'
        with open(home_url, 'r', encoding=enc) as f:
            data = f.read()
    
    else:
        user_agent = random.choice(USER_AGENTS)
        request = urllib.request.Request(band_url)
        request.add_header('User-Agent', user_agent)
        data = urllib.request.urlopen(request).read()
    
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








def run():

    metalscraper = MetalScraper()
    metalscraper.scrape()
    #print(band_id)

    #get_maximum_id()


    html = get_file()
    
    #save(band)
    """