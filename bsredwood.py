import discord
import asyncio
import os
import random
import brawlstats
import json

#Discord
client = discord.Client()

#BrawlStats
bs = brawlstats.Client('88834ccba20cb095f47cb9a0eab260e11b1f8143b42306bbe98c635af9545e53f7f73a52fa351b79')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    await client.change_presence(game=discord.Game(name="Brawl Stars"))

@client.event
async def on_message(message):
    message1 = str(message.content).split(' ',1)[0].upper()

    if '!CLUB' == message1 or '!CLAN' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
            try:
                club = bs.get_club(message2.upper())
            except:
                error = await client.send_message(message.channel, ':no_entry: Could not find club with this tag or there was an error getting club data. Please try again!')
                await asyncio.sleep(10)
                await client.delete_message(error)
        except:
            try:
                club = bs.get_club('RURJY9')
            except:
                error = await client.send_message(message.channel, ':no_entry: There was an error getting club data. Please try again!')
                await asyncio.sleep(10)
                await client.delete_message(error)

        try:
            members = club.members
            embed = discord.Embed(title=club.name + ' (#' + club.tag + ')', description=club.description, color= 0xffd633)
            embed.set_thumbnail(url= club.badge_url)

            embed.add_field(name='Trophies', value= str(club.trophies) + ' <:trophy:525016161285570571>', inline = False)

            embed.add_field(name='Required Trophies', value= str(club.required_trophies) + ' <:trophy:525016161285570571>')
            
            if club.status == 'Open':
                embed.add_field(name='Status', value= '<:opened:525268440106401792> ' + club.status)
            elif club.status == 'Invite Only':
                embed.add_field(name='Status', value= '<:invite:525268438156050432> ' + club.status)
            elif club.status == 'Closed':
                embed.add_field(name='Status', value= '<:closed:525268439426924544> ' + club.status)
                
            embed.add_field(name='Members', value= '**' + str(club.members_count) + '**/100 <:members:525017973379825665>')
            
            if club.members_count < 5:
                top5 = ''
                a = 0
                for i in range(club.members_count):
                    top5 = top5 + str(members[a].trophies) + ' <:trophy:525016161285570571> ' + members[a].name + '\n'
                    a = a+1
            else:
                top5 = ''
                a = 0
                for i in range(5):
                    top5 = top5 + str(members[a].trophies) + ' <:trophy:525016161285570571> ' + members[a].name + '\n'
                    a = a+1

            
            if club.online_members == 0:
                embed.add_field(name='Members Online', value= '<:nomembersonline:525268345323388929> **' + str(club.online_members) + '**/' + str(club.members_count))
            else:
                embed.add_field(name='Members Online', value= '<:membersonline:525268343607787520> **' + str(club.online_members) + '**/' + str(club.members_count))
            embed.add_field(name='Top Members', value= top5, inline=False)
            await client.send_message(message.channel, embed = embed)
        except:
            pass
        
    elif '!PROFILE' == message1 or '!STATS' == message1 or '!STAT' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
            try:
                profile = bs.get_profile(message2.upper())
            except:
                if '<@' in message2:
                    try:
                        linked = json.loads(open('linked.json').read())
                        message2 = message2.replace('<@', '')
                        message2 = message2.replace('>', '')
                        link = next(item for item in linked if item["discord_id"] == message2)
                        game_id = link.get("game_id")
                        try:
                            profile = bs.get_profile(game_id)
                        except:
                            error = await client.send_message(message.channel, ':no_entry: There was an error getting profile data. Please try again!')
                            await asyncio.sleep(10)
                            await client.delete_message(error)
                    except:
                        error = await client.send_message(message.channel, ':no_entry: This player didn\'t link his game account to discord!')
                        await asyncio.sleep(10)
                        await client.delete_message(error)
                elif '<@' not in message2:
                    error = await client.send_message(message.channel, ':no_entry: Couldn\'t find an account with this tag!')
                    await asyncio.sleep(10)
                    await client.delete_message(error)
        except:
            try:
                linked = json.loads(open('linked.json').read())
                link = next(item for item in linked if item["discord_id"] == str(message.author.id))
                game_id = link.get("game_id")
                try:
                    profile = bs.get_profile(game_id)
                except:
                    error = await client.send_message(message.channel, ':no_entry: There was an error getting profile data. Please try again!')
                    await asyncio.sleep(10)
                    await client.delete_message(error)
            except:
                error = await client.send_message(message.channel, ':no_entry: You must specify an user! If you want to display your own stats, link your account using `!link`')
                await asyncio.sleep(20)
                await client.delete_message(error)
        
        try:        
            embed = discord.Embed(title=profile.name + ' (#' + profile.tag + ')', color= 0xffd633)
            embed.set_thumbnail(url= profile.avatar_url)
            embed.add_field(name='Trophies', value= '**' + str(profile.trophies) + '**/' + str(profile.highest_trophies) + ' <:trophy:525016161285570571>')
            embed.add_field(name='Level', value= '<:levelstar:525297407383044097>' + str(profile.exp_level))
            embed.add_field(name='3v3 Wins', value= str(profile.victories))
            embed.add_field(name='Showdown Wins', value= '<:showdown:525299101022158878> ' + str(profile.solo_showdown_victories))
            embed.add_field(name='Duo Showdown Wins', value= '<:duoshowdown:525299098354712576> ' + str(profile.duo_showdown_victories))
            embed.add_field(name='Best Time as Boss', value= '<:boss:525299096567808023> ' + profile.best_time_as_boss)
            embed.add_field(name='Best Robo Rumble Time', value= '<:roborumble:525299100778889217> ' + profile.best_robo_rumble_time)
            embed.add_field(name='Brawlers Unlocked', value= '**' + str(profile.brawlers_unlocked) + '**/22')
            embed.add_field(name='Club', value= profile.club.name + ' (#' + profile.club.tag + ')')
            await client.send_message(message.channel, embed = embed)
        except:
            pass

    elif '!LINK' == message1:
        linked = json.loads(open('linked.json').read())
        try:
            link = next(item for item in linked if item["discord_id"] == str(message.author.id))
            game_id = link.get("game_id")
            error = await client.send_message(message.channel, ':no_entry: This discord account is already linked to #' + game_id)
            await asyncio.sleep(10)
            await client.delete_message(error)
        except:
            try:
                message2 = str(message.content).split(' ',1)[1]
                try:
                    message2 = message2.replace('#', '')
                except:
                    pass
                try:
                    profile = bs.get_profile(message2.upper())
                    linked = json.load(open('linked.json'))
                    data = {"discord_id": str(message.author.id), "game_id": message2.upper()}
                    linked.append(data)
                    with open('linked.json', 'w') as f:
                        json.dump(linked, f)
                    await client.send_message(message.channel, ':white_check_mark: Account succesfully linked to ' + profile.name + ' (#' + message2.upper() + ')')
                except:
                    error = await client.send_message(message.channel, ':no_entry: Couldn\'t find an account with that tag!')
                    await asyncio.sleep(10)
                    await client.delete_message(error)
            except:
                error = await client.send_message(message.channel, ':no_entry: You must specify your game tag!')
                await asyncio.sleep(10)
                await client.delete_message(error)

    elif '!UNLINK' == message1:
        try:
            obj  = json.load(open("linked.json"))

            for i in range(len(obj)):
                if obj[i]["discord_id"] == str(message.author.id):
                    obj.pop(i)
                    break

            open("linked.json", "w").write(json.dumps(obj))
            await client.send_message(message.channel, ':white_check_mark: Account succesfully unlinked!')
        except:
            error = await client.send_message(message.channel, ':no_entry: Account not linked!')
            await asyncio.sleep(10)
            await client.delete_message(error)

    
    elif '!BRAWLERS' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
            print(message2)
            try:
                profile = bs.get_profile(message2.upper())
            except:
                if '<@' in message2:
                    try:
                        linked = json.loads(open('linked.json').read())
                        message3 = message2.replace('<@', '')
                        message3 = message3.replace('>', '')
                        link = next(item for item in linked if item["discord_id"] == message3)
                        game_id = link.get("game_id")
                        try:
                            profile = bs.get_profile(game_id)
                        except:
                            error = await client.send_message(message.channel, ':no_entry: There was an error getting profile data. Please try again!')
                            await asyncio.sleep(10)
                            await client.delete_message(error)
                    except:
                        error = await client.send_message(message.channel, ':no_entry: This player didn\'t link his game account to discord!')
                        await asyncio.sleep(10)
                        await client.delete_message(error)
                elif '<@' not in message2:
                    error = await client.send_message(message.channel, ':no_entry: Couldn\'t find an account with this tag!')
                    await asyncio.sleep(10)
                    await client.delete_message(error)
        except:
            try:
                linked = json.loads(open('linked.json').read())
                link = next(item for item in linked if item["discord_id"] == str(message.author.id))
                game_id = link.get("game_id")
                try:
                    profile = bs.get_profile(game_id)
                except:
                    error = await client.send_message(message.channel, ':no_entry: There was an error getting profile data. Please try again!')
                    await asyncio.sleep(10)
                    await client.delete_message(error)
            except:
                error = await client.send_message(message.channel, ':no_entry: You must specify an user! If you want to display your own stats, link your account using `!link`')
                await asyncio.sleep(20)
                await client.delete_message(error)

        try:
            embed = discord.Embed(title=profile.name + ' (#' + profile.tag + ')', color= 0xffd633)
            brawlers = profile.brawlers
            x = 0
            brawed = json.loads(open('brawlers.json').read())
            ranks = json.loads(open('ranks.json').read())
            for brawler in brawlers:
                try:
                    braw = next(item for item in brawed if item["name"] == str(brawlers[x].name))
                except:
                    pass
                try:
                    rank = next(item for item in ranks if item["trophy"] <= brawlers[x].highest_trophies <= item["trophy_max"] and brawlers[x].trophies > item["trophy_min"])
                except:
                    rank = next(item for item in ranks if item["trophy"] <= brawlers[x].trophies <= item["trophy_max"])
                rankmoji = rank.get("emoji")
                minrank = rank.get("trophy_min")
                br_emoji = braw.get("emoji")
                embed.add_field(name= str(br_emoji) + ' ' + brawlers[x].name, value= '<:levelstar:525297407383044097> ' + str(brawlers[x].level) + ' | ' + rankmoji + ' | <:trophy:525016161285570571> ' + str(brawlers[x].trophies))
                x = x+1

            await client.send_message(message.channel, embed = embed)
        except:
            pass

            
client.run('NTI1MjUyNTQ5NTI4MjU2NTI3.Dvz_gw.DITUyWDGBLtcgJKKG5ehhzN9HA4')

#https://discordapp.com/oauth2/authorize?client_id=525252549528256527&scope=bot&permissions=537377864
