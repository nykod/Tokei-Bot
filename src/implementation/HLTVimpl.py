import discord
from commands.HLTVcommands import HLTVStats
from commands.HLTVcommands3 import HLTVStats3
from other.Exceptions import NoOngoingMatchesException
from other.WorkWithFiles import WorkWithErrorLog


class HLTVIMP:
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
        HLTV = HLTVStats()
        HLTV3 = HLTVStats3()
        Er = WorkWithErrorLog()

        if (hltvmsg + "players 12") == message.content:
            """!hltv players 12"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                temp = HLTV.hltv_top_players12()
                title = "***Top 10 players for last 12 months***\n"
                msg = ""

                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                for player in temp:
                    msg = msg + "**Nickname:** " + str(player["nickname"]) + "\n**K/D:** " + str(player["rating"]) \
                          + "\n**HLTV Rating:** " + str(player["hltv_rating"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Players 12 method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "players 6") == message.content:
            """!hltv players 6"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                temp = HLTV.hltv_top_players6()
                title = "***Top 10 players for last 6 months***\n"
                msg = ""
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                for player in temp:
                    msg = msg + "**Nickname:** " + str(player["nickname"]) + "\n**K/D:** " + str(player["rating"]) \
                          + "\n**HLTV Rating:** " + str(player["hltv_rating"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Players 6 method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "help") == message.content:
            """!hltv help"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                title = "Commands and their description\n\n"
                msg = ""
                msg2 = ""
                embed = discord.Embed(title=title)
                count = 0

                for command, description in HLTV.hltvcomhelp.items():
                    count += 1
                    if count < 14:
                        msg = msg + "**" + command + "**" + " - " + "*" + description + "*" + "\n"
                    else:
                        msg2 = msg2 + "**" + command + "**" + " - " + "*" + description + "*" + "\n"

                embed.add_field(name="\u200b", value=msg, inline=False)
                embed.add_field(name="\u200b", value=msg2)
                return embed
            except Exception as e:
                Er.errorlog("Exception", "Help method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "ongoing events") == message.content:
            """!hltv ongoing events"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                temp = HLTV.hltv_ongoing_events()
                title = "Ongoing events\n"
                msg = ""
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                length = len(temp)
                middle = length // 2
                fsthlf = temp[:middle]
                scndhlf = temp[middle:]

                for event in fsthlf:
                    msg = msg + "**Event name:** " + str(event["name"]) + "\n**Started:** " + str(event["from_date"]) \
                          + "\n**Will end:** " + str(event["to_date"]) + "\n\n"
                embed.add_field(name="\u200b", value=msg)

                msg = ""
                if scndhlf[0] is not None:
                    for event in scndhlf:
                        msg = msg + "**Event name:** " + str(event["name"]) + "\n**Started:** " + str(
                            event["from_date"]) \
                              + "\n**Will end:** " + str(event["to_date"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)

                return embed
            except AttributeError as e:
                Er.errorlog("Exception", "Ongoing events method " + str(e), str(message.content))
                return "There are no ongoing events right now"
            except Exception as e:
                Er.errorlog("Exception", "Ongoing events method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "upcoming events") == message.content:
            """!hltv upcoming events"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                temp, tempdate = HLTV.hltv_upcoming_events()
                title = "Upcoming events:\n" + str(tempdate) + "\n\n"
                msg = ""
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                """Because of max characters(1024) we must to split the list on 2 halves"""
                length = len(temp)
                middle = length // 2
                fsthlf = temp[:middle]
                scndhlf = temp[middle:]
                """--end"""

                for event in fsthlf:
                    msg = msg + "**Event name:** " + str(event["name"]) + "\n**Prize:** " + str(event["prize"]) \
                          + "\n**Type:** " + str(event["type"]) + "\n\n"
                embed.add_field(name="\u200b", value=msg)

                msg = ""
                """This if is needed for an extra situation - if there was only 1 item in list. If it is so it means
                 that second half of list should be None"""
                if scndhlf[0] is not None:
                    for event in scndhlf:
                        msg = msg + "**Event name:** " + str(event["name"]) + "\n**Prize:** " + str(event["prize"]) \
                              + "\n**Type:** " + str(event["type"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)
                """--end"""

                return embed
            except Exception as e:
                Er.errorlog("Exception", "Upcoming events method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "results") == message.content:
            """!hltv results"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                temp3, eventname, featured = HLTV.hltv_match_results()
                embList = []
                title = "**" + str(featured) + "**"
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")

                """Because of max characters(1024) we must to split the list on 2 halves"""
                length = len(temp3)
                middle = length // 2
                fsthlf = temp3[:middle]
                scndhlf = temp3[middle:]
                """--end"""

                msg = ""
                for result in fsthlf:
                    msg = msg + "**Event:** " + str(result["event_name"]) + "\n**Match:** " + str(result["team_1"]) \
                          + " " + str(result["score"]) + " " + str(result["team_2"]) + "\n\n"
                embed.add_field(name="\u200b", value=msg)

                msg = ""
                if scndhlf[0] is not None:
                    for result in scndhlf:
                        msg = msg + "**Event:** " + str(result["event_name"]) + "\n**Match:** " + str(result["team_1"]) \
                              + " " + str(result["score"]) + " " + str(result["team_2"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)
                embList.append(embed)

                temptest, day = HLTV.hltv_match_results2()
                title = "**" + day + "**"
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")

                msg = ""
                for result in temptest:
                    msg = msg + "**Event:** " + str(result["event_name"]) + "\n**Match:** " + str(result["team_1"]) \
                          + " " + str(result["score"]) + " " + str(result["team_2"]) + "\n\n"

                embed.add_field(name="\u200b", value=msg)
                embList.append(embed)

                """Return is emList. emList is list of 'embed' objects."""
                return embList
            except Exception as e:
                Er.errorlog("Exception", "Results method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "ongoing matches") == message.content:
            """!hltv ongoing matches"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                matches = HLTV.hltv_match_ongoing()
                title = "**Ongoing matches**\n"
                msg = ""
                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                if matches:
                    """If there are any ongoing matches"""
                    for match in matches:
                        msg = msg + "**Match priority (0-5):** " + str(match["stars"]) + "\n**Match format:** " + str(
                            match["format"]) \
                              + "\n**Teams:** " + str(match["team_1"]) + " - " + str(match["team_2"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)
                    return embed
                else:
                    """If there are not any ongoing matches"""
                    return "There are no ongoing matches"
            except NoOngoingMatchesException:
                return "There are no ongoing matches right now."
            except Exception as e:
                Er.errorlog("Exception", "Ongoing matches method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "upcoming matches") == message.content:
            """!hltv upcoming matches"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                upcoming, unknown, day = HLTV3.hltv_match_upcoming()
                title = "***Upcoming matches***\n" + "*" + day + "*" + "\n\n"
                msg = ""

                """Because of max characters(1024) we must to split the list on 2 halves"""
                length = len(upcoming)
                middle = length // 2
                fsthlf = upcoming[:middle]
                scndhlf = upcoming[middle:]
                """--end"""

                embed = discord.Embed(title=title)
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")

                for match in fsthlf:
                    if isinstance(match, dict):
                        msg = msg + "**Time:** " + str(match["time"]) \
                              + "\n**Match priority(0-5):** " + str(match["stars"]) + "\n**Match format:** " \
                              + str(match["format"]) + "\n**Teams: **" + str(match["team_1"]) \
                              + " : " + str(match["team_2"]) + "\n**Event:** " + str(match["event"]) + "\n\n"
                embed.add_field(name="\u200b", value=msg)

                msg = ""
                """This if is needed for an extra situation - if there was only 1 item in list. If it is so it means
                   that second half of list should be None"""
                if scndhlf[0] is not None:
                    for match in scndhlf:
                        if isinstance(match, dict):
                            msg = msg + "**Time:** " + str(match["time"]) \
                                  + "\n**Match priority(0-5):** " + str(match["stars"]) + "\n**Match format:** " \
                                  + str(match["format"]) + "\n**Teams: **" + str(match["team_1"]) \
                                  + " : " + str(match["team_2"]) + "\n**Event:** " + str(match["event"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)
                """--end"""

                return embed
            except Exception as e:
                Er.errorlog("Exception", "Upcoming matches method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (hltvmsg + "unknown matches") == message.content:
            """!hltv unknown matches"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                upcoming, unknown, day = HLTV3.hltv_match_upcoming()
                embed = discord.Embed(title="Unknown matches")
                embed.set_footer(text="Statistics were taken from https://www.hltv.org",
                                 icon_url="https://www.hltv.org/img"
                                          "/static/TopSmallLogo2x.png")
                msg = ""
                if unknown:
                    """If there are any unknown matches"""
                    for match in unknown:
                        msg = msg + "**Match info:** " + match + "\n"
                    embed.add_field(name="\u200b", value=msg)
                    return embed
                else:
                    """If there is not any unknown match"""
                    return "No matches found"
            except Exception as e:
                Er.errorlog("Exception", "Unknown matches method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        else:
            return None
