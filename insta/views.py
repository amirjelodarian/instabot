import sys
from os import remove, stat
import re
from typing import Match
from django.http import request
from django.shortcuts import render
from django.template.defaultfilters import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.webdriver import basestring
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from django.templatetags.static import static
import random
from re import findall

from bot.libray.xpath import read_xpath


# Create your views here.
messages = []



def index(request):
    return render(request,'index.html')



def bot(request):
    
    global messages
    try:
        messages = validate(request)
    except:
        messages.append('Something Wrong !')
    if messages:
        return render(request,'index.html',{ 'messages' : messages })

        
    




def validate(request):
    global messages
    messages = []
    if 'username' in request.POST and len(request.POST['username']) > 0 and 'password' in request.POST and len(request.POST['password']) > 0:
        if len(request.POST['username']) < 1 or len(request.POST['password']) < 1:
            messages.append('Username Or Password is empty !')    

        try:
            if request.POST['selectOption'] == 'likeOrFollowAsHashtags':
                likeOrFollowAsHashtagsValidate(request)
                hashtags = validatehashtagOrFollowTextArea(request.POST['addHashtags'],'Hashtags')
                if(not messages):
                    doLikeOrFollowByHashtags(request,hashtags)
                    
            elif request.POST['selectOption'] == 'followSuggestionPeople':
                followSuggestionPeopleValidate(request)
                userIds = validatehashtagOrFollowTextArea(request.POST['addUserID'],"People ID\'s")
                if(not messages):
                    messages.append(userIds)
                    # do follow suggestion validate
                    messages.append('do follow suggestion validate')

            else:
                messages.append("Don't change select option value !")
        except ValueError:
            messages.append(ValueError)
            # messages.append("Please Select A Option And Use !")

        
    else:
        messages.append('Username Or Password is Undifined !')   

    return messages




def likeOrFollowAsHashtagsValidate(request):
    global messages
    if 'followTag' not in request.POST and 'likeTag' not in request.POST:
        messages.append("Please choose checkbox options !")
    

    if 'addHashtags' not in request.POST or len(request.POST['addHashtags']) < 1:
        messages.append("Please add hashtags !")

    if 'countLikeOrFollow' in request.POST:
        countValidate(request,'countLikeOrFollow')
    else:
        messages.append("Please add count !")
    




def followSuggestionPeopleValidate(request):
    global messages
    if 'addUserID' not in request.POST or len(request.POST['addUserID']) < 1:
        messages.append("Please add user ID's !")
    
    if 'countSuggestion' in request.POST:
        countValidate(request,'countSuggestion')
    else:
        messages.append("Please add count !")




def countValidate(request,countElementName):
    global messages
    if request.POST[countElementName]:
        try:
            int(request.POST[countElementName])  
        except:
            messages.append("Data type error !") 
        finally:
            countElementName = int(request.POST[countElementName])
            if countElementName < 1:
                messages.append('Count value must be bigger than 0')
    else:
        messages.append("Please add count !")




def validatehashtagOrFollowTextArea(input,hashtagOrFollow):
    global messages
    itemWithNulls = []
    items = []

    if (input.find(',') != -1):
        allItems = input.strip().split(',')
        for item in allItems:
            itemWithNulls.append(item.strip().replace('\n',"").replace('\r',"").replace('\t',"").replace(' ',"").strip())
        for itemWithNull in itemWithNulls:
            if len(itemWithNull) > 0:
                items.append(itemWithNull)

    else:
        items = input.strip().replace('\n',"").replace('\r',"").replace('\t',"").strip()

    if not items:
        messages.append(hashtagOrFollow+' is empty !')
    else:
        return items

