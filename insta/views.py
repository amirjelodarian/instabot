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

        for i in range(6): 
            like(driver)


        if(type(hashtags) == str):
            break
        else:
            continue
        

    sleep(60*60*4)


def like(driver):
    likePath = driver.find_element_by_xpath("//*[contains(@class, 'fr66n')]/button/div/*[*[local-name()='svg']/@aria-label='Like']/*")
    if len(likePath) == 1 :
        driver.find_element_by_class_name("fr66n").click() # like post 
        sleep(5)    
        
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
