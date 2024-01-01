from waitress import serve
import sqlite3, os
from flask import Flask, render_template, request, jsonify, redirect, url_for
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
        username TEXT
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
    if request.method == 'POST':
        # Ottieni i dati dal form di registrazione
        username = request.form['username']
        # Esegui la logica di registrazione, ad esempio, salva l'utente in un database
        # Dopo la registrazione, reindirizza all'accesso o dove necessario

    # Renderizza il form di registrazione
    return render_template('register.html')

'''
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = "12345"#request.form['password']
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(r'select * from user where username=?', (username,))
    except IndexError as e:
        print(e, 'user not found')
        return render_template('form.html', message='Invaild username', username=username)
    finally:
        value = cursor.fetchall()
        print(value)
        try:
            if value[0][2] == hmac_sha256(value[0][1], password):
                # return render_template('accessed.html', username=username)
                print("sono  nel   line ----------------------------------------------77")
                return redirect(url_for('calendar_page', month=int(5), year=int(2022),
                                        username=username))  ### questi sono mostrati nel link
        except IndexError as e:
            print(e, 'user not found')
            return render_template('form.html', message='Invalid username or password', username=username)
    return render_template('form.html', message='Invalid username or password', username=username)


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottieni i dati dal form di accesso
        username = request.form['username']
        print("usernameu",username)
        # Esegui la logica di accesso, ad esempio, verifica l'utente nel database
        # Se l'accesso ha successo, salva l'username nella sessione
        #session['username'] = username
        return redirect(url_for('calendar_page',username=username))

    # Renderizza il form di accesso
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Elimina l'username dalla sessione se presente
    session.pop('username', None)
    return redirect(url_for('calendar_page'))


@app.route('/getallevents', methods=['GET'])
def get_events():

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("sono in getaaEvent------------------------- line 234")
    cursor.execute('SELECT date, event ,username FROM events')
    events = cursor.fetchall()

    # Se viene effettuata una richiesta GET, restituisce i dati nel formato richiesto
    if request.method == 'GET':
        #return jsonify(events=event_data)
        return jsonify(evenWts=events)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
def calendar_page(username=None):
    print("sono  nel index funton line ------username---133")
    print(username)
    if request.method == 'GET':
        # Qui renderai la pagina con il calendario
        # Potresti usare una libreria come FullCalendar.js per visualizzare il calendario
        #return render_template('index.html')
        return render_template('ktry.html',username=username)

    elif request.method == 'POST':
        print("sono in post metoh")
        # Qui gestirai l'aggiornamento del calendario quando viene premuto il bottone "Aggiorna"
        # Dovrai ottenere la data selezionata e aggiornare il calendario
        selected_date = request.form['selected_date']
        # Esegui le operazioni necessarie per aggiornare il calendario con la data selezionata
        # Potresti aggiornare il calendario utilizzando JavaScript o Flask, a seconda della tua implementazione
        #return render_template('calendar.html', selected_date=selected_date)
        return render_template('AsCorrect.html',username=username)

@app.route('/addevent', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    username = request.form['username']  # Aggiungi questa riga per ottenere l'username
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("line             160   date:", date)
    print("line             161    event:", event)
    print("line .....................162 username :", username)

    # Remove leading zero from the month component
    year, month, day = date.split('-')
    month = str(int(month))

    # Join the date parts back together
    formatted_date = '-'.join([year, month, day])
    print(" line 187 formatted_date::=", formatted_date)
    # Insert event into the database
    cursor.execute('INSERT INTO events (date, event, username) VALUES (?, ?, ?)', (formatted_date, event, username))
    conn.commit()
    print('liNe----------------------- 174 ..........di addevent ')
    # Get the month and year from the date
    year, month, _ = formatted_date.split('-')
    return  jsonify(result="ok")
    #return redirect(url_for('calendar_page', month=int(month), year=int(year), username=username))
if __name__ == '__main__':
    serve(app, host='0.0.0.0',port=80,threads=2)
