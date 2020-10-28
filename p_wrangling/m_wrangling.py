import pandas as pd
import re
import requests

HEADER = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/81.0.4044.141 Safari/537.36"}


# function to load DFs:
def load_df_products(name):
    return pd.read_csv(f'./data/processed/data_beer_{name}.csv')


# function to save DFs:
def save_df_products(data, name):
    data.to_csv(f'./data/processed/data_beer_{name}.csv', index=False)


# function to 'concat' the DFs of the different supermarkets:
def charge_data():
    data_beer_carrefour = load_df_products('carrefour')
    data_beer_alcampo = load_df_products('alcampo')
    data_beer_corteingles = load_df_products('corteingles')
    data_beer_dia = load_df_products('dia')
    data_beer_eroski = load_df_products('eroski')

    data_beer_total = pd.concat([data_beer_carrefour,
                                 data_beer_alcampo,
                                 data_beer_corteingles,
                                 data_beer_dia,
                                 data_beer_eroski], axis=0, ignore_index=True)
    return data_beer_total


# function to found the correct brand of the beer:
def change_brand(brand_raw):
    names_brands = '''ramblers|amstel|afrutado mahou|mahou|dia|heineken|san miguel|estrella galicia|voll-damm|
    |cruzcampo|buckler|dia shandy|desperado|grimbergen|franziskaner|paulaner|corona|guinness|el aguila|1906|
    |ambar|ámbar|alhambra|coronita|leffe|kronenbourg|carlsberg|la salve|warsteiner|mexicana|pacífico|guiness|
    |founders|spatem|beck|cubanisto|aurum|keler|woll-damm|aurum|ambar|free damm|ladrón de manzanas|
    |brewdog|ipa lagunitas|inedit|daura|oro|estrella damm|damm|complot|corgon gard|judas|olañeta|budweiser|
    |grevensteiner|inedit|chimay|house 13|lorea ipa boga|trappe|mort subite|kirin|urquell|cruz campo|
    |malquerida|moretti|clausthaler|affligem|stella artoi|sol|quilmes|daura marzen|turia|boga|
    |schöfferhofer|grolsch|la goudale|atkien dunkel|chérie|belzebuth|la virgen|lowenbrau|bulmers|jai alai|
    |strongbow|cruz del sur|voll damm|estrella levante|xibeca|victoria|estrella del sur|aliada|moritz|
    |brabante|superbock|kirin ichiban|staropramen|waterloo|weltenburger|schwaben|dab|praga|abbot|
    |lowenbräu|spaten|hofbräu|dos equis|birra moretti|karmeliet|kwak|gordon|martin's|delirium tremens|veltins|
    |pacifico|triple secret des moine|la bière du demon|baltika|molino viejo|cusqueña|cobra|zywiec|barista|
    |bischofshof|hoegaarden|schofferhofer|erdinger|konig ludwig|rosita|burro de sancho|gastro|
    |monkey|arriaca|ladron de manzanas|kopparberg|la sagra|sierra nevada|montseny|maisel & friends|
    |tyris|rabiosa|jaira|forastera|cibeles|mulhacen|gredos|ballut|madri chulapo|gastheiz|quijota|
    |marijuana|moli balear|dolina|icue|bizantina|bavaria|newcastle|timmermans|modelo|heifer|holbrand|
    |rubai|el águila|estrella de galicia|chouffe|peroni|miller|goya|super bock|sam miguel|karamalz|
    |skol|budejovicky|wersteiner|duvel|schneider weisse|john smith's|blue moon|rochefort-8|salitos|
    |old empire|köning ludwing weissbier|könig ludwig weissbier|blanche de charleroi|ruddles|aventinus|
    |madrí chulapo|abbaye d'aulne|g de goudale|cuzqueña|london pride|wychwood hobgoblin|sureña|
    |innis&gunn|intense gold|faxe|bitburger|lindemans|maisel&friends|pearl jet|the one|original intense|
    |licher|tennent's|tedeum|enigma|mulhacén|gervensteiner|abbaye du lys|greventeiner|liefmans|rubia 4|
    |san sebastian|maisel|carrefour|koenigsbier|polar|coors|kadabra|brooklyn|alsfelder|madriz|presidente|
    |fentiman's de jengibre|lammsbräu|riedenburger|benediktinerabtei|iron maiden|old speckled hen|
    |ordio minero|rubia dab|corte ingles|thatchers gold|maredsous|blue monn|vedett|shandy|greene king'''

    brand = re.findall(names_brands, brand_raw.lower())
    if len(brand) > 1:
        for name in brand:
            if len(name) > 3:
                return name
    else:
        if brand:
            return brand[0]
        else:
            return 'new model in the list'


