from flask import Flask, render_template, request, jsonify
import sqlite3, os

from flask import Flask, render_template, request, jsonify, redirect, url_for,session, g

import calendar
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "your_secret_key"

# SMTP email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "kebab2803"       #"colxitvygbmnchou
SMTP_PASSWORD = "colxitvygbmnchou"#"eeazzvwbyctfvpkr"
SENDER_EMAIL = "kebab2803@gmail.com"

def hmac_sha256(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'sha256').hexdigest()

conn = sqlite3.connect('events.db')
cursor = conn.cursor()

# Create events table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        event TEXT,
        username TEXT,
        colorCode TEXT
    )
''')

conn.commit()
class User(object):

    def __init__(self, username, password):
        self.username = username
        self.key = str([random.randint(48, 122) for x in range(20)])
        self.password = hmac_sha256(self.key, password)
# create database
db = os.path.join(os.path.dirname('__file__'), 'test.db')
if not os.path.isfile(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('create table user(username varchar(20), key varchar(10000), password varchar(10000))')
    #admin user
    admin = User('admin','12345')
    print('admin info:',admin.key,admin.password)
    cursor.execute(r"insert into user(username,key,password) values(?,?,?)",(admin.username,admin.key, admin.password))
    cursor.close()
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "email" in session:
        print(" redirect /calendar_page)  perche  if email in session  ")
        return redirect("/calendar_page")
    if request.method == 'POST':
        # Ottieni i dati dal form di registrazione
        username = request.form['username']
        email = request.form["email"]
        password = request.form["password"]
        print(f" line 63 password: {password}")
        print(f" line 64 username: {username}")
        print("sono in register con POST  ")
        if register_user(email, password, username):
            session["email"] = email
            send_registration_email(email)
            return redirect("calendar_page")
        else:
            return redirect(url_for('calendar_page'))  ############################ devo mettere  username
        # Esegui la logica di registrazione, ad esempio, salva l'utente in un database
        # Dopo la registrazione, reindirizza all'accesso o dove necessario
    print("sono in register con GET method ")
    # Renderizza il form di registrazione
    return render_template('Tregister.html')

def register_user(email, password,utente):
    db = get_database_connection()
    cursor = db.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is not None:
        return False
    db.execute("INSERT INTO users (email, password,username) VALUES (?, ?, ?)", (email, password, utente))
    db.commit()
    return True

def send_registration_email(email):
    msg = MIMEText("Thank you for registering!")
    msg["Subject"] = "Registration Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    print("line 106 sono in send_registration_email ")
    try:
        print("line 108 sono in send_registration_email  try ")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("117 Error sending email:", str(e))
        print("SMTP debug response:", server.get_debuglevel())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottieni i dati dal form di accesso
        username = request.form['username']
        print(" 73 usernameu",username)
        # Esegui la logica di accesso, ad esempio, verifica l'utente nel database
        # Se l'accesso ha successo, salva l'username nella sessione
        #session['username'] = username
        return redirect(url_for('calendar_page',username=username))
    # Renderizza il form di accesso
    print("sono in /login con get  verra indrizzato al root /ver ")
    return render_template('loginPage.html')
    #return render_template('login.html')

@app.route('/logout')
def logout():
    print("--line 91-----------logout------------")
    # Elimina l'username dalla sessione se presente
    #session.pop('username', None)
    session.pop("email", None)

    # da EmailRegit
    #return redirect(url_for('calendar_page'))
    return redirect(url_for('login')) # qui dentro trovi la funzione che verra eseguito

@app.route('/removeevent', methods=['POST'])
def remove_event():
    date = request.form['date']
    userIdy = request.form['userId']
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("date", date)

    year, month, giornot = date.split('-')

    meset = month.strip('0')
    print("97-meset", meset)
    print("98-anno", year)
    print("99-giornot", giornot)
    # Costruisci la nuova data senza lo zero iniziale per il giorno
    nuova_datay = f"{year}-{meset}-{giornot}"

    print("103-nuova_datay:-",nuova_datay)

    userIdyp="sahrif"
    #print("event_data", event_data)
    # Insert event into the database
    cursor.execute("DELETE FROM events WHERE date = ? AND username = ?", (nuova_datay, userIdy))
    conn.commit()
    #print("110 userIdy ",userIdyp)
    print("110 userIdy ",userIdy)
    # Get the month and year from the date
    cursor.execute('SELECT date, event FROM events')
    events = cursor.fetchall()

    event_data = {}
    for row in events:
        date = row[0]
        event = row[1]
        if date in event_data:
            event_data[date].append(event)
        else:
            event_data[date] = [event]
    print("event_data  fetchall",event_data)
    return jsonify({'events': event_data})

@app.route('/getallevents', methods=['GET'])
def get_events():

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("sono in getaaEvent------------------------- line 185")
    cursor.execute('SELECT date, event ,username ,colorCode FROM events')
    events = cursor.fetchall()
    print("events :-- ",events)

    # Se viene effettuata una richiesta GET, restituisce i dati nel formato richiesto
    if request.method == 'GET':
        #return jsonify(events=event_data)
        return jsonify(evenWts=events)
@app.route("/verloging", methods=["GET", "POST"])
def loging():
 # viene da EmailREgit progect
    #if "email" in session:
    #    return redirect("/")############################ devo mettere  username
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(f" line 163 email: {email}")
        print(f"line 164 password: {password}")
        print(" 165 verra indrizzato al / o /username  root  se supera verifica di loging")
        if login_user(email, password):
            nameY = login_user(email, password)
            session["email"] = email
            print(" line 168 sono logged in  ")
            #return redirect("/")############################ devo mettere  username
            return redirect(url_for('calendar_page',username=nameY))############################ devo mettere  username

        else:
            return render_template("loginPage.html", error="Invalid email or password.")
    print("index 50")
    return render_template("loginPage.html")


@app.route('/', methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
def calendar_page(username=None):
    if "email" not in session:
        print("sono  nel index funton line ------username---220 /loging")
        #print(username)
        #return redirect("/loging")
        #return redirect("/loging")
        return redirect("/verloging")                 ## funziona
        #return redirect(url_for("loging"))           ## funziona
    print("sono  nel /<username> def calendar_pag  funton line ------username---262")
    print("263 favicon.ico   se non esite un usename=",username)
    if username is None:
        print("sono  nel index funton line ------username---227")
        print(username)
        #return redirect("loging")        # non funziona
        # return redirect(url_for("loging"))      non so perche non va e dice troppi redirect
        return render_template("loginPage.html")
        #return redirect("/verloging")

    else:
        if request.method == 'GET':
            print( "line 183 in / root  con GET")
            print("username:-- ",username)
        # Qui renderai la pagina con il calendario
        # Potresti usare una libreria come FullCalendar.js per visualizzare il calendario
        #return render_template('index.html')
        #return render_template('ktry.html',username=username)
        #return render_template('calen1.html',username=username)
            return render_template('niceg.html',username=username)

        elif request.method == 'POST':
            print(" 239 sono in post metoh")
        # Qui gestirai l'aggiornamento del calendario quando viene premuto il bottone "Aggiorna"
        # Dovrai ottenere la data selezionata e aggiornare il calendario
            selected_date = request.form['selected_date']
        # Esegui le operazioni necessarie per aggiornare il calendario con la data selezionata
        # Potresti aggiornare il calendario utilizzando JavaScript o Flask, a seconda della tua implementazione
            return render_template('calendar.html', selected_date=selected_date)
DATABASE = "Nusers.db"
def get_database_connection():
    db = getattr(g, "_database", None)
    print("sono get_database_connection   line 196 ")
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)")
    return db

def login_user(email, password):
    db = get_database_connection()

    print(f" 204 email: {email}")
    print(f" 205 password: {password}")
    cursor = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    dati =cursor.fetchone()
    print("line 114 dati : ")
    print(dati)

    usernameY = dati[3]
    if usernameY is not None:

        print("line 118 username =", usernameY)
        print(type(dati))
        return usernameY

@app.route('/Baddevent', methods=['POST'])
def Badd_event():
    date = request.form['date']
    event = request.form['event']
    username = request.form['username']  # Aggiungi questa riga per ottenere l'username
    colorCod =request.form['colorCode']
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("line             160   date:", date)
    print("line             161    event:", event)
    print("line .....................162 username :", username)
    print("line             178    colorCod:", colorCod)


    # Remove leading zero from the month component
    year, month, day = date.split('-')
    month = str(int(month))

    # Join the date parts back together
    formatted_date = '-'.join([year, month, day])
    print(" line 303 formatted_date::=", formatted_date)
    # Insert event into the database
    cursor.execute('INSERT INTO events (date, event, username,colorCode) VALUES (?, ?, ?,?)', (formatted_date, event, username,colorCod))
    conn.commit()
    print('liNe----------------------- 174 ..........di addevent ')
    # Get the month and year from the date
    year, month, _ = formatted_date.split('-')
    return  jsonify(result="ok")
@app.route('/addevent', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    username = request.form['username']  # Aggiungi questa riga per ottenere l'username
    colorCod =request.form['colorCode']
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("line             160   date:", date)
    print("line             161    event:", event)
    print("line .....................162 username :", username)
    print("line             178    colorCod:", colorCod)

    # Remove leading zero from the month component
    year, month, day = date.split('-')
    month = str(int(month))

    # Join the date parts back together
    formatted_date = '-'.join([year, month, day])
    print(" line 187 formatted_date::=", formatted_date)
    # Insert event into the database
    cursor.execute('INSERT INTO events (date, event, username,colorCode) VALUES (?, ?, ?,?)', (formatted_date, event, username,colorCod))
    conn.commit()
    print('liNe----------------------- 174 ..........di addevent ')
    # Get the month and year from the date
    year, month, _ = formatted_date.split('-')
    return  jsonify(result="ok")
    #return redirect(url_for('calendar_page', month=int(month), year=int(year), username=username))

mode = "dev"
if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', port=50150, debug=True)
    else:
        serve(app, host='0.0.0.0', port=50100, threads=1)