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

# database function
def setUpdatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# create an alpha list of aquatic creatures
def create_acnh_labels(seafile, fishfile):
    seadict = load_json(seafile)
    aquatic_names_list = []
    for item in seadict:
        all_sea_names = seadict[item].get("name")
        english_sea_name = all_sea_names.get("name-USen")
        english_sea_name = english_sea_name.title()
        aquatic_names_list.append(english_sea_name)
    fishdict = load_json(fishfile)
    for item in fishdict:
        all_fish_names = fishdict[item].get("name")
        english_fish_name = all_fish_names.get("name-USen")
        english_fish_name = english_fish_name.title()
        aquatic_names_list.append(english_fish_name)
        aquatic_names_list.sort()
    return aquatic_names_list

#create animal crossing table of aquatic fish names
def create_acnh_name_table(cur, conn):
    ACNH_aquatic_species = create_acnh_labels("sea.json", "fish.json")
    cur.execute("DROP TABLE IF EXISTS ACNH_aquatic_species")
    cur.execute("CREATE TABLE ACNH_aquatic_species (id INTEGER PRIMARY KEY, species TEXT)")
    query = 'SELECT COUNT(*) FROM ACNH_aquatic_species;'
    cursor = conn.cursor()
    cursor.execute(query)
    index = cursor.fetchone()[0]
    print(index)
    count = 0
    for i in range(index, len(ACNH_aquatic_species)+1):
        count += 1
        if count % 26 == 0:
            break
        else:
            cur.execute("INSERT INTO ACNH_aquatic_species (id,species) VALUES (?,?)",(i,ACNH_aquatic_species[i]))
    conn.commit()

def create_monster_label(monster_file):
    monsterdict = load_json(monster_file)
    monster_names_list = []
    for names in monsterdict:
        all_weapons_f = monsterdict[names].get("rarity")
        all_weapons = all_weapons_f.title()
        monster_names_list.append(all_weapons)
        monster_names_list.sort()
    return monster_names_list
        
def create_monster_name_table(cur, conn):
    pass
    # monster_weapons = create_monster_label("weapons.json")
    # cur.execute("DROP TABLE IF EXISTS monster_weapons")
    # cur.execute("CREATE TABLE monster_weapons (species )
    # query = 'SELECT COUNT(*) FROM monster_weapons;'
    # cursor = conn.cursor()
    # cursor.execute(query)
    # count = cursor.fetchone()[0]
    # pass

def create_genshin_labels(genshin_file):
    genshindict = load_json(genshin_file)
    genshin_names_list = []
    for names in genshin_names_list:
        all_names = genshindict[names].get("rarity")
        labels = all_names.title()
        genshin_names_list.append(labels)
        genshin_names_list.sort()

    return genshin_names_list

def create_genshin_table(cur, con):
    genshin_weapon_types = create_genshin_table("genshinweapons.json")
    cur.execute("DROP TABLE IF EXISTS genshin_weapon_types")
    cur.execute("CREATE TABLE genshin_weapon_types (id INTEGER PRIMARY KEY, species TEXT)")
    q = 'SELECT COUNT(*) FROM genshin_weapon_types;'
    cursor = con.cursor()
    cursor.execute(q)
    counter = 0
    for x in range(len(genshin_weapon_types)):
        counter += 1
        if x == 0:
            print()
        pass

        
        
#part 3: processing data (this part is just for reference for stuff we need to do )

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
    animal_fish_cache("fish.json", "http://acnhapi.com/v1/fish/")
    animal_sea_cache("sea.json", "http://acnhapi.com/v1/sea/")
    create_acnh_name_table(cur, conn)


    
if __name__ == "__main__":
    main()