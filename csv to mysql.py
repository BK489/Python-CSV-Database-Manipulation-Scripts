import csv, os, mysql.connector #cheeky script to fill a db from csv file
from datetime import datetime

csvfile = "TennisTournamentData.csv" #put csv file in local and change name here

connection = mysql.connector.connect( #mysql settings 
    host="127.0.0.1",
    user="",
    password="",
    database="adv-db"
)

here = os.path.dirname(os.path.abspath(__file__)) #path sorting code
goodpath = os.path.join(here, csvfile)
rows = []

with open(goodpath, "r") as file: #fill rows from cv
    reader=csv.reader(file)
    for row in reader:
        rows.append(row)
file.close()

def properdate(datey):  #date formatting
    return datetime.strptime(datey, "%d/%m/%Y").strftime("%Y-%m-%d")

def fillatable(top, bottom, lefty, righty, table): #function fill table from rows
    for i in range(top,bottom):
        listy = []          
        for j in range(lefty,righty):
            try:
                listy.append(properdate(rows[i][j]))
            except:
                try:
                    listy.append((rows[i][j]).replace(',', '')) #500,000 isnt an int gotta take out the ,
                except:
                    listy.append(rows[i][j])
        table.append(listy)

playertable = []                    #make tables
tourntable = []


fillatable(47,56,0,7,playertable)     #fill tables from four corners of area within csv specified by numbers
fillatable(47,67,9,16,tourntable)

cursor = connection.cursor()
iq = """INSERT INTO `player_table`
    (Player_ID, Player_Name, Gender, DoB, Nationality, Hand, Year_Turnt_Pro)
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""  #all %s markers because mysql module handles conversion even if int or date or etc
cursor.executemany(iq, playertable)  

iq = """INSERT INTO `tournament_participation`
    (Participation_ID, Player_Name, Tournament, Year, Position, Prize_Money, Ranking_Points)
    VALUES (%s, %s, %s, %s, %s, %s, %s)""" 
cursor.executemany(iq, tourntable) 

connection.commit()
cursor.close()
connection.close()

