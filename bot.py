# Core Modules
import asyncio
from config import config

import discord

# Code for functions
import random
import json

token = config["token"]


async def displayEmbedCivs(message, playerNumber, civs):
    global civ_dict
    embed = discord.Embed(
        title='Player ' + str(playerNumber + 1),
        colour=random.randint(0, 0xffffff)
    )
    allImages = []
    for civ in civ_dict:
        for c in civs:
            if c == int(civ['ID']):
                embed.add_field(name=civ['Leader'], value=civ['Name'], inline=True)
                i = civ['Icon']
                allImages.append(i)

    ran = random.randint(1, len(allImages))
    embed.set_thumbnail(url=str(allImages[ran - 1]))
    await message.channel.send(embed=embed)
    embed.clear_fields()


async def displayEmbedCountries(message, playerNumber, countries):
    global hoi_dict
    embed = discord.Embed(
        title='Player ' + str(playerNumber + 1),
        colour=random.randint(0, 0xffffff)
    )
    allImages = []
    allCountries = []
    for country in hoi_dict:
        for countryID in countries:
            if int(countryID) == int(country['ID']):
                allCountries.append(country['Name'])
                i = country['Flag']
                allImages.append(i)

    totalString = ''
    for m in allCountries:
        totalString = totalString + m + '\n'
    embed.add_field(name='\u200b', value=totalString, inline=True)
    ran = random.randint(1, len(allImages))
    embed.set_thumbnail(url=str(allImages[ran - 1]))
    await message.channel.send(embed=embed)
    embed.clear_fields()


async def civDraft(self, message, players=0, civilizationsPerPlayer=0):
    global civ_dict

    def is_valid_number(m):
        return m.author == message.author and m.content.isdigit()

    def is_number(f):
        try:
            int(f)
            return True
        except (ValueError, Exception):
            return False

    # Ask for number of players if not provided
    if players == 0:
        await message.channel.send('How many players are playing?')
        try:
            number_players = await self.wait_for('message', check=is_valid_number)
        except asyncio.TimeoutError:
            return
    else:
        number_players = players

    # Ask for number of civilizations per player if not provided
    if civilizationsPerPlayer == 0:
        await message.channel.send('How many civilizations do you want to draft?')
        try:
            number_civilizations = await self.wait_for('message', check=is_valid_number)
        except asyncio.TimeoutError:
            return
    else:
        number_civilizations = civilizationsPerPlayer

    if not isinstance(number_civilizations, str):
        number_civilizations = number_civilizations.content
    if not isinstance(number_players, str):
        number_players = number_players.content

    if is_number(number_players):
        pass
    else:
        await message.channel.send(message.author.mention + ' Unknown what `' + number_players + '` means in context')
        return
    if is_number(number_civilizations):
        pass
    else:
        await message.channel.send(message.author.mention + ' Unknown what `' + number_civilizations + '` means in context')
        return

    unusedCivilizations = []
    for i in civ_dict:
        unusedCivilizations.append(int(i['ID']))

    randomIDArray = []
    civsLen = len(unusedCivilizations)
    for x in range(0, int(number_players)):
        randomIDArray.insert(x, [])
        for y in range(0, int(number_civilizations)):
            exitLoop = False
            while not exitLoop:
                randomInt = random.randint(1, civsLen)
                try:
                    unusedCivilizations.remove(randomInt)
                    randomIDArray[x].append(randomInt)
                    exitLoop = True
                except (ValueError, Exception):
                    pass

    for p in range(0, len(randomIDArray)):
        await displayEmbedCivs(message, p, randomIDArray[p])


