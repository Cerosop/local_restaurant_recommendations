import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# 可选：配置ChromeDriver的选项
chrome_options = Options()

chrome_options.add_argument("--disable-gpu")  # 如果你是使用Windows系统
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--accept-lang=zh-TW")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# 指定ChromeDriver的路径（如果没有放在系统路径中）
service = Service()


def get_web_text(web_url = None, debug=False):
    if not debug:
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--window-size=1366,768")
    
    # 启动浏览器
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    if web_url == None:
        # 打开目标网页
        # driver.get("https://keelung-for-a-walk.com/zh/%E5%90%83%E5%90%83/13610/")n
        # driver.get("https://supertaste.tvbs.com.tw/pack/347174")y
        # driver.get("https://www.welcometw.com/%E5%9F%BA%E9%9A%86%E7%BE%8E%E9%A3%9F/")y
        driver.get("https://yanmeiantrip.com/keelung-food/")
        # driver.get("https://markandhazyl.com/keelung-food-guide/")y
        # driver.get("https://www.kkday.com/zh-tw/blog/102476/asia-taiwan-keelung-food?srsltid=AfmBOopHI-qRJxq7rCyp7KrX5U4sTnvxHNcHbaTtYAHh8ZCqLa3s2uAl")y
        # driver.get("https://www.gomaji.com/blog/%E5%9F%BA%E9%9A%86%E7%BE%8E%E9%A3%9F-2/")y
        # driver.get("https://today.line.me/tw/v2/article/JPooKPK")y

        # driver.get("https://www.klook.com/zh-TW/blog/keelung-food/")n
    else:
        driver.get(web_url)

    # 等待页面加载完成
    driver.implicitly_wait(5)  # 等待5秒

    # 获取页面的标题
    title = driver.title
    # print("Page title:", title)

    # 查找元素并获取内容（例如获取所有段落文字）
    contents = []
    contents += [{'h1': i} for i in driver.find_elements(By.TAG_NAME, 'h1')]
    contents += [{'h2': i} for i in driver.find_elements(By.TAG_NAME, 'h2')]
    contents += [{'h2': i} for i in driver.find_elements(By.TAG_NAME, 'h3')]
    contents += [{'p': i} for i in driver.find_elements(By.TAG_NAME, 'p')]
    contents += [{'div': i} for i in driver.find_elements(By.TAG_NAME, 'div')]
    new_contents = []
    for content in contents:
        try:
            if list(content.values())[0].location['y']:
                new_contents.append(content)
        except:
            print(content)
            continue
            
    # print()
    contents = sorted(new_contents, key=lambda x: list(x.values())[0].location['y'])

    # contents = sorted(contents, key=lambda x: list(x.values())[0].location['y'])

    web_text_list = ["{title: " + title + "}"]
    for i, content in enumerate(contents):
        for key in content:
            if content[key].text.replace(" ", "") != "":
                y = True
                for j in web_text_list:
                    if content[key].text in j:
                        y = False
                        break
                if y:
                    web_text_list.append("{" + key + ": " + content[key].text + "}")
                    # print(i, key)
                    # print(content[key].text)
                    # print()

    # print(web_text_list)
    # 关闭浏览器
    driver.quit()
    print("success to get web text")
    return web_text_list


def get_recommend_web_url(place, debug=False):
    search_name = place + '+美食+推薦'
    if not debug:
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--window-size=1366,768")
    
    # 启动浏览器
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(f"https://www.google.com.tw/search?q={search_name}")

    # 等待页面加载完成
    driver.implicitly_wait(3)  # 等待5秒

    web_urls = driver.find_elements(By.XPATH, '//a[@jsname=\'UWckNb\']')
    web_urls = [i.get_attribute("href") for i in web_urls 
            if 'klook' not in i.get_attribute("href") and 'tripadvisor' not in i.get_attribute("href") and 'youtube' not in i.get_attribute("href") and 'facebook' not in i.get_attribute("href") and 'instagram' not in i.get_attribute("href")]

    driver.quit()
    print("success to get web url")
    return web_urls
    
    
if __name__ == '__main__':
    # get_recommend_web_url('基隆', debug=True)
    
    print(get_web_text(debug=True))