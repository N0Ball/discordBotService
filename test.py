import requests

URL = 'https://docs.google.com/spreadsheets/d/13ZacBjfuDXAaa5FzxsvG1Rt_qnoiGjVVHQyvkC3_igk/export?exportFormat=csv'


orders = requests.get(URL, allow_redirects=True)
orders.encoding = 'utf-8'

print(orders.text)