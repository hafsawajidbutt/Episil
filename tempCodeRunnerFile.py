@app.route('/verifyUser', methods = ["POST"])
def verifyUser():
    print("In verify user")
    d1 = Database()
    userName = request.form.get("userName")
    passWord = request.form.get("passWord")
    if (d1.verifyUser(userName, passWord)):
        resp = flask.make_response()
        letters = string.ascii_letters
        key = ' '.join(random.choice(letters) for i in range(5))
        resp.set_cookie(key, userName)
        #return flask.render_template("homePage.html")
        return "Let them in"
    else:
        return "Dont let them in"
        #return flask.render_template("login.html", error_message = "Invalid credentials")
