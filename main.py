import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from lxml import html
import json
from pprint import pprint


def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_vacancies():
    href = 'https://spb.hh.ru/search/vacancy'
    params = {
        'area': '2',
        'search_field':'name',
        'search_field':'company_name',
        'search_field':'description',
        'text':'python',
        'text':'Django',
        'text':'Flask',
        # 'currency_code':'USD',
        'ored_clusters':'true',
        'enable_snippets':'true'
    }
    html = requests.get(url=href, headers=get_headers(), params=params).text
    soup = BeautifulSoup(html,'lxml')
    vacancies_main_info = soup.findAll('div', class_="vacancy-serp-item-body__main-info")
    list_vacancies = []
    count = 0

    for vacancy_info in vacancies_main_info:
        link_vacancy = vacancy_info.find('a', class_="serp-item__title")['href']
        name_company = vacancy_info.find('a', class_="bloko-link bloko-link_kind-tertiary").text
        city = vacancy_info.findNext('div', class_='bloko-text').findNext('div', class_='bloko-text').text.split(',')[0]
        salary = vacancy_info.find('span', class_="bloko-header-section-3")
        #требование для проверки вхождения в требования ключевых слов
        requirement = vacancy_info.findNext('div', class_='g-user-content').findNext('div', class_='bloko-text').next_element.next_element.next_element.text

        if salary != None:
            salary = vacancy_info.find('span', class_="bloko-header-section-3").text
        else:
            salary = 'not specified'
        # print(city)
        # print(salary)
        # print(requirement)
        # print(name_company)
        list_vacancies.append({
            'link' : link_vacancy,
            'salary' : salary,
            'name_company' : name_company,
            'city' : city
        })
        count += 1
    print('Получено вакансий - ', count)
    return list_vacancies

if __name__ == '__main__':
    list_vacancies = get_vacancies()
    with open('vacancies_python_hh_ru.json', 'w', encoding="utf-8") as file:
        json.dump(list_vacancies,file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

