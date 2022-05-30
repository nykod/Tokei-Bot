import time
import discord
from implementation.HLTVimpl import HLTVIMP
from implementation.HLTVimpl2 import HLTVIMP2
from implementation.HLTVimpl3 import HLTVIMP3
from implementation.HLTVimpl4 import HLTVIMP4
from implementation.FaceitImpl import FACEITIMP
from implementation.PlayerInfoImpl import PlayerInfoIMP
from commands.PlayersInfo import Players
from other.WorkWithFiles import WorkWithErrorLog
from other.WorkWithFiles import WorkWithJSON
from other.WorkWithFiles import WorkWithBlockedJSON
from implementation.AdminImpl import AdmIMP


class DiscordClient:
    """
    Interpreter for discord
    """
    client = discord.Client()
    ErClass = WorkWithErrorLog()
    wrkBlcJSON = WorkWithBlockedJSON()

    def botEvents(self):
        @self.client.event
        async def on_ready():
            """writes in a console if bot has started working"""
            print("starting... {0.user}".format(self.client))
            time.sleep(2)
            print("started! {0.user}".format(self.client))

        @self.client.event
        async def on_message(message):
            """
            Method gets a command and distribute it between main options 'hltv', 'faceit', 'player' and 'help'.
            Every option has its own methods.
            :param message: incoming message from discord
            :return: return is a message that will be sent on discord
            """

            if message.author == self.client.user:
                return

            """Writes message in message.log"""
            if message.content.startswith("!hltv") or message.content.startswith("!player") \
               or message.content.startswith("!faceit"):
                msg = '{0.author}'.format(message)
                file = open("../log/messages.log", "a")
                file.write(msg + " -> " + message.content + "\n")
                file.close()
            else:
                pass
            """--end"""

            """Checks if command is in 'blocked commands' list"""
            blockedLoad = self.wrkBlcJSON.loadjson()
            listBkeys = blockedLoad.keys()
            cont = True
            for i in listBkeys:
                if message.content.startswith(str(i)):
                    cont = False
            """--end"""

            if cont is False:
                await message.channel.send("Oops, this commands is not available at the moment... Try another one")
            elif message.content.startswith("!hltv"):
                """Checks if command starts with '!hltv' if it's true it will check command in its own methods"""
                hltv = HLTVIMP()
                hltv2 = HLTVIMP2()
                hltv3 = HLTVIMP3()
                hltv4 = HLTVIMP4()

                ret = hltv.msg_send_hltv(message)
                if ret is None:
                    ret = hltv2.msg_send_hltv(message)
                    if ret is None:
                        ret = hltv3.msg_send_hltv(message)
                        if ret is None:
                            ret = hltv4.msg_send_hltv(message)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                """--end"""

                # ERR 400
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            if isinstance(i, discord.embeds.Embed):
                                await message.channel.send(embed=i)
                            else:
                                await message.channel.send(i)
                    elif isinstance(ret, discord.embeds.Embed):
                        await message.channel.send(embed=ret)
                    else:
                        await message.channel.send(ret)
                except discord.errors.HTTPException as e:
                    self.ErClass.errorlog("discord.errors.HTTPException", "ERR400 -> " + str(e), message.content)
                    await message.channel.send("We have some troubles with message... Try it later")

                # ERR102
                try:
                    if isinstance(ret, str):
                        ret.replace("\r", "")
                    else:
                        pass
                except AttributeError as e:
                    self.ErClass.errorlog("AttributeError", "ERR102 -> " + str(e), message.content)

                msg = '{0.user}'.format(self.client)
                file = open("../log/messages.log", "a")

                # ERR101
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            file.write(str(msg) + " -> " + str(i) + "\n\n")
                    else:
                        file.write(str(msg) + " -> " + str(ret) + "\n\n")
                    file.close()
                except TypeError as e:
                    self.ErClass.errorlog("TypeError", "ERR101 -> " + str(e), message.content)
                except ValueError as e:
                    self.ErClass.errorlog("ValueError", "ERR101 -> " + str(e), message.content)

            elif message.content.startswith("!player"):
                """Checks if command starts with '!player' if it's true it will check command in its own methods"""
                playerinf = PlayerInfoIMP()
                ret = playerinf.msg_send_plr(message)
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            if isinstance(i, discord.embeds.Embed):
                                await message.channel.send(embed=i)
                            else:
                                await message.channel.send(i)
                    elif isinstance(ret, discord.embeds.Embed):
                        await message.channel.send(embed=ret)
                    else:
                        await message.channel.send(ret)
                except discord.errors.HTTPException as e:
                    self.ErClass.errorlog("discord.errors.HTTPException", "ERR400 -> " + str(e), message.content)
                    await message.channel.send("We have some troubles with message... Try it later")

                msg = '{0.user}'.format(self.client)
                file = open("../log/messages.log", "a")

                # ERR101
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            file.write(str(msg) + " -> " + str(i) + "\n\n")
                    else:
                        file.write(str(msg) + " -> " + str(ret) + "\n\n")
                    file.close()
                except TypeError as e:
                    self.ErClass.errorlog("TypeError", "ERR101 -> " + str(e), message.content)
                except ValueError as e:
                    self.ErClass.errorlog("ValueError", "ERR101 -> " + str(e), message.content)

            elif message.content.startswith("!admin"):
                try:
                    """Checks if command starts with '!admin' if it's true it will check command in its own methods"""
                    perms = False
                    Aperms = False
                    JSONc = WorkWithJSON()
                    admnDict = JSONc.loadjson()
                    auth = '{0.author}'.format(message)

                    for key, item in admnDict.items():
                        if admnDict["ADMIN"] == auth:
                            Aperms = True
                            perms = True
                        elif admnDict[key] == auth:
                            Aperms = False
                            perms = True

                    ADMinf = AdmIMP(Aperms, perms)

                    ret = ADMinf.msg_send_adm(message)

                    if isinstance(ret, discord.embeds.Embed):
                        await message.channel.send(embed=ret)
                    else:
                        await message.channel.send(ret)
                except discord.errors.HTTPException as e:
                    self.ErClass.errorlog("discord.errors.HTTPException", "!admin " + str(e), message.content)
                    await message.channel.send("Oops, something bad happened...")

            elif message.content.startswith("!faceit"):
                """Checks if command starts with '!faceit' if it's true it will check command in its own methods"""
                faceitinf = FACEITIMP()
                ret = faceitinf.msg_send_faceit(message)
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            if isinstance(i, discord.embeds.Embed):
                                await message.channel.send(embed=i)
                            else:
                                await message.channel.send(i)
                    elif isinstance(ret, discord.embeds.Embed):
                        await message.channel.send(embed=ret)
                    else:
                        await message.channel.send(ret)

                except discord.errors.HTTPException as e:
                    self.ErClass.errorlog("discord.errors.HTTPException", "ERR400 -> " + str(e), message.content)
                    await message.channel.send("We have some troubles with message... Try it later")

                msg = '{0.user}'.format(self.client)
                file = open("../log/messages.log", "a")

                # ERR101
                try:
                    if isinstance(ret, list):
                        for i in ret:
                            file.write(str(msg) + " -> " + str(i) + "\n\n")
                    else:
                        file.write(str(msg) + " -> " + str(ret) + "\n\n")
                    file.close()
                except TypeError as e:
                    self.ErClass.errorlog("TypeError", "ERR101 -> " + str(e), message.content)
                except ValueError as e:
                    self.ErClass.errorlog("ValueError", "ERR101 -> " + str(e), message.content)

            elif message.content == "!help":
                """Checks if command is'!help' if it's true it will send command list with help commands"""
                player = Players.help
                try:
                    title = "Commands and their description\n\n"
                    msg = ""
                    embed = discord.Embed(title=title)

                    for command, description in player.items():
                        msg = msg + "**" + command + "**" + "\n" + "*" + description + "*" + "\n"

                    embed.add_field(name="\u200b", value=msg, inline=False)
                    await message.channel.send(embed=embed)
                except Exception as e:
                    self.ErClass.errorlog("Exception", "Player help method " + str(e), str(message.content))
                    await message.channel.send("Oops, something bad happened... Try it later")
