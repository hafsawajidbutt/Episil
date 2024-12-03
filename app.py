import flask
from flask import Flask, request, jsonify
import sqlite3
from database import Database, localStorage
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
    downloadLocation = request.form.get("downloadLocation")
    try:
        if(downloadLocation == ""):
            d1.insertUser(userName, passWord, profilePictureLink, email)
        else:
            d1.insertUser(userName, passWord, profilePictureLink, email, downloadLocation)
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
    ls = localStorage()
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    if (d1.verifyUser(userName, passWord)):
        print(ls.insertData(userName))
        data = {'message': 'Success'}
        response = flask.make_response(jsonify(data))
        #print(userName)
        #response.set_cookie('userName', userName, expires = datetime.datetime.now() + datetime.timedelta(days = 30), httponly = False, secure = True)
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
    print("Username" + userName)
    print("show" + show)
    try:
        d1.insertShow(userName, show)
        print("Inserted")
        data = {'message': 'Success'}
        response = flask.make_response(jsonify(data))
        return response
    except Exception as e:
        print(e)
        data = {'message': 'Failure'}
        response = flask.make_response(jsonify(data))
        return response

@app.route('/getUserShows', methods = ["GET"])
def getShows():
    d1 = Database()
    userName = request.args.get("userName")
    try:
        rows = d1.getUserShows(userName)
        if(rows == "User has no shows"):
            return "User has no shows"
        else:
            animeNames = []
            bannerPics = []
            resArr = []
            for row in rows:
                animeNames.append(row[0]['value'])
                anilist = Anilist()
                anime_data = anilist.get_anime(row[0]['value'])
                bannerPics.append(anime_data['cover_image'])
            for i in range(len(animeNames)):
                resArr.append(animeNames[i])
                resArr.append(bannerPics[i])
            print(resArr)
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
    except Exception as e:
        return e

@app.route('/getUser', methods = ["GET"])
def getUser():
    ls = localStorage()
    userName = ls.extractData()
    if(userName):
        data = {'userName': str(userName)}
        print(data)
        response = flask.make_response(jsonify(data))
        return response
    else:
        data = {'userName': "No username"}
        print(data)
        response = flask.make_response(jsonify(data))
        return response

@app.route('/getDownloadOptions', methods = ["GET"])
def getDownloadOptions():
    userName = request.args.get("userName")
    show = request.args.get("show")
    print("Username: " + userName)
    print("Show: "+ show)
    d1 = downloader(userName)
    try:
        rows = d1.getDownloadOptions(show)
        return rows
    except Exception as e:
        return e

@app.route('/download', methods = ["POST"])
def download():
    print("In download")
    userName = request.form.get("userName")
    show = request.form.get("show")
    print(userName)
    print(show)
    d1 = downloader(userName)
    try:
        print("In try")
        d1.download(show)
        data = {'message': "Success"}
        response = flask.make_response(jsonify(data))
        return response
    except Exception as e:
        print(e)
        data = {'message': "Failure"}
        response = flask.make_response(jsonify(data))
        return response

@app.route('/changeUserName', methods = ["POST"])
def changeUserName():
    userName = request.form.get("userName")
    newUserName = request.form.get("newUserName")
    print("Username: " + str(userName))
    print("New Username: "+ str(newUserName))
    d1 = Database()
    try:
        rows = d1.changeUserName(userName, newUserName)
        return rows
    except Exception as e:
        return e

@app.route('/changeProfilePicture', methods = ["POST"])
def changeProfilePicture():
    userName = request.form.get("userName")
    profilePictureLink = request.form.get("profilePictureLink")
    print("Username: " + userName)
    print("Profile Picture Link: "+ profilePictureLink)
    d1 = Database()
    try:
        rows = d1.changeProfilePictureLink(userName, profilePictureLink)
        return rows
    except Exception as e:
        return e
    
@app.route("/removeShow", methods = ["POST"])
def removeShow():
    userName = request.form.get("userName")
    show = request.form.get("show")
    print("Username: " + userName)
    print("Show: "+ show)
    d1 = Database()
    try:
        rows = d1.removeShow(userName, show)
        return rows
    except Exception as e:
        return e

@app.route('/getUserDownloadDirectory', methods = ["GET"])
def getUserDownloadDirectory():
    userName = request.args.get("userName")
    print("Username: " + userName)
    d1 = Database()
    try:
        rows = d1.getUserDownloadDirectory(userName)
        return rows["results"][0]["response"]["result"]["rows"][0][0]["value"]
    except Exception as e:
        return e

          
@app.route('/logOut', methods = ["POST"])
def logOut():
    ls = localStorage()
    try:
        ls.deleteData()
        data = {'message' : 'Successful logout'}
        response = flask.make_response(jsonify(data))       
        return response
    except Exception as e:
        print(e)
        data = {'message' : 'Failed logout'}
        response = flask.make_response(jsonify(data))       
        return response
        
if __name__ == "__main__":
    app.run(debug=True)