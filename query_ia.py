import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute('SELECT name, theme, location, start_date, end_date, description FROM ConferenceApp_conference WHERE theme LIKE ?', ('%IA%',))
row = c.fetchone()

if row:
    print(f'Name: {row[0]}')
    print(f'Theme: {row[1]}')
    print(f'Location: {row[2]}')
    print(f'Dates: {row[3]} to {row[4]}')
    print(f'Description: {row[5]}')
else:
    print('No IA conference found')

conn.close()
