import sqlite3
import bcrypt
import configparser
import requests
import os
from abc import ABC, abstractmethod

class DB(ABC):
    @abstractmethod
    def insertData(self):
        pass
    def extractData(self):
        pass
    
class Database():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('credentials.ini')
        self.salt = config['encryption']['salt']
        self.salt = self.salt.encode()
        self.url = "https://users-baastheglass.turso.io/v2/pipeline"
        self.auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzE5NTQ3OTYsImlkIjoiZTNiMGI2NzItYjVhZC00MmNlLWEzMDAtNTA0ZjY4ZTRhZWM1In0.KX9ntzXmHg84ZPGze4HZsr-qB9ZB8JMD_UJIlwH9nHggtFuqu37WFO8UEYgHARx45RPkFcw61Tf_h5SjnoBvBA"
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": """CREATE TABLE IF NOT EXISTS User
                            (userName TEXT PRIMARY KEY,
                            password TEXT,
                            profilePictureLink TEXT,
                            email TEXT,
                            downloadLocation TEXT)"""}},
                {"type": "execute", "stmt": {"sql": """CREATE TABLE IF NOT EXISTS UserShow
                            (userName TEXT,
                            show TEXT,
                            PRIMARY KEY(userName, show))"""}},
                {"type" : "execute", "stmt" : {"sql": """CREATE TABLE IF NOT EXISTS UserHistory
                                               (userName TEXT,
                                               show TEXT,
                                               episodeNum INT,
                                               PRIMARY KEY(userName, show, episodeNum))"""}},
                {"type": "close"}
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            print(data)
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    
    def insertUser(self, userName, passWord, profilePictureLink, email, downloadLocation = " "):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        passWord = bcrypt.hashpw(passWord.encode(), self.salt)
        email = bcrypt.hashpw(email.encode(), self.salt)
        if downloadLocation == " ":                
            path = "C:/Users/"+ os.getlogin() + "/Downloads"
            if os.path.exists(path):
                downloadLocation = path
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" INSERT INTO User (userName, passWord, profilePictureLink, email, downloadLocation) VALUES ("{userName}", "{passWord}", "{profilePictureLink}", "{email}", "{downloadLocation}")"""}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
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
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" SELECT userName, passWord FROM User where userName = "{userName}" and passWord = "{passWord}" """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            rows = data["results"][0]["response"]["result"]["rows"]
            if(len(rows) > 0):
                return True
            else:
                return False
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def insertHistory(self, userName, show, episodeNum):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" INSERT INTO UserHistory (userName, show, episodeNum) VALUES ("{userName}", "{show}", {episodeNum}) """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            return data
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def insertShow(self, userName, show):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f""" INSERT INTO UserShow (userName, show) VALUES ("{userName}", "{show}") """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            return data
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def getUserShows(self, userName):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f"""SELECT show from UserShow where userName = "{userName}" """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            rows = data["results"][0]["response"]["result"]["rows"]
            if len(rows) == 0:
                return "User has no shows"
            else:
                return rows
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def getShowHistory(self, userName, show):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f"""SELECT episodeNum from UserHistory where userName = "{userName}" and show = "{show}" """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            rows = data["results"][0]["response"]["result"]["rows"]
            if len(rows) == 0:
                return "No episodes have been downloaded for this show"
            else:
                return rows
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def getEpisodeRecord(self, userName, show, episodeNum):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f"""SELECT userName, show, episodeNum from UserHistory where userName = "{userName}" and show = "{show}" and episodeNum = {episodeNum}"""}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            rows = data["results"][0]["response"]["result"]["rows_read"]
            print(rows)
            #return data
            return rows
            #rows = data[""]
            # rows = data["results"][0]["response"]["result"]["rows"]
            # if len(rows) == 0:
            #     return "No episodes have been downloaded for this show"
            # else:
            #     return rows
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    
    def getUserHistory(self, userName):
        userName = bcrypt.hashpw(userName.encode(), self.salt)
        body = {
            "requests": 
                [
                {"type": "execute", "stmt": {"sql": f"""SELECT show, episodeNum from UserHistory where userName = "{userName}" """}},
                {"type": "close"},
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            data = response.json()
            rows = data["results"][0]["response"]["result"]["rows"]
            if len(rows) == 0:
                return "No episodes have been downloaded for this show"
            else:
                return rows
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
        
class localStorage(DB):
    def __init__(self):
        self.conn = sqlite3.connect("episil.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users(userName TEXT)")
        
    
    def insertData(self, userName):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE userName = '?'", userName)
            row = self.cursor.fetchone()
            if(row):
                return "User already exists"
            else:
                self.cursor.execute("INSERT INTO Users VALUES(?)", (userName,))
                self.conn.commit()
                return "Done successfully"
        except Exception as e:
            return e
    def extractData(self):
        try:
            self.cursor.execute("SELECT * FROM Users")
            row = self.cursor.fetchall()
            return row
        except Exception as e:
            print(e)
    def deleteData(self):
        try:
            self.cursor.execute("DELETE FROM Users")
            self.conn.commit()
            return "Deleted"
        except Exception as e:
            return e
                
if __name__ == "__main__":
    #base = localStorage()
    #print(base.insertData("Baasil"))
    #print(base.extractData())
    base = Database()
    if(base.verifyUser("Baasil", "booter") == True):
        print("True")
    else:
        print("False")
    #print(base.deleteData())             