import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import configparser



class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome('./chromedriver')      
        self.base = 'https://www.instagram.com/'       
      

    def login(self):
        self.driver.get(f'{self.base}')
        time.sleep(3)                      

        self.driver.find_element_by_name('username').send_keys(self.username)        
        self.driver.find_element_by_name('password').send_keys(self.password)
        
        time.sleep(1)
        self.driver.find_element_by_name('password').send_keys(Keys.RETURN)
        # self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button/div').click()
        # self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(3)
        

    def nav_user(self):              
        self.driver.get(f'{self.base}{self.username}/')
        time.sleep(2)

        

    def findMyFollowers(self, number_of_followers):
        self.driver.find_element_by_xpath('//a[@href="/' + self.username + '/followers/"]').click()
        # self.driver.find_element_by_xpath(f"//a[@href='{self.username}'/followers/").click()        
        # self.driver.find_element_by_link_text(' follower').click()
        # self.driver.get(f'{self.base}{self.username}/followers/')        
        
        time.sleep(1)

        popup = self.driver.find_element_by_class_name('isgrP')
        
        followers_array = []

        i = 1

        while len(followers_array) <= number_of_followers:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            time.sleep(0.5)

            followers = self.driver.find_elements_by_class_name('FPmhX')

            for follower in followers:
                if follower not in followers_array:
                    followers_array.append(follower.text)

            i += 1
        print(followers_array)
        self.followers = followers_array

    def followTheirFollowers(self, number_of_follow):

        for follower in self.followers:
            self.driver.get(f'{self.base}{follower}')
            time.sleep(2)

            if(len(self.driver.find_elements_by_xpath("//*[contains(text(), 'This Account is Private')]")) > 0):
                continue
        
            self.driver.find_element_by_xpath('//a[@href="/' + follower + '/followers/"]').click()
            time.sleep(3)

            follow = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")

            i = 1

            for follower in follow:
                if i != 1:
                    self.driver.execute_script('arguments[0].click()', follower)
                if i > number_of_follow:
                    break
                
                i += 1
            time.sleep(2)



if __name__ == "__main__":      

    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    username = cparser['AUTH']['username']
    password = cparser['AUTH']['password']

    insta_bot = InstagramBot(username, password)
    insta_bot.login()    
    insta_bot.nav_user()    
    insta_bot.findMyFollowers(5)
    insta_bot.followTheirFollowers(10)
    

    
    
    
    

