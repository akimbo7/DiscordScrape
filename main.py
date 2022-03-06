import Scrape
from colorama import *; init()

client = Scrape.Scrape(token = 'OTQ0MjEwNzk5MDA4ODA4OTgx.Yg-S4Q.2iDO1FLFoDojRQEUAlOIb5tpL9M')
print(f'[{Fore.YELLOW}%{Fore.RESET}] Fetching members...')

client.fetchMembers('417762285172555786', '762830936911773717')
print(f'[{Fore.YELLOW}+{Fore.RESET}] Members fetched')

ids = client.getIDs()
for id in ids:
    id = id.strip()
    x = client.getUsername(id)
    if x == None:
        pass
    else:
        client.getPicture(id, x)
