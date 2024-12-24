# 0. Import necessary packages
import requests as req
from bs4 import BeautifulSoup as bs
import re
import os


# 1. Get all chinese books urls as dictionary
url = "https://www.gutenberg.org/browse/languages/zh"
res = req.get(url)
soup = bs(res.text, "lxml")

# 1.1 The selector of books info and then store all <a> as a list
selector = "body > div.container > div > div.pgdbbylanguage > ul > li > a"
soup_a_element_list = soup.select(selector)


# 1.2 Function to filter chinese book
def is_all_chinese(text):
    chinese_pattern = re.compile(r'^[\u4e00-\u9fff]+$')
    return bool(chinese_pattern.match(text))


# 1.3 Get all book title and url from <a> and then store at a dict
book_dict = {}
for a_element in soup_a_element_list:
    book_title = a_element.text 
    text_url = f"https://www.gutenberg.org{a_element['href']}.txt.utf-8"
    if is_all_chinese(book_title):
        book_dict[book_title] = text_url


# 2. Navigate to the url of text and download as .txt files

# 2.1 Stored path
folder_name = "project_gutenberg"
current_directory = os.getcwd()
folder_path = os.path.join(current_directory, folder_name)

# Download as file .txt at "project_gutenberg"
for book_title, text_url in book_dict.items():
    text_str = req.get(text_url).text
    # Text structure
    # The biginning of text is "*** START OF THE PROJECT GUTENBERG EBOOK book_title ***"
    # The end of text is "Updated"
    start_index = text_str.index(f"*** START OF THE PROJECT GUTENBERG EBOOK {book_title} ***")
    end_index = text_str.index("Updated")
    # Filter the contents
    content_str = text_str[start_index:end_index]
    # Download the contents as file .txt
    file_name = book_title + '.txt'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content_str)
