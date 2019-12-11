
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        time.sleep(1)

        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)

        buttons = self.browser.find_elements_by_css_selector('button')

        notNowButton = list(filter(lambda button: button.text == 'Not Now', buttons))[0]
        notNowButton.click()

    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")
    
    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")
    
    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def likePostsWithHashtag(self, hashtag, interval, m=1000):
        self.loadHashtag(hashtag)
        posts = list(filter(lambda x: x.text == '', self.browser.find_elements_by_css_selector('a')))
        post = posts[0]
        post.click()
        time.sleep(2)
        like_xpath = '//html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button/span'
        for i in range(m):
            try:    
                like_button = self.browser.find_element_by_xpath(like_xpath)    
                like_button.click()
            except:
               pass
            time.sleep(interval)
            try:
                next_button = list(filter(lambda x: x.text == 'Next', self.browser.find_elements_by_css_selector('a')))[0]
                next_button.click()
            except:
                    continue
            time.sleep(interval)


    def loadHashtag(self, hashtag):
    	self.browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


username = input('Username: ')
password = input('Password: ')
try:
    bot = InstagramBot(username, password)
except:
    exit()
while True:
    key = input('0 -> End\n1 -> Sign In \n2 -> Like Posts With Hashtag \n')
    if key == '0':
        bot.exit()
        exit()
    elif key == '1':
    	bot.signIn()
    elif key == '2':
        hashtag = input('Hashtag: ')
        m = int(input('Maximum Posts to Like: '))
        interval = int(input('Interval: '))
        bot.likePostsWithHashtag(hashtag, interval, m)
    elif key == 'b': #for developer to run in interactive mode
        break
    else:
    	print('Not acceptable action')
