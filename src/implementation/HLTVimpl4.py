import discord
from commands.HLTVcommands4 import HLTVStats4
from commands.HLTVcommands3 import HLTVStats3
from commands.HLTVcommands2 import HLTVStats2
from commands.HLTVcommands import HLTVStats
from other.WorkWithFiles import WorkWithErrorLog
from other.Exceptions import IllegalArgumentException, WebSiteNotFoundException, NoMapsException


class HLTVIMP4:
    """
    Class that implements methods from other classes and sends return message to bot.py
    """
    def msg_send_hltv(self, message):
        """
        This method resends message(which is rewritten for discord) to a discord bot
        :param message: message which we use for recognition if it is a method or not
        :return: return is a message(could be a list, string, embed or list of embeds)
        """
        hltvmsg = "!hltv "
        HLTV4 = HLTVStats4()
        HLTV3 = HLTVStats3()
        HLTV2 = HLTVStats2()
        HLTV = HLTVStats()
        Er = WorkWithErrorLog()

        if (hltvmsg + "matches") in message.content:
            """!hltv matches"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 3:
                    teamname = splitts[2]

                    try:
                        test = int(teamname)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception:
                        pass
                    try:
                        info = HLTV2.hltv_recent_matches(teamname)
                        info2 = HLTV4.hltv_upcoming_matches(teamname)
                    except FileNotFoundError:
                        return "Oops, it looks like our database is damaged. Try it later."
                    except WebSiteNotFoundException as e:
                        Er.errorlog("WebSiteNotFoundException", "ERRXXX -> " + str(e), str(message.content))
                        return "Oops, it looks like we cant find this team... Try it later"
                elif len(splitts) == 4:
                    teamname = splitts[2] + " " + splitts[3]

                    try:
                        test = int(teamname)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception:
                        pass

                    try:
                        info = HLTV2.hltv_recent_matches(teamname)
                        info2 = HLTV4.hltv_upcoming_matches(teamname)
                    except FileNotFoundError as e:
                        Er.errorlog("FileNotFoundError", "Matches method " + str(e), str(message.content))
                        return "Oops, it looks like our database is damaged. Try it later."
                    except WebSiteNotFoundException as e:
                        Er.errorlog("WebSiteNotFoundException", "ERRXXX -> " + str(e), str(message.content))
                        return "Oops, it looks like we cant find this team... Try it later"
                else:
                    raise IllegalArgumentException
            except IllegalArgumentException as e:
                Er.errorlog("IllegalArgumentException", "Matches method " + str(e), str(message.content))
                return "Oops, you tried invalid input! Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Matches method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

            embed = discord.Embed(title="Upcoming matches for " + teamname.title())
            embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                             icon_url="https://www.hltv.org/img"
                                      "/static/TopSmallLogo2x.png")
            msg = ""
            emList = []

            if isinstance(info2, list):
                for i in info2:
                    keyList = list(i.keys())
                    for k in keyList:
                        eventName = k.strip("\n")
                        msg = msg + "***" + eventName + "***\n"
                        valueOut = i[k]
                        for j in valueOut:
                            msg = msg + "**Match:** " + j["match"] + "  **Date:** " + j["date"] + "\n"
                        msg = msg + "\n\n"
            else:
                msg = msg + info2

            embed.add_field(name="\u200b", value=msg)
            emList.append(embed)

            embed = discord.Embed(title="Recent results for " + teamname.title())
            embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                             icon_url="https://www.hltv.org/img"
                                      "/static/TopSmallLogo2x.png")

            msg = ""
            for i in info:
                keyList = list(i.keys())
                for k in keyList:
                    eventName = k.strip("\n")
                    msg = msg + "***" + eventName + "***\n"
                    valueOut = i[k]
                    for j in valueOut:
                        msg = msg + "**Match:** " + j["match"] + "\n**Date:** " + j["date"] + "\n"
                    msg = msg + "\n"
            embed.add_field(name="\u200b", value=msg)
            emList.append(embed)

            return emList

        elif (hltvmsg + "maps") in message.content:
            """!hltv maps"""
            """Getting value/values from a method. Many try catches, which writes errors in Error log file"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 3:
                    teamname = splitts[2]
                    try:
                        test = int(teamname)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception:
                        pass

                    info = HLTV2.hltv_team_maps(teamname)
                elif len(splitts) == 4:
                    teamname = splitts[2] + " " + splitts[3]

                    try:
                        test = int(teamname)
                        return "Oops, you tried invalid input! Try it later"
                    except Exception:
                        pass

                    info = HLTV2.hltv_team_maps(teamname)
                else:
                    raise IllegalArgumentException
            except IllegalArgumentException:
                return "Oops, you tried invalid input! Try it later"
            except WebSiteNotFoundException as e:
                Er.errorlog("WebSiteNotFoundException", "ERRXXX -> " + str(e), str(message.content))
                return "Oops, it looks like we cant find this team... Try it later"
            except FileNotFoundError as e:
                Er.errorlog("FileNotFoundError", "ERR105 -> " + str(e), str(message.content))
                return "Oops, it looks like our database is damaged. Try it later."
            except NoMapsException:
                Er.errorlog("NoMapsException", "ERR606", message.content)
                return "Oops, it looks like team has not played a match in 3 past months. Try it later."
            except Exception as e:
                Er.errorlog("Exception", "Maps method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
            """--end"""

            embed = discord.Embed(title="***Map win statistics past 3 months***\n")
            embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                             icon_url="https://www.hltv.org/img"
                                      "/static/TopSmallLogo2x.png")
            embed.set_author(name="Tokei bot")

            for i in info:
                keyList = list(i.keys())
                for k in keyList:
                    map = "**Map:** " + k
                    msg = "**Win %:** " + i[k] + "\n"
                    embed.add_field(name=map, value=msg)
            return embed

        else:
            return "Wrong command! Try '!hltv help'"
