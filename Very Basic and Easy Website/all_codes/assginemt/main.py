from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L1F4Q8z\xec]/' #It is necessary to hide the session.

@app.route("/")
@app.route("/home") # If we are at the home route we first connect to the database.
def index():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT cname FROM Category") # Got cname from the category.
    category_list = c.fetchall()
    conn.close()

    return render_template("home.html", category_list=category_list)

@app.route("/register") #If the user selects register we are going to the register page.
def registration():
    return render_template("registration.html")

@app.post("/applyregister") # If the user registers in the registration page. It comes here.
def applyRegister():
    username = request.form.get("username")
    pwd = request.form.get("pwd")
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    telno = request.form.get("telno") # In this function up to here, we get the entered fields from the register.html
    # We validated if correct password is entered. If there is no trouble we are inserting it into our  database.
    error = validate(username, pwd, fullname, email, telno)
    if error: #Went back to the registration page with an error in case of an error(Wrong password type).
        return render_template("registration.html", error = error)
    else:
        return render_template("registerConfirmation.html")


def validate(username, pwd, fullname, email, telno):
    if upperCaseChecker(pwd) == 0:
        return "Password must include at least one upper case letter."
    if lowerCaseChecker(pwd) == 0:
        return "Password must include at least one lower case letter."
    if digitChecker(pwd) == 0:
        return "Password must include at least one digit."
    if specialSymbolChecker(pwd) == 0:
        return "Password must include at least [+, !, *, -] one of these symbols."
    if len(pwd) < 10:
        return "Password is too short! Password's length must be at least 10 characters."
    # At first, we checked the password. If the password is okay we inserted the entered information
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()
    c.execute("SELECT username FROM User WHERE username = ?", (username,))

    if(c.fetchone() != None): #Username is primary key. Therefore, it can't have a duplicate.
        conn.close()
        return "This username is taken!"
    else:
        c.execute("INSERT INTO User VALUES (?,?,?,?,?)", (username, pwd, fullname, email, telno))
        conn.commit()
        conn.close()

    return None


def specialSymbolChecker(pwd):  # This function checks the existence and the number of special characters.
    specialSymbolCounter = 0
    for char in pwd:
        if (char == "+") or (char == "!") or (char == "*") or (char == "-"):
            specialSymbolCounter += 1
        if specialSymbolCounter == 1:
            return specialSymbolCounter
    return 0


def upperCaseChecker(pwd):  # This function checks the existence and the number of upper case numbers.
    upperCaseCounter = 0
    for char in pwd:
        if char.isupper():
            upperCaseCounter += 1
        if upperCaseCounter == 1:
            return upperCaseCounter
    return 0


def lowerCaseChecker(pwd):  # This function checks the existance and the number of lower case numbers.
    lowerCaseCounter = 0
    for char in pwd:
        if char.islower():
            lowerCaseCounter += 1
        if lowerCaseCounter == 1:
            return lowerCaseCounter
    return 0


def digitChecker(pwd):  # This function checks the number of digits.
    digitCounter = 0
    for char in pwd:
        if char.isdigit():
            digitCounter += 1
        if digitCounter == 1:
            return digitCounter
    return 0


@app.route("/applylogin", methods=["GET", "POST"])  # If the user presses the applylogin in the home.html we come here
def applylogin():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")

        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()

        c.execute("SELECT * FROM USER WHERE username = ? AND password = ?", (username, pwd))
        if (c.fetchone() == None): #If our code wasn't able to get any result it gives and error.
            return render_template("home.html", error = "Invalid username or password!")
            return render_template("home.html", error = "Invalid username or password!")
        session["username"] = username
        return  render_template("home.html", showMenu=True)
    else:
        return  render_template("home.html", showMenu=True)


@app.route("/logout") #If the user decides to logout
def logoutoperation():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.get("/myadvertisements") # We basically got the advertisement for the current user here.
def myadvertisements():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT cname FROM Category")
    category_list = c.fetchall()

    c.execute("SELECT a.aid, a.title,a.description,c.cname,a.isactive FROM ADVERTISEMENT a, Category c WHERE a.cid = c.cid AND a.username = ?", (session["username"],))
    advertisement_list = c.fetchall()

    conn.close()
    return render_template("myadvertisements.html", category_list = category_list, advertisement_list = advertisement_list)


@app.post("/addAdvertisement")  # If add advertisement is selected we reached here.
def addAdvertisement():
    conn = sqlite3.connect("mydb.db")  # We connected to the mydb.db.
    c = conn.cursor()

    title = request.form.get("title")  # Got the title
    desc = request.form.get("desc")  # Got the description
    selected_category = request.form.get("category")  # Got the category.

    c.execute("SELECT cid FROM Category WHERE cname = ? ", (selected_category,)) #We selected the id here.
    cid = c.fetchone()
    #And inserted into our advertisements.
    c.execute("INSERT INTO ADVERTISEMENT (title, description, isactive, username, cid) VALUES (?, ?, ?, ?, ?)",(title, desc, 1, session["username"], cid[0]))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))

