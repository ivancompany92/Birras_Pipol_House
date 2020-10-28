import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os

HEADER = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/81.0.4044.141 Safari/537.36"}


# acquisition functions
# scraping Carrefour function:
def scraping_carrefour():
    print('Starting to scrape Carrefour...')
    list_pages_carrefour = list(range(0, 336, 24))
    table_pages_carrefour = []
    for num in list_pages_carrefour:
        url_carrefour = f'https://www.carrefour.es/supermercado/bebidas/cerveza/todas-las-cervezas/N-1uq8b5u/c?No={num}'
        html = requests.get(url_carrefour, headers=HEADER).text
        soup_carrefour = BeautifulSoup(html, 'lxml')
        table_carrefour = soup_carrefour.find_all({'article': 'product-card-item'})
        table_pages_carrefour.append(table_carrefour)
    return table_pages_carrefour


def info_carrefour(scraping_list_info):
    data_raw_carrefour = []
    for i in range(len(scraping_list_info)):
        for j in range(len(scraping_list_info[i])):
            rows_carrefour = scraping_list_info[i][j].find_all(['span', 'p', 'a'], {
                'class': ['price', 'price-less', 'format-price', 'js-gap-product-click-super']})
            promotion_carrefour = scraping_list_info[i][j].find_all(['p'], {'class': ['promocion-copy']})
            if len(rows_carrefour) != 0:
                if len(promotion_carrefour) != 0:
                    data_raw_carrefour.append(rows_carrefour + promotion_carrefour)
                else:
                    data_raw_carrefour.append(rows_carrefour)
    print('Finished scraping Carrefour')
    return data_raw_carrefour


def get_price_carrefour(data_text):
    price_raw = data_text.text
    price = re.sub('\xa0€', '', price_raw)
    price = re.sub('\n', '', price)
    return float(re.sub(",", '.', price))


def get_price_l_carrefour(data_text):
    price_l_raw = data_text.text
    price_l = re.findall('[0-9]+,[0-9]+', price_l_raw)
    price_liter = re.sub(',', '.', price_l[0])
    return float(price_liter)


def get_title_carrefour(data_text):
    title_raw = data_text.text
    title = re.sub("\n", '', title_raw)
    return title


def get_promotion_carrefour(data_text):
    promotion_raw = data_text.text
    promotion = re.sub("\n", '', promotion_raw)
    return promotion


def get_brand_carrefour(data_text):
    brand_raw = data_text.text
    brand = re.split('(Cerveza )|( pack)|( botella)|( lata)+|(cl)', brand_raw)
    return brand[6].lower()


def get_container(data_text):
    container_raw = data_text.text
    container = re.findall('botella|lata|barril', container_raw)
    if len(container) != 0:
        return container[0]
    else:
        return 'No specified'


def get_volumen_unid_carrefour(data_text):
    volumen_raw = data_text.text
    volumen = re.findall('[0-9,.]+ cl', volumen_raw)
    if len(volumen) != 0:
        return volumen[0]
    else:
        volumen_l = re.findall('[0-9,.]+[ mcl]+', volumen_raw)
        return volumen_l[0]


def get_quantity_pack(data_text):
    quantity_raw = data_text.text
    quantity_split = re.split('pack de|pack', quantity_raw)
    if len(quantity_split) == 2:
        quantity = re.findall('[0-9]+', quantity_split[1])
        return quantity[0]
    else:
        return 1


def get_image_carrefour(data_text):
    return data_text.find_all('img')[0].get('src')


