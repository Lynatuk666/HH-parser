import requests
from fake_headers import Headers
import bs4
import json
import re

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
    try:
        city = vacancy_tag.find("span", attrs={"class": "bloko-text","data-qa": "vacancy-serp__vacancy-address"}).text
    except:
        city = "не указан"
    new_response = requests.get(link, headers=header)
    vacancy_page_data = bs4.BeautifulSoup(new_response.text,
                                          features="lxml")
    try:
        salary = vacancy_page_data.find("span", class_="magritte-text___pbpft_3-0-13 magritte-text_style-primary___AQ7MW_3-0-13 magritte-text_typography-label-1-regular___pi3R-_3-0-13").text
        salary = re.sub("&nbsp", "", salary)
    except AttributeError:
        salary = "не указано"
    try:
        vacancy_description = vacancy_page_data.find("div", class_="g-user-content").text
    except:
        vacancy_description = "no description"
    if "Django" in vacancy_description or "Flask" in vacancy_description:
        vacancy_inf = {"vacancy_name": name, "city": city, "salary": salary, "link": link}
        vacancies[name] = vacancy_inf
        #print(name)
        #print(salary)
with open("data.json", "w", encoding="UTF-8") as file:
    json.dump(vacancies, file)
print(f"данные записаны. Собрано {len(vacancies)} вакансий")