def doLikeOrFollowByHashtags(request,hashtags):
    global messages
    if 'followTag' in request.POST:   
        followTag = True
    else:
        followTag = False

    if 'likeTag' in request.POST:
        likeTag = True
    else:
        likeTag = False
        
    driver = login(request)

    # divid count between tags or ids sort list have one item or more
    # for count of like each tag

    #if(type(hashtags) == str):
    #    count = int(request.POST['countLikeOrFollow'])
    #else:
    #    count = (int(request.POST['countLikeOrFollow'])) / int(len(hashtags))

    for hashtag in hashtags:
        # now bot is in hashtag
        driver.get('https://www.instagram.com/explore/tags/%s' % checkStrOrList(hashtags,hashtag))
        sleep(5)
        driver.find_element_by_class_name('_9AhH0').click() # click first post
        sleep(8)

        like(driver,4)


        if(type(hashtags) == str):
            break
        else:
            continue
        

    sleep(60*60*4)


def like(driver,count):
    
    #likePath = driver.find_element_by_xpath("//*[contains(@class, 'fr66n')]/button/div/*[*[local-name()='svg']/@aria-label='Like']/*")
    #if len(likePath) == 1 :
    #    driver.find_element_by_class_name("fr66n").click() # like post 
    #    sleep(5)    

    #next post
    #driver.find_element_by_xpath("//div[contains(@class, ' l8mY4 ')]").click()
    for i in range(count):
        sleep(random.randint(5,8))
        like_xpath = "//*[contains(@class, 'fr66n')]/button/div/*[*[local-name()='svg']/@aria-label='Like']/*"
        unlike_xpath = "//*[contains(@class, 'fr66n')]/button/div/*[*[local-name()='svg']/@aria-label='Unlike']/*"
        like_elem = driver.find_elements_by_xpath(like_xpath)
        if len(like_elem) == 1:
        # sleep real quick right before clicking the element
            sleep(2)
            like_elem = driver.find_elements_by_xpath(like_xpath)
        if len(like_elem) > 0:
            click_element(driver, like_elem[0])
        # check now we have unlike instead of like
        liked_elem = driver.find_elements_by_xpath(unlike_xpath)
        #next post
        driver.find_element_by_xpath("//div[contains(@class, ' l8mY4 ')]").click()
            
  
def checkStrOrList(val1,val2):
    if(type(val1) == str):
        return val1
    else:
        return val2

def login(request):
    driver = webdriver.Chrome('bot/chromedriver')
    driver.get('https://www.instagram.com/')

    driver.find_element_by_name("username").send_keys(request.POST['username'])
    driver.find_element_by_name("password").send_keys(request.POST['password'])
    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(7)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
    return driver


def click_element(driver, element, tryNum=0):

    try:
        # use Selenium's built in click function
        element.click()


    except Exception:
        # click attempt failed
        # try something funky and try again

        if tryNum == 0:
            # try scrolling the element into view
            try:
                # This tends to fail because the script fails to get the element class
                if element.get_attribute("class") != "":
                    driver.execute_script(
                        "document.getElementsByClassName('"
                        + element.get_attribute("class")
                        + "')[0].scrollIntoView({ inline: 'center' });"
                    )
            except Exception:
                pass

        elif tryNum == 1:
            # well, that didn't work, try scrolling to the top and then
            # clicking again
            driver.execute_script("window.scrollTo(0,0);")

        elif tryNum == 2:
            # that didn't work either, try scrolling to the bottom and then
            # clicking again
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        else:
            # try `execute_script` as a last resort
            # print("attempting last ditch effort for click, `execute_script`")
            try:
                if element.get_attribute("class") != "":
                    driver.execute_script(
                        "document.getElementsByClassName('"
                        + element.get_attribute("class")
                        + "')[0].click()"
                    )
                    # update server calls after last click attempt by JS
            except Exception:
                messages.append("Failed to click an element, giving up now")

            # end condition for the recursive function
            return

        # update server calls after the scroll(s) in 0, 1 and 2 attempts

        # sleep for 1 second to allow window to adjust (may or may not be
        # needed)
        sleep_actual(1)

        tryNum += 1

        # try again!
        click_element(driver, element, tryNum)
