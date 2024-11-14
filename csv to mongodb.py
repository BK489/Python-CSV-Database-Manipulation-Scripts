import csv, os #cheeky script to fill a -MONGO- db from csv file@
from datetime import datetime
from pymongo import MongoClient
from bson import BSON
from bson.objectid import ObjectId


csvfile = "TennisTournamentData.csv" #put csv file in local and change name here

here = os.path.dirname(os.path.abspath(__file__)) #path sorting code
goodpath = os.path.join(here, csvfile)
rows = []

with open(goodpath, "r") as file: #fill rows from cv
    reader=csv.reader(file)
    for row in reader:
        rows.append(row)
file.close()

def properdate(datey): #date formating
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

fillatable(47,56,0,7,playertable)     #fill tables taking input of fourcorners of area within csv file
fillatable(47,67,9,16,tourntable)

client = MongoClient("mongodb://localhost:27017/") #classic localhost and standard port for mongoDB
db = client["adv-db"]

players_collection = db["player_table"]
participation_collection =db["tournament_participation"]

for player in playertable:
    properplayer = {
        "Player_ID": player[0],
        "Player_Name": player[1],
        "Gender": player[2],
        "DoB": player[3],
        "Nationality": player[4],
        "Hand": player[5],
        "Year_Turnt_Pro": int(player[6]),
    }
    players_collection.insert_one(properplayer)

for participation in tourntable:
    properparticipant ={
        "Participation_ID": participation[0],
        "Player_Name": participation[1],
        "Tournament": participation[2],
        "Year": int(participation[3]),
        "Position": int(participation[4]),
        "Prize_Money": int(participation[5]),
        "Ranking_Points": int(participation[6]),
    }
    participation_collection.insert_one(properparticipant)
