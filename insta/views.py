from os import remove
import re
from typing import Match
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

# Create your views here.
messages = []
# =========================================
def index(request):
    return render(request,'index.html')
# =========================================
def bot(request):
    messages = validate(request)
    if messages:
        return render(request,'index.html',{ 'messages' : messages })

    if not messages:
        return render(request,'index.html',{ 'messages' : 'ok' })
# =========================================
def validate(request):
    global messages
    messages = []
    if 'username' in request.POST and 'password'  in request.POST:
        if len(request.POST['username']) < 1 or len(request.POST['password']) < 1:
            messages.append('Username Or Password is empty !')    

        if request.POST['selectOption'] == 'likeOrFollowAsHashtags':
            likeOrFollowAsHashtagsValidate(request)
            if(not messages):
                validateHashtags(request)
                # do hashtags validate
                messages.append('do hashtags validate')
        elif request.POST['selectOption'] == 'followSuggestionPeople':
            followSuggestionPeopleValidate(request)
            if(not messages):
                # do follow suggestion validate
                messages.append('do follow suggestion validate')
        else:
            messages.append("Don't change select option value !")
    else:
        messages.append('Username Or Password is Undifined !')   

    return messages
# =========================================
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
    return messages
# =========================================
def followSuggestionPeopleValidate(request):
    global messages
    if 'addUserID' not in request.POST or len(request.POST['addUserID']) < 1:
        messages.append("Please add user ID's !")
    
    if 'countSuggestion' in request.POST:
        countValidate(request,'countSuggestion')
    else:
        messages.append("Please add count !")
# =========================================
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
# =========================================
def validateHashtags(request):
    global messages
    hashtagsWithNull = []
    hashtags = []

    if (request.POST['addHashtags'].find(',') != -1):
        allHashtags = request.POST['addHashtags'].strip().split(',')
        for hashtag in allHashtags:
            hashtagsWithNull.append(hashtag.strip().replace('\n',"").replace('\r',"").replace('\t',"").replace(' ',"").strip())
        
        for i in len(hashtagsWithNull):
            if '' in hashtagsWithNull[i] :
                hashtagsWithNull[i].remove()

        hashtags = hashtagsWithNull

    else:
        hashtags = request.POST['addHashtags'].strip().replace('\n',"").replace('\r',"").replace('\t',"").strip()
    messages.append(hashtags)
# =========================================
# =========================================
# =========================================
# =========================================
# =========================================
