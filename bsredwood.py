import discord
import asyncio
import os
import re
import brawlstats
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


keyfile_dict = {
  "type": "service_account",
  "project_id": "bsbot-226217",
  "private_key_id": "ec051d1f245707de80095dc8b22215df5ab7cdee",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDH5+tqNsb1/0Wg\noF/A+g/xHcfiFLcsGzLiMMHFCXinouDyUQAl/smSV8eC8hfPZYR6G3ZuAQB/6vkE\nA8BCYTxE5fZjP92jz0TwhN8VvKDLbKFZn3ExObPODJeNwGUyeKsqWKMh8J+AxCXy\nX1f5E4jULw3hLzdjZ7Z+idhtFN1pFdkb4PK6v/6UkjHDyJkT+7IW5BDtq61sCsRS\ntGL6V9foW6nnuON3IzFBDR5ii5si6mIFIQGGlTGEY+ptiKs10fO7eWpQrpQiIK+U\nELYR7gKP7rxnF2Yqk5oTeONsz2x9CodcGBHQ0zsPM0xLmPLSPPo6h65JS88iEY6B\nJhlnC7G7AgMBAAECggEARz2f2FjQG9/OtPkiVrfnEYMO9kNyqc3BmvlMPMdsz7UM\nnF6Agonj1PriV4imMpuXlBqQYJCL2IppFuStUhqr61PWtDUQ7C1UALEhfXIdDZHX\niIR5RtUs/lvfcL1lcxCs0ykGbfR+K1n7uf3/cHzlMNTaCeuVPiA6WasPTYR3iViG\nDd07FyyQp44dZEqfCt//IzKOj7aJ27iJgOQpMbeM3F2zZBmYr9JlB6bhEehQGB6Q\nZmasy9pe9YXXZUVN8N/y/+cXemeBEoNfbOu7jSvpO+0hXtzi2PwXTGog0Q30Sxzf\nVfMt1upMOncdKMdYBiCyzJAbQDoZzlo2IJcUlIp6pQKBgQDq4NeD/Bl8MyglYGkM\nRTAf77Pd9RN8N6grEB6xeoM9JLqO/vrAvmFxhYhIB9rfV8LzIx2U8PfT+ol7zfXl\nc3/MLgiyTIphkvS+hzdzETsijBaIgZwDPm7BMbcpTNNiPk9rS24Bu9vgegsXocs1\n4KzS2G97AO9LPxUkbnZGbQ4AvwKBgQDZ4fm4cTFVGs+3xpCXaDohCeuUjzxynfwW\nu0vuJeG38uR9mU2KesV6Mf9c04rV+YXbSaYh/pHwyjlYLe7MglOD2fJ7axIthyjl\nJhcVCIUTU0fPXK+JYAZDSpVOFIhkWtVHlQ/v0pW2J1Aeb38bHCkgZ1RXCKm/AsoI\nQlI0SBfSBQKBgQC6b0YiKZVBFIolQOWhK7oLX4TyBXo1+yetJtp2HbzWZ7T9lD8N\nhxBpv4hxRGrjJRJFU/ZDJxJQXGmMr+si+g7Szydv/3lIAhHqugG1gFPkFDY+nEJu\nALyA9Slhyu1u6e64R+NF1QuunrD3TSGz3mbP5aR3ikJnA+eQR23ycNXQmQKBgQDV\nqD0DWyxvMi2DH1pmvrRR9bJoKdWy561udRhOXiNsCOl7KLvbEe1YmHK7ik3Y6ikT\nErOxHjvqjcOR7uj+7sYKw8x+rk5TCvlVS/bSj1o/yyjd9RvFcL5zek3TFVtyXYhL\n+6Z3HF/nEcIFNnzEDuddeTZBaqNaRdfsJW0LC68gKQKBgHK1cx7uoVFaQm6VQ36x\nmQdUkeezbOOsPwZ27AcwgrFbh2HdD3aO5h7obIqHXYqB0siAAvCyDCGb3cCsKcV6\n+1OBMlS497faCUNpSvqDPwlvI84kBp4IZziY0zwnZ5bXVWhqrUgxjMb97Y6mL0Z5\n52fEkDn4cn0TgRaWKpJI7bUy\n-----END PRIVATE KEY-----\n",
  "client_email": "bsbotredwood@bsbot-226217.iam.gserviceaccount.com",
  "client_id": "108560087435782443699",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bsbotredwood%40bsbot-226217.iam.gserviceaccount.com"
}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    keyfile_dict=keyfile_dict, scopes=scope)