# function to get the different types of the brand Mahou:
def mahou_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'mahou sin gluten'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'mahou radler sin alcohol (0,0%)'
        else:
            return 'mahou radler'

    clasica = re.findall('[clasiá]{7,}|afrutado mahou', title)
    if len(clasica) != 0:
        return 'mahou clasica'

    mixta = re.findall('mixta|shandy', title)
    if len(mixta) != 0:
        return 'mahou mixta'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'mahou sin alcohol (0,0%)'

    ipa = re.findall('ipa', title)
    if len(ipa) != 0:
        return 'mahou ipa'

    maestra = re.findall('maestra', title)
    if len(maestra) != 0:
        return 'mahou maestra'

    barrica = re.findall('barrica', title)
    if len(barrica) != 0:
        return 'mahou barrica'

    casimiro = re.findall('casimiro', title)
    if len(casimiro) != 0:
        return 'mahou casimiro'

    roja = re.findall('mahou', title)
    if len(roja) != 0:
        return 'mahou 5 estrellas'


# function to get the different types of the brand San Miguel:
def san_miguel_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'san miguel sin gluten'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'san miguel radler sin alcohol (0,0%)'
        else:
            return 'san miguel radler'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'san miguel sin alcohol (0,0%)'

    ipa = re.findall('ipa', title)
    if len(ipa) != 0:
        return 'san miguel ipa'

    magna = re.findall('magna', title)
    if len(magna) != 0:
        return 'san miguel magna'

    selecta = re.findall('selecta', title)
    if len(selecta) != 0:
        return 'san miguel selecta'

    manila = re.findall('manila', title)
    if len(manila) != 0:
        return 'san miguel manila'

    eco = re.findall('ecológica', title)
    if len(eco) != 0:
        return 'san miguel ecologica'

    premium = re.findall('1516', title)
    if len(premium) != 0:
        return 'san miguel 1516'

    fresca = re.findall('fresca', title)
    if len(fresca) != 0:
        return 'san miguel fresca'

    return 'san miguel'


# function to get the different types of the brand Amstel:
def amstel_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'amstel sin gluten'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'amstel radler sin alcohol (0,0%)'
        else:
            return 'amstel radler'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'amstel sin alcohol (0,0%)'

    oro = re.findall('oro', title)
    if len(oro) != 0:
        return 'amstel oro'

    extra = re.findall('extra', title)
    if len(extra) != 0:
        return 'amstel extra'

    clasica = re.findall('[clasiá]{7,}', title)
    if len(clasica) != 0:
        return 'amstel clasica'

    return 'amstel original'


# function to get the different types of the brand Cruzcampo:
def cruzacampo_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'cruzcampo sin gluten'

    shandy = re.findall('shandy', title)
    if len(shandy) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'cruzcampo shandy sin alcohol (0,0%)'
        else:
            return 'cruzcampo shandy'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'cruzcampo sin alcohol (0,0%)'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        return 'cruzcampo radler'

    ipa = re.findall('ipa|andalusian', title)
    if len(ipa) != 0:
        return 'cruzcampo ipa'

    reserva = re.findall('gran reserva', title)
    if len(reserva) != 0:
        return 'cruzcampo reserva'

    especial = re.findall('especial', title)
    if len(especial) != 0:
        return 'cruzcampo especial'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        return 'cruzcampo radler'

    cruzial = re.findall('cruzial', title)
    if len(cruzial) != 0:
        return 'cruzcampo cruzial'

    return 'cruzcampo'


# function to get the different types of the brand Ambar:
def ambar_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'ambar sin gluten'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'ambar radler sin alcohol (0,0%)'
        else:
            return 'ambar radler'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'ambar sin alcohol (0,0%)'

    export = re.findall('export', title)
    if len(export) != 0:
        return 'ambar export'

    ipa = re.findall('ipa|indian', title)
    if len(ipa) != 0:
        return 'ambar ipa'

    number = re.findall('1900', title)
    if len(number) != 0:
        return 'ambar 1900'

    ambiciosa = re.findall('ambiciosa', title)
    if len(ambiciosa) != 0:
        return 'ambar ambiciosa'

    pedigree = re.findall('pedigree', title)
    if len(pedigree) != 0:
        return 'marston’s pedigree'

    return 'ambar'