def database_carrefour(data_raw_carrefour):
    data_beer_carrefour = pd.DataFrame(index=range(0, len(data_raw_carrefour)),
                                       columns=['price', 'price_liter', 'title', 'promotion', 'brand',
                                                'container', 'volumen_unid', 'quantity_pack', 'image_url',
                                                'supermarket'])
    for beer_number in range(len(data_raw_carrefour)):
        data_beer_carrefour.iloc[beer_number, 0] = get_price_carrefour(data_raw_carrefour[beer_number][1])
        data_beer_carrefour.iloc[beer_number, 1] = get_price_l_carrefour(data_raw_carrefour[beer_number][2])
        data_beer_carrefour.iloc[beer_number, 2] = get_title_carrefour(data_raw_carrefour[beer_number][3])
        data_beer_carrefour.iloc[beer_number, 4] = get_brand_carrefour(data_raw_carrefour[beer_number][3])
        data_beer_carrefour.iloc[beer_number, 5] = get_container(data_raw_carrefour[beer_number][3])
        data_beer_carrefour.iloc[beer_number, 6] = get_volumen_unid_carrefour(data_raw_carrefour[beer_number][3])
        data_beer_carrefour.iloc[beer_number, 7] = get_quantity_pack(data_raw_carrefour[beer_number][3])
        data_beer_carrefour.iloc[beer_number, 8] = get_image_carrefour(data_raw_carrefour[beer_number][0])
        data_beer_carrefour.iloc[beer_number, 9] = 'Carrefour'
        if len(data_raw_carrefour[beer_number]) > 4:
            data_beer_carrefour.iloc[beer_number, 3] = get_promotion_carrefour(data_raw_carrefour[beer_number][4])
        else:
            data_beer_carrefour.iloc[beer_number, 3] = 'No promotion'
    return data_beer_carrefour


# scraping Alcampo function:
def scraping_alcampo():
    print('Starting to scrape Alcampo...')
    list_pages_alcampo = list(range(0, 10))
    table_pages_alcampo = []
    for number in list_pages_alcampo:
        url_alcampo = f'https://www.alcampo.es/compra-online/bebidas/cervezas/c/W1107?q=%3Arelevance&page={number}'
        html = requests.get(url_alcampo, headers=HEADER).text
        soup_alcampo = BeautifulSoup(html, 'lxml')
        table_alcampo = soup_alcampo.find_all('div', {'class': 'productGridItem'})
        table_pages_alcampo.append(table_alcampo)
    return table_pages_alcampo


def info_alcampo(table_pages_alcampo):
    data_raw_alcampo = []
    for i in range(len(table_pages_alcampo)):
        for j in range(len(table_pages_alcampo[i])):
            rows_alcampo = table_pages_alcampo[i][j].find_all(['span', 'div'], {'class': ['price',
                                                                                          'productName',
                                                                                          'thumb cut-alt-img']})
            promotion_alcampo = table_pages_alcampo[i][j].find_all('div', {'class': 'financiacionMensual'})
            if len(rows_alcampo) != 0:
                if len(promotion_alcampo) != 0:
                    data_raw_alcampo.append(rows_alcampo + promotion_alcampo)
                else:
                    data_raw_alcampo.append(rows_alcampo)
    print('Finished scraping Alcampo')
    return data_raw_alcampo


# price Alcampo / Corte Ingles / Dia
def get_price_al_ce_dia(data_text):
    price_raw = data_text.text
    price = re.findall('[0-9,]+', price_raw)
    return float(re.sub(",", '.', price[0]))


# price_liter Alcampo / Corte Ingles / Dia
def get_price_l_al_ce_dia(data_text):
    price_raw = data_text.text
    price = re.findall('[0-9,]+', price_raw)
    if len(price) == 1:
        return float(re.sub(",", '.', price[0]))
    else:
        return float(re.sub(",", '.', price[1]))


# title Alcampo / Corte Ingles
def get_title_al_ce(data_text):
    tittle_raw = data_text.text
    tittle = re.sub('\n', '', tittle_raw)
    return tittle.lower()


# promotion Alcampo / Corte Ingles / Dia
def get_promotion_al_ce_dia(data_text):
    promotion_raw = data_text.text
    promotion_pre = re.sub('\r\n\r\n\t\t\t\t\t\t\t\t\t\t', '', promotion_raw)
    promotion = re.sub('Ver promoción ¡pulsa aquí!', '', promotion_pre)
    return promotion


