import flask
from flask import Flask, request
import sqlite3
from database import Database
import string
import random
import bcrypt
import configparser

app = Flask(__name__)

@app.route('/addUser', methods = ["POST"])
def addUser():
    d1 = Database()
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    email = request.form.get("email")    
    profilePictureLink = request.form.get("profilePictureLink")
    try:
        d1.insertUser(userName, passWord, profilePictureLink, email)
        return "User added successfully!" 
    except Exception as e:
        return e

@app.route('/verifyUser', methods = ["POST"])
def verifyUser():
    d1 = Database()
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    if (d1.verifyUser(userName, passWord)):
        resp = flask.make_response()
        letters = string.ascii_letters
        key = ' '.join(random.choice(letters) for i in range(5))
        resp.set_cookie(key, userName)
        return resp
    else:
        return "Invalid Credentials"

@app.route('/insertHistory', methods = ["POST"])
def insertHistory():
    d1 = Database()
    userName = request.form.get("userName")
    show = request.form.get("show")
    episodeNum = request.form.get("episodeNum")
    try:
        return d1.insertHistory(userName, show, episodeNum)
    except Exception as e:
        return e

@app.route('/insertShow', methods = ["POST"])
def insertShow():
    d1 = Database()
    userName = request.form.get("userName")
    show = request.form.get("show")
    try:
        return d1.insertShow(userName, show)
    except Exception as e:
        return e

@app.route('/getUserShows', methods = ["GET"])
def getShows():
    d1 = Database()
    userName = request.form.get("userName")
    try:
        rows = d1.getUserShows(userName)
        animeNames = []
        for row in rows:
            animeNames.append(row[0]['value'])
        return animeNames
    except Exception as e:
        return {"error": str(e)}

@app.route('/getShowHistory', methods = ["GET"])
def getShowHistory():
    d1 = Database()
    userName = request.form.get("userName")
    show = request.form.get("show")
    try:
        rows = d1.getShowHistory(userName, show)
        episodes = []
        for row in rows:
            episodes.append(row[0]['value'])
        return episodes
    except Exception as e:
        return e

@app.route('/getDownloadHistory', methods = ["GET"])
def getDownloadHistory():
    d1 = Database()
    userName = request.form.get("userName")
    try:
        rows = d1.getUserHistory(userName)
        animeNames = []
        episodeNums = []
        finalRes = []
        for row in rows:
            animeNames.append(row[0]['value'])
            episodeNums.append(row[1]['value'])
        print(animeNames)
        print(episodeNums)
        for i in range(len(animeNames)):
            finalRes.append(animeNames[i])
            finalRes.append(episodeNums[i])
        return finalRes
    except Exception as e:
        return e

if __name__ == "__main__":
    
    app.run(debug=True)