# function to get the different types of the brand Alhambra:
def alhambra_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'alhambra sin gluten'

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'alhambra radler sin alcohol (0,0%)'
        else:
            return 'alhambra radler'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'alhambra sin alcohol (0,0%)'

    number = re.findall('1925', title)
    if len(number) != 0:
        return 'alhambra 1925'

    ipa = re.findall('ipa', title)
    if len(ipa) != 0:
        return 'alhambra ipa'

    roja = re.findall('roja', title)
    if len(roja) != 0:
        return 'alhambra roja'

    granadino = re.findall('granadino', title)
    if len(granadino) != 0:
        return 'alhambra gran granadino'

    baltic = re.findall('baltic', title)
    if len(baltic) != 0:
        return 'alhambra baltic porter'

    envejecida = re.findall('envejecida', title)
    if len(envejecida) != 0:
        return 'alhambra envejecida'

    especial = re.findall('especial', title)
    if len(especial) != 0:
        return 'alhambra especial'

    return 'alhambra'


# function to get the different types of the brand Heineken:
def heineken_types(title):
    title = title.lower()

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'heineken sin alcohol (0,0%)'

    return 'heineken'


# function to get the different types of the brand Estrella Galicia:
def estrella_galicia_types(title):
    title = title.lower()

    sin_gluten = re.findall('sin gluten', title)
    if len(sin_gluten) != 0:
        return 'estrella galicia sin gluten'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'estrella galicia sin alcohol (0,0%)'

    return 'estrella galicia'


# function to get the different types of the brand Estrella galicia 1906:
def estrella_1906_types(title):
    title = title.lower()

    red = re.findall('red', title)
    if len(red) != 0:
        return 'estrella galicia 1906 red'

    return 'estrella galicia 1906'


# function to get the different types of the brand Carrefour:
def carrefour_types(title):
    title = title.lower()

    radler = re.findall('radler', title)
    if len(radler) != 0:
        sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
        if len(sin_alcohol) != 0:
            return 'carrefour radler sin alcohol (0,0%)'
        else:
            return 'carrefour radler'

    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', title)
    if len(sin_alcohol) != 0:
        return 'carrefour sin alcohol (0,0%)'

    shandy = re.findall('shandy', title)
    if len(shandy) != 0:
        return 'carrefour shandy'

    pils = re.findall('pils', title)
    if len(pils) != 0:
        return 'carrefour pils'

    abadia = re.findall('abad', title)
    if len(abadia) != 0:
        return 'carrefour abadia'

    negra = re.findall('negra', title)
    if len(negra) != 0:
        return 'carrefour negra'

    especial = re.findall('especial', title)
    if len(especial) != 0:
        return 'carrefour especial'

    extra = re.findall('extra', title)
    if len(extra) != 0:
        return 'carrefour extra'

    return 'carrefour'


# function to change the duplicate brands and apply the types of the important brands:
def duplicate_brand(info):
    data = info[0]
    title = info[1]

    if data == 'guiness':
        return 'guinness'
    elif data == 'voll damm':
        return 'voll-damm'
    elif data == 'schofferhofer':
        return 'schöfferhofer'
    elif data == 'ladron de manzanas':
        return 'ladrón de manzanas'
    elif data == 'el aguila':
        return 'el águila'
    elif data == 'superbock':
        return 'super bock'
    elif data == 'madri chulapo':
        return 'madrí chulapo'
    elif data == 'blue monn':
        return 'blue moon'
    elif data == ('maisel' or 'maisel&friends'):
        return 'maisel & friends'
    elif data == 'köning ludwing weissbier':
        return 'könig ludwig weissbier'
    # we divide the big brands by their types
    elif (data == 'sam miguel') or (data == 'san miguel'):
        return san_miguel_types(title)
    elif (data == 'cruz campo') or (data == 'cruzcampo') or (data == 'shandy'):
        return cruzacampo_types(title)
    elif (data == 'estrella de galicia') or (data == 'estrella galicia'):
        return estrella_galicia_types(title)
    elif (data == 'ambar') or (data == 'ámbar'):
        return ambar_types(title)
    elif data == '1906':
        return estrella_1906_types(title)
    elif (data == 'mahou') or (data == 'afrutado mahou'):
        return mahou_types(title)
    elif data == 'amstel':
        return amstel_types(title)
    elif data == 'alhambra':
        return alhambra_types(title)
    elif data == 'heineken':
        return heineken_types(title)
    elif data == 'carrefour':
        return carrefour_types(title)
    else:
        return data