# brand Alcampo
def get_brand_alcampo(data_text):
    brand_raw = data_text.text
    brand = re.sub('\n', '', brand_raw)
    brand = brand.lower()
    brand_2 = re.sub('cervez\S+', '', brand)
    return brand_2


# volumen Alcampo / Corte ingles / Dia
def get_volumen_unid_al_ce_dia(data_text):
    volumen_raw = data_text.text
    volumen = re.findall('[0-9.,]+ cl|33 c|25 c|50 c|1 l| 2 l', volumen_raw)
    if len(volumen) != 0:
        return volumen[0]
    else:
        volumen_l = re.findall('[0-9.,]+[ mclL]+', volumen_raw)
        if len(volumen_l) == 2:
            return volumen_l[1]
        else:
            return volumen_l[0]


# image Alcampo
def get_image_alcampo(data_text):
    return data_text.find_all('img')[0].get('data-blzsrc')


def database_alcampo(data_raw_alcampo):
    data_beer_alcampo = pd.DataFrame(index=range(0, len(data_raw_alcampo)),
                                     columns=['price', 'price_liter', 'title', 'promotion', 'brand',
                                              'container', 'volumen_unid', 'quantity_pack', 'image_url',
                                              'supermarket'])
    for beer_number in range(len(data_raw_alcampo)):
        data_beer_alcampo.iloc[beer_number, 0] = get_price_al_ce_dia(data_raw_alcampo[beer_number][2])
        data_beer_alcampo.iloc[beer_number, 1] = get_price_l_al_ce_dia(data_raw_alcampo[beer_number][2])
        data_beer_alcampo.iloc[beer_number, 2] = get_title_al_ce(data_raw_alcampo[beer_number][1])
        data_beer_alcampo.iloc[beer_number, 4] = get_brand_alcampo(data_raw_alcampo[beer_number][1])
        data_beer_alcampo.iloc[beer_number, 5] = get_container(data_raw_alcampo[beer_number][1])
        data_beer_alcampo.iloc[beer_number, 6] = get_volumen_unid_al_ce_dia(data_raw_alcampo[beer_number][1])
        data_beer_alcampo.iloc[beer_number, 7] = get_quantity_pack(data_raw_alcampo[beer_number][1])
        data_beer_alcampo.iloc[beer_number, 8] = get_image_alcampo(data_raw_alcampo[beer_number][0])
        data_beer_alcampo.iloc[beer_number, 9] = 'Alcampo'
        if len(data_raw_alcampo[beer_number]) > 3:
            data_beer_alcampo.iloc[beer_number, 3] = get_promotion_al_ce_dia(data_raw_alcampo[beer_number][3])
        else:
            data_beer_alcampo.iloc[beer_number, 3] = 'No promotion'
    return data_beer_alcampo


# scraping Corte Ingles function:
def scraping_corteingles():
    print('Starting to scrape Corte Ingles...')
    list_pages_corteingles = list(range(1, 26))
    table_pages_corteingles = []
    for number in list_pages_corteingles:
        url_corteingles = f'https://elcorteingles.es/supermercado/bebidas/cervezas/{number}/'
        html = requests.get(url_corteingles, headers=HEADER).text
        soup_corteingles = BeautifulSoup(html, 'lxml')
        table_corteingles = soup_corteingles.find_all('div', {'class': 'grid-item'})
        table_pages_corteingles.append(table_corteingles)
    return table_pages_corteingles


def info_corteingles(table_pages_corteingles):
    data_raw_corteingles = []
    for i in range(len(table_pages_corteingles)):
        for j in range(len(table_pages_corteingles[i])):
            rows_corteingles = table_pages_corteingles[i][j].find_all(['div', 'h3'],
                                                                      {'class': ['prices-price',
                                                                                 'product_tile-description',
                                                                                 'product_tile-image _fade']})
            promotion_corteingles = table_pages_corteingles[i][j].find_all('div',
                                                                           {'class': 'product_tile-offer offer'})
            if len(rows_corteingles) > 4:
                rows_corteingles.pop(1)
            if len(rows_corteingles) > 3:
                if len(promotion_corteingles) != 0:
                    data_raw_corteingles.append(rows_corteingles + promotion_corteingles)
                else:
                    data_raw_corteingles.append(rows_corteingles)
    print('Finished scraping Corte Ingles')
    return data_raw_corteingles


