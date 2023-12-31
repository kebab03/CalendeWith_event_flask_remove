import json
from flask import Flask, request, render_template
import sqlite3, os
import hmac, random, re
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import calendar
from datetime import datetime

app = Flask(__name__)


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


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('form.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(r'select * from user where username=?', (username,))
    except IndexError as e:
        print(e,'user not found')
        return render_template('form.html', message='Invaild username', username=username)
    finally:
        value = cursor.fetchall()
        print(value)
        try:
            if value[0][2] == hmac_sha256(value[0][1], password):
                #return render_template('accessed.html', username=username)
                print("sono  nel   line ----------------------------------------------77")
                return redirect(url_for('index', month=int(5), year=int(2022),username=username))### questi sono mostrati nel link 
        except IndexError as e:
            print(e, 'user not found')
            return render_template('form.html', message='Invalid username or password', username=username)
    return render_template('form.html', message='Invalid username or password', username=username)
    
@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)

    # Redirect to the login page
    return redirect(url_for('login'))


@app.route('/')
@app.route('/<int:month>/<int:year>/<username>')
def index(month=None, year=None,username=None):
    print("sono  nel index funton line ------------username-----------96")
    print(username)
    if not month or not year:
        current_date = datetime.now()
        month = current_date.month
        year = current_date.year

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    date = f'{year}-{month:02d}-01'
    #cursor.execute('SELECT date, event FROM events WHERE strftime("%Y-%m", date) = ?', (f'{year}-{month:02d}',))
    cursor.execute('SELECT date, event , username FROM events')
    events = cursor.fetchall()
    print("events     111__----== ",events)
    event_data = {}
    for row in events:
        print("calendar_rows ---------------line 113")
        date = row[0]
        event = row[1]
        uten = row[2]
        print("date     119_--== ",date)
        
        print("events     121--== ",event)
        print("uten     122--== ",uten)
        
        if date in event_data:
            event_data[date].append(event)
            event_data[date].append(uten)
            print("event_data if  ------------line 127",event_data)
        else:
            event_data[date] = [event]
            event_data[date].append(uten)
            print("event_data ---------------line 131",event_data)

    calendar_rows = []
    numDays = calendar.monthrange(year, month)[1]

    dayCounter = 1
    for _ in range(5):
        print("calendar_rows ---------------line 125")
        row = []
        for _ in range(7):
            if dayCounter <= numDays:
                date = f'{year}-{month:02d}-{dayCounter:02d}'
                if date in event_data:
                    print("calendar_rows ---------------line 133")
                    day_data = event_data[date]
                else:
                    day_data = []
                row.append((date, day_data))
                print("calendar_rows ---------------line 138")
                dayCounter += 1
            else:
                row.append(('', []))
        calendar_rows.append(row)
    print("sono  nel index funton line ----------------------------143")
    print("year --------------------------",year)
    print("calendar_rows ---------------line 145------")
    print(calendar_rows)
    
    print("sono  nel index funton line ----------------------------146")
    print("username ---------------line ------142---::",username)
    print("line 152 event_data:::::")
    print(event_data)
    #print(" 173data---------------::", data)
    #print(type(data))

    peventDataVar = [
            ['2023-01-05', '555555', 'admin'],
            ['2023-01-08', '8888', 'sharif']     
        ];
    print(" 161 data---------------::",peventDataVar)
    print(type(peventDataVar))
    print(" 163 event_data---------------::",event_data)
    print(type(event_data))
    formatted_listy=[]
    for key, value in event_data.items():
        
        formatted_listy.append(key)
        formatted_listy.extend(value)
        print("formatted_listy- prima -",formatted_listy)
        print("value:-",value)
        print(len(value))
        pt=value
        print("pt----",pt)
        chunksy = [formatted_listy[i:i + 3] for i in range(0, len(formatted_listy), 3)]
        print("chunksy==--:::::::::==",chunksy) 
        print("formatted_listy--",formatted_listy)
    '''
    formatted_listy=[]
    for key, value in event_data.items():
        formatted_listy.append(key)
        print(value)
        print(len(value))
        pt=value
        yt=pt[0].split(' ', 1)
        print("len(yt)==",len(yt))
        for i in range(len(yt)):
            print("yt[i]===",yt[i])
            formatted_listy.append(yt[i])
            print("i--------",i)
            print("yt" ,yt)
        chunksy = [formatted_listy[i:i + 3] for i in range(0, len(formatted_listy), 3)]
        print("chunksy==--:::::::::==",chunksy)'''
    
    
    #return render_template('index.html', first_name=x) 
    #return render_template('index.html', first_name=event_data)
    #return render_template('index.html', first_name=data)  
    #return render_template('Qaccessed.html',username=username, calendar_rows=calendar_rows,Pevents= event_data)#event_data)
    return render_template('Qaccessed.html',Pusername=username, calendar_rows=calendar_rows,first_name= chunksy)#event_data)
