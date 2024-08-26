import requests
from fake_headers import Headers
import bs4
import json
import re

def get_vacancies(url):
    header = Headers(browser="chrome", os="win", headers=True).generate()
    response = requests.get(url, headers=header)
    response.raise_for_status()  # Добавлена проверка на сетевые ошибки
    main_page_data = bs4.BeautifulSoup(response.text, 'lxml')
    return main_page_data.find_all("div", class_="vacancy-search-item__card")

def parse_vacancy(vacancy_tag, header):
    name = vacancy_tag.find("span", class_="vacancy-name").text
    link = vacancy_tag.find("a", class_="bloko-link")["href"]
    city = vacancy_tag.find("span", {"data-qa": "vacancy-serp__vacancy-address"}).get_text(strip=True, default="не указан")

    new_response = requests.get(link, headers=header)
    new_response.raise_for_status()  # Проверка на ошибки запроса
    vacancy_page_data = bs4.BeautifulSoup(new_response.text, "lxml")
    
    salary = vacancy_page_data.find("span", class_="salary").get_text(strip=True, default="не указано")
    salary = re.sub("&nbsp", "", salary)

    vacancy_description = vacancy_page_data.find("div", class_="g-user-content").get_text(strip=True, default="no description")

    if "Django" in vacancy_description or "Flask" in vacancy_description:
        return {"vacancy_name": name, "city": city, "salary": salary, "link": link}

def save_vacancies_to_json(vacancies, file_name="data.json"):
    with open(file_name, "w", encoding="UTF-8") as file:
        json.dump(vacancies, file, ensure_ascii=False, indent=2)
    print(f"Данные записаны. Собрано {len(vacancies)} вакансий.")

def main():
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    vacancies = {}
    try:
        header = Headers(browser="chrome", os="win", headers=True).generate()
        vacancy_tags = get_vacancies(url)
        
        for vacancy_tag in vacancy_tags:
            vacancy_data = parse_vacancy(vacancy_tag, header)
            if vacancy_data:
                vacancies[vacancy_data['vacancy_name']] = vacancy_data

        save_vacancies_to_json(vacancies)

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
