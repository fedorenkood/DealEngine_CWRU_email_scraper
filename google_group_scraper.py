#!/usr/bin/env python
# coding: utf-8

# In[278]:


import requests
import time, re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

import my_cwru_token as token


# In[301]:


url = 'https://groups.google.com/a/case.edu/forum/#!forumsearch/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

# Pop Google login page.
time.sleep(3)
driver = webdriver.Chrome()
driver.get(url)
driver.get("https://accounts.google.com/AccountChooser?continue=https%3A%2F%2Fgroups.google.com%2Fa%2Fcase.edu%2Fd%2Fforumsearch%2F&hl=en&service=groups2")

# Login my CWRU Gmail account
time.sleep(3)
driver.find_element_by_xpath("//input[@type='email']").send_keys(token.account + '@case.edu')
driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()

# Go through CWRU confirmation page.
time.sleep(3)
driver.find_element_by_xpath("//input[@id='username']").send_keys(token.account)
driver.find_element_by_xpath("//input[@id='password']").send_keys(token.password)
driver.find_element_by_xpath("//input[@class='button']").click()

# Jump back to google group page.
time.sleep(3)
driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()


# In[304]:


# Scroll the google page, this is actually too much of an overkill
time.sleep(5)
for i in range(300):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(0.1)

# Get the node with forum link inside.
time.sleep(3)
soup1 = BeautifulSoup(driver.page_source, 'lxml')
divTags = soup1.find_all('a', attrs={'class': 'gwt-Anchor F0XO1GC-c-a'})

# Get the forum link URL.
time.sleep(3)
info = []
for i in divTags:
    info.append(i['href'])
    
# Concatecate the forum URLs with the prefix.
urlpart1 = 'https://groups.google.com/a/case.edu/forum/'
newurl = []
for i in range(len(info)):
    new = urlpart1 + info[i]
    newurl.append(new)


# In[312]:


# For each forum, scroll till the end to get all the post.
# 1 sec waiting time seems a bit too short for large forums, but I got way more than 500 results so I'll just let it be.
info2 = []
for i in newurl:
    driver.get(i)
#     time.sleep(1)
    
    try:
        topic_last = driver.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
    except:
        continue
        
    try:
        id1 = topic_last.get_attribute('id')
    except:
        continue
    n = 0;
    while True:
        js = 'document.getElementById("' + id1 + '").focus()'
        driver.execute_script(js)
        time.sleep(1)
        t1 = time.time()
        try:
            topic_last = driver.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
        except:
            break
        try:
            id2 = topic_last.get_attribute('id')
        except:
            break
        if (id1 != id2):
            n = n + 1
            id1 = id2
            if (time.time() - t1 >= 1):
                break
        else:
            time.sleep(1)
            topic_last = driver.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
            id2 = topic_last.get_attribute('id')
            if (time.time() - t1 >= 1):
                break
            if (id1 != id2):
                n = n + 1
                id1 = id2
            else:
                print ("\nAll content loaded!")
                break
                    
    soup2=BeautifulSoup(driver.page_source)
    url_tag = soup2.find_all('a', attrs={'class': 'F0XO1GC-q-R'})
    for i in url_tag:
        print(i['href'])
        info2.append(i['href'])


# In[314]:


# Concatenate post URL with their prefixes.
finalURL = []
for i in info2:
    new = urlpart1 + i
    finalURL.append(new)


# In[328]:


# Get the @case.edu email from page source with regex.
mailing_list = []
for i in range(3000):
    driver.get(finalURL[i])
    time.sleep(0.5)
    results=BeautifulSoup(driver.page_source)
    x = re.findall(r'[\w\.-]+@case.edu', str(results))
    mailing_list.extend(set(x))


# In[352]:


# Get rid of incomplete emails with "...".
case_mailing_list = []
for i in mailing_list:
#     if '@case.edu' in i and '...' not in i:
    if '...' not in i:
        case_mailing_list.append(i)


# In[353]:


# Get rid of repretative emails.
case_mailing_list = set(case_mailing_list)
case_mailing_list.remove(token.account + '@case.edu')


# In[354]:


with open('CWRU_scrapped_mailing_list.txt', 'w') as f:
    for i in case_mailing_list:
        f.write(f'{i}\n')

