import os
import time
import requests
import random
import string
import discum
from colorama import *; init()
#from fetch import *

class Scrape:

    def __init__(self, token, proxy = None):

        self.token = token
        self.session = requests.Session()
        self.header = {'authorization': token}
        self.proxy = {'https': f'http://{proxy}'}

        self.session.headers.update(self.header)

        if proxy != None:
            self.session.proxies.update(self.proxy)
        else:
            pass

    def fetchMembers(self, guildID, channelID):

        bot = discum.Client(token=self.token, log=False)

        def closeAfterFetching(resp, guild_id):
        	if bot.gateway.finishedMemberFetching(guild_id):
        		bot.gateway.removeCommand({'function': closeAfterFetching, 'params': {'guild_id': guild_id}})
        		bot.gateway.close()

        def getMembers(guild_id, channel_id):
        	bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=1, reset=False)
        	bot.gateway.command({'function': closeAfterFetching, 'params': {'guild_id': guild_id}})
        	bot.gateway.run(); bot.gateway.resetSession()
        	return bot.gateway.session.guild(guild_id).members

        members = getMembers(guildID, channelID)

        for id in members:
            with open('ids.txt', 'a+') as f:
                f.write(f'{id}\n')


    def getIDs(self):
        with open('ids.txt') as f:
            file = f.readlines()
            return file


    def rateLimit(self, response):
        time.sleep(0.1)
        response = self.session.get(f'https://discord.com/api/v9/users/@me')

        response = self.session.get(f'https://discord.com/api/v9/users/{response.json()["id"]}')

        if 'retry_after' in response.text:
            wait = response.json()['retry_after']
            print(f'[{Fore.RED}-{Fore.RESET}] Rate limited for {wait}s')
            time.sleep(float(int(wait)))
            self.rateLimit(response)
        return True


    def getUsername(self, id):

        response = self.session.get(f'https://discord.com/api/v9/users/{id}')

        if 'rate limited' in response.text:
            self.rateLimit(response)

            response = self.session.get(f'https://discord.com/api/v9/users/{id}')

        id = response.json()['id']
        pfp = response.json()['avatar']
        username = response.json()['username']
        discriminator = response.json()['discriminator']

        with open('usernames.txt', 'a+') as f:
            f.write(f'{username}\n')

        print(f'[{Fore.GREEN}+{Fore.RESET}] Username scraped - {username}')

        return pfp


    def getPicture(self, id, pfp):

        dirPath = os.path.dirname(os.path.realpath(__file__))

        response = self.session.get(f'https://cdn.discordapp.com/avatars/{id}/{pfp}', stream=True)

        if response.status_code == 200:
            with open(f'{dirPath}/pfps/{"".join(random.choice(string.ascii_lowercase + string.digits) for i in range(8))}.png', 'wb') as f:
                for chunk in response:
                    f.write(chunk)

        print(f'[{Fore.BLUE}+{Fore.RESET}] PFP saved')