# brand Corte Ingles
def get_brand_corteingles(data_text):
    brand_raw = data_text.text
    brand = re.split('cervez', brand_raw)
    return brand[0].lower()


# volumen Corte Ingles
def get_volumen_corteingles(data_text):
    brand_raw = data_text.text
    brand = re.split('botel', brand_raw)
    return brand[0]


# #image Corte Ingles
def get_image_corteingles(data_text):
    return 'https:' + data_text.find_all('img')[0].get('src')


def database_corteingles(data_raw_corteingles):
    data_beer_corteingles = pd.DataFrame(index=range(0, len(data_raw_corteingles)),
                                         columns=['price', 'price_liter', 'title', 'promotion', 'brand',
                                                  'container', 'volumen_unid', 'quantity_pack', 'image_url',
                                                  'supermarket'])
    for beer_number in range(len(data_raw_corteingles)):
        data_beer_corteingles.iloc[beer_number, 0] = get_price_al_ce_dia(data_raw_corteingles[beer_number][1])
        data_beer_corteingles.iloc[beer_number, 1] = get_price_l_al_ce_dia(data_raw_corteingles[beer_number][2])
        data_beer_corteingles.iloc[beer_number, 2] = get_title_al_ce(data_raw_corteingles[beer_number][3])
        data_beer_corteingles.iloc[beer_number, 4] = get_brand_corteingles(data_raw_corteingles[beer_number][3])
        data_beer_corteingles.iloc[beer_number, 5] = get_container(data_raw_corteingles[beer_number][3])
        data_beer_corteingles.iloc[beer_number, 6] = get_volumen_unid_al_ce_dia(data_raw_corteingles[beer_number][3])
        data_beer_corteingles.iloc[beer_number, 7] = get_quantity_pack(data_raw_corteingles[beer_number][3])
        data_beer_corteingles.iloc[beer_number, 8] = get_image_corteingles(data_raw_corteingles[beer_number][0])
        data_beer_corteingles.iloc[beer_number, 9] = 'El Corte Ingles'
        if len(data_raw_corteingles[beer_number]) > 4:
            data_beer_corteingles.iloc[beer_number, 3] = get_promotion_al_ce_dia(data_raw_corteingles[beer_number][4])
            if len(data_raw_corteingles[beer_number]) > 5:
                data_beer_corteingles.iloc[beer_number, 3] += '..SECOND OFFERT: ' + \
                                                              get_promotion_al_ce_dia(data_raw_corteingles[beer_number][5])
        else:
            data_beer_corteingles.iloc[beer_number, 3] = 'No promotion'
    return data_beer_corteingles


# scraping Dia function:
def scraping_dia():
    print('Starting to scrape Dia...')
    list_pages_dia = list(range(0, 3))
    table_pages_dia = []
    for number in list_pages_dia:
        url_dia = f'https://www.dia.es/compra-online/productos/bebidas/cervezas/c/WEB.008.064.00000?page={number}&disp='
        html = requests.get(url_dia, headers=HEADER).text
        soup_dia = BeautifulSoup(html, 'lxml')
        table_dia = soup_dia.find_all('div', {'class': 'prod_grid'})
        table_pages_dia.append(table_dia)
    return table_pages_dia


def info_dia(table_pages_dia):
    data_raw_dia = []
    for i in range(len(table_pages_dia)):
        for j in range(len(table_pages_dia[i])):
            rows_dia = table_pages_dia[i][j].find_all(['div', 'span'],
                                                      {'class': ['price_container', 'details', 'thumb']})
            if len(rows_dia) > 2:
                data_raw_dia.append(rows_dia)
    print('Finished scraping Dia')
    return data_raw_dia