# function to classify special type of beer: Artesana
def artesana_func(text):
    artesana = re.findall('artesana', text.lower())
    if len(artesana) != 0:
        return 'artesana'


# function to classify special type of beer: IPA
def ipa_func(text):
    ipa_beer = re.findall('ipa', text.lower())
    if len(ipa_beer) != 0:
        return 'IPA'


# function to classify special type of beer: Black
def oscura_func(text):
    oscura = re.findall('oscura|negra|porter', text.lower())
    if len(oscura) != 0:
        return 'negra'


# function to classify special type of beer: Sin Alcohol
def sin_alcohol_func(text):
    sin_alcohol = re.findall('[0.,]{3}|sin alcohol', text.lower())
    if len(sin_alcohol) != 0:
        return 'sin alcohol'


# function to classify special type of beer: Radler
def radler_func(text):
    radler = re.findall('radler', text.lower())
    if len(radler) != 0:
        return 'radler'


# function to classify special type of beer: Sin gluten
def sin_gluten_func(text):
    sin_gluten = re.findall('sin gluten', text.lower())
    if len(sin_gluten) != 0:
        return 'sin gluten'


# function to classify special type of beer: Eco
def eco_func(text):
    eco = re.findall('ecológica|ecologica|eco', text.lower())
    if len(eco) != 0:
        return 'ecologica'


# function to apply the special beers in the DF:
def beer_specials(text):
    add = ''
    ipa = ipa_func(text)
    if ipa:
        add += ipa + ' '

    osc = oscura_func(text)
    if osc:
        add += osc + ' '

    rad = radler_func(text)
    if rad:
        add += rad + ' '

    sia = sin_alcohol_func(text)
    if sia:
        add += sia + ' '

    sig = sin_gluten_func(text)
    if sig:
        add += sig + ' '

    art = artesana_func(text)
    if art:
        add += art + ' '

    eco = eco_func(text)
    if eco:
        add += eco + ' '

    if len(add) > 1:
        return add
    else:
        return 'others'


# function to apply if the beer has or not promotion, in the DF:
def promotion_list(text):
    if text != 'No promotion':
        return 'yes'
    else:
        return 'no'


# function to download the beer images of the supermarkets (we use in the test model of ML):
def download_image(url):
    im_file = requests.get(url[1], headers=HEADER)
    open(f'./beer_images/supermarkets/{url[0]}.jpg', 'wb').write(im_file.content)


# function to make nice the volumen of the beers:
def change_volume(text):
    text = text.lower()
    text = text.rstrip()
    text = text.lstrip()
    number_cl = re.findall('[a-z]+', text)
    if len(number_cl) == 0:
        take_number = re.findall('[0-9]+', text)
        return take_number[0] + ' cl'
    if text == '33cl':
        return '33 cl'
    elif text == '50cl':
        return '50 cl'
    number_c = re.findall('l', text)
    if len(number_c) == 0:
        return text + 'l'

    return text


# main function, call all other functions:
def wrangle(scrape, download):
    if scrape == 'Y':
        print('Start filtering our beers ...')
        data_beer_total = charge_data()
        data_beer_total['promotion_check'] = data_beer_total['promotion'].apply(promotion_list)
        data_beer_total['id'] = data_beer_total.index
        if download == 'Y':
            print('Starting to download the beers images of the supermarkets...')
            data_beer_total[['id', 'image_url']].apply(download_image, axis=1)
            print('Finished to download the beer images!')
        data_beer_total['brand'] = data_beer_total['title'].apply(change_brand)
        data_beer_total['brand'] = data_beer_total[['brand', 'title']].apply(duplicate_brand, axis=1)
        data_beer_total['specials'] = data_beer_total['title'].apply(beer_specials)
        data_beer_total['volumen_unid'] = data_beer_total['volumen_unid'].apply(change_volume)
        save_df_products(data_beer_total, 'total')
        print('Beers ready to buy!')
        return data_beer_total
    else:
        data_beer_total = load_df_products('total')
        return data_beer_total
