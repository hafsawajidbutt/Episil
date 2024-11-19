import sqlite3
import bcrypt
import configparser
from abc import ABC, abstractmethod
import requests
import os

class database(ABC):
    pass
class Userbase(database):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('info.ini')
        self.salt = config['encryption']['salt']
        self.salt = self.salt.encode()
    
    def insertUser(self, userName, passWord, profilePictureLink, email, downloadLocation = " "):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        passWord = bcrypt.hashpw(passWord.encode(), self.salt)
        email = bcrypt.hashpw(email.encode(), self.salt)
        if downloadLocation == " ":                
            path = "C:/Users/"+ os.getlogin() + "/Downloads"
            if os.path.exists(path):
                downloadLocation = path
        url = "https://users-baastheglass.turso.io/v2/pipeline"
        auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzE5NTQ3OTYsImlkIjoiZTNiMGI2NzItYjVhZC00MmNlLWEzMDAtNTA0ZjY4ZTRhZWM1In0.KX9ntzXmHg84ZPGze4HZsr-qB9ZB8JMD_UJIlwH9nHggtFuqu37WFO8UEYgHARx45RPkFcw61Tf_h5SjnoBvBA"
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" INSERT INTO User (userName, passWord, profilePictureLink, email, downloadLocation) VALUES ("{userName}", "{passWord}", "{profilePictureLink}", "{email}", "{downloadLocation}")"""}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            print(data)
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def verifyUser(self, userName, passWord):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        print(userName)
        passWord = bcrypt.hashpw(passWord.encode(), self.salt)
        print(passWord)
        url = "https://users-baastheglass.turso.io/v2/pipeline"
        auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzE5NTQ3OTYsImlkIjoiZTNiMGI2NzItYjVhZC00MmNlLWEzMDAtNTA0ZjY4ZTRhZWM1In0.KX9ntzXmHg84ZPGze4HZsr-qB9ZB8JMD_UJIlwH9nHggtFuqu37WFO8UEYgHARx45RPkFcw61Tf_h5SjnoBvBA"
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" SELECT userName, passWord FROM User where userName = "{userName}" and passWord = "{passWord}" """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            print(type(data))
            # results_dict = data["results"]
            # response_dict = results_dict["response"]
            # result_dict = response_dict["result"]
            # rows_dict = result_dict["rows"]
            rows = data["results"][0]["response"]["result"]["rows"]
            #print(len(rows[0][0]))
            return data["results"][0]["response"]["result"]["rows"]
            # return data["results"]["response"]["result"]["rows"]
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
        # selUsername = data[0]
        # selPassword = data[1]
        # if(selPassword and selUsername):
        #     print("In true")
        #     return True
        # else:
        #     print("In false")
        #     return False
            
class Localdatabase(database):
    def __init__(self):
        self.conn = sqlite3.connect("epnis.db")
        self.cursor = self.conn.cursor() 
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS History 
                            userName TEXT,
                            showName TEXT,
                            episodeNum INT
                            PRIMARY KEY (userName, showName, episodeNum)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UserShow
                            userName TEXT,
                            showName TEXT,
                            PRIMARY KEY(userName, showName)''')
        config = configparser.ConfigParser()
        config.read('info.ini')
        self.salt = config['encryption']['salt']
        self.salt = self.salt.encode()

        
               
#d1.insertUser("Hafsa Butt", "buttmaster", "butt", "butt@gmail.com")
#d1.verifyUser("Hafsa Butt", "buttmaster")