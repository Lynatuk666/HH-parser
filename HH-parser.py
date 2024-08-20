import requests
from fake_headers import Headers
import bs4
import json

url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

header = Headers(
    browser="chrome",
    os="win",
    headers=True).generate()

response = requests.get(url, headers=header)
main_page_data = bs4.BeautifulSoup(response.text,
                                   features='lxml')
vacancy_tags = main_page_data.findAll("div", class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS")
vacancies = {}
for vacancy_tag in vacancy_tags:
    name = vacancy_tag.find("span", class_="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link").text
    link = vacancy_tag.find("a", class_="bloko-link")["href"]
    city = vacancy_tag.find(attrs={"class": "wide-container--lnYNwDTY2HXOzvtbTaHf","data-qa": "vacancy-serp__vacancy-address"}).text
    new_response = requests.get(link, headers=header)
    vacancy_page_data = bs4.BeautifulSoup(new_response.text,
                                          features="lxml")
    try:
        salary = vacancy_page_data.find("span", class_="magritte-text___pbpft_3-0-13 magritte-text_style-primary___AQ7MW_3-0-13 magritte-text_typography-label-1-regular___pi3R-_3-0-13").text
    except AttributeError:
        salary = "не указано"
    try:
        vacancy_description = vacancy_page_data.find("div", class_="g-user-content").text
    except:
        vacancy_description = "no description"
    if "Django" in vacancy_description or "Flask" in vacancy_description:
        #print(f"{name}, {city}, {salary}, {link}")
        vacancy_inf = {"vacancy_name": name, "city":city, "salary":salary, "link":link}
        vacancies[name] = vacancy_inf
        print(name)
with open("data.json", "w") as file:
    json.dump(vacancies, file)
print(len(vacancies))