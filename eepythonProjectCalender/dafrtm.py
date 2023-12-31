from datetime import datetime
import sqlite3
# Data originale
data_originale = '2023-01-12'

# Converti la stringa in un oggetto datetime
data = datetime.strptime(data_originale, '%Y-%m-%d')
print("nuova_data:-",data)
# Costruisci la nuova stringa senza lo zero iniziale per il mese
nuova_data = data.strftime('%m')

print("nuova_data:-",nuova_data)
anno = data.year
mese = data.strftime('%m')  # Ottieni l'abbreviazione del mese
giorno = str(data.day)  # Ottieni il giorno come stringa senza zero iniziale se presente
meset=mese.strip('0')
print( "meset",meset)
print( "anno",anno)
print( "mese",mese)
# Costruisci la nuova data senza lo zero iniziale per il giorno
nuova_datay = f"{anno}-{meset}-{giorno}  "

print(nuova_datay)

conn = sqlite3.connect('events.db')
#conn = sqlite3.connect(r'C:\Users\Sharif\PycharmProjects\pythonProjectCalender\events.db')
cursor = conn.cursor()


year, month, giornot = data_originale.split('-')

meset = month.strip('0')
print("meset", meset)
print("anno", year)
print("giornot", giornot)
# Costruisci la nuova data senza lo zero iniziale per il giorno
nuova_datay = f"{year}-{meset}-{giornot}  "

print("nuova_datay:-", nuova_datay)
userIdy='admin'
# print("event_data", event_data)
# Insert event into the database
cursor.execute("DELETE FROM events WHERE date = ? AND username = ?", (nuova_datay, userIdy))
conn.commit()
print("userIdy ", userIdy)
# Get the month and year from the date
cursor.execute('SELECT date, event FROM events')
events = cursor.fetchall()
print("event_data  fetchall",events)