import requests
import urllib3
import asyncio
from AnilistPython import Anilist
from qbittorrent import Client
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import time
import getpass
from selenium.webdriver.common.keys import Keys
import glob
import os
import datetime
import subprocess
import sqlite3
from database import Database, localStorage
import pyautogui
from abc import ABC, abstractmethod

class airedDownloader():
    def __init__(self):
        self.qb = None
    
    def airedDownload(self, anime_name):
        try:
            self.qb = Client('http://127.0.0.1:8080/')
            qb = self.qb
            qb.login('admin', 'hafsapotty')
        except Exception as e:
            if(type(e) == requests.exceptions.ConnectionError):
                for root, dirs, files in os.walk(r'C:\Program Files'):
                    for name in files:
                        if name == "qbittorrent.exe":
                            path = os.path.abspath(os.path.join(root, name))
                            break
                subprocess.call([path])
                qb.login('admin', 'hafsapotty')
        new_anime_name = "%20".join(anime_name.split())
        try:
            response = requests.get(f"https://nyaaapi.onrender.com/nyaa?q={new_anime_name}", verify=True)
            dic = response.json()
            animeTitle = dic["data"][0]["title"]
            torrentLink = dic["data"][0]["torrent"]
            magnetLink = dic["data"][0]["magnet"]
            print(magnetLink)
            print(torrentLink)
            qb.download_from_link(torrentLink)
        except Exception as e:
            print("In exception block")
            print(e.args)
    
    
