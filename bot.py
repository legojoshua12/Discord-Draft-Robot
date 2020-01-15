# Core Modules
import asyncio
import io

import discord
import requests

# Code for functions
import random
import json
from PIL import Image

token = 'NjYzNDg0NTA5NTA4OTkzMDQ0.XhJMJA.3dyqXNPjbLrbHMF8h2apDAnAF9Y'


async def displayembed(message, playerNumber, civs):
    global civ_dict
    embed = discord.Embed(
        title='Player ' + str(playerNumber+1),
        colour=random.randint(0, 0xffffff)
    )
    # imageArray = []
    allImages = []
    for civ in civ_dict:
        for c in civs:
            if c == int(civ['ID']):
                embed.add_field(name=civ['Leader'], value=civ['Name'], inline=True)
                # r = requests.get(url=civ['Icon'])
                i = civ['Icon']
                allImages.append(i)
                # image = Image.open(io.BytesIO(r.content))
                # imageName = 'Test' + str(c) + '.png'
                # image.save('icons/'+imageName)
                # imageArray.append('icons/'+imageName)

    ran = random.randint(1, len(allImages))
    embed.set_thumbnail(url=str(allImages[ran-1]))

    # images = [Image.open(x) for x in imageArray]
    # widths, heights = zip(*(i.size for i in images))

    # total_width = sum(widths)
    # max_height = max(heights)

    # new_im = Image.new('RGBA', (total_width, max_height))

    # x_offset = 0
    # for im in images:
        # new_im.paste(im, (x_offset, 0))
        # x_offset += im.size[0]

    # new_im.save('icons/test.png')
    # file = discord.File("icons/test.png", filename="test.png")
    # embed.set_image(url='')
    await message.channel.send(embed=embed)
    # await message.channel.send(file=file)
    embed.clear_fields()


class MyClientBot(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('Loading civs: ')
        global civ_dict
        with open('civilizations.json', 'r') as f:
            civ_dict = json.load(f)
        print('Setting Status')
        await client.change_presence(activity=discord.Game(name='Sid Meier’s Civilization 5'),
                                     status=discord.Status.online, afk=False)
        print('Done!')
        print('')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user.id:
            return

        if message.content.startswith('!draft'):
            global civ_dict

            def is_valid_number(m):
                return m.author == message.author and m.content.isdigit()

            # Ask for number of players
            await message.channel.send('How many players are playing?')
            try:
                number_players = await self.wait_for('message', check=is_valid_number)
            except asyncio.TimeoutError:
                return

            # Ask for number of civs per player
            await message.channel.send('How many civilizations do you want to draft?')
            try:
                number_civs = await self.wait_for('message', check=is_valid_number)
            except asyncio.TimeoutError:
                return

            unusedCivs = []
            for i in civ_dict:
                unusedCivs.append(int(i['ID']))

            randomIDArray = []
            civsLen = len(unusedCivs)
            for x in range(0, int(number_players.content)):
                randomIDArray.insert(x, [])
                for y in range(0, int(number_civs.content)):
                    exit = False
                    while exit == False:
                        randomInt = random.randint(1, civsLen)
                        try:
                            unusedCivs.remove(randomInt)
                            randomIDArray[x].append(randomInt)
                            exit = True
                        except asyncio.TimeoutError:
                            print('Generated a number that already exists')

            for p in range(0, len(randomIDArray)):
                await displayembed(message, p, randomIDArray[p])

civ_dict = "NULL"
client = MyClientBot()
client.run(token)
