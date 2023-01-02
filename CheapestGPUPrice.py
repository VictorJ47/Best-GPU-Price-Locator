#This program utilizes Beautiful Soup 4 to webscrape Newegg to find the cheapest price for an entered GPU
#This program will output all buying options on the webite in order of cheapest to most expensive
#As well as a corresponding link.
#This program can be modified to search for other products, as well as to search on other websites.



from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser") 
#sends an HTTP request, then uses beautiful soup to read the page

page_text = doc.find(class_ = "list-tool-pagination-text").strong
#the page number is under the strong tag
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
#extracts the page number out of the string in strong by splitting it at the "/" into 3 separate strings
#then takes the middle/second one, -2, then splits again at ">" and takes the last element
#then turns that into an integer

items_found = {}

for page in range(1, pages + 1): #loop through pages, grabbing the elements on them
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_= "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))
    #this makes sure we're only grabbing the elements on the page that we want

        
    for item in items:
        parent = item.parent
        if parent.name != "a": #the link is under the a tag, so if the parent is not in a, skip and continue
            continue
        
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(","," ")), "link": link}
        except:
            pass
        #obtains the price which is under the parent item-container. Used try except ti work around an AttributeError encountered
        
sorted_items= sorted(items_found.items(), key=lambda x: x[1]['price'])
#sorts the list of items, placing the prices in ascending order

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("-------------------------")
#prints the item name, price, link, as well as a string of dashes to separate and make the list more readable
