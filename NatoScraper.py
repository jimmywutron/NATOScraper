#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:21:23 2024

@author: jimmywu
"""

#%%
import requests, sys, webbrowser, bs4, os, datetime
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
def ExtractText(urlString):
    browser = webdriver.Firefox()
    browser.get(urlString)
    text = browser.find_element(By.CSS_SELECTOR, 'section[class = "content cf"]').text
    browser.quit()
    return text

#%%
def ExtractTitle(urlString):
    browser = webdriver.Firefox()
    browser.get(urlString)
    title = browser.find_element(By.CSS_SELECTOR, 'h1[class = "fs-huge"').text
    browser.quit()
    return title

#%%
def ExtractTitleText(urlString):
    browser = webdriver.Firefox()
    try:
        browser.get(urlString)
        try:
            title = browser.find_element(By.CSS_SELECTOR, 'h1[class = "fs-huge"').text
        except:
            title = 'No title found'
        try:
            text = browser.find_element(By.CSS_SELECTOR, 'section[class = "content cf"]').text
        except:
            text = "No content found"
    except:
        title = 'No title found'
        text = "No content found"
    browser.quit()
    return title,text

#%% Returns all the URLs for the search results on one page
def GetResultUrls(urlString):
    browser = webdriver.Firefox()
    browser.get(urlString)
    resultsUrls = browser.find_elements(By.CSS_SELECTOR, 'tr td h3 a')
    links = [elem.get_attribute('href') for elem in resultsUrls]
    browser.quit()
    return links

#%%
def NextPageURL(urlString):
    browser = webdriver.Firefox()
    browser.get(urlString)
    nextPageButton = browser.find_element(By.CSS_SELECTOR, 'a[class = pager-next]')
    nextPageUrl = nextPageButton.get_attribute('href')
    browser.quit()
    if str(nextPageUrl).endswith('#'):
        return 'You are on the last page'
    else:
        return nextPageUrl

#%% 
def ScrapeSearch(urlString):
    keyWord = input("What keyword(s) would you like to search? ")
    searchURL = urlString
    searchResultsURL = []
    browser = webdriver.Firefox()
    browser.get(urlString)
    #Get the urls for all search results for all pages, up to, but not including, the last
    while NextPageURL(searchURL) != 'You are on the last page':
        #Extract the search result links from the page
        pageRes = GetResultUrls(searchURL)
        #Append the links to the master list
        for res in pageRes:
            searchResultsURL.append(res)
        #Go to the next page
        searchURL = NextPageURL(searchURL)       
    print("Scraped %s articles" %(len(searchResultsURL)))
    return searchResultsURL
#%%
#Save the results as text files in a folder
#Create a folder named after the keyWord
keyWord = input("What keyword(s) would you like to search? ")
SavePath = Path.cwd()/'documents'/'NATOScraper'
folder_path = SavePath/keyWord
os.makedirs(folder_path, exist_ok=True)
#Create a text file for each search result within the folder
for res in resList :
    title = ExtractTitleText(str(res))[0]
    text = ExtractTitleText(str(res))[1]
    #Get title for file naming, limit string length
    titleSave = title.replace(" ","")[0:50]
    with open(folder_path/f"{titleSave}.txt", "w" ) as f:
        f.write(str(title) + "\n" + str(text))
    f.close()
#%% Testing Sandbox
searchURL = 'https://www.nato.int/cps/en/natohq/search_380.htm?query=&search_phrase=Communication+Technology&without_words=&search_types=*&search_languages=en&page_size=10'
searchUrls = ScrapeSearch(searchURL)

#%%
titleSave = "asdgahskdgja;lsdg"
title = titleSave[0:20]
print(title)

#%%
for resList in resLinkList:
    for res in resList:
        titleText = ExtractTitleText(str(res))
        print("Title: %s/n Text: %s" %(titleText[0],titleText[1]))
    

#%%
for ele in ExtractTitleText('https://www.nato.int/cps/en/natohq/news_151250.htm?selectedLocale=en'):
    print(str(ele))
    