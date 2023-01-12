from responses import target
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class InstagramBot:
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        sleep(3)
        self.login()
        self.driver.implicitly_wait(5)
        sleep(1)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        sleep(1)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/div[1]/div/form/div[1]/div[3]/button').click()

    def navigate_user(self, user):
        sleep(2)
        self.driver.get("https://www.instagram.com/" + str(user) + "/")

    def obtain_follower_list(self, user):
        sleep(1)
        self.navigate_user(user)
        sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        js_scroll = '''
        let followers = document.querySelector(".isgrP")
        followers.scrollTo(0, followers.scrollHeight)
        let lenOfPage = followers.scrollHeight
        return lenOfPage
        '''
        """#Find the followers page
dialog = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
#find number of followers
allfoll=int(driver.find_element_by_xpath("//li[2]/a/span").text) 
#scroll down the page
for i in range(int(allfoll/2)):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
    time.sleep(random.randint(500,1000)/1000)
    print("Extract friends %",round((i/(allfoll/2)*100),2),"from","%100")"""

        sleep(2)
        len_page = self.driver.execute_script(js_scroll)
        match = False
        while match == False:
            last_count = len_page
            sleep(2)
            len_page = self.driver.execute_script(js_scroll)
            if last_count == len_page: match = True
            # self.driver.find_element_by_tag_name('html').send_keys(Keys.END)

        sleep(1)
        followers = self.driver.find_elements_by_css_selector('.FPmhX.notranslate._0imsa ')
        follower_list = []
        for follower in followers: follower_list.append(follower.text)
        print(follower_list)
        print(len(follower_list))

        return follower_list

    def obtain_following_list(self, user):
        sleep(1)
        self.navigate_user(user)
        sleep(1)
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        js_scroll = '''
                let followers = document.querySelector(".isgrP")
                followers.scrollTo(0, followers.scrollHeight)
                let lenOfPage = followers.scrollHeight
                return lenOfPage
                '''
        sleep(2)
        len_page = self.driver.execute_script(js_scroll)
        match = False
        while match == False:
            last_count = len_page
            sleep(2)
            len_page = self.driver.execute_script(js_scroll)
            if last_count == len_page: match = True

        sleep(1)
        followings = self.driver.find_elements_by_css_selector('.FPmhX.notranslate._0imsa ')
        following_list = []
        for following in followings: following_list.append(following.text)
        print(following_list)
        print(len(following_list))

        """#Find the followers page
dialog = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
#find number of followers
allfoll=int(driver.find_element_by_xpath("//li[2]/a/span").text) 
#scroll down the page
for i in range(int(allfoll/2)):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
    time.sleep(random.randint(500,1000)/1000)
    print("Extract friends %",round((i/(allfoll/2)*100),2),"from","%100")"""
        return following_list

    def start_follow_followers(self, user):
        self.obtain_follower_list(user)
        for target in self.obtain_follower_list(user):
            self.navigate_user(target)
            self.driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div/div/span/span[1]/button") \
                .click()

    def who_do_not_following_back(self, user):
        return list(set(self.obtain_following_list(user)) - set(self.obtain_follower_list(user)))
    def saver_for_all(self, user):
        with open(f"{user}.txt", 'w') as file:
            file.write("followers : " + '\n')
            for row in self.obtain_follower_list(user): file.write(str(row)+'\n')
            file.write("following :" + '\n')
            for row1 in self.obtain_following_list(user):file.write(str(row1)+'\n')










if __name__ == '__main__':
    ig_bot = InstagramBot('username', 'py.bot.exe12345')
    ig_bot.obtain_following_list("target_user")