@app.get("/deactivate")
def deactivate():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    aid = request.args.get("aid")
    print(aid)

    c.execute("UPDATE ADVERTISEMENT SET isactive = 0 WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))


@app.get("/activate")  # If the user decides to activate his/her advertisement, our code comes here.
def activate():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    aid = request.args.get("aid")

    c.execute("UPDATE ADVERTISEMENT SET isactive = 1 WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))

@app.route("/myprofile")
def myprofile():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT * FROM USER WHERE username = ?", (session["username"],))
    user_details = c.fetchone()

    conn.close()

    return render_template("myprofile.html", user_details = user_details)


@app.post("/editprofile")  # The user decides to edit his/her profile.
def editprofile():
    username = request.form.get("username")
    pwd = request.form.get("password")
    name = request.form.get("fullname")
    email = request.form.get("email")
    telno = request.form.get("telno")
    #Then, we come here, and we get the entered username, password etc.
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT password, fullname, email, telno FROM USER WHERE username = ?", (session["username"],))
    updated_list = c.fetchone()

    user_details = (username, pwd, name, email, telno)

    if session["username"] != username: # Username is updated
        c.execute("SELECT * FROM USER WHERE username = ?", (username,))
        if c.fetchone() == None: # Username can be updated
            c.execute("UPDATE USER SET username=? WHERE username = ?", (username, session["username"]))
            c.execute("UPDATE ADVERTISEMENT SET username=? WHERE username = ?", (username, session["username"]))
            conn.commit()
            conn.close()
            session["username"] = username
            return render_template("myprofile.html", user_details=user_details, error = "Username is updated!")
        else: # If the username provided is not unique
            conn.close()
            return render_template("myprofile.html", user_details=user_details, error = "This username is already taken!")
    # What we do is we basically update the selected fields.
    if updated_list[0] != pwd: # Password has been updated
        c.execute("UPDATE USER SET password=? WHERE username = ?", (pwd, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Password is updated!")
    if updated_list[1] != name: # Name has been updated
        c.execute("UPDATE USER SET fullname=? WHERE username = ?", (name, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Fullname is updated!")
    if updated_list[2] != email:  # Email has been updated
        c.execute("UPDATE USER SET email=? WHERE username = ?", (email, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Email is updated!")
    if updated_list[3] != telno:  # Telno has been updated
        c.execute("UPDATE USER SET telno=? WHERE username = ?", (telno, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Telno is updated!")
    else:
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="No update has been occured!")

@app.post("/searchadvertisement")
def searchadvertisement():
    keywords = request.form.get("keywords")
    cname = request.form.get("category")

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    if cname != "all":
        c.execute("""
                  SELECT a.title, a.description, u.fullname, a.aid 
                  FROM Category c, ADVERTISEMENT a, USER u 
                  WHERE c.cid = a.cid  AND a.username = u.username AND 
                  a.isactive = 1 AND c.cname = ? AND 
                  (a.title LIKE ? OR a.description LIKE ? OR u.fullname LIKE ?)
                  """, (cname, f"%{keywords}%", f"%{keywords}%", f"%{keywords}%"))
        searchList = c.fetchall()
        conn.close()
        return render_template("searchadvertisement.html", searchList=searchList, cname=cname)

    else:
        c.execute("""
               SELECT a.title, a.description, u.fullname, a.aid 
               FROM Category c, ADVERTISEMENT a, USER u 
               WHERE c.cid = a.cid AND a.username = u.username AND a.isactive = 1 
               AND (a.title LIKE ? OR a.description LIKE ? OR u.fullname LIKE ?)
           """, (f"%{keywords}%", f"%{keywords}%", f"%{keywords}%"))
        searchList = c.fetchall()
        conn.close()
        return render_template("searchadvertisement.html", searchList=searchList, cname=cname)

@app.route("/seeadvertisement", methods=["GET"])
def seeadvertisement():
    aid = request.args.get("aid")

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()
    c.execute("""
        SELECT a.title, a.description, c.cname, u.fullname, u.email, u.telno
        FROM ADVERTISEMENT a, Category c, USER u
        WHERE a.cid = c.cid AND a.username = u.username AND
        a.aid = ?        
        """, (aid,))
    advertisement = c.fetchone()

    conn.close()

    return render_template("seeadvertisement.html", advertisement=advertisement)


if __name__ == "__main__":
    app.run(debug=True)