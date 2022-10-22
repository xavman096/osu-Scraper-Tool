from requests_html import HTMLSession
import csv
import urllib.request

headerlist = ['Player', 'User ID', 'Map', 'PP', 'Accuracy', 'Mods']

session = HTMLSession()
r = session.get('https://osu.ppy.sh/home')
print("Connected to osu! Home")

RegPlayers = r.html.find('strong', first = True).text
RegPlayers = RegPlayers.replace(',', '')
RegPlayers = int(RegPlayers)
CurrentPlayerId = 0
print("Got", RegPlayers, "Registered Players")

while CurrentPlayerId < RegPlayers:
    
    mods = ['EZ', 'NF', 'HT', 'HR', 'SD', 'PF', 'DT', 'NC', 'HD', 'FL', 'SO']
    modsUsed = []
    PlayerDetails = []

    session = HTMLSession()

    r = session.get("https://osu.ppy.sh/users/" + str(CurrentPlayerId))
    print("Connected to Player:", CurrentPlayerId)
    
    if r.status_code == 404:
        print("Player with id:", CurrentPlayerId, "doesn't exists")
        print("Scrapping next id")
        CurrentPlayerId += 1
        continue

    r.html.render()

    name = r.html.find('.u-ellipsis-pre-overflow', first = True).text
    print("Players name:", name, "has been scrapped")

    Top100 = r.html.find('.play-detail__pp')
    TopPlay = int(0)

    for i in Top100:
        PrefPoints = i.find('span', first = True).text
        try:
            PrefPoints = PrefPoints.replace('pp','')
            PrefPoints = PrefPoints.replace(',', '')
            PrefPoints = int(PrefPoints)
        except:
            continue
        
        if PrefPoints > TopPlay:
            TopPlay = PrefPoints

    print(name + "'s top was worth:", TopPlay)
    
    Map = r.html.find('.play-detail')

    for m in Map:
        MapTitle = m.find('a', first = True).text
        MapPP = m.find('.play-detail__pp', first = True)
        MapPP = MapPP.find('span', first = True).text
        MapPP = MapPP.replace('pp', '')
        MapPP = MapPP.replace(',','')
        MapPP = int(MapPP)
        
        if MapPP == TopPlay:
            print(name+ "'s top play:", MapTitle, "has been scrapped")
            Accuracy = m.find('.play-detail__accuracy', first = True).text
            for i in mods:
                Mod = m.find('.mod--'+ i, first = True)
                if Mod != None:
                    modsUsed.append(i)
            break
        
    strModsUsed = ','.join(modsUsed)
    try:
        print(name, "used:", modsUsed[0], "in their top play")
    except:
        print("No Mods used")
        strModsUsed = "No Mods used"

    PlayerDetails.append(name)
    PlayerDetails.append(CurrentPlayerId)
    PlayerDetails.append(MapTitle)
    PlayerDetails.append(MapPP)
    PlayerDetails.append(Accuracy)
    PlayerDetails.append(strModsUsed)

    with open('osu!TopPlays.csv', 'a', newline = '') as MyFile:
        
        wr = csv.writer(MyFile, quoting = csv.QUOTE_ALL)
        if CurrentPlayerId == 2:
            wr.writerow(headerlist)
        wr.writerow(PlayerDetails)
    
    print(name + "'s data was stored to osu!TopPlays.csv")
    print("Scrapping next id")
    
    CurrentPlayerId += 1