import streamlit as st
import pandas as pd
import webbrowser
import re

CARREFOUR_LINK = 'https://www.carrefour.es/?q='
ALCAMPO_LINK = 'https://www.alcampo.es/compra-online/search/?department=&text='
CORTEINGLES_LINK = 'https://www.elcorteingles.es/supermercado/buscar/?term='
DIA_LINK = 'https://www.dia.es/compra-online/search?text='
EROSKI_LINK = 'https://supermercado.eroski.es/es/search/multiple/?q='


def url_web(best_place, number, data):
    if best_place == 'Carrefour':
        place = data['title'].tolist()
        return CARREFOUR_LINK + place[number]
    if best_place == 'Alcampo':
        place = data['title'].tolist()
        return ALCAMPO_LINK + place[number]
    if best_place == 'El Corte Ingles':
        place = data['title'].tolist()
        return CORTEINGLES_LINK + place[number]
    if best_place == 'Dia':
        place = data['title'].tolist()
        return DIA_LINK + place[number]
    if best_place == 'Eroski':
        place = data['title'].tolist()
        change = re.split(',', place[number])
        return EROSKI_LINK + change[0]


def cheap_beers(number, brands, quantity_pack, promotion_beer, supermarket_beer, specials_beer, volume_beer, data):
    if number == 0:
        st.subheader('The cheapest option (€/l) is: ')
    elif number == 1:
        st.subheader('The second option (€/l) is: ')
    elif number == 2:
        st.subheader('The third option (€/l) is: ')
    elif number == 3:
        st.subheader('The fourth option (€/l) is: ')
    elif number == 4:
        st.subheader('The fifth option (€/l) is: ')

    if brands or quantity_pack or promotion_beer or supermarket_beer or specials_beer or volume_beer:
        product_img = data['image_url'].tolist()
        st.image(product_img[number], width=224)
        best_price_l = data['price_liter'].tolist()
        best_price = data['price'].tolist()
        best_place = data['supermarket'].tolist()
        best_link = url_web(best_place[number], number, data)
        promotion = data['promotion_check'].tolist()
        size_pack = data['quantity_pack'].tolist()
        size_unit = data['volumen_unid'].tolist()

        st.write(' with the price (€/l): `%s`' % best_price_l[number],
                 ' and the product price (€): `%s`' % best_price[number])
        st.write(' in the supermarket: `%s`' % best_place[number],
                 '  and this beer have any promotion?: `%s`' % promotion[number])
        if size_pack[number] == 1:
            st.write('sold in single units with a size of: `%s`' % size_unit[number])
        else:
            st.write('sold in packs of ', size_pack[number], ' units with a size of: `%s`' % size_unit[number])

        if number == 0:
            if st.button('Open the web site 1:'):
                webbrowser.open_new_tab(best_link)
        elif number == 1:
            if st.button('Open the web site 2:'):
                webbrowser.open_new_tab(best_link)
        elif number == 2:
            if st.button('Open the web site 3'):
                webbrowser.open_new_tab(best_link)
        elif number == 3:
            if st.button('Open the web site 4'):
                webbrowser.open_new_tab(best_link)
        elif number == 4:
            if st.button('Open the web site 5'):
                webbrowser.open_new_tab(best_link)


def app():
    data = pd.read_csv('./data/processed/data_beer_total.csv')
    data.sort_values(['price_liter', 'promotion', 'quantity_pack'], inplace=True, ignore_index=True)

    st.title('BirrasPipol House!')

    st.markdown('''Welcome beer lovers! \U0001f37a  
In this dashboard you will be able to discover the price of your favorite beer in the following supermarkets:
- Carrefour
- Alcampo
- El Corte ingles
- Dia
- Eroski ''')

    beers_brands = data['brand'].nunique()
    beers_promo = data[data['promotion'] != 'No promotion']['promotion'].count()
    beers_total = data['title'].count()

    st.markdown('''information about this dashboard:''')
    st.write(f'Number of brands: `%s`' % beers_brands)
    st.write(f'Number of beers: `%s`' % beers_total)
    st.write(f'Number of beers with promotions!: `%s`' % beers_promo)

    st.header('My favorite beer ... where is it cheaper to buy it? \U0001f914')
    st.markdown('''To do this, you can choose the following options to 
                mark which beer/s you would like to know the price:''')
    brands = st.multiselect("Brands", data['brand'].sort_values().unique())
    if brands:
        data = data[data.brand.isin(brands)]

    quantity_pack = st.multiselect("Quantity per pack", data['quantity_pack'].sort_values().unique())
    if quantity_pack:
        data = data[data.quantity_pack.isin(quantity_pack)]

    promotion_beer = st.multiselect("Promotion", data['promotion_check'].sort_values().unique())
    if promotion_beer:
        data = data[data.promotion_check.isin(promotion_beer)]

    supermarket_beer = st.multiselect("Supermarket", data['supermarket'].sort_values().unique())
    if supermarket_beer:
        data = data[data.supermarket.isin(supermarket_beer)]

    specials_beer = st.multiselect("Specials beers", data['specials'].sort_values().unique())
    if specials_beer:
        data = data[data.specials.isin(specials_beer)]

    volume_beer = st.multiselect("Size of the beer", data['volumen_unid'].sort_values().unique())
    if volume_beer:
        data = data[data.volumen_unid.isin(volume_beer)]

    for i in range(5):
        if i < data['brand'].count():
            cheap_beers(i, brands, quantity_pack, promotion_beer, supermarket_beer, specials_beer, volume_beer, data)
