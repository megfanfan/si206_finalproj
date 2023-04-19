import requests
import sqlite3
import json
import os
import matplotlib.pyplot as plt

#Megan Fan, Katelyn Ma, Sabrina Yu :)

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

#cache json of api
def cache_json(filename, url):
    data = get_json_info(url)
    write_json(filename, data)

# database function
def setUpdatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#animal crossing dictionary
def create_acnh_dictionary(fishfile, seafile):
    fishdict = load_json(fishfile)
    acnhdict = {}
    for item in fishdict:
        item_names = fishdict[item].get("name")
        eng_name = item_names.get("name-USen")
        eng_name = eng_name.title()
        item_price = fishdict[item].get("price")
        item_avail = fishdict[item].get("availability")
        item_rarity = item_avail.get("rarity")
        acnhdict[eng_name] = [item_price, item_rarity]
    seadict = load_json(seafile)
    for item in seadict:
        item_names = seadict[item].get("name")
        eng_name = item_names.get("name-USen")
        eng_name = eng_name.title()
        item_price = seadict[item].get("price")
        item_speed = seadict[item].get("speed")
        if item_speed == "Stationary":
            rarity = "Common"
        elif item_speed == "Very slow":
            rarity = "Common"
        elif item_speed == "Slow":
            rarity == "Common"
        elif item_speed == "Medium":
            rarity = "Uncommon"
        elif item_speed == "Fast":
            rarity = "Rare"
        else:
            rarity = "Ultra-rare"
        acnhdict[eng_name] = [item_price, rarity]
        
    return acnhdict

#create animal crossing table of aquatic creature rarity
def create_acnh_name_table(cur, conn):
    acnhdict = create_acnh_dictionary("fish.json", "sea.json")
    cur.execute("CREATE TABLE IF NOT EXISTS ACNH_Aquatic_Creatures (species_id INTEGER PRIMARY KEY, species TEXT, price INTEGER, rarity TEXT)")
    query = 'SELECT COUNT(*) FROM ACNH_Aquatic_Creatures;'
    cursor = conn.cursor()
    cursor.execute(query)
    index = cursor.fetchone()[0]
    print(index)
    count = 0
    for i in range(index, len(acnhdict)):
        count += 1
        if count % 26 == 0:
            break
        else:
            allkeys = list(acnhdict.keys())
            cur.execute("INSERT INTO ACNH_Aquatic_Creatures (species_id, species, price, rarity) VALUES (?,?,?,?)",(i+1,allkeys[i],acnhdict[allkeys[i]][0],acnhdict[allkeys[i]][1]))
    conn.commit()

#main function
def main():
    #create single database to store all tables
    cur, conn = setUpdatabase('gamecollectables.db')
    # create json caches
    genshin_cache("genshinweapons.json", "https://api.genshin.dev/weapons")
    cache_json("monsterweapons.json", "https://mhw-db.com/weapons")
    cache_json("fish.json", "http://acnhapi.com/v1/fish/")
    cache_json("sea.json", "http://acnhapi.com/v1/sea/")
    # create tables
    create_acnh_name_table(cur, conn)
    
if __name__ == "__main__":
    main()