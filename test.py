# Task 1

import requests
import json


class GetCountry:
    def __init__(self, country_code):
        code = {"codes": country_code}
        url = requests.get("https://restcountries.com/v3.1/alpha", params=code)
        country_str = url.text[1:-1]
        country_json = json.loads(country_str)
        country = country_json["name"]["common"]
        capital = country_json["capital"][0]
        flag = country_json["flags"]["png"]

        print(
            f"{'Country':10} {'Capital':^10} {'Flag':^30}\n{country:10} {capital:^10} {flag:^30}"
        )

GetCountry("UA")

# Task 2

import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class GetItemInfo:
    def __init__(self, url_from_find):

        url = requests.get(url_from_find)
        convert_page = url.text
        get_page = BeautifulSoup(convert_page, "html.parser")
        find_tag_product_name = get_page.find("h1", class_="x-item-title__mainTitle")
        tag_product_name = find_tag_product_name.contents[4]
        product_name = tag_product_name.contents[0]

        find_tag_product_image = get_page.find_all(
            "div", class_="ux-image-carousel-item"
        )
        count_tag = int(len(find_tag_product_image) / 2)
        step = 0
        new_list_images_url = []
        patter = r"(?<=data-zoom-src=\").*?(?=\" )"
        while step < count_tag:
            finding_image_url = re.search(patter, str(find_tag_product_image[step]))[0]
            new_list_images_url.append(finding_image_url)
            step += 1

        find_tag_price = get_page.find("div", class_="x-price-primary")
        price = find_tag_price.contents[3].contents[0]

        driver = webdriver.Edge()
        driver.get(url_from_find)
        find_tag_shipping = driver.find_element(
            By.CLASS_NAME, "ux-labels-values__values-content"
        ).text
        patter2 = r"\D\d{1,}.\d{1,}"
        try:
            shipping_price = re.search(patter2, find_tag_shipping)[0]
        except:
            shipping_price = "Does not ship in your country"

        find_tag_seller = get_page.find(
            "div", class_="x-sellercard-atf__info__about-seller"
        )
        finding_seller = find_tag_seller.get("title")

        find_tag_url = get_page.find("link", rel="canonical")
        find_url = find_tag_url.contents[2]
        get_url = find_url.get("content")

        print(
            f" Product name: {product_name}\nProduct link: {get_url}\nPrice: {price}\nShipping: {shipping_price}\nSeller: {finding_seller}\nImages: {str(new_list_images_url)}"
        )

GetItemInfo("https://www.ebay.com/itm/315492450880")
