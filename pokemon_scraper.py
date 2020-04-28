import csv
from selenium import webdriver

#Specify head start
head_start = False

#Open/Create CSV
if not(head_start) :
	with open('pokemon.csv', 'w') as f :
		f.write("ID,Name,Subname,Generation,Sprite,Icon Locations,Tier,Type 1,Type 2,Ability 1,Ability 2,Hidden Ability,Special Ability,Egg Group 1,Egg Group 2,HP,ATK,DEF,SPA,SPD,SPE,BST,Size,Weight,Gender Ratio,Color,Link\n")
	print("wrote header for pokemon.csv")
else :
	print("Starting in Head Start Mode. Skipped writing header")

#Open up a Firefox browser
driver = webdriver.Firefox()
print("defined driver")

#Navigate to Showdown's Pokedex
driver.get("https://dex.pokemonshowdown.com/pokemon/")
driver.set_page_load_timeout(15)
print("webpage loaded")

#Load all results
while True :
	try :
		driver.find_element_by_xpath('//button[@class="button big"]').click()
	except :
		break
print("results loaded")

#Get names
list_names_unfilitered = driver.find_elements_by_xpath('//span[@class="col pokemonnamecol"]')
list_names = []
list_subnames = []
for i in list_names_unfilitered :
	split_name = i.text.split('-', 1)
	list_names.append(split_name[0])
	if len(split_name) == 1 :
		list_subnames.append(None)
	else :
		list_subnames.append(split_name[1])
print("pokemon names retrieved")

#Get icon locations on sprite sheet
list_icon_locations_unfilitered = driver.find_elements_by_xpath('//span[@style]')
list_icon_locations = []
for i in list_icon_locations_unfilitered :
	list_icon_locations.append(i.get_attribute("style").split('scroll ')[1])
print("pokemon icon locations retrieved")

#Get Tiers
list_tiers_unfiltered = driver.find_elements_by_xpath('//span[@class="col numcol"]')
list_tiers = []
for i in list_tiers_unfiltered :
	list_tiers.append(i.text)
print("pokemon tiers retrieved")

#Get list of stats
list_stats_unfiltered = driver.find_elements_by_xpath('//span[@class="col statcol"]')
list_hp = []
list_atk = []
list_def = []
list_spa = []
list_spd = []
list_spe = []
for i in range(len(list_stats_unfiltered)) :
	if i % 6 == 0 :
		list_hp.append(list_stats_unfiltered[i].text[3:].replace("\n", ""))
	elif i % 6 == 1 :
		list_atk.append(list_stats_unfiltered[i].text[4:])
	elif i % 6 == 2 :
		list_def.append(list_stats_unfiltered[i].text[4:])
	elif i % 6 == 3 :
		list_spa.append(list_stats_unfiltered[i].text[4:])
	elif i % 6 == 4 :
		list_spd.append(list_stats_unfiltered[i].text[4:])
	elif i % 6 == 5 :
		list_spe.append(list_stats_unfiltered[i].text[4:])
print("pokemon stats retrieved")

#Get BST
list_bst_unfiltered = driver.find_elements_by_xpath('//span[@class="col bstcol"]')
list_bst = []
for i in list_bst_unfiltered :
	list_bst.append(i.text[4:])
print("pokemon base stat totals retrieved")

#Get links
list_links_unfiltered = driver.find_elements_by_xpath('//a[@data-target="push"]')
list_links = []
for i in list_links_unfiltered :
	list_links.append(i.get_attribute("href"))
print("pokemon links retrieved")

#Specify Generation
#NOTE: MAKE SURE TO SET THE GENERATION MANUALLY IF STARTING IN HEAD START MODE
generation = 1

#Specify starting location and boolean for setting this location
#NOTE: MAKE SURE TO SET THE STARTING LOCATION MANUALLY IF STARTING IN HEAD START MODE
start_location = 0
set_to_start = False

