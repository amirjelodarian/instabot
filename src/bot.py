from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
# username = input('Username : ')
# password = input('Password : ')


chrome_options = Options()

chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('./chromedriver',options=chrome_options)


driver.get('https://www.instagram.com/')

driver.find_element_by_name("username").send_keys('amir__jn')
driver.find_element_by_name("password").send_keys('#amir0007amir0007#')
driver.find_element_by_xpath("//button[@type='submit']").click()
sleep(7)
driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
sleep(60*60*4)