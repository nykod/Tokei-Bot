import discord
from commands.HLTVcommands4 import HLTVStats4
from commands.HLTVcommands3 import HLTVStats3
from commands.HLTVcommands2 import HLTVStats2
from commands.HLTVcommands import HLTVStats
from other.WorkWithFiles import WorkWithErrorLog
from other.Exceptions import IllegalArgumentException, WebSiteNotFoundException
import datetime


class HLTVIMP3:
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
        ErClass = WorkWithErrorLog()
        Er = WorkWithErrorLog()

        if (hltvmsg + "team ranking 30") == message.content:
            """!hltv team ranking 30"""
            try:
                """Gets value/list of values from a method. Method is without any inputs."""
                temp = HLTV4.hltv_teams_ranking3()
                mydate = datetime.datetime.now()
                today = datetime.date.today()
                yearday = today.strftime("%d, %Y")
                title = "Top 21-30 teams on " + mydate.strftime("%B") + " " + yearday + "\n"

                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                msg = ""
                for team in temp:
                    msg = msg + "" + str(team["position"]) + " " + str(team["name"]) \
                          + " " + str(team["points"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)

                return embed
            except Exception as e:
                Er.errorlog("Exception", "Team ranking 30 method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "team history") in message.content:
            """!hltv team history"""
            """Calls method 'team history' for a player"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                infoteams, infobreakdown, img = HLTV3.hltv_player_team_history(splitts[3])
                msg = ""
                if len(splitts) == 4:
                    embed = discord.Embed(title="***" + splitts[3] + "'s team stats***")

                    embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                     icon_url="https://www.hltv.org/img"
                                              "/static/TopSmallLogo2x.png")
                    embed.set_image(url=img)
                    embed.set_author(name="Tokei bot")

                    for i in infoteams:
                        keyList = list(i.keys())
                        for k in keyList:
                            msg = msg + "**" + str(k) + "**: " + str(i[k]) + "\n"

                    embed.add_field(name="***Team stats for " + splitts[3] + "***", value=msg)

                    msg = ""

                    for i in infobreakdown:
                        msg = msg + "**Period**: " + str(i["period"]) + "\n" + "**Team**: " + \
                              str(i["team"]).replace("\n", "") + "\n-----\n"

                    msg = msg.rstrip("-----\n")
                    embed.add_field(name="***Breakdown of " + splitts[3] + "'s teams***", value=msg)

                    return embed
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except ValueError:
                return "Oops, something bad happened with count! Try it later"
            except KeyError:
                return "Oops, it looks like we have some troubles with this nickname... Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except FileNotFoundError as e:
                ErClass.errorlog("FileNotFoundError", "ERR105 -> " + str(e), message.content)
                return "Oops, it looks like our database is damaged. Try it later."
            except Exception as e:
                Er.errorlog("Exception", "Team history method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "team ranking 10") == message.content:
            """!hltv team ranking 10"""
            try:
                """Gets value/list of values from a method. Method is without any inputs."""
                temp = HLTV.hltv_teams_ranking()
                mydate = datetime.datetime.now()
                today = datetime.date.today()
                yearday = today.strftime("%d, %Y")

                title = "Top 10 teams on " + mydate.strftime("%B") + " " + yearday + "\n"
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                msg = ""
                """Position/Name/Points"""
                for team in temp:
                    msg = msg + "" + str(team["position"]) + " " + str(team["name"]) \
                          + " " + str(team["points"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Team ranking 10 method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "team ranking 20") == message.content:
            """!hltv team ranking 20"""
            try:
                """Gets value/list of values from a method. Method is without any inputs."""
                temp = HLTV.hltv_teams_ranking2()
                mydate = datetime.datetime.now()
                today = datetime.date.today()
                yearday = today.strftime("%d, %Y")
                title = "Top 11-20 teams on " + mydate.strftime("%B") + " " + yearday + "\n"

                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                msg = ""
                """Values: Position/Name/Points"""
                for team in temp:
                    msg = msg + "" + str(team["position"]) + " " + str(team["name"]) \
                          + " " + str(team["points"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Team ranking 20 method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "news") == message.content:
            """!hltv news"""
            try:
                """Gets value/list of values from a method. Method is without any inputs."""
                newslist = HLTV3.hltv_news()
                middle = len(newslist) // 2
                list_full = [newslist[:middle], newslist[middle:]]

                embed = discord.Embed(title="***HLTV news***")
                embed.set_footer(text="News were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img/static/TopSmallLogo2x.png")
                embed.set_author(name="Tokei bot")

                """Values: Article/webpage/Time(how many days ago)"""
                for i in list_full:
                    for news in i:
                        for key in news.keys():
                            article = str(news[key]["article"])
                            weblink = str(news[key]["site"])
                            embed.add_field(name=news[key]["time"],
                                            value="[" + article + "](" + weblink + ")", inline=False)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "News method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "player") in message.content:
            """!hltv player"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                info, img = HLTV2.hltv_player_stats(splitts[2])

                if len(splitts) == 3:
                    """Values: KD2.0/DPR/KAST/ADR/IMPACT/RATING/KPR"""
                    msg = "\n**K/D 2.0:** " + str(info["2.0"]) + "\n**DPR:** " + str(info["DPR"]) + "\n**KAST:** " \
                          + str(info["KAST"]) + "\n**Impact:** " + str(info["IMPACT"]) + \
                          "\n**ADR:** " + str(info["ADR"]) + "\n**KPR:** " + str(info["KPR"]) + "\n\n**RATING:** " \
                          + str(info["FFRATING"]) + "\n\n"

                    embed = discord.Embed(title="***" + splitts[2] + " stats***")

                    embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                     icon_url="https://www.hltv.org/img"
                                              "/static/TopSmallLogo2x.png")
                    embed.set_image(url=img)
                    embed.set_author(name="Tokei bot")
                    embed.add_field(name="Last 3 months", value=msg)

                    return embed
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except ValueError as e:
                Er.errorlog("ValueError", "Player method " + str(e), str(message.content))
                return "Oops, something bad happened with count! Try it later"
            except KeyError as e:
                Er.errorlog("KeyError", "Player method " + str(e), str(message.content))
                return ("Oops, it looks like we have some troubles with this nickname..."
                        " Try it later")
            except AssertionError:
                return "Oops, looks like we have some troubles with input!"
            except FileNotFoundError as e:
                Er.errorlog("FileNotFoundError", "Player method " + str(e), str(message.content))
                return "Oops, it looks like our database is damaged. Try it later."
            except Exception as e:
                Er.errorlog("Exception", "Player method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "team information") in message.content:
            """!hltv team information"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                if len(splitts) == 4:
                    teamname = splitts[3]
                    info, players = HLTV2.hltv_team_info(teamname)
                elif len(splitts) == 5:
                    teamname = splitts[3] + " " + splitts[4]
                    info, players = HLTV2.hltv_team_info(teamname)
                else:
                    raise IllegalArgumentException
            except IllegalArgumentException as e:
                Er.errorlog("IllegalArgumentException", "Team information method " + str(e), str(message.content))
                return "Oops, you tried invalid input! Try it later"
            except FileNotFoundError as e:
                Er.errorlog("FileNotFoundError", "Team information method " + str(e), str(message.content))
                return "Oops, it looks like our database is damaged. Try it later."
            except AssertionError:
                return "Oops, looks like we have some troubles with input!"
            except IndexError as e:
                Er.errorlog("IndexError", "Team information method " + str(e), str(message.content))
                return "Oops, we have problem with this team (may be problem is not on our side)... Try it later"
            except WebSiteNotFoundException as e:
                Er.errorlog("WebSiteNotFoundException", "ERRXXX -> " + str(e), str(message.content))
                return "Oops, it looks like we cant find this team... Try it later"

            titleField = "***" + info["name"].title() + "***"

            embed = discord.Embed(title="Team information")
            embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                             icon_url="https://www.hltv.org/img"
                                      "/static/TopSmallLogo2x.png")

            """Values: REGION/WEEKS IN TOP 30/HLTV RANK/AVERAGE AGE/COACH"""
            msg = "\n**Region:** " + str(info["region"]) + "\n**HLTV Rank:** " + str(info["rank"]) \
                  + "\n**Weeks in top 30:** " + str(info["weeks"]) + "\n**Average age:** " + str(info["age"]) \
                  + "\n**Coach:** " + str(info["coach"]) + "\n\n"

            embed.add_field(name=titleField, value=msg)

            msg = ""

            """Getting players from a list"""
            for player in players:
                msg = msg + player + ", "

            msg = msg.rstrip(", ")
            embed.add_field(name="Roster", value=msg, inline=False)

            return embed

        else:
            return None
