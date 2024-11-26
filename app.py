import flask
from flask import Flask, request, jsonify
import sqlite3
from database import Database
import string
import random
import bcrypt
import configparser
import requests
from AnilistPython import Anilist
import datetime
from downloader import downloader

app = Flask(__name__)

@app.route('/addUser', methods = ["POST"])
def addUser():
    d1 = Database()
    print("In add user")
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    email = request.form.get("email")    
    profilePictureLink = request.form.get("profilePictureLink")
    try:
        d1.insertUser(userName, passWord, profilePictureLink, email)
        data = data = {'message': 'Success'}
        print("About to send response")
        response = flask.make_response(jsonify(data))
        return response
    except Exception as e:
        return e

@app.route('/verifyUser', methods = ["POST"])
def verifyUser():
    print("In verify user")
    d1 = Database()
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    if (d1.verifyUser(userName, passWord)):
        data = {'message': 'Success'}
        response = flask.make_response(jsonify(data))
        print(userName)
        response.set_cookie('userName', userName, expires = datetime.datetime.now() + datetime.timedelta(days = 30), httponly = False, secure = True)
        return response
    else:
        data = {'message': 'Failure'}
        response = flask.make_response(jsonify(data))
        return response
     
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
        bannerPics = []
        resArr = []
        for row in rows:
            animeNames.append(row[0]['value'])
            #new_anime_name = "%20".join(animeNames[animeNames.index(row[0]['value'])].split())
            anilist = Anilist()
            anime_data = anilist.get_anime(row[0]['value'])
            bannerPics.append(anime_data['cover_image'])
        for i in range(len(animeNames)):
            resArr.append(animeNames[i])
            resArr.append(bannerPics[i])
        return resArr
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

@app.route('/getEpisodeRecord', methods = ["GET"])
def getEpisodeRecord():
    d1 = Database()
    userName = request.form.get("userName")
    show = request.form.get("show")
    episodeNum = request.form.get("episodeNum")
    try:
        rows = d1.getEpisodeRecord(userName, show, episodeNum)
        return str(rows)
        # episodes = []
        # for row in rows:
        #     episodes.append(row[0]['value'])
        # return episodes
    except Exception as e:
        return e

@app.route('/getCookie', methods = ["GET"])
def getCookie():
    userName = request.cookies.get('userName')
    print(userName)
    if(userName):
        data = {'userName': str(userName)}
        response = flask.make_response(jsonify(data))
        return response
    else:
        data = {'userName': "No username"}
        response = flask.make_response(jsonify(data))
        return response

@app.route('/getDownloadOptions', methods = ["GET"])
def getDownloadOptions():
    userName = request.form.get("userName")
    show = request.form.get("show")
    d1 = downloader(userName)
    try:
        rows = d1.getDownloadOptions(show)
        return rows
        # episodes = []
        # for row in rows:
        #     episodes.append(row[0]['value'])
        # return episodes
    except Exception as e:
        return e 

if __name__ == "__main__":
    app.run(debug=True)