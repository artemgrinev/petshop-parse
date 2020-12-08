import requests
from bs4 import BeautifulSoup
import pickle

class LinksPetshop:
    def __init__(self, url):
        self.url = url
        self.html = self.get_html()
        self.soup = self.get_soup()
        
    def get_html(self):
        try:
            r = requests.get(self.url)
            r.raise_for_status()
            return r.text
        except(requests.RequestException, ValueError):
            print('Server error')
            return False
        
    def get_soup(self):
        soup = BeautifulSoup(self.html, 'lxml')
        return soup
     
    def bs(self, url):
        html = LinksPetshop(url)
        s = html.get_soup()
        return s
    
    def catalog_links(self):
        catalog_links =[]
        catalog = self.soup.find_all("a", class_="categories__title-link")
        links = [i.get('href') for i in catalog]
        animals_categories = [i.split('/')[-2] for i in links]
        catalog_links = [f'https://www.petshop.ru/catalog/{i}/' for i in animals_categories]
        return list(filter(None, catalog_links))

    def categories_links(self):
        categories_link = []
        for url in self.catalog_links():
            soup = self.bs(url)
            categories = soup.find_all('a', class_='categories__title-link')           
            for i in categories:
                links = 'https://www.petshop.ru' + i.get('href')
                categories_link.append(links)
        return list(filter(None, categories_link))

    def product_links(self):
        product_links =[]
        for urls in self.get_categories():
            print("categories:" + urls.split('/')[4])
            print('    '+urls.split('/')[-2])
            soup = self.bs(urls)
            try:
                number_of_pages = int(soup.find('div', class_='page-navigation').find_all('a')[-2].text)
            except:
                number_of_pages = 1
            products_list = []
            for i in range(1,number_of_pages+1):
                u = f'{urls}?page={i}'
                soup = self.bs(u)
                print(u)
                print(f'        processing page: {i}')
                for a in soup.find_all('a', class_='j_product-brand j_product-link'):
                    url = 'https://www.petshop.ru' + a.get('href')
                    soup = self.bs(url)
                    count = 0
                    for i in soup.find_all('label', class_ = 'style_tile_label__NBrsJ'):
                        count += 1
                        label_id =f'{url}?oid='+i['id']
                        products_list.append(label_id)
                        print('            packing size: ' + str(count))
                    print('next product')

if __name__ == "__main__":
    url = 'https://www.petshop.ru/catalog/'
    get_links = LinksPetshop(url)