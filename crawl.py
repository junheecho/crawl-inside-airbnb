import http.client
import re
import pathlib
import urllib
import copy

DOMAIN = 'insideairbnb.com'
LIST_URI = '/get-the-data.html'
DATA_DOMAIN = 'data.insideairbnb.com'
PATTERN = r'http://data.insideairbnb.com/([^\'\"]*)'
DIR = 'data'

def crawl_file_list():
  conn = http.client.HTTPConnection(DOMAIN)
  conn.request('GET', LIST_URI)
  res = conn.getresponse()
  html = res.read()
  print('HTTP Request to', 'http://' + DOMAIN + LIST_URI, ':', res.status, res.reason)
  conn.close()

  return re.findall(PATTERN, html.decode('utf-8'))

def download(files, only_latest=False):
  files = copy.copy(files)
  files.sort(reverse=True)
  latest_by_city = {}
  for i, uri in enumerate(files, 1):
    tokens = uri.split('/')

    country, province, city, date, data_type, file_name = tokens
    if only_latest and city in latest_by_city and latest_by_city[city] > date:
      continue

    dir_name = '/'.join([DIR, city, date, data_type])
    file_path = '/'.join([dir_name, file_name])

    conn = http.client.HTTPConnection(DATA_DOMAIN)
    conn.request('GET', '/' + uri)
    res = conn.getresponse()
    if res.status == 200:
      pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
      with open(file_path, 'wb') as f:
        f.write(res.read())
      latest_by_city[city] = date
    print('[', i, '/', len(files), ']', res.status, res.reason, uri)
    conn.close()

if __name__ == '__main__':
  files = crawl_file_list()
  download(files, only_latest=True)
