import requests, json
from bs4 import BeautifulSoup

# Gathering proxies for proxy rotation
res = requests.get('http://www.free-proxy-list.net/')
content = BeautifulSoup(res.text, 'lxml')
# accessing table element
table = content.find('table')
# accessing all rows inside the table
rows = table.find_all('tr')
# creates a nested list, where each nested list contains table data of a row
cols = [[col.text for col in row.find_all('td')] for row in rows]

# creating empty list to store proxy address
proxy_list = []

# looping through the cols list
for col in cols:
    try:
        # address appended if from USA and supports https 
        if col[3]=='United States' and col[6] == 'yes':
            # appending only the ip address and the port adress
            proxy_list.append('https://'+col[0]+':'+col[1])
    except:
        # this is to skip the error raised due to first empty nested list of cols
        pass

# function to access the site using rotation proxy
def fetch(url):
    proxy_index = 0
    while proxy_index < len(proxy_list):
        try:
            # testing if current proxy works
            print("Current Proxy", proxy_list[proxy_index])
            res = requests.get(url, proxies={'https':proxy_list[proxy_index]}, timeout=5)
            return res
        except:
            # Moving to next proxy if current proxy doesn't work
            print("Current Proxy Failed....")
            proxy_index += 1
    

# Creating a list of dictionary
# creating empty list
products = []
page = 1
# We have 2 pages to parse
while page < 3:
    # accessing website to be parsed
    res = fetch(f"https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={page}")
    # in case proxies do not work
    if res == None:
        print(f"None of the proxies work scraping page {page} data from own IP address")
        res = requests.get(f"https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={page}")
    soup = BeautifulSoup(res.text, 'html.parser')

    # accessing the prices of all the products
    price_list = soup.find_all("span", {"class":"price"})
    # accessing the names of all the products
    name_list = soup.find_all("a", {"class":"catalog-item-name"})
    # accessing the availability of all the products
    availability = soup.find_all("span", {"class":"out-of-stock"})
    # accessing the manufacturers of all the products
    manufacturers = soup.find_all("a", {"class":"catalog-item-brand"})
    total_products = len(price_list)

    i = 0
    while i < total_products:
        # creating empty dictionary
        product_info = {}
        # setting price key store price float value
        product_info['price'] = float(price_list[i].text.lstrip("$"))
        # setting title key store title value
        product_info['title'] = name_list[i].text
        # storing the availability data into dictionary
        if availability[i].text == 'Out of Stock':
            product_info['stock'] = False
        else:
            product_info['stock'] = True
        # setting manufacturer's key store manufacturers name as string value
        product_info['maftr'] = manufacturers[i].text
        # appending the dictionary to products list
        products.append(product_info)
        i = i+1
    page = page+1

# converting list of dictionary into json
json_object = json.dumps(products, indent = 4)
print(json_object)
