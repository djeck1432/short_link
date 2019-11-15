import os
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BITLINK_TOKEN')
parser = argparse.ArgumentParser(
    description='Введите вашу ссылку'
)
parser.add_argument('url', help='Введите ссылку')
args = parser.parse_args()

def shorten_link(url):
  headers = {'Authorization': 'Bearer '+token}
  payload = {'long_url':url,'title':'111'}
  response = requests.post('https://api-ssl.bitly.com/v4/shorten',json=payload,headers=headers)
  response.raise_for_status()
  return response.json()['id']


def count_clicks(url): 
  headers = {'Authorization': 'Bearer '+token}
  main_url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=url)
  params = {'unit':'day','units':'-1'}
  response = requests.get(main_url,params=params,headers=headers)
  response.raise_for_status()
  return response.text


def get_check(url):
  check = 'bit.ly'
  if url.startswith(check):
    return count_clicks(url)
  else:
    return "Битлинк "+ shorten_link(url)


if __name__== "__main__":
  get_check(args.url)
  try:
    print(shorten_link(args.url))
  except requests.exceptions.HTTPError:
    print('Ooops,Your web address has shorten link,but look at static of count clicks')

  try:
    print(count_clicks(args.url))
  except requests.exceptions.HTTPError:
    print('Ooops,Your web address is not correct for show you count of clicks, write short link')