async def hoiDraft(self, message, pl=0, cpp=0, notRequireMajor=False):
    global hoi_dict

    def is_valid_number(m):
        return m.author == message.author and m.content.isdigit()

    def is_number(f):
        try:
            int(f)
            return True
        except (ValueError, Exception):
            return False

    # Ask for number of players if not provided
    if pl == 0:
        await message.channel.send('How many players are playing?')
        try:
            number_players = await self.wait_for('message', check=is_valid_number)
        except asyncio.TimeoutError:
            return
    else:
        number_players = pl

    # Ask for number of countries per player if not provided
    if cpp == 0:
        await message.channel.send('How many countries do you want to draft?')
        try:
            number_countries = await self.wait_for('message', check=is_valid_number)
        except asyncio.TimeoutError:
            return
    else:
        number_countries = cpp

    if not isinstance(number_countries, str):
        number_countries = number_countries.content
    if not isinstance(number_players, str):
        number_players = number_players.content

    if is_number(number_players):
        pass
    else:
        await message.channel.send(message.author.mention + ' Unknown what `' + number_players + '` means in context')
        return
    if is_number(number_countries):
        pass
    else:
        await message.channel.send(message.author.mention + ' Unknown what `' + number_countries + '` means in context')
        return

    unusedCountries = []
    for g in hoi_dict:
        unusedCountries.append(g)
    randomIDArray = []
    countryListLength = len(unusedCountries)
    if notRequireMajor:
        for x in range(0, int(number_players)):
            randomIDArray.insert(x, [])
            for y in range(0, int(number_countries)):
                exitLoop = False
                while not exitLoop:
                    randomInt = random.randint(1, countryListLength)
                    try:
                        unusedCountries.remove(hoi_dict[randomInt-1])
                        randomIDArray[x].append(int(hoi_dict[randomInt-1]['ID']))
                        exitLoop = True
                    except (ValueError, Exception):
                        pass
    else:
        for x in range(0, int(number_players)):
            randomIDArray.insert(x, [])
            hasMajorCountry = False
            for y in range(0, int(number_countries)):
                exitLoop = False
                while not exitLoop:
                    randomInt = random.randint(1, countryListLength)
                    if hasMajorCountry == False and hoi_dict[randomInt-1]['IsMajor'] == 'True':
                        try:
                            unusedCountries.remove(hoi_dict[randomInt-1])
                            randomIDArray[x].append(int(hoi_dict[randomInt-1]['ID']))
                            hasMajorCountry = True
                            exitLoop = True
                        except (ValueError, Exception):
                            pass
                    elif hasMajorCountry:
                        try:
                            unusedCountries.remove(hoi_dict[randomInt-1])
                            randomIDArray[x].append(int(hoi_dict[randomInt-1]['ID']))
                            exitLoop = True
                        except (ValueError, Exception):
                            pass

    for p in range(0, len(randomIDArray)):
        await displayEmbedCountries(message, p, randomIDArray[p])


class MyClientBot(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')
        print('Loading civs')
        global civ_dict
        with open('JSON/civilizations.json', 'r') as f:
            civ_dict = json.load(f)
        print('Loading countries')
        global hoi_dict
        with open('JSON/hoi4Countries.json', 'r') as m:
            hoi_dict = json.load(m)
        print('Setting Status')
        await client.change_presence(activity=discord.Game(name='Something Random!'),
                                     status=discord.Status.online, afk=False)
        print('Done!')
        print('')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user.id:
            return

        if message.content.startswith('*'):
            s = message.content.split()
            messageLength = len(s)
            if s[0].lower() == '*help':
                if messageLength == 1:
                    embed = discord.Embed(
                        title='Commands',
                        colour=random.randint(0x53a635, 0x7d1414)
                    )
                    embed.add_field(name='*help', value='Displays all commands.', inline=False)
                    embed.add_field(name='*help games', value='Displays all currently supported games.', inline=False)
                    embed.add_field(name='*draft [game] [args]',
                                    value='Starts a draft, you must specify a game for the robot to draft',
                                    inline=False)
                    await message.channel.send(embed=embed)
                elif s[1].lower() == 'games':
                    embed = discord.Embed(
                        title='Games',
                        colour=random.randint(0x53a635, 0x7d1414)
                    )
                    embed.add_field(name='*draft hoi4 [players] [countries] [disableMajorRule]',
                                    value='Hearts of Iron IV', inline=False)
                    embed.add_field(name='*draft civ [players] [civs]', value='Sid Meier’s Civilization V',
                                    inline=False)
                    await message.channel.send(embed=embed)
            elif messageLength == 1 and s[0].lower() == '*draft':
                await message.channel.send(
                    message.author.mention + ' Unspecified game. Please use `*help games` to view the list of all the supported games.')
            elif s[0].lower() != '*draft':
                await message.channel.send(
                    message.author.mention + ' Unknown command. Use `*help` to view the list of all commands.')
            if s[0] == '*draft':
                if messageLength >= 2:
                    if s[1] == 'civ':
                        if messageLength == 2:
                            await civDraft(self, message)
                        elif messageLength == 3:
                            await civDraft(self, message, s[2])
                        elif messageLength == 4:
                            await civDraft(self, message, s[2], s[3])
                        else:
                            await message.channel.send(
                                message.author.mention + ' Unknown command arguments. Use `*help` for more information.')
                    elif s[1] == 'hoi4':
                        if messageLength == 2:
                            await hoiDraft(self, message)
                        elif messageLength == 3:
                            await hoiDraft(self, message, s[2])
                        elif messageLength == 4:
                            await hoiDraft(self, message, s[2], s[3])
                        elif messageLength == 5:
                            if s[4].lower() == 'true':
                                await hoiDraft(self, message, s[2], s[3], True)
                            elif s[4].lower() == 'false':
                                await hoiDraft(self, message, s[2], s[3])
                            else:
                                await message.channel.send(
                                    message.author.mention + ' Unknown ' + s[4] + '. Please specify `true` or `false`.')
                        else:
                            await message.channel.send(
                                message.author.mention + ' Unknown command arguments. Use `*help` for more information.')
                    else:
                        await message.channel.send(
                            message.author.mention + ' Unknown game. Please use `*help games` to view the list of all the supported games.')


civ_dict = None
hoi_dict = None
client = MyClientBot()
client.run(token)