####       username passato 


@app.route('/addevent', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    username = request.form['username']  # Aggiungi questa riga per ottenere l'username

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("line             160   date:",date)
    print("line             161    event:",event)
    print("line .....................162 username :",username)
    
    # Remove leading zero from the month component
    year, month, day = date.split('-')
    month = str(int(month))

    # Join the date parts back together
    formatted_date = '-'.join([year, month, day])
    print(" line 187 formatted_date::=",formatted_date)
    # Insert event into the database
    cursor.execute('INSERT INTO events (date, event, username) VALUES (?, ?, ?)', (formatted_date, event, username))
    conn.commit()
    print('liNe----------------------- 174 ..........di addevent ')
    # Get the month and year from the date
    year, month, _ = formatted_date.split('-')

    return redirect(url_for('index', month=int(month), year=int(year), username=username))

@app.route('/removeevent', methods=['POST'])
def remove_event():
    date = request.form['date']
    userIdy = request.form['userId']
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print(" line 247 _date::=",date)
    print(" line 248 userIdy::=",userIdy)
    # Insert event into the database
   
    print("userIdy " ,userIdy)
    # Get the month and year from the date
    cursor.execute('SELECT date, event FROM events')
    events = cursor.fetchall()


    #return jsonify({'events': event_data})
    year, month, day = date.split('-')
    month = str(int(month))

    # Join the date parts back together
    formatted_date = '-'.join([year, month, day])
    print(" line 187 formatted_date::=",formatted_date)
    # Insert event into the database
    cursor.execute("DELETE FROM events WHERE date = ? AND username = ?", (formatted_date, userIdy))
    conn.commit()
    print('liNe----------------------- 174 ..........di addevent ')
    # Get the month and year from the date
    year, month, _ = formatted_date.split('-')

    #return redirect(url_for('index', month=int(month), year=int(year), username=userIdy))

    
    print("sono in getaaEvent------------------------- line 234")
    cursor.execute('SELECT date, event ,username FROM events')
    events = cursor.fetchall()
    print("event line 256::::             ",events)
    
    return jsonify({'events': events})







@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    sec_password = request.form['sec_password']
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute('select username from user where username=?', (username,))
        if cursor.rowcount == -1:
            print('A User tried a valid username to register!')
    except sqlite3.OperationalError as e:
        print('OperationalError:', e)
    finally:
        values = cursor.fetchall()
    if not values:
        if re.match('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password):
            if sec_password == password:
                enc_user = User(username,password)
                cursor.execute('insert into user(username,key,password) values(?,?,?)', (enc_user.username, enc_user.key, enc_user.password))
                print('New User Registered:', enc_user.username, enc_user.key, enc_user.password)
                cursor.close()
                conn.commit()
                conn.close()
            else:
                return render_template('register.html',message='Sorry,the passwords you input twice are not matched!',username=username)
        else:
            return render_template('register.html', message='Sorry,the password is invalid! At least 6 digits,alphabet and numbers are required!',username=username)
        return render_template('form.html', message='Registered sucessfully!',username=username)
    return render_template('register.html', message='Sorry,the username already exit!')


'''
@app.route('/addevent', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    # Insert event into the database
    cursor.execute('INSERT INTO events (date, event) VALUES (?, ?)', (date, event))
    conn.commit()

    # Get the month and year from the date
    year, month, _ = date.split('-')
    print("date ,  event ", date , event)
    return redirect(url_for('index', month=int(month), year=int(year)))
'''
@app.route('/getallevents', methods=['GET'])
def get_all_events():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    print("sono in getaaEvent------------------------- line 234")
    cursor.execute('SELECT date, event ,username FROM events')
    events = cursor.fetchall()
    print("event line 256::::             ",events)
    event_data = {}
    event_dataT = {}
    for row in events:
        date = row[0]
        event = row[1]
        print("date 261   ", date)
        print("date 263   ", event)
        username= row[2]
        print("username 268 ", username)
        if date in event_data:
            print("event line 263::::             ")#, event_data[date])
            event_data[date].append(event)
            #event_data[date].append(username)
            #event_dataT[date].append(event)
            #event_dataT[date].append(username)
        else:
            print("event line 266::::             ")#, event_data[date])
            event_data[date] = [event]
            #event_dataT[date] = [event]
            #event_dataT[date].append(username)
        print("sono in getaallEvent-------------------------- line 262")
    print("event_data line 269::::             ",event_dataT)
    print("event_data line 326::::             ",event_dataT)
    #return jsonify({'events': event_data})
    return jsonify({'events': events})

if __name__ == '__main__':
    app.run()
