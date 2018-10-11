#!/usr/bin/env

import ConfigParser
from time import sleep
from datetime import datetime, timedelta
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException 
# from selenium.webdriver.support import expected_conditions
# import pickle

class instagramNukeIt():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.default_content_setting_values.notifications" : 2}
        # chrome_options.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)


    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        sleep(2)
        a = driver.find_element_by_name('username')
        a.send_keys(self.username)
        b = driver.find_element_by_name('password')
        b.send_keys(self.password)
        c = driver.find_element_by_xpath('//button[text()="Log in"]')
        c.click()
        sleep(2)

    def unlike_photo(self, link):
        
    def untag_photo(self, link):
       


TestUser = igNukeIt("aaa", "hello");
TestUser.login()
