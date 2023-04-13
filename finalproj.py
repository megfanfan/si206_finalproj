import unittest
import requests
import sqlite3
import json
import os
import matplotlib.pyplot as plt

#Megan Fan, Katelyn Ma, Sabrina Yu :)

#NOTES FOR US TO LOOK AT LATER !!!!!!!!!!
    #useful SQL commands:
    #SELECT MAX(col) FROM table
    #SELECT COUNT(col) FROM table
    #SELECT AVG(col) FROM table
    #SELECT SUM(col) FROM table
    
    #sys.exit()
        #ends the program
        
#part 2: gathering data

# database function
def setUpdatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# load json
def load_json(filename):
    try:
        file = open(filename, 'r')
        contents = file.read()
        data = json.loads(contents)
        file.close()
        return data
    except:
        return {}

#write json cache
def write_json(filename, dict):
    json_str = json.dumps(dict)
    file = open(filename, 'w')
    file.write(json_str)
    file.close()

# get api info as json
def get_json_info(url, params=None):
    if params is None:
        response = requests.get(url)
    else:
        response = requests.get(url, params)
    if response.status_code == 200:
        data = response.text
        info = json.loads(data)
        return info
    
#cache genshin weapon info
def genshin_cache(filename, url):
    weapons = get_json_info(url)
    dict = {}
    for weapon in weapons:
        weapon_url = url + "/" + weapon 
        weapon_info = get_json_info(weapon_url)
        dict[weapon] = weapon_info
    write_json(filename, dict)

#cache monster hunter world armor info
def monster_cache(filename, url):
    armors = get_json_info(url)
    write_json(filename, armors)

#cache animal crossing aquatic organisms info
def animal_fish_cache(filename, url):
    fish = get_json_info(url)
    write_json(filename, fish)

def animal_sea_cache(filename, url):
    sea = get_json_info(url)
    write_json(filename, sea)

#part 3: processing data

#create table if doesnt exist

#read things from file

#keep a counter of the number retrieved from API and stop at 100 ?

#check if item is already in the database
    #if so, continue
    #otherwise get data from current item and add to database
    #increment the count of items retrieved

#sleep every 10th retrieved item

#part 4: visualize the data


    
#main function
def main():
    #create single database to store all tables
    cur, conn = setUpdatabase('gamecollectables.db')

    genshin_cache("genshinweapons.json", "https://api.genshin.dev/weapons")
    monster_cache("monsterweapons.json", "https://mhw-db.com/weapons")
    animal_fish_cache("fish.json", "http://acnhapi.com/v1/fish/", "http://acnhapi.com/v1/sea/")
    animal_sea_cache("sea.json", "http://acnhapi.com/v1/sea/")
     
if __name__ == "__main__":
    main()