import codecs
from urllib.request import urlopen

import re

import requests
import bs4 as bs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os  # allows for directory manipulation
import webbrowser  # allows for displaying websites in browsers

# NOTE
# selenium automates browsers
# chromedriver targets chrome

driver = webdriver.Chrome(ChromeDriverManager().install())   # open chrome through driver
driver.get("https://www.costco.ca/laptops.html")    # opens link
# Bestbuy Link
# https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352

# Option 2
# chrome_options = Options()
# driver = webdriver.Chrome(executable_path=r"C:\Users\Kevin\Downloads\chromedriver_win32.zip\chromedriver.exe", options=chrome_options)

# Option 3: Antiwebscraping Blocked
# page = requests.get(URL)


target_soup = BeautifulSoup(driver.page_source, 'lxml')  # parses site

html = codecs.open("test.html", "r", "utf-8")  # reads local html
replacement_soup = BeautifulSoup(html, 'lxml')  # html -> Soup parsing

# Option 2
# html = urlopen('file:///' + os.path.abspath('test.html')); #reads html from

# NOTE
# html.parser- built-in - no extra dependencies needed
# html5lib - the most lenient - better use it if HTML is broken
# lxml - the fastest
#
# lenient parsing: can interpret inputs that do not match strict formats


class Item:
    name = ""
    html = ""
    link = ""
    price = 0
    description = ""
    spec_list = []
    sale = 0
    out_of_stock = False

    def __init__(self, name, html):
        self.name = name
        self.html = html


item_list = []


if __name__ == '__main__':
    # print(soup.prettify())

    target_soup.prettify()  # Soup -> String

    html_item_list = target_soup.find_all("span", {'class' : 'description'})  # extracts all items on site

    # stores data from html into Item object
    for i in range(len(html_item_list)):
        cur_html = html_item_list[i]
        item_as_string = str(html_item_list[i])
        item_as_string_front_chopped = item_as_string[item_as_string.find("href"):]
        cur_link = re.findall(r'href="([^"]*)"', item_as_string_front_chopped)[0]
        # item_list[i].name = re.findall(item_list[i].link + '">([^<]*)<', html_item_list[i])
        item_list.append(Item(cur_html, cur_link))
        print(item_list[i].link)

    items_as_string = ""  # converts items into string awaiting insert to HTML

    # turns list of items into a chunk of html text
    for item in html_item_list:
        items_as_string += str(item) + "\n"

    #reads html file
    # with open(r"C:\Users\Kevin\Desktop\Dev\Webscraper\test.html", 'r') as f:

        # f.write(items_as_string)

        # replacement_soup = BeautifulSoup(f.read());

    title = "<h1>\n Welcome to Scrap Yard\n </h1> \n"

    # replacement_soup.body.append("<body>" + items_as_string + "</body>", 'html.parser')
    replacement_soup.find("body").replace_with("<body> \n" + title + items_as_string + "</body>")

    with open(r"C:\Users\Kevin\Desktop\Dev\Webscraper\test.html", 'w') as f:
        new_str = str(replacement_soup.prettify())  # Soup -> String

        # fixes "<" and ">" in html
        new_str = new_str.replace("&lt;", "<")
        new_str = new_str.replace("&gt;", ">")

        new_str = new_str.replace("</a>", "</a> <br>")  # adds some line breaks

        f.write(new_str)  # inputs into html file

        driver.quit()  # closes chrome driver













