import pathlib
import gzip
import csv
import os

DATA = 'data'
GZ_FILE_NAME = 'reviews.csv.gz'
CSV_FILE_NAME = 'reviews.csv'
OUTPUT_FILE_NAME = 'reviews.ko.csv'

def contains_ko(s):
  for ch in s:
    if ('\uAC00' <= ch and ch <= '\uD7A3'
      or '\u1100' <= ch and ch <= '\u11FF'
      or '\u3130' <= ch and ch <= '\u318F'
      or '\uA960' <= ch and ch <= '\uA97F'
      or '\uD7B0' <= ch and ch <= '\uD7FF'):
      return True
  return False

def traverse(path):
  for child in path.iterdir():
    if child.is_dir():
      traverse(child)
    elif child.name == GZ_FILE_NAME:
      with gzip.open(child, 'rb') as gz:
        content = gz.read().decode('utf-8')
      with open(path / CSV_FILE_NAME, 'w') as f:
        f.write(content)
      cnt = 0
      with open(path / CSV_FILE_NAME, 'r', newline='') as f:
        with open(path / OUTPUT_FILE_NAME, 'w', newline='') as ko:
          reader = csv.reader(f, delimiter=',', quotechar='"')
          writer = csv.writer(ko, delimiter=',', quotechar='"')
          for row in reader:
            if contains_ko(row[-1]):
              writer.writerow(row)
              cnt += 1
      os.remove(path / CSV_FILE_NAME)
      print('[', cnt, ']', child)

if __name__ == '__main__':
  traverse(pathlib.Path(DATA))
