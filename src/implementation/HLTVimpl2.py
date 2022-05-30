import discord
from commands.HLTVcommands2 import HLTVStats2
from commands.HLTVcommands3 import HLTVStats3
from commands.HLTVcommands4 import HLTVStats4
from other.Exceptions import IllegalArgumentException, PlayerNotFoundException, MatchBoxListException, \
    WebSiteNotFoundException
from other.WorkWithFiles import WorkWithErrorLog
from other.WorkWithFiles import WorkWithCSV


class HLTVIMP2:
    """
    Class that implements methods from other classes and sends return message to bot.py
    """

    """Needed for !hltv leaderboard help"""
    tableDict = {"RATING": "Rating 2.0",
                 "DAMAGE": "Damage per round",
                 "KILLS": "Total kills",
                 "DPR": "Deaths per round",
                 "ASSISTS": "Total assists",
                 "KAST": "KAST",
                 "CLUTCHES": "Clutches (1vsX) won",
                 "HEADSHOTS": "Headshots per round",
                 "AWP": "Total AWP kills",
                 "OPEN": "Total opening kills",
                 "DUELS": "Success in opening duels"}

    def msg_send_hltv(self, message):
        """
        This method resends message(which is rewritten for discord) to a discord bot
        :param message: message which we use for recognition if it is a method or not
        :return: return is a message(could be a list, string, embed or list of embeds)
        """
        hltvmsg = "!hltv "
        HLTV2 = HLTVStats2()
        HLTV3 = HLTVStats3()
        HLTV4 = HLTVStats4()
        ErClass = WorkWithErrorLog()
        csvfile = WorkWithCSV()

        if (hltvmsg + "achievements") in message.content:
            """!hltv achievements"""
            """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 3:
                    teamname = splitts[2]

                    # ERR103
                    try:
                        test = int(teamname)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception as e:
                        ErClass.errorlog("Exception", "ERR103 -> " + str(e), str(message.content))

                    info = HLTV4.hltv_team_achievements(teamname)
                elif len(splitts) == 4:
                    teamname = splitts[2] + " " + splitts[3]
                    # ERR103
                    try:
                        try:
                            test = int(teamname)
                            return "Oops, you tried invalid input! Try it later"
                        except Exception as e:
                            ErClass.errorlog("Exception", "ERR103 -> " + str(e), str(message.content))

                        info = HLTV4.hltv_team_achievements(teamname)
                    except FileNotFoundError as e:
                        ErClass.errorlog("Exception", "ERR206 -> " + str(e), str(message.content))
                        return "Oops, it looks like our file is damaged. Try it later."
                else:
                    raise IllegalArgumentException
            except IllegalArgumentException:
                return "Oops, you tried invalid input! Try it later"
            except WebSiteNotFoundException as e:
                ErClass.errorlog("WebSiteNotFoundException", "ERRXXX -> " + str(e), str(message.content))
                return "Oops, it looks like we cant find this team... Try it later"
            except Exception as e:
                ErClass.errorlog("Exception", "Achievements method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            """--end"""

            title = "List of last " + str(len(info)) + " " + teamname.title() + "'s LAN achievements"

            embed = discord.Embed(title=title)
            embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                             icon_url="https://www.hltv.org/img"
                                      "/static/TopSmallLogo2x.png")
            msg = ""
            for i in info:
                keyList = list(i.keys())
                for j in keyList:
                    eventName = j.strip("\n")
                    valueOut = i[j]
                    msg = msg + "**" + valueOut + "**   " + "***" + eventName + "***\n"

            embed.add_field(name="\u200b", value=msg)
            return embed

        elif (hltvmsg + "career") in message.content:
            """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                graph = HLTV2.hltv_player_career(splitts[2])
                title = "***" + splitts[2] + " career***\n"
                msg = graph
                return [title, msg]
            except ValueError:
                return "Oops, something bad happened with count! Try it later"
            except KeyError:
                return ("Oops, it looks like we have some troubles with this nickname..."
                        " Try it later")
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except Exception as e:
                ErClass.errorlog("Exception", "carrer method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "leaderboard") in message.content:
            """!hltv leaderboard"""
            """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
            """Check if message.content contains '!hltv leaderboard help'"""
            if "!hltv leaderboard help" == message.content:
                msg = ""
                embed = discord.Embed(title="**[OPTION** - Statistics**]**\n")
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                embed.set_author(name="Tokei bot")
                for key, item in self.tableDict.items():
                    msg = msg + "**" + key + "**" + " - " + item + "\n"
                msg = msg + "\n**!hltv leaderboard** *'an option'*"
                embed.add_field(name="\u200b", value=msg)
                return embed
            else:
                """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
                try:
                    leaderboard = HLTV3.hltv_leaderboard()
                    """leaderboard structure: list[dict{'key': [{'key':{'key':'value'}}]}] - it's awful but why not:)"""

                    cnsl = message.content
                    splitts = cnsl.split()
                    embed = ""
                    msg = ""
                    """--end"""

                    """Gets all information from a method - there are Dictionary in Dictionary in list etc. which makes
                     harder to get information out of there"""
                    for i in leaderboard:
                        """List"""
                        keyList = list(i.keys())
                        temp = self.tableDict[splitts[2].upper()]
                        for k in keyList:
                            """List of dict.keys"""
                            if temp in k:
                                title = "***" + temp + "***\n"
                                embed = discord.Embed(title="***Leaderboard - " + title + "***\n")
                                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                                 icon_url="https://www.hltv.org/img"
                                                          "/static/TopSmallLogo2x.png")
                                embed.set_author(name="Tokei bot")
                                templist = i[temp]
                                for j in templist:
                                    templist2 = j.keys()
                                    for x in templist2:
                                        if "leader" in x:
                                            tempkey = list(j[x].keys())
                                            name = str(tempkey[0].rstrip("-"))
                                            val = j[x][tempkey[0]]
                                            msg = msg + "**" + name + "**\n" + val + "\n**-----**\n"
                                        else:
                                            tempkey = list(j[x].keys())
                                            name = tempkey[0].rstrip("-")
                                            val = j[x][tempkey[0]]
                                            msg = msg + "**" + name + "**\n" + val + "\n**-----**\n"
                                embed.add_field(name="**Leader**", value=msg)
                            msg = ""
                    """--end"""
                    return embed
                except IndexError:
                    return 'Oops, we do not have statistic about that... Try "!hltv leaderboard help"'
                except KeyError:
                    return 'Oops, we do not have statistic about that... Try "!hltv leaderboard help"'
                except Exception as e:
                    ErClass.errorlog("Exception", "Leaderboard method " + str(e), str(message.content))
                    return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "last match") in message.content:
            """!hltv last match"""
            """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 4:
                    name = splitts[3]

                    teamBool = False
                    info = None
                    img = None

                    try:
                        test = int(name)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception:
                        pass
                    """Checks if its player"""
                    try:
                        code = csvfile.get_info_player()[name]
                    except KeyError:
                        """If it is not player it will raise KeyError and then it will check if it is team"""
                        team = name.lower()
                        if " " in team:
                            team = team.replace(" ", "-")
                        try:
                            code = csvfile.get_info_teams()[team]
                            teamBool = True
                        except FileNotFoundError as e:
                            ErClass.errorlog("FileNotFoundError", "ERR105 -> " + str(e), str(message.content))
                            return "Oops, it looks like we have some problems with this value... Try it later"
                        except KeyError as e:
                            ErClass.errorlog("KeyError", "Last match method " + str(e), str(message.content))
                            return "Oops, it looks like we cannot find this player/team... Try something else"

                    if teamBool is False:
                        """if it is not a team (teamBool = False) - then that's calling player method"""
                        retInfo = HLTV3.hltv_lastmatch_player(name)
                        if isinstance(retInfo, list):
                            info = retInfo[0]
                            img = retInfo[1]
                        else:
                            raise PlayerNotFoundException
                    else:
                        """else it is a team it is calling team method"""
                        info = HLTV4.hltv_lastmatch_team(name)

                elif len(splitts) == 5:

                    teamBool = False
                    info = None
                    img = None

                    name = splitts[3] + " " + splitts[4]
                    team = name.lower()
                    if " " in team:
                        team = team.replace(" ", "-")
                    try:
                        code = csvfile.get_info_teams()[team]
                        teamBool = True
                    except FileNotFoundError as e:
                        ErClass.errorlog("FileNotFoundError", "ERR105 -> " + str(e), str(message.content))
                        return "Oops, it looks like we have some problems with this value... Try it later"
                    except KeyError as e:
                        ErClass.errorlog("KeyError", "Last match method " + str(e), str(message.content))
                        return "Oops, it looks like we cannot find this player/team... Try something else"
                    info = HLTV4.hltv_lastmatch_team(name)
                else:
                    raise IllegalArgumentException
            except IllegalArgumentException as e:
                ErClass.errorlog("Exception", "ERR601 -> " + str(e), str(message.content))
                return "Oops, you tried invalid input! Try it later"
            except PlayerNotFoundException as e:
                ErClass.errorlog("Exception", "ERR603 -> " + str(e), str(message.content))
                return "Oops, we have problem with this player last match... Try it later"
            except FileNotFoundError as e:
                ErClass.errorlog("FileNotFoundError", "ERR105 -> " + str(e), str(message.content))
                return "Oops, it looks like we have some problems with this player... Try it later"
            except MatchBoxListException as e:
                ErClass.errorlog("Exception", "ERR602 -> " + str(e), str(message.content))
                return "Oops, it looks like something bad happened... Try it later"
            except KeyError as e:
                ErClass.errorlog("KeyError", "Last match method " + str(e), str(message.content))
                return "Oops, it looks like we cannot find this player/team... Try something else"
            except Exception as e:
                ErClass.errorlog("Exception", "Last match method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

            """If it is a player"""
            if teamBool is False:
                title = "***" + info["NICKNAME"] + "*** - Last match stats\n"
                embed = discord.Embed(title=title)
                embed.set_image(url=img)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                embed.set_author(name="Tokei bot")
                embed.add_field(name="Kills", value=info["KILLS"])
                embed.add_field(name="Assists", value=info["ASSISTS"])
                embed.add_field(name="Deaths", value=info["DEATHS"])
                embed.add_field(name="KAST", value=info["KAST"])
                embed.add_field(name="ADR", value=info["ADR"])
                embed.add_field(name="First kills difference", value=info["FIRSTKILLS"])
                embed.add_field(name="K/D 2.0", value=info["KD20"])
                """--end"""
                return embed
            else:
                """If it is a team"""
                title = "***" + name + "*** - Last match stats\n"
                embed = discord.Embed(title=title)
                if img is not None:
                    embed.set_image(url=img)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                embed.add_field(name="Score", value=info["score"], inline=False)
                embed.add_field(name="Event time info", value="Time: " + info["time"] + "\nDay: " +
                                                              info["day"] + "\nEvent: " + info["event"], inline=False)
                msg = ""
                for i in info["MAPS"]:
                    msg = msg + "Map: " + i["NAME"] + "\n" + i["LOST"] + " " + i["LOST_SCORE"] + " : " \
                          + i["WON_SCORE"] + " " + i["WON"] + "\n"
                embed.add_field(name="Maps", value=msg, inline=False)
                """--end"""
                return embed

        else:
            return None
