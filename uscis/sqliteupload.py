# bulk upload csv into sqlite file using python

import csv
import sqlite3

#create sqlite connection in memory and a cursor object

con = sqlite3.connect("immigration.db")
cur = con.cursor()

#create a table to load in the data with reciept number as primary key

cur.execute('''CREATE TABLE casestatus 
                (downloaded text, recipt text PRIMARY KEY, heading text, detail text)''')

#open the csv file and then insert the value in to table create above
with open("uscis_status.csv", "r") as readfile:
    dictreader = csv.DictReader(readfile)
    to_db = [(row['downloaded'], row['receipt'], row['heading'], row['detail']) \
        for row in dictreader ]
# execute insert commands and then commit the change into database

cur.executemany('INSERT INTO casestatus VALUES (?,?,?,?)',
        to_db)
con.commit()
con.close()