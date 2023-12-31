from flask import Flask, render_template, request, jsonify
import sqlite3, os
from flask import Flask, render_template, jsonify, request, session, redirect, g
import sqlite3
import os
import threading
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template,session, request, jsonify, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import calendar
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'yourkey'
# I tuoi dati di esempio
event_data = [
    ('2023-1-07', '8 JAN ', 'admin'),
    ('2023-1-29', '29 evt', 'admin'),
    ('2023-1-09', '10 jnnn ', 'admin'),
    ('2023-1-22', '22 rtrik', 'admin'),
    ('2023-1-26', '26   jennu ', 'admin')
]
app.secret_key = "your_secret_key"

# SMTP email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "kebab2803"       #"colxitvygbmnchou
SMTP_PASSWORD = "colxitvygbmnchou"#"eeazzvwbyctfvpkr"
SENDER_EMAIL = "kebab2803@gmail.com"

# SQLite database setup
DATABASE = "Nusers.db"
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
def register_user(email, password,username):
    db = get_database_connection()
    print("73 sono in register_user")
    cursor = db.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is not None:
        return False
    db.execute("INSERT INTO users (email, password,username) VALUES (?, ?,?)", (email, password,username))
    db.commit()
    return True
from PIL import Image

# Crea un'immagine vuota
favicon = Image.new('RGB', (32, 32), color = 'red')  # Sostituisci con i tuoi dettagli

# Salva l'immagine come favicon.ico
favicon.save('favicon.ico')

def send_registration_email(email):
    print(" line 82 send mail ")
    msg = MIMEText("Thank you for registering!")
    msg["Subject"] = "Registration Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))
        print("SMTP debug response:", server.get_debuglevel())

@app.route('/Oldregister', methods=['GET', 'POST'])
def Oldregister():
    if request.method == 'POST':
        # Ottieni i dati dal form di registrazione
        username = request.form['username']
        # Esegui la logica di registrazione, ad esempio, salva l'utente in un database
        # Dopo la registrazione, reindirizza all'accesso o dove necessario

    # Renderizza il form di registrazione
    return render_template('register.html')
def login_user(email, password):
    db = get_database_connection()

    print(f"email: {email}")
    print(f"password: {password}")
    cursor = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    dati =cursor.fetchone()
    print("line 114 dati : ")
    print(dati)

    usernameY=dati[3]
    print("line 118 username ", usernameY)
    print(type(dati))
    if usernameY is not None:
        return usernameY
    #return usernameY is not None
    #return cursor.fetchone() is not None
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottieni i dati dal form di accesso
        username = request.form['username']
        print("usernameu",username)
        print("----------------trying-----------------------")
        # Esegui la logica di accesso, ad esempio, verifica l'utente nel database
        # Se l'accesso ha successo, salva l'username nella sessione
        #session['username'] = username
        return redirect(url_for('calendar_page',username=username))
    # Renderizza il form di accesso
    #return render_template('login.html')
    print("in get metod")
    return redirect(url_for('calendar_page', username="username"))
def get_database_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT,username TEXT)")
    return db
@app.route('/get_dan', methods=['GET'])
def get_dan():
    print("trying-----------------------")
    #return redirect(url_for('login'))
    return render_template("indexT.html")

@app.route('/logout', methods=['GET'])
def logout():

    # Elimina l'username dalla sessione se presente
    session.pop("email", None)
    print("-------------logout")
    #session.pop('username', None)
    return redirect('login')

@app.route("/register", methods=["GET", "POST"])
def register():
    if "email" in session:
        print(" line 150 if email in session: ")
        return redirect("/<username>")
    print(" line 152  /register th")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form['username']
        print(' 157 line username' )
        print(username)
        if register_user(email, password,username):
            session["email"] = email
            send_registration_email(email)
            return redirect("/<username>")
        else:
            return render_template("Tregister.html", error="Email already registered.")
    return render_template("Tregister.html")
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
    print("sono in getaaEvent------------------------- line 234")
    cursor.execute('SELECT date, event ,username ,colorCode FROM events')
    events = cursor.fetchall()
    print("events :-- ",events)

    # Se viene effettuata una richiesta GET, restituisce i dati nel formato richiesto
    if request.method == 'GET':
        #return jsonify(events=event_data)
        return jsonify(evenWts=events)
@app.route("/", methods=["GET", "POST"])
def home():
    # viene  eseguito se sono logged in
    if "email" in session:
        print("sonin  -------------- home----------")
        return redirect("/admin")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("232  password ")
        print(password)
        username = login_user(email, password)
        print("line 242 username ", username)
        if username:
        #if login_user(email, password):

            session["email"] = email
            print("226 sono in lgo ")
            return redirect("/"+username)
            #return redirect("/"+email)
        else:
            return render_template("indexT.html", error="Invalid email or password.")
    return render_template("indexT.html")

#  @app.route('/', methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
def calendar_page(username=None):
#    if "email" not in session:
 #       return redirect("/")
    print("sono  nel /<username> def calendar_pag  funton line ------username---262")
    print("263 favicon.ico   se non esite un usename=",username)
    if request.method == 'GET':
        dta = request.url
        #print("dta:= ",dta.keys())
        print("dta:= ",dta )
        #id = current_user.id
        #print("269-  id ",id)
        # Qui renderai la pagina con il calendario
        # Potresti usare una libreria come FullCalendar.js per visualizzare il calendario
        #return render_template('index.html')
        #return render_template('ktry.html',username=username)
        #return render_template('calen1.html',username=username)

        return render_template('niceg.html',username=username)
        #return render_template('indexT.html',username=username)

    elif request.method == 'POST':
        print("sono in post metoh")
        # Qui gestirai l'aggiornamento del calendario quando viene premuto il bottone "Aggiorna"
        # Dovrai ottenere la data selezionata e aggiornare il calendario
        selected_date = request.form['selected_date']
        # Esegui le operazioni necessarie per aggiornare il calendario con la data selezionata
        # Potresti aggiornare il calendario utilizzando JavaScript o Flask, a seconda della tua implementazione
        return render_template('calendar.html', selected_date=selected_date)


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
    return jsonify(result="ok")
    #return redirect(url_for('calendar_page', month=int(month), year=int(year), username=username))
mode = "dev"

if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', port=50150, debug=True)
    else:
        serve(app, host='0.0.0.0', port=50100, threads=1)
