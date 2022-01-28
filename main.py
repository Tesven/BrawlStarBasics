import brawlstats
from collections import Counter

token = open('token.txt').read()
inputTag = input("Input your tag: ")

client = brawlstats.Client(token)
target = client.get_profile(inputTag)

target_battle = client.get_battle_logs(target.tag)

print("Name of player:", target,
      "\nTrophies:", target.trophies,
      "\nSolo victories:", target.solo_victories,
      "\nDuo victories:", target.duo_victories,
      "\nTeam victories:", target['3vs3Victories'],
      "\nLevel:", target.expLevel)

winRate = 0
brawlers = []
for index in range(len(target_battle)):
    try:
        result = target_battle[index].battle.result
    except:
        rank = target_battle[index].battle.rank
        battleType = target_battle[index].battle.mode
        if rank <= 2 and battleType == 'duoShowdown':
            result = 'victory'
        elif rank <= 4 and battleType == 'soloShowdown':
            result = 'victory'
        else:
            result = 'lost'

    try:
        for participant in target_battle[index].battle.teams:
            for jndex in range(len(participant)):
                if participant[jndex].tag == target.tag:
                    brawlers.append(participant[jndex].brawler.name)
    except:
        for participant in target_battle[index].battle.players:
            if participant.tag == target.tag:
                brawlers.append(participant.brawler.name)

    if result == 'victory':
        winRate += 1

winRate *= (100 / len(target_battle))
print("WinRate:", winRate, "% on", len(target_battle), "battles.")
print("Brawler usage:", Counter(brawlers))


club = target.get_club()
if club is not None:
    print("Club:", club.name)
    print("\nBest players in target's club")
    members = club.get_members()
    index = min(5, len(members))
    best_players = members[:index]

    for player in best_players:
        print(player.trophies, "\t|", player.name)
        battle = client.get_battle_logs(player.tag)
        time = battle[0].battle_time[6:8] + "/" \
               + battle[0].battle_time[4:6] + "/" \
               + battle[0].battle_time[0:4] + " " \
               + battle[0].battle_time[9:11] + ":" \
               + battle[0].battle_time[11:13] + "Z"
        try:
            result = battle[0].battle.result
        except:
            result = battle[0].battle.rank

        brawler = ""  # To avoid to forget declaration
        try:
            for participant in battle[0].battle.teams:
                for index in range(len(participant)):
                    if participant[index].tag == player.tag:
                        brawler = participant[index].brawler.name
        except:
            for participant in battle[0].battle.players:
                if participant.tag == player.tag:
                    brawler = participant.brawler.name

        print("\tLast play:", time,
              "\n\tmode:", battle[0].battle.mode,
              "\n\tResult:", result,
              "\n\tBrawler:", brawler)
else:
      print("No club")