# title Dia
def get_tittle_dia(data_text):
    tittle_raw = data_text.text
    tittle = re.sub('\r\n\t\t\t\t', '', tittle_raw)
    return tittle


# brand Dia
def get_brand_dia(data_text):
    brand_raw = data_text.text
    brand_sub = re.sub('\r\n\t\t\t\t', '', brand_raw)
    brand = re.split(' cervez', brand_sub)
    return brand[0].lower()


# image Dia
def get_image_dia(data_text):
    return data_text.find_all('img')[0].get('data-original')


def database_dia(data_raw_dia):
    data_beer_dia = pd.DataFrame(index=range(0, len(data_raw_dia)),
                                 columns=['price', 'price_liter', 'title', 'promotion', 'brand',
                                          'container', 'volumen_unid', 'quantity_pack', 'image_url',
                                          'supermarket'])
    for beer_number in range(len(data_raw_dia)):
        data_beer_dia.iloc[beer_number, 0] = get_price_al_ce_dia(data_raw_dia[beer_number][2])
        data_beer_dia.iloc[beer_number, 1] = get_price_l_al_ce_dia(data_raw_dia[beer_number][2])
        data_beer_dia.iloc[beer_number, 2] = get_tittle_dia(data_raw_dia[beer_number][1])
        data_beer_dia.iloc[beer_number, 4] = get_brand_dia(data_raw_dia[beer_number][1])
        data_beer_dia.iloc[beer_number, 5] = get_container(data_raw_dia[beer_number][1])
        data_beer_dia.iloc[beer_number, 6] = get_volumen_unid_al_ce_dia(data_raw_dia[beer_number][1])
        data_beer_dia.iloc[beer_number, 7] = get_quantity_pack(data_raw_dia[beer_number][1])
        data_beer_dia.iloc[beer_number, 8] = get_image_dia(data_raw_dia[beer_number][0])
        data_beer_dia.iloc[beer_number, 9] = 'Dia'
        if len(data_raw_dia[beer_number]) > 3:
            data_beer_dia.iloc[beer_number, 3] = get_promotion_al_ce_dia(data_raw_dia[beer_number][3])
        else:
            data_beer_dia.iloc[beer_number, 3] = 'No promotion'
    return data_beer_dia


# scraping Eroski function:
def scraping_eroski():
    print('Starting to scrape Eroski...')
    os.environ['PATH'] = f'{os.environ["PATH"]}:{os.getcwd()}'
    driver_options = Options()
    driver_options.headless = True
    driver = webdriver.Firefox(options=driver_options)
    driver.get('https://supermercado.eroski.es/es/supermercado/2060211-bebidas/2060233-cervezas/')
    for i in range(20):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1.1)
    selenium_raw_eroski = driver.find_elements_by_class_name('product-item')
    images = driver.find_elements_by_tag_name('img')
    return selenium_raw_eroski, images


def images_eroski(images):
    list_images = []
    for i in images:
        list_images.append(i.get_attribute('src'))

    beer_images_eroski = []
    for i in list_images:
        if 'https://supermercado.eroski.es/images/' in i:
            beer_images_eroski.append(i)
    return beer_images_eroski


def info_eroski(selenium_raw_eroski):
    data_raw_eroski = []
    for i in selenium_raw_eroski:
        data_raw_eroski.append(i.text)
    print('Finished scraping Eroski')
    return data_raw_eroski


# price Eroski
def get_price_eroski(data_text):
    price = re.findall('[0-9,]+', data_text)
    last = len(price) - 1
    return float(re.sub(",", '.', price[last]))


# price_liter Eroski
def get_price_liter_eroski(data_text):
    price_raw = re.split(' LITRO A ', data_text)
    if len(price_raw) > 1:
        price = re.findall('[0-9,]+', price_raw[1])
    else:
        price = re.findall('[0-9,]{2,}', data_text)
    return float(re.sub(",", '.', price[0]))


