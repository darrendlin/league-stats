from pprint import PrettyPrinter
from functools import reduce
from riotwatcher import RiotWatcher
import pandas as pd

# initialize
pp = PrettyPrinter(indent=2)
watcher = RiotWatcher('RGAPI-0e63de8c-1053-474a-a4e2-16d01b7bbc64')

# variables
regions = ['na1', 'br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'oc1', 'tr1', 'ru']
sr_ranked_solo_str = 'RANKED_SOLO_5x5'
sr_ranked_solo = 420

# run
for region in regions:
  df = pd.DataFrame(columns=['accountId', 'avgGoldEarned'])
  print(region);
  challengers = watcher.league.challenger_by_queue(region, sr_ranked_solo_str)
  for i, playerEntry in enumerate(challengers['entries']):
    print('\t({:d}/{:d}) player:'.format(i+1, len(challengers['entries'])), playerEntry['playerOrTeamName'])
    accountId = watcher.summoner.by_name(region, playerEntry['playerOrTeamName'])['accountId']
    matches = watcher.match.matchlist_by_account(region, accountId, queue=sr_ranked_solo, end_index=20)
    goldEarnedList = [];
    for match in matches['matches']:
      #print('\t\tmatch:', match['gameId'])
      matchData = watcher.match.by_id(region, match['gameId'])
      participantId = list(filter(lambda p: p['player']['currentAccountId'] == accountId, matchData['participantIdentities']))[0]['participantId']
      goldEarned = list(filter(lambda p: p['participantId'] == participantId, matchData['participants']))[0]['stats']['goldEarned']
      goldEarnedList.append(goldEarned);
    avgGoldEarned = reduce(lambda x, y: x + y, goldEarnedList) / len(goldEarnedList)
    #print(accountId, avgGoldEarned)
    df = df.append(pd.DataFrame([[accountId, avgGoldEarned]], columns=['accountId', 'avgGoldEarned']), ignore_index=True)
    #print(df)
  df.to_csv(region + '.csv')