from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

def get_category_detail_urls(driver):
    category_elements = driver.find_elements(By.XPATH, "//a[contains(text(),'Travel') or contains(text(),'Nonfiction')]")
    category_detail_links = []
    for category_element in category_elements:
        category_detail_links.append(category_element.get_attribute("href"))
    return category_detail_links

def get_book_links_from_category(driver, category_url):
    all_book_links = []
    driver.get(category_url)
    time.sleep(2)
    book_detail_links = driver.find_elements(By.XPATH, "//h3/a")
    for book_detail_link in book_detail_links:
        href = book_detail_link.get_attribute("href")
        all_book_links.append(href)
    return all_book_links

def get_book_detail(driver, book_url):
    driver.get(book_url)
    time.sleep(2)
    div_element = driver.find_element(By.XPATH, "//div[@class='content']")
    inner_html = div_element.get_attribute("innerHTML")
    soup = BeautifulSoup(inner_html, "html.parser")
    name = soup.find("h1").text
    price = soup.find("p", attrs={"class":"price_color"}).text
    regex = re.compile("^star-rating ")
    star_elem = soup.find("p", attrs={"class":regex})
    star = star_elem["class"][-1] if star_elem else None
    product_info = {}
    table_rows = soup.find("table").find_all("tr")
    for row in table_rows:
        key = row.find("th").text
        value = row.find("td").text
        product_info[key] = value
    return {
        "name": name,
        "price": price,
        "star": star,
        "product_info": product_info
    }

driver = webdriver.Chrome(options=options)
driver.get("https://books.toscrape.com/")
time.sleep(2)

category_detail_links = get_category_detail_urls(driver)

all_book_links = []
for category_url in category_detail_links:
    all_book_links.extend(get_book_links_from_category(driver, category_url))

print(f"Toplam kitap linki: {len(all_book_links)}")

product_details = []
for book_link in all_book_links:
    detail = get_book_detail(driver, book_link)
    product_details.append(detail)
    print(detail)

driver.quit()







      