#Get Individual Pokemon's Data
for i in range(len(list_links)) :
	if not(set_to_start) :
		if i != start_location :
			continue
		else :
			set_to_start = True

	while True :
		try :
			driver.get(list_links[i])
			break
		except :
			print("Page load timeout, trying again")
			continue
	print("working on " + list_names[i])

	#Get id
	try :
		ID = driver.find_element_by_xpath('//code').text[1:]
	except :
		ID = None
	print("got ID")

	#Get Sprite
	sprite_link = driver.find_element_by_xpath('//img[@class="sprite"]').get_attribute("src")
	print("got sprite")

	#Get Types
	temp = driver.find_elements_by_xpath('//a[@data-target="push"]')
	type_1 = temp[2].text
	if temp[3].text != "Grass Knot" :
		type_2 = temp[3].text.replace("\n", "")
	else :
		type_2 = None
	print("got types")

	#Get Size and Weight
	size_string = driver.find_elements_by_xpath('//dd')[1].text.split(',')
	size = size_string[0]
	weight = size_string[1].split('\n')[0][1:]
	print("got size and weight")

	#Get Abilities
	abilities = driver.find_element_by_xpath('//dd[@class="imgentry"]').text.split(" | ")
	special_ability = None
	hidden_ability = None
	ability_1 = None
	ability_2 = None
	if "(special)" in abilities[-1] :
		special_ability = abilities.pop(-1)[:-10]
	if "(H)" in abilities[-1] :
		hidden_ability = abilities.pop(-1)[:-4]
	if len(abilities) == 2 :
		ability_1 = abilities[0]
		ability_2 = abilities[1]
	else :
		ability_1 = abilities[0]
	print("got abilities")

	#Get Egg Groups
	egg_groups = driver.find_element_by_xpath('//dl[@class="colentry"]').text[12:].split(", ")
	egg_group_1 = None
	try :
		egg_group_1 = egg_groups.pop(0)
		egg_group_2 = egg_groups.pop(0)
	except :
		egg_group_2 = None
	print("got egg groups")

	#Get Gender Ratio
	gender_ratio = driver.find_elements_by_xpath('//dl[@class="colentry"]')[1].text.split('\n')[1].replace(",", " ")
	print("got gender ratio")

	#Get Color
	driver.find_element_by_xpath('//button[@value="details"]').click()
	possible_colors = driver.find_elements_by_xpath('//dl')
	color = ""
	for j in possible_colors :
		if "Color:" in j.text :
			color = j.text.split("\n")[1]
	print("got color")

	#Iterate generation if necessary
	if list_names[i] == "Chikorita" :
		generation = 2
	elif list_names[i] == "Treecko" :
		generation = 3
	elif list_names[i] == "Turtwig" :
		generation = 4
	elif list_names[i] == "Victini" :
		generation = 5
	elif list_names[i] == "Chespin" :
		generation = 6
	elif list_names[i] == "Rowlet" :
		generation = 7
	elif list_names[i] == "Grookey" :
		generation = 8
	elif list_names[i] == "MissingNo." :
		generation = "glitch"
	elif list_names[i] == "Tomohawk" :
		generation = "CAP"

	#Write pokemon to file
	try :
		with open("pokemon.csv", "a") as f :
			f.write(str(ID) + "," + str(list_names[i]) + "," + str(list_subnames[i]) + "," + str(generation) + "," + str(sprite_link) + "," + str(list_icon_locations[i]) + "," + str(list_tiers[i]) + "," + str(type_1) + "," + str(type_2) + "," + str(ability_1) + "," + str(ability_2) + "," + str(hidden_ability) + "," + str(special_ability) + "," + str(egg_group_1) + "," + str(egg_group_2) + "," + str(list_hp[i]) + "," + str(list_atk[i]) + "," + str(list_def[i]) + "," + str(list_spa[i]) + "," + str(list_spd[i]) + "," + str(list_spe[i]) + "," + str(list_bst[i]) + "," + str(size) + "," + str(weight) + "," + str(gender_ratio) + "," + str(color) + "," + str(list_links[i]) + "\n")
	except :
		with open("pokemon.csv", "a") as f :
			f.write(str(ID) + "," + str(None) + "," + str(list_subnames[i]) + "," + str(generation) + "," + str(sprite_link) + "," + str(list_icon_locations[i]) + "," + str(list_tiers[i]) + "," + str(type_1) + "," + str(type_2) + "," + str(ability_1) + "," + str(ability_2) + "," + str(hidden_ability) + "," + str(special_ability) + "," + str(egg_group_1) + "," + str(egg_group_2) + "," + str(list_hp[i]) + "," + str(list_atk[i]) + "," + str(list_def[i]) + "," + str(list_spa[i]) + "," + str(list_spd[i]) + "," + str(list_spe[i]) + "," + str(list_bst[i]) + "," + str(size) + "," + str(weight) + "," + str(gender_ratio) + "," + str(color) + "," + str(list_links[i]) + "\n")

#Close web browser
driver.close()