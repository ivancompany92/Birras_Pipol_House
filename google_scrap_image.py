import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import urllib.request
import time


# function to download image from google, with this image we can get more beer images for to have a better model
def main():
    print("What do you want to download?")
    download = input()
    site = 'https://www.google.com/search?tbm=isch&q='+download
    # Creating folder directory (if not exists) with input value
    folder_name = download.replace(' ', '_').lower()
    path = ('./beer_images/google_download/'+folder_name+'/')
    if not os.path.exists(path):
        os.mkdir(path)
    # Get path of your Firefox/Chrome drivers and make a connection with it
    os.environ['PATH'] = f'{os.environ["PATH"]}:{os.getcwd()}'
    driver_options = Options()
    driver_options.headless = True
    driver = webdriver.Firefox(options=driver_options)

    # passing site url
    driver.get(site)
    elm = driver.find_element_by_tag_name('html')
    i = 0
    while i < 10:
        # for scrolling page to the bottom
        # driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        elm = driver.find_element_by_tag_name('html')
        elm.send_keys(Keys.END)
        try:
            # for clicking show more results button
            driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
        except Exception as e:
            pass
        time.sleep(1)
        i += 1
    # Identifies the elements to store in a list the url of the images
    element_1 = driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[4]')
    images_google=[]
    for i in element_1.find_elements_by_css_selector('div.bRMDJf.islir'):
        if i.find_element_by_css_selector('img.rg_i.Q4LuWd').get_attribute('src') != None:
            images_google.append(i.find_element_by_css_selector('img.rg_i.Q4LuWd').get_attribute('src'))
        elif i.find_element_by_css_selector('img.rg_i.Q4LuWd').get_attribute('data-src') != None:
            images_google.append(i.find_element_by_css_selector('img.rg_i.Q4LuWd').get_attribute('data-src'))
        else:
            pass
    # close connection
    driver.close()
    # Extract images to local disk
    count = 1
    for i in images_google:
        urllib.request.urlretrieve(i, path+str('{:d}'.format(count))+".jpg")
    #     urllib.request.urlretrieve(i, path+str('{:d}'.format(count).zfill(6))+".jpg")
        count += 1
        print('Images downloaded = '+str(count), end='\r')


if __name__ == '__main__':
    main()