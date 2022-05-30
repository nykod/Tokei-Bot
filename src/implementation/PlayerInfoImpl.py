import discord
from other.WorkWithFiles import WorkWithErrorLog
from commands.PlayersInfo import Players


class PlayerInfoIMP:
    """
    Class with commands which are parsing page for information
    """
    def msg_send_plr(self, message):
        """
        This method resends message(which is rewritten for discord) to a discord bot
        :param message: message which we use for recognition if it is a method or not
        :return: return is a message(could be a list, string, embed or list of embeds)
        """
        playermsg = "!player "
        Player = Players()
        Er = WorkWithErrorLog()

        # TODO CHECK WRONG PLAYERS NICKNAME
        if (playermsg + "settings") in message.content:
            """!player settings"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                temp2, monitorsettings = Player.player_settings(splitts[2])


                if len(splitts) == 3:

                    embed = discord.Embed(title="Player settings", colour=discord.Colour(0xFF9F00))
                    embed.set_footer(text="Statistics were taken from https://csgopedia.com",
                                     icon_url="https://frozesport.dk/template/thenewclassy/stuff/img/gametypes/CSGO.png")

                    msg = "**DPI:** " + str(temp2["DPI"]) + "\n**Sensitivity:** " + str(temp2["sensitivity"]) \
                          + "\n**eDPI:** " + str(temp2["eDPI"]) + "\n**Zoom sensitivity:** " + str(temp2["zoom-sens"]) \
                          + "\n**Mouse acceleration:** " + str(temp2["mouse_ac"]) \
                          + "\n**m_rawinput:** " + str(temp2["rawinp"])

                    embed.add_field(name="Game settings", value=msg)

                    msg = "**Resolution:** " + str(monitorsettings["resolution"]) + "\n**AR:** " + str(
                          monitorsettings["AR"]) + "\n**Scaling:** " + str(monitorsettings["scaling"])\
                          + "\n**Frame rate:** " + str(monitorsettings["frames"])

                    embed.add_field(name="Monitor settings", value=msg)

                    return embed
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Player settings method " + str(e), str(message.content))
                return "Oops, it looks like we have some troubles with this nickname... Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except IndexError as e:
                Er.errorlog("IndexError", "Player settings method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with input! Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Player settings method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (playermsg + "stats") in message.content:
            """!player stats"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                stats = Player.player_stats(splitts[2])

                if len(splitts) == 3:
                    msg = "***Player stats*** *(last 3 months)*\n"
                    msg = msg + "**K/D:** " + str(stats["K/D"]) + "\n**K/D difference:** " + str(stats["diff"]) \
                          + "\n**Rating(2.0):** " + str(stats["rating"]) + "\n**Maps played:** " + str(stats["maps"]) \
                          + "\n**Kills per rounds:** " + str(stats["kpr"]) + "\n**Death per round:** " + str(stats["dpr"]) \
                          + "\n**Headshot percentage:** " + str(stats["hs"]) + "\n**Rounds contributed:** " \
                          + str(stats["rndscon"]) + "\n\n"
                    return msg
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Player stats method " + str(e), str(message.content))
                return "Oops, it looks like we have some troubles with this nickname... Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except IndexError as e:
                Er.errorlog("IndexError", "Player stats method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with input! Try it later"

        elif (playermsg + "info") in message.content:
            """!player info"""
            try:
                cnsl = message.content
                splitts = cnsl.split()
                info = Player.player_info(splitts[2])

                if len(splitts) == 3:
                    embed = discord.Embed(title="Player's information", colour=discord.Colour(0xFF9F00))
                    embed.set_footer(text="Statistics were taken from https://csgopedia.com",
                                     icon_url="https://frozesport.dk/template/thenewclassy/stuff/img/gametypes/CSGO.png")

                    msg = str(info["name"]) + ' *"' + str(info["nickname"]) + '"* ' + str(info["surname"]) \
                          + "\n**Country:** " + str(info["country"]) + "\n**Age:** " + str(info["age"]) \
                          + "\n**Team:** " + str(info["team"]) + "\n\n"
                    embed.add_field(name="\u200b", value=msg)

                    return embed
                else:
                    return "Oops, looks like we have some troubles with input! Try something else!"
            except AttributeError as e:
                Er.errorlog("AttributeError", "Player info method " + str(e), str(message.content))
                return "Oops, it looks like we have some troubles with this nickname... Try it later"
            except AssertionError:
                return "Oops, looks like we have some troubles with input! Try it later"
            except IndexError as e:
                Er.errorlog("IndexError", "Player info method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with input! Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Player info method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"

        elif (playermsg + "help") == message.content:
            """!player help"""
            """Gets value/list of values from a method. Method is without any inputs."""
            try:
                title = "Commands and their description\n\n"
                msg = ""
                embed = discord.Embed(title=title)

                for command, description in Player.playercomhelp.items():
                    msg = msg + "**" + command + "**" + "\n" + "*" + description + "*" + "\n"

                embed.add_field(name="\u200b", value=msg, inline=False)
                return embed
            except IndexError as e:
                Er.errorlog("IndexError", "Player help method " + str(e), str(message.content))
                return "Oops, looks like we have some troubles with input! Try it later"
            except Exception as e:
                Er.errorlog("Exception", "Player help method " + str(e), str(message.content))
                return "Oops, something bad happened... Try it later"
        else:
            return "Wrong command! Try '!player help'"
