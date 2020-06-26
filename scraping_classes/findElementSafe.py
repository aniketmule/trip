from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path


class HelperMethods:
    #driver = webdriver.PhantomJS('C:\\Users\\Aniket\\PycharmProjects\\webscraping\\scraping\\scraping\\drivers\\phantomjs.exe')
    project_path =  str(Path().absolute())

    chromedriver_path =  project_path+'\drivers\chromedriver.exe'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=chromedriver_path)
#    driver = webdriver.Chrome(chromedriver_path,chrome_options=options)

    def find_element_safe(self,String):
        try:
            self.driver.find_element_by_xpath(String)
        except NoSuchElementException:
            return False