gc = gspread.authorize(credentials)

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
            await client.send_typing(message.channel)
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
            await client.send_typing(message.channel)
            message2 = str(message.content).split(' ',1)[1]
            try:
                profile = bs.get_profile(message2.upper())
            except:
                if '<@' in message2:
                    try:
                        linked = gc.open('BSlinked').sheet1
                        message3 = message2.replace('<@', '')
                        message3 = message3.replace('>', '')
                        discid = linked.find(message3)
                        game_id = linked.cell(discid.row, 2).value
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
                linked = gc.open('BSlinked').sheet1
                discid = linked.find(str(message.author.id))
                game_id = linked.cell(discid.row, 2).value
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
            embed.add_field(name='Trophies', value= str(profile.trophies) + ' <:trophy:525016161285570571>')
            embed.add_field(name='Highest Trophies', value= str(profile.highest_trophies) + ' <:trophy:525016161285570571>')
            embed.add_field(name='Level', value= '<:levelstar:525297407383044097>' + str(profile.exp_level), inline=False)
            embed.add_field(name='3v3 Wins', value= '<:gemgrab:525416312629886976> ' + str(profile.victories))
            embed.add_field(name='Showdown Wins', value= '<:showdown:525299101022158878> ' + str(profile.solo_showdown_victories))
            embed.add_field(name='Duo Showdown Wins', value= '<:duoshowdown:525299098354712576> ' + str(profile.duo_showdown_victories))
            embed.add_field(name='Best Time as Boss', value= '<:boss:525299096567808023> ' + profile.best_time_as_boss)
            embed.add_field(name='Best Robo Rumble Time', value= '<:roborumble:525299100778889217> ' + profile.best_robo_rumble_time)
            embed.add_field(name='Brawlers Unlocked', value= '<:cards:525383827632422958> **' + str(profile.brawlers_unlocked) + '**/22')
            embed.add_field(name='Club', value= profile.club.name + ' (#' + profile.club.tag + ')')
            await client.send_message(message.channel, embed = embed)
        except:
            pass

    elif '!LINK' == message1 or '!SAVE' == message1:
        linked = gc.open('BSlinked').sheet1
        try:
            await client.send_typing(message.channel)
            discid = linked.find(str(message.author.id))
            gameid = linked.cell(discid.row, 2).value
            profilename = linked.cell(discid.row, 3).value
            error = await client.send_message(message.channel, ':no_entry: This discord account is already linked to ' + profilename + ' #' + gameid)
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
                    linked.append_row([str(message.author.id), message2.upper(), profile.name])
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
            await client.send_typing(message.channel)
            linked = gc.open('BSlinked').sheet1

            discid = linked.find(str(message.author.id))
            linked.delete_row(discid.row)

            await client.send_message(message.channel, ':white_check_mark: Account succesfully unlinked!')
        except:
            error = await client.send_message(message.channel, ':no_entry: Account not linked!')
            await asyncio.sleep(10)
            await client.delete_message(error)

    
    elif '!BRAWLERS' == message1:
        try:
            await client.send_typing(message.channel)
            message2 = str(message.content).split(' ',1)[1]
            try:
                profile = bs.get_profile(message2.upper())
            except:
                if '<@' in message2:
                    try:
                        linked = gc.open('BSlinked').sheet1
                        message3 = message2.replace('<@', '')
                        message3 = message3.replace('>', '')
                        discid = linked.find(message3)
                        game_id = linked.cell(discid.row, 2).value
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
                linked = gc.open('BSlinked').sheet1
                discid = linked.find(str(message.author.id))
                game_id = linked.cell(discid.row, 2).value
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

    elif '!EVENTS' == message1 or '!MAPS' == message1:
        try:
            message2 = str(message.content).split(' ',1)[1]
        except:
            pass
        events = bs.get_events()
        y = 0
        gmodes = json.loads(open('gamemodes.json').read())
        modifiers = json.loads(open('modifiers.json').read())
        if 'later' == message2 or 'next' == message2:
            await client.send_typing(message.channel)
            for event in events.upcoming:
                print(events.upcoming[y].game_mode)
                gmode = next(item for item in gmodes if item["gamemode"] == events.upcoming[y].game_mode)

                gamemoji = gmode.get("emoji")
                embed = discord.Embed(title= gamemoji + ' ' + events.upcoming[y].game_mode + ' - ' + events.upcoming[y].map_name, color= 0xffd633)
                
                if events.upcoming[y].has_modifier == True:
                    modifier = next(item for item in modifiers if item["modifier"] == events.upcoming[y].modifier_name)
                    modmoji = modifier.get("emoji")
                    embed.add_field(name= 'Modifier', value = modmoji + ' ' + events.upcoming[y].modifier_name, inline=False)
                else:
                    pass
                print(events.upcoming[y].slot_name)
                embed.set_thumbnail(url=events.upcoming[y].map_image_url)
                embed.add_field(name= 'Ends in', value= '<:clock:525632375888281610> ' + str(datetime.timedelta(seconds=events.upcoming[y].end_time_in_seconds)))
                if events.upcoming[y].slot_name == "Ticketed Events":
                    embed.add_field(name= 'Rewards', value = '<:ticket:525661772896665621> ' + str(events.upcoming[y].free_keys) + ' Free')
                else:
                    embed.add_field(name= 'Rewards', value= '<:keys:525629631735267328> ' + str(events.upcoming[y].free_keys) + ' Free')
                await client.send_message(message.channel, embed = embed)
                y = y+1
        else:
            await client.send_typing(message.channel)
            for event in events.current:
                try:
                    gmode = next(item for item in gmodes if item["gamemode"] == events.current[y].game_mode)
                except:
                    pass

                gamemoji = gmode.get("emoji")
                embed = discord.Embed(title= gamemoji + ' ' + events.current[y].game_mode + ' - ' + events.current[y].map_name, color= 0xffd633)
                
                if events.current[y].has_modifier == True:
                    modifier = next(item for item in modifiers if item["modifier"] == events.current[y].modifier_name)
                    modmoji = modifier.get("emoji")
                    embed.add_field(name= 'Modifier', value = modmoji + ' ' + events.current[y].modifier_name, inline=False)
                else:
                    pass
                print(events.current[y].slot_name)
                embed.set_thumbnail(url=events.current[y].map_image_url)
                embed.add_field(name= 'Ends in', value= '<:clock:525632375888281610> ' + str(datetime.timedelta(seconds=events.current[y].end_time_in_seconds)))
                if events.current[y].slot_name == "Ticketed Events":
                    embed.add_field(name= 'Rewards', value = '<:ticket:525661772896665621> ' + str(events.current[y].free_keys) + ' Free')
                else:
                    embed.add_field(name= 'Rewards', value= '<:keys:525629631735267328> ' + str(events.current[y].free_keys) + ' Free')
                await client.send_message(message.channel, embed = embed)
                y = y+1
        

            
client.run('NTI1MjUyNTQ5NTI4MjU2NTI3.Dvz_gw.DITUyWDGBLtcgJKKG5ehhzN9HA4')

#https://discordapp.com/oauth2/authorize?client_id=525252549528256527&scope=bot&permissions=537377864