# title Eroski
def get_tittle_eroski(data_text):
    tittle = re.split('\n', data_text)
    return tittle[1]


# brand Eroski
def get_brand_eroski(data_text):
    brand_raw = re.split('erveza |, |ider |idra ', data_text)
    return brand_raw[1].lower()


# container Eroski
def get_container_eroski(data_text):
    container = re.findall('botella|lata|barril', data_text)
    if len(container) != 0:
        return container[0]
    else:
        return 'No specified'


# volume Eroski
def get_volumen_unid_eroski(data_text):
    volumen = re.findall('[0-9.,]+ cl|[125] l', data_text)
    if len(volumen) != 0:
        return volumen[0]
    else:
        volumen_l = re.findall('[0-9.,]+[ mclL]+', data_text)
        if len(volumen_l) == 2:
            return volumen_l[1]
        else:
            return volumen_l[0]


# quantity Eroski
def get_quantity_pack_eroski(data_text):
    quantity_split = re.split('pack de|pack', data_text)
    if len(quantity_split) == 2:
        quantity = re.findall('[0-9]+', quantity_split[1])
        return quantity[0]
    else:
        return 1


# promotion Eroski
def get_promotion_eroski(data_text):
    promotion = re.split("\n", data_text)
    if len(promotion) > 8:
        number = len(promotion) - 6
        return promotion[number] + ' ' + promotion[number + 1]
    else:
        return 'No promotion'


# image Eroski
def get_image_eroski(beer_images_eroski, number):
    return beer_images_eroski[number * 2]


def database_eroski(data_raw_eroski, beer_images_eroski):
    data_beer_eroski = pd.DataFrame(index=range(0, len(data_raw_eroski)),
                                    columns=['price', 'price_liter', 'title', 'promotion', 'brand',
                                             'container', 'volumen_unid', 'quantity_pack', 'image_url',
                                             'supermarket'])
    for beer_number in range(len(data_raw_eroski)):
        data_beer_eroski.iloc[beer_number, 0] = get_price_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 1] = get_price_liter_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 2] = get_tittle_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 3] = get_promotion_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 4] = get_brand_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 5] = get_container_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 6] = get_volumen_unid_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 7] = get_quantity_pack_eroski(data_raw_eroski[beer_number])
        data_beer_eroski.iloc[beer_number, 8] = get_image_eroski(beer_images_eroski, beer_number)
        data_beer_eroski.iloc[beer_number, 9] = 'Eroski'
    return data_beer_eroski


def carrefour_fun():
    carrefour_data = info_carrefour(scraping_carrefour())
    carrefour = database_carrefour(carrefour_data)
    return carrefour


def alcampo_fun():
    alcampo_data = info_alcampo(scraping_alcampo())
    alcampo = database_alcampo(alcampo_data)
    return alcampo


def corteingles_fun():
    corteingles_data = info_corteingles(scraping_corteingles())
    corte_ingles = database_corteingles(corteingles_data)
    return corte_ingles


def dia_fun():
    dia_data = info_dia(scraping_dia())
    dia = database_dia(dia_data)
    return dia

def eroski_fun():
    selenium_raw_eroski, images = scraping_eroski()
    data_images = images_eroski(images)
    eroski_data = info_eroski(selenium_raw_eroski)
    eroski = database_eroski(eroski_data, data_images)
    return eroski


def save_df_products(data, name):
    data.to_csv(f'./data/processed/data_beer_{name}.csv', index=False)


def acquire(scrape):
    if scrape == 'Y':
        car = carrefour_fun()
        alc = alcampo_fun()
        coi = corteingles_fun()
        dia = dia_fun()
        ero = eroski_fun()
        save_df_products(car, 'carrefour')
        save_df_products(alc, 'alcampo')
        save_df_products(coi, 'corteingles')
        save_df_products(dia, 'dia')
        save_df_products(ero, 'eroski')
        print('finish saved DFs')
    else:
        pass

