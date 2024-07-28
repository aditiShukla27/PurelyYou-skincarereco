from bs4 import BeautifulSoup
import requests


start = 'https://www.skincarisma.com/search?category=Serums%2C+Essence%2C+Ampoules&page='

for i in range(1,193):
    new_link = start+str(i)
    source = requests.get(new_link).text
    soup = BeautifulSoup(source, 'html.parser')

    skin_list = soup.find('ul', class_='list-unstyled mt-2 mb-0')

    for skincare in skin_list.find_all('li'):
        details = skincare.find('a')['href']
        link = "https://www.skincarisma.com/"+details+"/ingredient_list"
        # print(link)
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'html.parser')

        brand = soup.find('h2', class_="font-090 d-inline-block text-muted").text
        product = soup.find('h1', class_='card-title font-125').text

        ingredient_list = soup.find('table', class_='table table-sm mt-4 ingredients-table').tbody
        properties = []

        for ingredient in ingredient_list.find_all('tr'):
            details = ingredient.find_all('td', class_='align-middle')[3]
            item = details.find('span')
            if item:
                text = item.text
                text_simplified = text.replace("\n", "")
                properties.append(text_simplified)

        print(brand, product, properties)