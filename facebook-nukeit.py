#!/usr/bin/env

import configparser
from time import sleep
from datetime import datetime, timedelta
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pdb
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException 
# from selenium.webdriver.support import expected_conditions
import pickle
import pandas as pd

class FacebookNukeIt():

    def __init__(self, username, password):
        if username == None:
            print("no username provided in config")
            return False
        if password == None:
            print("no password provided in config")
            return False

        self.username = username
        self.password = password
        self.fb_activity_url = "https://mbasic.facebook.com/" + username +  "/allactivity"
        print(self.fb_activity_url)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)

    def run(self, start_date, end_date):

        date_range_list = pd.date_range(start_date, end_date, freq="M").tolist()
        years_list = pd.date_range(start_date, end_date, freq="Y").tolist()

        self.date_range_list = [_.strftime("%B %Y") for _ in date_range_list]
        self.years_list = [ _.strftime("%Y") for _ in years_list]

        print(self.date_range_list)
        print(self.years_list)

        self.driver.get('https://mbasic.facebook.com/')
        print("Opened facebook...")
        a = self.driver.find_element_by_id('m_login_email')
        a.send_keys(self.username)
        print("Email Id entered...")
        b = self.driver.find_element_by_name('pass')
        b.send_keys(self.password)
        print("Password entered...")
        c = self.driver.find_element_by_name('login')
        c.click()

        # try:
        #     self.driver.find_elements_by_xpath("//*[contains(text(), 'Activity Log')]")
        # except:
        #     print("Did not find the \"Acivity Log\". Perhaps Facebook thinks we are a robot.")
        #     input("Press Enter to continue...")
        #     pass

        self.driver.get(self.fb_activity_url)
        print(self.fb_activity_url)


        # pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
        # cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in cookies:
        #     self.driver.add_cookie(cookie)

        self.load_more_activity()

        return True

    def load_more_activity(self):

        self.delete_activity()
        self.unlike_activity()
        self.remove_reaction()
        self.hide_from_timeline_activity()

        # pdb.set_trace()

        try:
            load_more = self.driver.find_element_by_partial_link_text('Load more from').click()
            print("Successfully loaded more activity for this month.")

        except NoSuchElementException as exception:
            print("Failed to load more activity for this month.")
            self.load_month_activity()


        self.load_more_activity()
        return False

    def load_year_activity(self):

        year_text = self.years_list[-1]
        try:
            more_activity = self.driver.find_element_by_partial_link_text(year_text).click()
            del self.years_list[-1]
            self.load_month_activity()
            print("Success : Found another year ", year_text)
        except NoSuchElementException as exception:
            print("Failed : Could not find another year ", year_text)
            return
        
        # self.load_more_activity()
        return True

    def load_month_activity(self):
        date_text = self.date_range_list[-1]
        try:
            more_activity = self.driver.find_element_by_partial_link_text(date_text).click()
            del self.date_range_list[-1]
            print("Success : Found another month ", date_text)

            self.load_more_activity()

        except NoSuchElementException as exception:
            print("Failed : Could not find another month ", date_text) 

        
        self.load_year_activity()
        return False

    def remove_reaction(self):
        try:
            delete_link = self.driver.find_element_by_partial_link_text('Remove Reaction').click()
            print("Successfully removed a reaction.")
            self.driver.execute_script("window.history.go(-1)")
        except NoSuchElementException as exception:
            try:
                delete_link = self.driver.find_element_by_partial_link_text('remove reaction').click()
                print("Successfully removed a reaction.")
                self.driver.execute_script("window.history.go(-1)")
            except:
                print("Failed to find any reactions to reactions. Moving on...")
                return False
        self.remove_reaction()

    def delete_activity(self):
        try:
            delete_link = self.driver.find_element_by_partial_link_text('Delete').click()
            print("Successfully deleted an activity.")
            self.driver.execute_script("window.history.go(-1)")
        except NoSuchElementException as exception:
            try:
                delete_link = self.driver.find_element_by_partial_link_text('delete').click()
                print("Successfully deleted an activity.")
                self.driver.execute_script("window.history.go(-1)")
            except:
                print("Failed to find any acivity to delete. Moving on...")
                return False
        self.delete_activity()

    def hide_from_timeline_activity(self):
        try:
            delete_link = self.driver.find_element_by_partial_link_text('Hide from Timeline').click()
            print("Successfully deleted an activity.")
            self.driver.execute_script("window.history.go(-1)")
        except NoSuchElementException as exception:
            try:
                delete_link = self.driver.find_element_by_partial_link_text('hide from timeline').click()
                print("Successfully deleted an activity.")
                self.driver.execute_script("window.history.go(-1)")
            except:
                print("Failed to find any acivity to delete. Moving on...")
                return False
        self.hide_from_timeline_activity()

    def unlike_activity(self):
        try:
            unlike_link = self.driver.find_element_by_partial_link_text('Unlike').click()
            print("Successfully unliked an activity.")
            self.driver.execute_script("window.history.go(-1)")
        except NoSuchElementException as exception:
            try:
                delete_link = self.driver.find_element_by_partial_link_text('unlike').click()
                print("Successfully unliked an activity.")
                self.driver.execute_script("window.history.go(-1)")
            except:
                print("Failed to find any acivity to unlike. Moving on...")
                return False
        self.unlike_activity()


def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    fb_username = config.get('facebook', 'username')
    fb_password = config.get('facebook', 'password')
    start_date = config.get('facebook', 'start_date')
    end_date = config.get('facebook', 'end_date')

    fbni = FacebookNukeIt(fb_username, fb_password)
    fbni.run(start_date, end_date)


if __name__ == '__main__':
    main()
