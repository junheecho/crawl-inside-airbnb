import http.client
import re
import pathlib

DOMAIN = 'insideairbnb.com'
LIST_URI = '/get-the-data.html'
DATA_DOMAIN = 'data.insideairbnb.com'
PATTERN = r'http://data.insideairbnb.com/([^\'\"]*)'
DIR = 'data/'

def crawl_file_list():
  conn = http.client.HTTPConnection(DOMAIN)
  conn.request('GET', LIST_URI)
  res = conn.getresponse()
  html = res.read()
  print('HTTP Request to', 'http://' + DOMAIN + LIST_URI, ':', res.status, res.reason)
  conn.close()

  return re.findall(PATTERN, html.decode('utf-8'))

if __name__ == '__main__':
  files = crawl_file_list()
  for i, uri in enumerate(files, 1):
    tokens = uri.split('/')
    dir_name, file_name = '/'.join(tokens[:-1]), tokens[-1]

    pathlib.Path(DIR + dir_name).mkdir(parents=True, exist_ok=True)
    with open(DIR + uri, 'wb') as f:
      conn = http.client.HTTPConnection(DATA_DOMAIN)
      conn.request('GET', '/' + uri)
      res = conn.getresponse()
      f.write(res.read())
      print('[', i, '/', len(files), ']', res.status, res.reason, uri)
      conn.close()
