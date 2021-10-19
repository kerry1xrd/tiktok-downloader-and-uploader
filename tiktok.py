import time, shutil, os, ugents

from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

# download video path
path = 'C:\\Users\\Mrsla\\Desktop\\tiktok-uploader\\video'

downloadPath = path + '\\'

# initilizating
def init():
    options = webdriver.ChromeOptions()

    prefs = {'download.default_directory': downloadPath}

    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=' + ugents.getAgent())
    options.add_experimental_option('prefs', prefs)

    global driver
    driver = webdriver.Chrome(options=options,  executable_path=CM().install())
    driver.set_window_size(1680, 900)

# init
init()

while 1:
    # link
    link = input('Введите ссылку для скачивания: ')

    # download tt video page
    driver.get('https://ssstik.io')

    # send keys link
    driver.find_element_by_xpath('/html/body/main/section[1]/div/div/form/div[2]/input[1]').send_keys(link)

    # click download video
    driver.find_element_by_xpath('/html/body/main/section[1]/div/div/form/div[3]/button').click()

    # get desc
    while 1:
        try:
            description = driver.find_element_by_xpath('/html/body/main/section[1]/div/div/div[3]/div/div/p').text.split('#')
            break
        except:
            pass

    # download video from href
    driver.get(driver.find_element_by_xpath('/html/body/main/section[1]/div/div/div[3]/div/div/a[1]').get_attribute('href'))

    # waitting when downloaded
    while 1:
        files = os.listdir(downloadPath)
        if str(files).endswith('''.mp4']'''):
            break
        else:
            print(str(files))

    # print govno
    print(description)

    time.sleep(2)

    # open tiktok uploud page
    driver.get('https://www.tiktok.com/upload?lang=ru-RU')

    # time sleep 1
    time.sleep(1)

    # uploading video
    while 1:
        try:
            driver.find_element_by_name('upload-btn').send_keys(downloadPath + files[0])
            break
        except Exception as a:
            print(a)
            pass
        driver.implicitly_wait(100)

    # caption
    caption = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')

    # wait
    driver.implicitly_wait(10)

    # i dont know really
    ActionChains(driver).move_to_element(caption).click(caption).perform()

    # entering description
    for a in description:
        if a == description[0]:
            ActionChains(driver).send_keys(a).perform()
            time.sleep(1)
            ActionChains(driver).send_keys(Keys.SPACE).perform()
            time.sleep(1)
            description.remove(description[0])
        else:
            pass

    for d in description:
        ActionChains(driver).send_keys('#' + d).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.RETURN).perform()
        time.sleep(1)

    time.sleep(5)

    os.remove(downloadPath + files[0])