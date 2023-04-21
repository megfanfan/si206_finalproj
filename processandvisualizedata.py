import requests
import sqlite3
import json
import os
import matplotlib.pyplot as plt

#Megan Fan, Katelyn Ma, Sabrina Yu :)

def process_acnh_data(db):
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, db)
    con = sqlite3.connect(full_path)
    cur = con.cursor()
    cur.execute("""
        SELECT ACNH_Aquatic_Creatures.price, ACNH_Aquatic_Creatures.rarity, ACNH_Rarity_Reference.rarity_type
        FROM ACNH_Aquatic_Creatures
        JOIN ACNH_Rarity_Reference ON ACNH_Rarity_Reference.rarity_id = ACNH_Aquatic_Creatures.rarity
        """
        )
    variable = cur.fetchall()
    con.close()
    common_total = 0
    common_count = 0
    uncommon_total = 0
    uncommon_count = 0
    rare_total = 0
    rare_count = 0
    ultrarare_total = 0
    ultrarare_count = 0
    for x in variable:
        rarity_type = x[2]
        price = x[0]
        if rarity_type == "Common":
            common_total += price 
            common_count = common_count + 1
        elif rarity_type == "Uncommon":
            uncommon_total += price
            uncommon_count = uncommon_count + 1
        elif rarity_type == "Rare":
            rare_total += price
            rare_count = rare_count + 1
        elif rarity_type == "Ultra-rare":
            ultrarare_total += price
            ultrarare_count = ultrarare_count + 1
    common_avg = round(common_total / common_count, 2)
    uncommon_avg = round(uncommon_total / uncommon_count, 2)
    rare_avg = round(rare_total / rare_count, 2)
    ultrarare_avg = round(ultrarare_total / ultrarare_count, 2)
    new_dict = {}
    new_dict["Common"] = common_avg
    new_dict["Uncommon"] = uncommon_avg
    new_dict["Rare"] = rare_avg
    new_dict["Ultra-rare"] = ultrarare_avg
    return new_dict

def create_acnh_graph(new_dict):
    x_var = list(new_dict.keys())
    y_var = list(new_dict.values())
    plt.figure(figsize = (25,8))
    plt.bar(x_var,y_var, color="lightgreen")
    plt.ylabel('Average Price of Aquatic Creature (Bells)') 
    plt.xlabel('The Rarity Type')
    plt.title("What is the Aquatic Creature's Average Price Based on its Rarity in Animal Crossing?")    
    plt.show()

def process_monster_data(db):
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, db)
    con = sqlite3.connect(full_path)
    cur = con.cursor()
    cur.execute("""
        SELECT Monster_Weapons.attack, Monster_Weapons.rarity
        FROM Monster_Weapons 
        """
        )
    variable = cur.fetchall()
    con.close()
    monster_dict = {}
    for x in variable:
        attack = x[0]
        rarity = x[1]
        if rarity not in monster_dict:
            monster_dict[rarity] = attack
        else:
            if attack > monster_dict[rarity]:
                monster_dict[rarity] = attack
    return monster_dict

def create_monster_graph(monster_dict):
    x_var = list(monster_dict.keys())
    y_var = list(monster_dict.values())
    plt.figure(figsize = (25,8))
    plt.scatter(x_var, y_var, color="darkred")
    plt.xlabel('Rarity Level')
    plt.ylabel('Attack Damage')
    plt.title('What is the Maximum Attack Value for Each Weapon Rarity Level in Monster Hunter?')
    plt.show()

def process_genshin_data(db):
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, db)
    con = sqlite3.connect(full_path)
    cur = con.cursor()
    cur.execute("""
        SELECT Genshin_Weapons.base_attack, Genshin_Weapons.rarity
        FROM Genshin_Weapons 
        """
        )
    variable = cur.fetchall()
    con.close()
    genshin_dict = {}
    for x in variable:
        attack = x[0]
        rarity = x[1]
        if rarity not in genshin_dict:
            genshin_dict[rarity] = attack
        else:
            if attack < genshin_dict[rarity]:
                genshin_dict[rarity] = attack
    return genshin_dict

def create_genshin_graph(genshin_dict):
    x_var = list(genshin_dict.keys())
    y_var = list(genshin_dict.values())
    plt.figure(figsize = (25,8))
    plt.scatter(x_var, y_var, color="purple")
    plt.xlabel('Rarity Level')
    plt.ylabel('Base Attack')
    plt.title('What is the Minimum Base Attack Value for Each Weapon Rarity Level in Genshin Impact?')
    plt.show()

def write_txt(filename, acnh_dict, monster_dict, genshin_dict):
    f = open(filename, 'w')
    f.write("Animal Crossing Calculations:" + "\n")
    acnhkeys = list(acnh_dict.keys())
    acnhvalues = list(acnh_dict.values())
    for i in range(0, len(acnh_dict)):
        f.write(str(acnhkeys[i]) + " Aquatic creatures cost about " + str(acnhvalues[i]) + " bells on average" + "\n")
    f.write("\n" + "Monster Hunter Calculations:" + "\n")
    monsterkeys = list(monster_dict.keys())
    monstervalues = list(monster_dict.values())
    for i in range(0, len(monster_dict)):
        f.write("The maximum attack value is " + str(monstervalues[i]) + " for a weapon with a rarity number of " + str(monsterkeys[i]) + "\n")
    f.write("\n" + "Genshin Calculations:" + "\n")
    genshinkeys = list(genshin_dict.keys())
    genshinvalues = list(genshin_dict.values())
    for i in range(0, len(genshin_dict)):
        f.write("The minimum base attack value is " + str(genshinvalues[i]) + " for a weapon with a rarity number of " + str(genshinkeys[i]) + "\n")
    f.close()

def main():
    acnh_dict = process_acnh_data("gamecollectables.db")
    create_acnh_graph(acnh_dict)

    monster_dict = process_monster_data("gamecollectables.db")
    create_monster_graph(monster_dict)

    genshin_dict = process_genshin_data("gamecollectables.db")
    create_genshin_graph(genshin_dict)

    write_txt("calculations.txt", acnh_dict, monster_dict, genshin_dict)

if __name__ == "__main__":
    main()