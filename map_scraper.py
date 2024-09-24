# -*- coding: utf-8 -*-
import logging
import time
import traceback
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 10
MAX_RETRY = 5
MAX_SCROLLS = 40


class GoogleMapsScraper:
    def __init__(self, debug=False):
        self.debug = debug
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()


    def __enter__(self):
        return self


    def exit(self):
        self.driver.close()
        self.driver.quit()
    

    def sort_by(self, url, ind='Newest'):
        self.driver.get(url)
        # self.__click_on_cookie_agreement()

        wait = WebDriverWait(self.driver, MAX_WAIT)

        # open dropdown menu
        clicked = False
        tries = 0
        while not clicked and tries < MAX_RETRY:
            try:
                menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-value=\'Sort\']')))
                menu_bt.click()

                clicked = True
                time.sleep(1)
            except Exception as e:
                tries += 1
                self.logger.warn('Failed to click sorting button')

            # failed to open the dropdown
            if tries == MAX_RETRY:
                return -1


        #  element of the list specified according to ind
        recent_rating_bts = self.driver.find_elements(By.XPATH, '//div[@role=\'menuitemradio\']')
        recent_rating_bt = None
        for r in recent_rating_bts:
            if r.accessible_name.lower() == ind.lower():
                recent_rating_bt = r
        if not recent_rating_bt:
            self.logger.warn(f'Failed to click {ind} button')
            return -1
        recent_rating_bt.click()

        # wait to load review (ajax call)
        time.sleep(3)

        return 0


    def get_reviews(self, offset):
        # scroll to load reviews
        self.__scroll()

        # wait for other reviews to load (ajax)
        time.sleep(4)

        # expand review text
        self.__expand_reviews()
        
        time.sleep(2)
        
        # return review translation
        self.__untranslate()
        
        time.sleep(2)

        review_blocks = self.driver.find_elements(By.XPATH, '//div[@class=\'jftiEf fontBodyMedium \']')
        if not review_blocks:
            review_blocks = self.driver.find_elements(By.XPATH, '//div[@class=\'m6QErb XiKgde \']')[-1]
            time.sleep(1)
            review_blocks = review_blocks.find_elements(By.TAG_NAME, 'div')
        
        parsed_reviews = []
        for index, review_blocks in enumerate(review_blocks):
            if index >= offset:
                r = self.__parse(review_blocks)
                parsed_reviews.append(r['text'])

                # logging to std out
                # print(r)

        return parsed_reviews


    def get_review_page_url(self, search_name):
        self.driver.get("https://www.google.com/maps/")
        # self.__click_on_cookie_agreement()

        wait = WebDriverWait(self.driver, MAX_WAIT)

        search_box = self.driver.find_elements(By.XPATH, '//input[@class=\'fontBodyMedium searchboxinput xiQnY \']')
        for s in search_box:
            s.clear()
            s.send_keys(search_name)

        time.sleep(1)
        suggestions = self.driver.find_elements(By.XPATH, '//div[@jsaction=\'suggestion.select\']')
        is_find = False
        for suggestion in suggestions:
            # jslog 6986
            s = suggestion.find_elements(By.TAG_NAME, 'div')[0]
            
            if "6986" in s.get_attribute("jslog"):
                is_find = True
                s.click()
                break
        
        if is_find:
            time.sleep(3)
            
            review_button = self.driver.find_elements(By.XPATH, '//button[@class=\'hh2c6 \' and @data-tab-index=\'1\']')
            review_button[0].click()
            
            time.sleep(1)
            
            current_url = self.driver.current_url
            
            print("success to get review url")
            return current_url
        else:
            return 0
    
    
    def __parse(self, review):
        item = {}

        try:
            # TODO: Subject to changes
            review_id = review['data-review-id']
        except Exception as e:
            review_id = None

        try:
            # TODO: Subject to changes
            username = review['aria-label']
        except Exception as e:
            username = None

        try:
            # TODO: Subject to changes
            review_text = self.__filter_string(review.find_elements(By.CLASS_NAME, 'wiI7pd')[0].text)
        except Exception as e:
            review_text = None 

        try:
            # TODO: Subject to changes
            rating = float(review.find('span', class_='kvMYJc')['aria-label'].split(' ')[0])
        except Exception as e:
            rating = None

        try:
            # TODO: Subject to changes
            relative_date = review.find('span', class_='rsqaWe').text
        except Exception as e:
            relative_date = None

        try:
            n_reviews = review.find('div', class_='RfnDt').text.split(' ')[3].replace(',')
        except Exception as e:
            n_reviews = 0

        try:
            user_url = review.find('button', class_='WEBjve')['data-href']
        except Exception as e:
            user_url = None

        item['review_id'] = review_id
        item['text'] = review_text

        # depends on language, which depends on geolocation defined by Google Maps
        # custom mapping to transform into date should be implemented
        item['relative_date'] = relative_date

        # store datetime of scraping and apply further processing to calculate
        # correct date as retrieval_date - time(relative_date)
        item['retrieval_date'] = datetime.now()
        item['rating'] = rating
        item['username'] = username
        item['n_review_user'] = n_reviews
        #item['n_photo_user'] = n_photos  ## not available anymore
        item['url_user'] = user_url

        return item
    
    
    # return review translation
    def __untranslate(self):
        # use XPath to load complete reviews
        # TODO: Subject to changes
        translate_buttons = self.driver.find_elements(By.XPATH, '//button[@role=\'switch\']')
        for button in translate_buttons:
            if 'original' in button.accessible_name.lower():
                self.driver.execute_script("arguments[0].click();", button)


    # expand review description
    def __expand_reviews(self):
        # use XPath to load complete reviews
        # TODO: Subject to changes
        expand_buttons = self.driver.find_elements(By.CSS_SELECTOR,'button.w8nwRe.kyuRq')
        for button in expand_buttons:
            self.driver.execute_script("arguments[0].click();", button)


    def __scroll(self):
        # TODO: Subject to changes m6QErb DxyBCb kA9KIf dS8AEf 
        scrollable_div = self.driver.find_element(By.XPATH,'//div[@jslog=\'26354;mutable:true;\']')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def __get_logger(self):
        # create logger
        logger = logging.getLogger('googlemaps-scraper')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        fh = logging.FileHandler('gm-scraper.log')
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)

        return logger


    def __get_driver(self, debug=False):
        options = Options()

        if not self.debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        #options.add_argument("--lang=en-GB")
        options.add_argument("--accept-lang=en-GB")
        input_driver = webdriver.Chrome(service=Service(), options=options)

         # click on google agree button so we can continue (not needed anymore)
         # EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "I agree")]')))
        input_driver.get(GM_WEBPAGE)

        return input_driver
    
    
    def __click_on_cookie_agreement(self):
        try:
            agree = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Reject all")]')))
            agree.click()

            # back to the main page
            # self.driver.switch_to_default_content()

            return True
        except:
            return False


    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return strOut


