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

# create a list of aquatic creature rarity
def get_acnh_rarity(seafile, fishfile):
    seadict = load_json(seafile)
    aquatic_rarity_list = []
    for item in seadict:
        sea_speed = seadict[item].get("speed")
        if sea_speed == "Stationary":
            rarity = "Common"
        elif sea_speed == "Very slow":
            rarity = "Common"
        elif sea_speed == "Slow":
            rarity == "Common"
        elif sea_speed == "Medium":
            rarity = "Uncommon"
        elif sea_speed == "Fast":
            rarity = "Rare"
        else:
            rarity = "Ultra-rare"
        aquatic_rarity_list.append(rarity)
    fishdict = load_json(fishfile)
    for item in fishdict:
        fish_avail = fishdict[item].get("availability")
        fish_rarity = fish_avail.get("rarity")
        aquatic_rarity_list.append(fish_rarity)
    print(aquatic_rarity_list)
    return aquatic_rarity_list

# create a list of aquatic creature price
def get_prices(seafile, fishfile):
    seadict = load_json(seafile)
    aquatic_price_list = []
    for item in seadict:
        sea_price = seadict[item].get("price")
        aquatic_price_list.append(sea_price)
    fishdict = load_json(fishfile)
    for item in fishdict:
        fish_price = fishdict[item].get("price")
        aquatic_price_list.append(fish_price)
    print(aquatic_price_list)
    return aquatic_price_list

#create animal crossing table of aquatic creature rarity
def create_acnh_name_table(cur, conn):
    ACNH_aquatic_rarity = get_acnh_rarity("sea.json", "fish.json")
    cur.execute("CREATE TABLE IF NOT EXISTS ACNH_aquatic_rarity (id INTEGER PRIMARY KEY, rarity TEXT)")
    query = 'SELECT COUNT(*) FROM ACNH_aquatic_rarity;'
    cursor = conn.cursor()
    cursor.execute(query)
    index = cursor.fetchone()[0]
    print(index)
    if index < 100:
        count = 0
        for i in range(index, len(ACNH_aquatic_rarity)+1):
            count += 1
            if count % 26 == 0:
                break
            else:
                cur.execute("INSERT INTO ACNH_aquatic_rarity (id,rarity) VALUES (?,?)",(i,ACNH_aquatic_rarity[i]))
    conn.commit()

#create animal rossing table of aquatic creature price
    ACNH_aquatic_price = get_prices("sea.json", "fish.json")
    cur.execute("CREATE TABLE IF NOT EXISTS ACNH_aquatic_price (id INTEGER PRIMARY KEY, price TEXT)")
    query = 'SELECT COUNT(*) FROM ACNH_aquatic_price;'
    cursor = conn.cursor()
    cursor.execute(query)
    index = cursor.fetchone()[0]
    print(index)
    if index < 100:
        count = 0
        for i in range(index, len(ACNH_aquatic_price)+1):
            count += 1
            if count % 26 == 0:
                break
            else:
                cur.execute("INSERT INTO ACNH_aquatic_price (id,price) VALUES (?,?)",(i,ACNH_aquatic_price[i]))
        conn.commit()

# def create_monster_label(monster_file):
#     monsterdict = load_json(monster_file)
#     monster_names_list = []
#     for names in monsterdict:
#         all_weapons_f = monsterdict[names].get("rarity")
#         all_weapons = all_weapons_f.title()
#         monster_names_list.append(all_weapons)
#         monster_names_list.sort()
#     return monster_names_list
        
# def create_monster_name_table(cur, conn):
#     pass

# def create_genshin_labels(genshin_file):
#     genshindict = load_json(genshin_file)
#     genshin_names_list = []
#     for names in genshin_names_list:
#         all_names = genshindict[names].get("rarity")
#         labels = all_names.title()
#         genshin_names_list.append(labels)
#         genshin_names_list.sort()

#     return genshin_names_list

# def create_genshin_table(cur, con):
#     pass

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