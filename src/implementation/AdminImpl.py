import discord

from commands.AdminCommands import AdminComms, HighAdminComms
import shlex


class AdmIMP:
    """
    Class that uses admin commands
    """
    perms = False
    Aperms = False

    def __init__(self, Aperms, perms):
        self.Aperms = Aperms
        self.perms = perms

    def msg_send_adm(self, message):
        """
        This method resends message(which is rewritten for discord) to a discord bot
        :param message: message which we use for recognition if it is a method or not
        :return: return is a message(could be a list, string, embed or list of embeds)
        """
        admmsg = "!admin "
        ADMIN = AdminComms()
        HAdmin = HighAdminComms()

        if (admmsg + "add") in message.content:
            """!admin add ..."""
            if self.Aperms is True:
                if "#" in message.content:
                    cnsl = message.content
                    splitts = cnsl.split()
                    if len(splitts) == 3:
                        ADMIN.setNewAdmin(splitts[2])
                        return "Admin successfully added!"
                    else:
                        return "Oops something bad happened... Try again later"
                else:
                    return "Oops something bad happened... Try again later"

        elif (admmsg + "remove") in message.content:
            """!admin remove ..."""
            if self.Aperms is True:
                if "#" in message.content:
                    cnsl = message.content
                    splitts = cnsl.split()
                    if len(splitts) == 3:
                        ADMIN.removeAdmin(splitts[2])
                        return "Admin successfully removed!"
                    else:
                        return "Oops something bad happened... Try again later"
                else:
                    return "Oops something bad happened... Try again later"
            else:
                return "Not enough permissions"

        elif (admmsg + "block") in message.content:
            """!admin block ..."""
            if self.perms is True:
                cnsl = message.content
                splitts = shlex.split(cnsl)
                try:
                    HAdmin.blockCommand(splitts[2])
                    return "Command successfully blocked!"
                except Exception:
                    return "Oops something bad happened... Try again later"
            else:
                return "Not enough permissions"

        elif (admmsg + "unblock") in message.content:
            """!admin unblock ..."""
            if self.perms is True:
                cnsl = message.content
                splitts = shlex.split(cnsl)
                try:
                    HAdmin.unblockCommand(splitts[2])
                    return "Command successfully unblocked!"
                except Exception:
                    return "Oops something bad happened... Try again later"
            else:
                return "Not enough permissions"

        elif (admmsg + "help") == message.content:
            if self.perms is True:
                try:
                    title = "Commands and their description\n\n"
                    msg = ""
                    embed = discord.Embed(title=title)

                    for command, description in ADMIN.comhelp.items():
                        msg = msg + "**" + command + "**" + "\n" + "*" + description + "*" + "\n"

                    embed.add_field(name="\u200b", value=msg)
                    return embed
                except Exception:
                    return "Oops something bad happened... Try again later"
            else:
                return "Not enough permissions"