def get_reviews(review_url, review_num=40, debug=False):
    GM_WEBPAGE = 'https://www.google.com/maps/'
    MAX_WAIT = 10
    MAX_RETRY = 5
    MAX_SCROLLS = 40
    
    driver = GoogleMapsScraper(debug=debug)
    
    driver.sort_by(review_url)
    print('success to sort reviews')
    
    n = 0
    N = review_num
    reviews_list = []
    while len(reviews_list) < N:

        reviews = driver.get_reviews(n)
        if len(reviews) == 0:
            break

        for r in reviews:
            row_data = r
            
            if row_data:
                reviews_list.append(row_data)

        n += len(reviews)
        print(f'get {len(reviews_list)} reviews')
    
    driver.exit()
    return reviews_list


def get_review_page_url(search_name, debug=False):
    GM_WEBPAGE = 'https://www.google.com/maps/'
    MAX_WAIT = 10
    MAX_RETRY = 5
    MAX_SCROLLS = 40
    
    driver = GoogleMapsScraper(debug=debug)
    
    review_url = driver.get_review_page_url(search_name)
    # print(url)
    
    driver.exit()
    return review_url


if __name__ == '__main__':
    driver = GoogleMapsScraper(debug=True)
    
    # driver.sort_by('https://www.google.com/maps/place/%E7%B7%B4+%E7%B6%93%E6%BF%9F%E5%B0%8F%E5%90%83/@25.1217542,121.7210682,17z/data=!3m1!4b1!4m8!3m7!1s0x345d4fa36f0efca5:0xb78d754d30216052!8m2!3d25.1217542!4d121.7236431!9m1!1b1!16s%2Fg%2F11sqst80zl?authuser=0&entry=ttu&g_ep=EgoyMDI0MDgyOC4wIKXMDSoASAFQAw%3D%3D')
    driver.sort_by('https://www.google.com/maps/place/IDF%E8%88%87%E9%9B%9E%E5%90%8C%E8%A1%8C/@25.1255153,121.7136652,17.25z/data=!4m8!3m7!1s0x345d4d3bc04393f7:0x4d51253f410b687f!8m2!3d25.1264205!4d121.7147294!9m1!1b1!16s%2Fg%2F11y7cyk5kt?authuser=0&entry=ttu&g_ep=EgoyMDI0MDgyOC4wIKXMDSoASAFQAw%3D%3D')
    
    n = 0
    N = 100
    reviews_list = []
    while len(reviews_list) < N:

        reviews = driver.get_reviews(n)
        if len(reviews) == 0:
            break

        for r in reviews:
            # row_data = list(r.values())
            row_data = r
            
            if row_data:
                print(row_data)
                reviews_list.append(row_data)

        n += len(reviews)
        print(len(reviews_list))
    
    print()
    for i, x in enumerate(reviews_list):
        print(i, x)
    print()
    
    # review_url = get_review_page_url("123")
    # print(review_url)