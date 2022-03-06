import Scrape
from colorama import *; init()

token = 'token'
guildID = '111111111111111111
channelID = '222222222222222222'

client = Scrape.Scrape(token = token)
print(f'[{Fore.YELLOW}%{Fore.RESET}] Fetching members...')

client.fetchMembers(guildID, channelID)
print(f'[{Fore.YELLOW}+{Fore.RESET}] Members fetched')

ids = client.getIDs()
for id in ids:
    id = id.strip()
    x = client.getUsername(id)
    if x == None:
        pass
    else:
        client.getPicture(id, x)
