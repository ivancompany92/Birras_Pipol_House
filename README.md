# BirrasPipol House!

![Image](https://ep00.epimg.net/elpais/imagenes/2016/08/04/tentaciones/1470312023_876749_1470312647_noticia_normal.jpg)

#### Ivan Company    [linkedin](https://www.linkedin.com/in/ivan-company-hernando/)

#### Data Analytics Bootcamp - Final project


## **Overview**
Welcome beer lovers!

This project is the house where any beer lover can find the cheapest price for their favorite beer.
For this I have carried out the scraping of 5 supermarket websites:

    - Carrefour
    - Alcampo
    - El Corte Inglés
    - Dia
    - Eroski
Obtaining from each of them the most important data of their current beer catalogs:
 
    - price and price per liter of each beer 🤑
    - brand
    - container size
    - units in which the pack (or individual) comes
    - beer picture
    - and if the beer has any active promotions!  😍


## **How can you view all this information?**

To better view all this information, you will only have to execute the following file with "Streamlit":

`streamlit run BirrasPipolHouse.py`

You will be able to search for your favorite beer (PAGE 1) or if you don't know which beer you have in front of you (PAGE 2), you can put the ML model to the test to know the brand !!

![]( https://raw.github.com/ivancompany92/Birras_Pipol_House/master/beer_images/readme_image/navigation.png)

## In the seccion: "Where is my beer?" 

you will choose different options to find your favorite beer with the cheapest price!

![](https://raw.github.com/ivancompany92/Birras_Pipol_House/master/beer_images/readme_image/options_to_search.png)

and you will see the 5 cheapest options (depending on the filters you put):

![](https://raw.github.com/ivancompany92/Birras_Pipol_House/master/beer_images/readme_image/result.png)



## In th seccion: "What beer is this?" 

you can upload a photo from the local repository or paste the url link to know the beer brand (*Currently the model is only trained for 5 brands): 

Mahou 5 estrellas, Mahou clasica, Estrella Galicia, Heineken, San Miguel

![](https://raw.github.com/ivancompany92/Birras_Pipol_House/master/beer_images/readme_image/model_predict.png)


## **Data**

* [.csv Dataset](https://github.com/ivancompany92/Birras_Pipol_House/blob/master/data/processed/data_beer_total.csv) 

The dataset is obtained from scraping the websites of the different supermarkets. In order to update it, you can run the command:

`python main_script.py -s Y`



## **Model**

The machine learning model is trained with 5 brands of beer. We use the pre-trained model "InceptionV3" entering from its pre-trained layer "mixed7".

If you want to train the model, you can do it with the photos already uploaded to the repository by executing the following command:

`python main_script.py -m Y`

*If you need to download more photos to train the model from google, you can use the following command:

`python google_scrap_image.py`

## **Requirements**
You need to have Python installed with the following libraries:
- Python

- Pandas

- Numpy

- Matplotlib

- Seaborn

- Requests

- Beautifulsoup4

- Selenium

- Tensorflow

- Streamlit  


You have more information in the file: requirements.txt


### **Folder structure**
```
└── project
    ├── .gitignore
    ├── requeriments.txt
    ├── README.md
    ├── main_cript.py
    ├── BirrasPipolHouse.py
    ├── google_scrap_image.py
    ├── apps
    │   ├── BPH1.py
    │   └── BPH2.py
    ├── beer_images
    │   ├── beers_train
    │   ├── beers_validation
    │   ├── google_download
    │   ├── readme_image
    │   └── supermarkets
    ├── data
    │   └── processed
    │       ├── data_beer_alcampo.csv
    │       ├── data_beer_carrefour.csv
    │       ├── data_beer_corteingles.csv
    │       ├──data_beer_dia.csv
    │       ├──data_beer_eroski.csv
    │       └── data_beer_total.csv
    ├── p_acquisition
    │   ├── __init__.py
    │   └── m_acquisition.py
    ├── p_analysis
    │   ├── __init__.py
    │   └── m_analysis.py
    ├── p_wrangling
    │   ├── __init__.py
    │   └── m_wrangling.py
    ├── saved_model
    │   ├── model_3_inceptionv3_280x280_full.json
    │   └── model_3_inceptionv3_280x280_full_weights.h5
    └── upload_image

    
```


## **Next steps:**
- Add more supermarkets, such as Mercadona, in order to have more prices for your favorite beers
- Improve the prediction model for brands with more beers, such as Alhambra, Guinness ...


## **Contact info**
- If you have any questions about the repository or any suggestion to improve it, you can write to me on [Linkedin](https://www.linkedin.com/in/ivan-company-hernando/)