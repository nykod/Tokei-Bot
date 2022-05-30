import discord
from commands.FaceitCommands import FACEITStats
from commands.FaceitCommands2 import FACEITStats2
from commands.FaceitCommands3 import FACEITStats3
from other.Exceptions import WebSiteNotFoundException, PlayerEloException
from other.WorkWithFiles import WorkWithErrorLog


class FACEITIMP:
    """
    Class that uses methods from other classes(gets their output - rewrite it) and sends return message to bot.py
    """
    def msg_send_faceit(self, message):
        """
        This method resends message(which is rewritten for discord) to a discord bot
        :param message: message which we use for recognition if it is a method or not
        :return: return is a message(could be a list, string, embed or list of embeds)
        """
        faceitmsg = "!faceit "
        FACEIT = FACEITStats()
        FACEIT2 = FACEITStats2()
        FACEIT3 = FACEITStats3()
        Er = WorkWithErrorLog()

        if (faceitmsg + "stats") in message.content:
            """!faceit stats"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                info, img = FACEIT.faceit_stats_count(splitts[2])
                title = "***" + splitts[2] + " stats***"
            except ValueError as e:
                Er.errorlog("ValueError", "Stats method " + str(e), str(message.content))
                return "Oops, something bad happened with stats! Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Stats method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                Er.errorlog("WebSiteNotFoundException", "Stats method", str(message.content))
                return "Oops, looks like this nickname does not exist! Try something else"
            except PlayerEloException:
                Er.errorlog("PlayerEloException", "Stats method", str(message.content))
                return "Oops, something bad happened with count! Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Stats method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            if len(splitts) == 3:
                """Setting embed"""
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.faceit.com",
                                 icon_url="https://res.cloudinary.com/crunchbase-production/image/upload/"
                                          "c_lpad,f_auto,q_auto:eco,dpr_1/xtrxobrlttwixe1kfzo5")
                embed.set_author(name="Tokei bot")
                embed.set_thumbnail(url=img)

                """Sets 'Skill Level' field"""
                msg = "**Level: **" + str(info["LVL"]) + "\n**Elo: **" + str(info["ELO"]) \
                      + "\n**Rank: **" + str(info["RANK"])
                embed.add_field(name="Skill Level", value=msg)
                """--end"""

                """Sets 'Matches' field"""
                msg = "**All matches: **" + str(info["MATCHES"]) + "\n**Winrate: **" + str(info["WINRATE"]) \
                      + "\n**Wins: **" + str(info["WINS"]) + "\n**Wins: **" + str(info["LOSES"])
                embed.add_field(name="Matches", value=msg, inline=False)
                """--end"""

                """Sets 'Average player stats' field"""
                msg = "**K/D Rating: **" + str(info["KDR"]) + "\n**Kills Per Round: **" + str(info["KPR"]) \
                      + "\n**Kills: **" + str(info["KILLS"]) + "\n**Deaths: **" + str(info["DEATHS"])
                embed.add_field(name="Average player stats", value=msg, inline=False)
                """--end"""
                """--end"""

                return embed
            else:
                return "Oops, looks like we have some troubles with input! Try something else!"

        elif (faceitmsg + "compare") in message.content:
            """!faceit compare"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                nickname1 = splitts[2]
                nickname2 = splitts[3]
                infop1, infop2 = FACEIT.faceit_comparision(nickname1, nickname2)
                title = nickname1 + " and " + nickname2 + " comparison"
            except ValueError as e:
                Er.errorlog("ValueError", "Comparison method " + str(e), str(message.content))
                return "Oops, something bad happened with stats! Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Comparison method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                Er.errorlog("WebSiteNotFoundException", "Comparison method", str(message.content))
                return "Oops, looks like this nickname does not exist! Try something else"
            except PlayerEloException:
                Er.errorlog("PlayerEloException", "Elo exception in comparison method", str(message.content))
                return "Oops, something bad happened with count! Try it later"
            except IndexError:
                return "Oops, wrong input... Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Comparison method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            if len(splitts) == 4:

                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.faceit.com",
                                 icon_url="https://res.cloudinary.com/crunchbase-production/image/upload/"
                                          "c_lpad,f_auto,q_auto:eco,dpr_1/xtrxobrlttwixe1kfzo5")
                embed.set_author(name="Tokei bot")

                """Skill comparison between them."""
                msg = "Level: " + str(infop1["LVL"]) + "\nElo: " + str(infop1["ELO"]) \
                      + "\nRank: " + str(infop1["RANK"]) + "\nRating: " + str(infop1["RATING"])
                embed.add_field(name="Skill Level", value=msg)
                embed.add_field(name='\u200b', value='\u200b')
                msg = "Level: " + str(infop2["LVL"]) + "\nElo: " + str(infop2["ELO"]) \
                      + "\nRank: " + str(infop2["RANK"]) + "\nRating: " + str(infop2["RATING"])
                embed.add_field(name="Skill Level", value=msg)
                """--end"""

                """Matches comparison between them."""
                msg = "All matches: " + str(infop1["MATCHES"]) + "\nWinrate: " + str(infop1["WINRATE"]) \
                      + "\nWins: " + str(infop1["WINS"]) + "\nLoses: " + str(infop1["LOSES"])
                embed.add_field(name="Matches", value=msg)
                embed.add_field(name='\u200b', value='\u200b')
                msg = "All matches: " + str(infop2["MATCHES"]) + "\nWinrate: " + str(infop2["WINRATE"]) \
                      + "\nWins: " + str(infop2["WINS"]) + "\nLoses: " + str(infop2["LOSES"])
                embed.add_field(name="Matches", value=msg)
                """--end"""

                """Rating comparison between them."""
                msg = "K/D Rating: " + str(infop1["KDR"]) + "\nKills Per Round: " + str(infop1["KPR"]) \
                      + "\nKills: " + str(infop1["KILLS"]) + "\nDeaths: " + str(infop1["DEATHS"])
                embed.add_field(name="Average player stats", value=msg)
                embed.add_field(name="\u200b", value="\u200b")
                msg = "K/D Rating: " + str(infop2["KDR"]) + "\nKills Per Round: " + str(infop2["KPR"]) \
                      + "\nKills: " + str(infop2["KILLS"]) + "\nDeaths: " + str(infop2["DEATHS"])
                embed.add_field(name="Average player stats", value=msg)
                """--end"""

                return embed
            else:
                return "Oops, looks like we have some troubles with input! Try something else!"

        elif (faceitmsg + "teammates") in message.content:
            """!faceit teammates"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                nickname = splitts[2]
                info = FACEIT2.faceit_teammates_link(splitts[2])
                title = "Top 3 " + nickname + "'s teammates"
            except AttributeError as e:
                Er.errorlog("AttributeError", str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                Er.errorlog("WebSiteNotFoundException", "Teammates method", str(message.content))
                return "Oops, looks like this nickname does not exist! Try something else"
            except Exception as e:
                Er.errorlog("Exception", "Teammates method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            if len(splitts) == 3:
                emList = []
                count = 0

                embed = discord.Embed(title=title)
                embed.set_author(name="Tokei bot")
                emList.append(embed)

                for i in info:
                    count += 1
                    embed = discord.Embed(title="\u200b")
                    embed.set_footer(text="Statistics were taken from https://www.faceit.com",
                                     icon_url="https://res.cloudinary.com/crunchbase-production/image/upload/"
                                              "c_lpad,f_auto,q_auto:eco,dpr_1/xtrxobrlttwixe1kfzo5")
                    embed.set_author(name=i["NICKNAME"], icon_url=i["IMGSRC"])
                    msg = "Matches: " + i["MATCHES"] + "\nWins: " + i["WINS"] + "\nLoses: " + i["LOSES"] \
                          + "\nWinrate: " + i["WINRATE"]
                    embed.add_field(name="Match stats", value=msg)
                    emList.append(embed)

                return emList
            else:
                return "Oops, looks like we have some troubles with input! Try something else!"

        elif (faceitmsg + "enemies") in message.content:
            """!faceit enemies"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                nickname = splitts[2]
                info = FACEIT2.faceit_enemies_link(splitts[2])
                title = "Top 3 " + nickname + "'s enemies"
            except AttributeError as e:
                Er.errorlog("AttributeError", str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                return "Oops, looks like this nickname does not exists! Try something else"
            except Exception as e:
                Er.errorlog("Exception", "Enemies method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            if len(splitts) == 3:
                emList = []
                count = 0

                embed = discord.Embed(title=title)
                embed.set_author(name="Tokei bot")
                emList.append(embed)

                for i in info:
                    count += 1
                    embed = discord.Embed(title="\u200b")
                    embed.set_footer(text="Statistics were taken from https://www.faceit.com",
                                     icon_url="https://res.cloudinary.com/crunchbase-production/image/upload/"
                                              "c_lpad,f_auto,q_auto:eco,dpr_1/xtrxobrlttwixe1kfzo5")
                    embed.set_author(name=i["NICKNAME"], icon_url=i["IMGSRC"])
                    msg = "Enemy stats: " + i["MATCHES"] + "\nWins: " + i["WINS"] + "\nLoses: " + i["LOSES"] \
                          + "\nWinrate: " + i["WINRATE"]
                    embed.add_field(name="Match stats", value=msg)
                    emList.append(embed)

                return emList
            else:
                return "Oops, looks like we have some troubles with input! Try something else!"

        elif (faceitmsg + "highlights") in message.content:
            """!faceit highlights"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                nickname = splitts[2]
                info = FACEIT3.faceit_highlights(nickname)
            except AttributeError as e:
                Er.errorlog("AttributeError", str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                return "Oops, looks like this nickname does not exists! Try something else"
            except Exception as e:
                Er.errorlog("Exception", "Enemies method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            if len(splitts) == 3:
                emList = []
                count2 = 0
                for x, y in info.items():
                    count2 += 1
                    count = 0
                    title = ""

                    if x == "MKILLS":
                        title = "Most kills"
                    elif x == "BKDR":
                        title = "Best KDR"
                    elif x == "BPLUSM":
                        title = "Best +/-"

                    embed = discord.Embed(title=title)
                    embed.set_footer(text="Statistics were taken from https://www.faceit.com",
                                     icon_url="https://res.cloudinary.com/crunchbase-production/image/upload/"
                                              "c_lpad,f_auto,q_auto:eco,dpr_1/xtrxobrlttwixe1kfzo5")

                    for i in y:
                        if count < 3:
                            kills = i["KILLS"]
                            plus = i["PLMI"]
                            kdr = i["KDR"]

                            if count2 == 1:
                                kills = "**" + i["KILLS"] + "**"
                            elif count2 == 3:
                                plus = "**" + i["PLMI"] + "**"
                            elif count2 == 2:
                                kdr = "**" + i["KDR"] + "**"

                            msg = "Match number: " + i["MATCH"] + "\nDate: " + i["DATE"].replace("-", "/") \
                                  + "\nMap: " + i["MAP"] + "\nScore: " + i["SCORE"].replace("/", ":") \
                                  + "\nK/A/D: " + kills + "/" + i["ASSISTS"] + "/" + i["DEATHS"] + "\n+/- :" + plus \
                                  + "\nKDR: " + kdr
                            embed.add_field(name="\u200b", value=msg)
                        count += 1
                    emList.append(embed)

                return emList
            else:
                return "Oops, looks like we have some troubles with input! Try something else!"

        elif (faceitmsg + "help") == message.content:
            """!faceit help"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                title = "Commands and their description\n\n"
                msg = ""
                msg2 = ""
                embed = discord.Embed(title=title)
                count = 0

                for command, description in FACEIT3.faceitCommands.items():
                    count += 1
                    if count < 4:
                        msg = msg + "**" + command + "**" + "\n" + "*" + description + "*" + "\n"
                    else:
                        msg2 = msg2 + "**" + command + "**" + "\n" + "*" + description + "*" + "\n"

                embed.add_field(name="\u200b", value=msg, inline=False)
                embed.add_field(name="\u200b", value=msg2)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Faceit help method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (faceitmsg + "names") in message.content:
            """!faceit names"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 3:
                    nickname = splitts[2]
                    info = FACEIT3.faceit_names(nickname)
                    embed = discord.Embed(title="Faceit name history")
                    for i in info:
                        msg = "**Last game played:** " + i["LAST_MATCH"].strip("Last ") + "\n**First game played:** "\
                              + i["FIRST_MATCH"].strip("First ")
                        embed.add_field(name=i["NICKNAME"], value=msg)

                    return embed
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Faceit names method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with this nickname! Try it later"
            except WebSiteNotFoundException:
                return "Oops, looks like this nickname does not exists! Try something else"
            except Exception as e:
                Er.errorlog("Exception", "Faceit names method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        else:
            return "Wrong command! Try '!faceit help'"
