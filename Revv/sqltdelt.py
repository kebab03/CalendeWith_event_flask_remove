import sqlite3
conn = sqlite3.connect('events.db')
cursor = conn.cursor()
data_originale = '2023-12-04'

year, month, giornot = data_originale.split('-')
meset = month.strip('0')
nuova_datay = f"{year}-{meset}-{giornot}"
print("nuova_datay:-", nuova_datay)
'''
cursor.execute("DELETE FROM events WHERE date= '2023-1-12' AND username = 'admin'")
#cursor.execute("DELETE FROM events WHERE date= '2023-12-28' AND username = 'sharif'")
conn.commit()'''
#userIdy="sahrif"
userIdy = 'admin'
cursor.execute("DELETE FROM events WHERE date = ? AND username = ?", (nuova_datay, userIdy))
conn.commit()