class airingDownloader():
    def __init__(self):
        self.driver = None
        self.driver2 = None
        d1 = Database()
        self.customDownload = False
        self.userName = localStorage().extractData()
        download_dir = d1.getUserDownloadDirectory(self.userName)["results"][0]["response"]["result"]["rows"][0][0]["value"]
        if(download_dir[-9::] == "Downloads"):
            # Create Chrome options
            self.customDownload = True
            self.chrome_options = Options()
            prefs = {"download.default_directory": download_dir}
            self.chrome_options.add_experimental_option("prefs", prefs)
        
        
    def findingEpisodes(self, name, quality):  
        self.driver = uc.Chrome()
        driver = self.driver
        driver.get("https://animepahe.ru/")
        time.sleep(10)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located, (By.CSS_SELECTOR, "input[placeholder='Search']"))
        time.sleep(5)
        print("Selector located")
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']").send_keys(name)
        time.sleep(10)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located, (By.XPATH, "/html[1]/body[1]/header[1]/nav[1]/div[1]/form[1]/div[1]/ul[1]/li[1]/a[1]"))
        driver.find_element(By.XPATH, "/html[1]/body[1]/header[1]/nav[1]/div[1]/form[1]/div[1]/ul[1]/li[1]/a[1]").click()
        time.sleep(5)
        play_links = driver.find_elements(By.CLASS_NAME, "play")
        links = []
        for playlink in play_links:
            links.append(playlink.get_attribute('href'))
        links.reverse()
        driver.quit()
        return links
    
    def animepahe(self, link, quality):
        if(self.customDownload == False):
            self.driver = uc.Chrome()
        else:
            self.driver = uc.Chrome(options=self.chrome_options)
        driver = self.driver
        #driver2 = self.driver2
        driver.get(link)
        #driver.get("https://animepahe.ru/play/af8ae120-37b5-8f96-59b4-f40d31af59d3/a4d2ec9c2510ffdf52fd30713f42cfc7cbb4a8b3646eccd28e33decb2f127a62")
        time.sleep(10)
        print(self.driver.current_url)
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#downloadMenu")))
        orgWindowHandle = driver.current_window_handle
        driver.find_element(By.CSS_SELECTOR, "#downloadMenu").click()
        print("Download menu clicked")
        time.sleep(10)
        print("Slept")
        driver.switch_to.window(orgWindowHandle)
        print("Switched")
        time.sleep(10)
        print(driver.current_window_handle)
        downloadLinks = driver.find_elements(By.CLASS_NAME, "dropdown-item")
        winLink = ""
        for link in downloadLinks:
            if(quality in link.text):
                winLink = link.get_attribute('href')
            #winLink = link.get_attribute('href')
        if(winLink == ""):
            driver.quit()
            return "Quality not found"
        print("Download button found")
        print(winLink)
        #driver.quit()
        response = requests.get(winLink)
        soup = BeautifulSoup(response.content, 'html.parser')
        scriptLine = soup.select_one('script[type]')
        print(scriptLine)
        script_content = scriptLine.text.strip()
        start_index = script_content.find('"href","https:') + len('"href",')  # Skip unnecessary part
        end_index = script_content.find(')', start_index)
        href_part = script_content[start_index:end_index]
        href_value = href_part[href_part.find('"') + 1: href_part.rfind('"')]  # Extract href within quotes
        if(self.customDownload == False):
            self.driver2 = uc.Chrome()
        else:
            self.driver2 = uc.Chrome(options=self.chrome_options)
        driver2 = self.driver2
        driver2.get(href_value)
        time.sleep(5)
        pyautogui.moveTo(x=2665, y=667)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(2)
        pyautogui.click()
        #use OS to make my own watchdog
        username = getpass.getuser()
        print("Started")
        downloadBegun = False
        downloadEnded = False
        while True:
            time.sleep(1)
            list_of_files = glob.glob(f"C:\\Users\\{username}\\Downloads\\*") # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file[-10::])
            if(latest_file[-10::] == "crdownload"):
                downloadBegun = True
            if(downloadBegun == True):
                if(latest_file[-3::] == "mp4"):
                    downloadEnded = True
                    break
        downloadBegun = False
        downloadEnded = False
        print("While loop exited")
        driver2.quit()
   
    def getDownloadOptions(self, name):
        self.driver = uc.Chrome()
        driver = self.driver
        driver.get("https://animepahe.ru/")
        time.sleep(10)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located, (By.CSS_SELECTOR, "input[placeholder='Search']"))
        time.sleep(5)
        print("Selector located")
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']").send_keys(name)
        time.sleep(10)
        searchResults = driver.find_element(By.CLASS_NAME, "search-results")
        searchArr = searchResults.text.split('\n')
        count = 0
        for res in searchArr:
            if(searchArr.index(res) % 3 != 0):
                searchArr[searchArr.index(res)] = " "       
                count += 1
        for i in range(count):
            searchArr.remove(" ")
        driver.quit()
        return searchArr
    
    def airingDownload(self, anime_name, quality):
        if(quality != "360p" and quality != "720p" and quality != "1080p"):
            return "Incorrect Quality"
        links = self.findingEpisodes(anime_name, quality)
        db = Database()
        for plink in links:
            index = links.index(plink)
            record = db.getEpisodeRecord(self.userName, anime_name, index)
            if(record == 1 and index != 0):    
                if(self.animepahe(plink, quality) == "Quality not found"):
                    return "Quality not found"
                db.insertHistory(self.userName, anime_name, index + 1)
            else:
                oldLink = links[links.index(plink) - 1]
                if(self.animepahe(oldLink, quality) == "Quality not found"):
                    return "Quality not found"
                db.insertHistory(self.userName, anime_name, index)
                if(self.animepahe(plink, quality) == "Quality not found"):
                    return "Quality not found"
                db.insertHistory(self.userName, anime_name, index)

class downloader():
    def __init__(self):
        self.anilist = Anilist()
            
    def download(self, anime_name, quality):
        anilist = self.anilist    
        print("In download")
        anime_data = anilist.get_anime(anime_name)
        print(anime_data)
        if anime_data['airing_status'] == "FINISHED":
            print("Already aired")
            try:
                ad = airedDownloader()
                ad.airedDownload(anime_name)
            except:
                ad = airingDownloader()
                ad.airingDownload(anime_name, quality)
        else:
            print("Airing")
            ad = airingDownloader()
            ad.airingDownload(anime_name, quality)    
            
    
        
if __name__ == "__main__":
    d1 = downloader()
    #d1.airingDownload("Tokyo Ghoul")
    d1.download("Tokyo Ghpul", "1080p")
    #print(d1.getDownloadOptions("Tokyo Ghoul"))
        
