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
        if item_rarity == "Common":
            item_rarity = 1
        elif item_rarity == "Uncommon":
            item_rarity = 2
        elif item_rarity == "Rare":
            item_rarity = 3
        elif item_rarity == "Ultra-rare":
            item_rarity = 4
        acnhdict[eng_name] = [item_price, item_rarity]
    seadict = load_json(seafile)
    for item in seadict:
        item_names = seadict[item].get("name")
        eng_name = item_names.get("name-USen")
        eng_name = eng_name.title()
        item_price = seadict[item].get("price")
        item_speed = seadict[item].get("speed")
        if item_speed == "Stationary":
            rarity = 1
        elif item_speed == "Very slow":
            rarity = 1
        elif item_speed == "Slow":
            rarity == 1
        elif item_speed == "Medium":
            rarity = 2
        elif item_speed == "Fast":
            rarity = 3
        else:
            rarity = 4
        acnhdict[eng_name] = [item_price, rarity]

    return acnhdict

#create animal crossing table of aquatic creature rarity
def create_acnh_name_table(cur, conn):
    acnhdict = create_acnh_dictionary("fish.json", "sea.json")
    cur.execute("CREATE TABLE IF NOT EXISTS ACNH_Aquatic_Creatures (species_id INTEGER PRIMARY KEY, species TEXT, price INTEGER, rarity INTEGER)")
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

# create reference table
def create_reference_table(cur, conn):
    rarity_types = ["Common", "Uncommon", "Rare", "Ultra-rare"]
    cur.execute("""
        DROP TABLE IF EXISTS ACNH_Rarity_Reference
    """)
    cur.execute("CREATE TABLE IF NOT EXISTS ACNH_Rarity_Reference (rarity_id INTEGER PRIMARY KEY, rarity_type TEXT)")
    for i in range(0,4):
        cur.execute("INSERT INTO ACNH_Rarity_Reference (rarity_id, rarity_type) VALUES (?,?)",(i+1, rarity_types[i])) 
    conn.commit() 


#create genshin dictionary
def create_genshin_dictionary(genshinfile):
    genshininfo = load_json(genshinfile)
    weapondict = {}
    for item in genshininfo:
        weapon_name = genshininfo[item].get("name")
        weapon_rarity = genshininfo[item].get("rarity")
        weapon_base_attack = genshininfo[item].get("baseAttack")
        if weapon_base_attack == None:
            weapon_base_attack = genshininfo[item].get("BaseAttack")
        weapondict[weapon_name]=[weapon_base_attack,weapon_rarity]
    return weapondict

#create genshin weapons table
def create_genshin_table(cur, conn):
    genshindict = create_genshin_dictionary("genshinweapons.json")
    cur.execute("CREATE TABLE IF NOT EXISTS Genshin_Weapons (weapon_id INTEGER PRIMARY KEY, name TEXT, base_attack INTEGER, rarity INTEGER)")
    query = 'SELECT COUNT(*) FROM Genshin_Weapons;'
    cursor = conn.cursor()
    cursor.execute(query)
    index = cursor.fetchone()[0]
    print(index)
    count = 0
    for i in range(index, len(genshindict)):
        count += 1
        if count % 26 == 0:
            break
        else:
            allkeys = list(genshindict.keys())
            cur.execute("INSERT INTO Genshin_Weapons (weapon_id, name, base_attack, rarity) VALUES (?,?,?,?)",(i+1,allkeys[i],genshindict[allkeys[i]][0],genshindict[allkeys[i]][1]))
    conn.commit()

#creating monster weapons info 
def create_monster_dict(monster_file):
    monster_dict_directory = load_json(monster_file)
    monster_dict = {}
    for item in monster_dict_directory:
        #print(item)
        #this is an int
        id = item["id"]
        #print(id)
        #string
        name_v = item["name"]
        name = name_v.title()
        #string
        type_v = item["type"]
        type = type_v.title()
        #int 
        rarity = item["rarity"]
        monster_dict[name] = [id, type, rarity]
    #print(monster_dict.items())
    return monster_dict

# create monster table 
def create_monster_table(cur, conn):
    monster_dict = create_monster_dict("monsterweapons.json")
    cur.execute("CREATE TABLE IF NOT EXISTS Monster_Weapons (weapon_id INTEGER PRIMARY KEY, name TEXT, rarity INTEGER, type TEXT)")
    variable = 'SELECT COUNT(*) FROM Monster_Weapons;'
    cursor = conn.cursor()
    cursor.execute(variable)
    index = cursor.fetchone()[0]
    #print(index)
    count = 0
    
    for i in range(index, len(monster_dict)):
        count += 1
        if count % 26 == 0:
            break
        else:
            allkeys = list(monster_dict.keys())
            cur.execute("INSERT INTO Monster_Weapons (weapon_id, name, rarity, type) VALUES (?,?,?,?)",(i+1,allkeys[i],monster_dict[allkeys[i]][0],monster_dict[allkeys[i]][1]))
    conn.commit()

#creating monster weapons info 
def create_monster_dict(monster_file):
    monster_dict_directory = load_json(monster_file)
    monster_dict = {}
    for item in monster_dict_directory:
        #print(item)
        #this is an int
        id = item["id"]
        #print(id)
        #string
        name_v = item["name"]
        name = name_v.title()
        #string
        attack_v = item["attack"]
        attack = attack_v.get("display")
        #int 
        rarity = item["rarity"]
        monster_dict[name] = [id, attack, rarity]
    #print(monster_dict.items())
    return monster_dict

# create monster table 
def create_monster_table(cur, conn):
    monster_dict = create_monster_dict("monsterweapons.json")
    cur.execute("CREATE TABLE IF NOT EXISTS Monster_Weapons (weapon_id INTEGER PRIMARY KEY, name TEXT, rarity INTEGER, attack INTEGER)")
    variable = 'SELECT COUNT(*) FROM Monster_Weapons;'
    cursor = conn.cursor()
    cursor.execute(variable)
    index = cursor.fetchone()[0]
    #print(index)
    count = 0
    
    for i in range(index, len(monster_dict)):
        count += 1
        if count % 26 == 0:
            break
        else:
            allkeys = list(monster_dict.keys())
            cur.execute("INSERT INTO Monster_Weapons (weapon_id, name, rarity, attack) VALUES (?,?,?,?)",(i+1,allkeys[i],monster_dict[allkeys[i]][2],monster_dict[allkeys[i]][1]))
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
    create_genshin_table(cur, conn)
    create_monster_table(cur, conn)
    create_reference_table(cur, conn)
    
if __name__ == "__main__":
    main()