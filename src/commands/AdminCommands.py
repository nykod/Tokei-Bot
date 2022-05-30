import json
import os
from other.WorkWithFiles import WorkWithJSON, WorkWithBlockedJSON


class AdminComms:
    """
    Commands for admins with highest admin permissions
    """
    JSONw = WorkWithJSON()
    JSONBlocked = WorkWithBlockedJSON()

    comhelp = {
        "!admin add 'discord username with code'": "Adds new admin",
        "!admin remove 'discord username with code'": "Removes an admin",
        '!admin block "command that you want to be blocked"': "Blocks commands",
        '!admin unblock "command that you want to be blocked"': "Unblocks commands"
    }

    def setNewAdmin(self, admin):
        """
        Method adds new admin
        :param admin: admin nickname we want to add
        :return: there is no return(Except if the file with blocked commands is missing)
        """
        assert isinstance(admin, str)

        """If config file does not exists it will create him and try method once again."""
        if os.path.isfile("../json/admins.json"):

            loaded = self.JSONw.loadjson()
            with open("../json/admins.json", "w", encoding='UTF8') as file:
                templist = list(loaded.keys())
                tempval = len(templist) + 1
                loaded["L_ADMIN" + str(tempval)] = admin
                json.dump(loaded, file, ensure_ascii=False, indent=4)
        else:
            """if file does not exists"""
            self.JSONw.dfconfigjson()
            return self.setNewAdmin(admin)
        """--end"""

    def removeAdmin(self, admin):
        """
        Method removes an admin
        :param admin: admin nickname we want to remove
        :return: there is no return(Except if the file with blocked commands is missing)
        """
        assert isinstance(admin, str)

        """If config file does not exists it will create him and try method once again."""
        if os.path.isfile("../json/admins.json"):
            loaded = self.JSONw.loadjson()
            with open("../json/admins.json", "w", encoding='UTF8') as file:
                templist = list(loaded.keys())
                for key, value in dict(loaded).items():
                    if value == admin:
                        del loaded[key]
                json.dump(loaded, file, ensure_ascii=False, indent=4)
        else:
            """if file does not exists"""
            self.JSONw.dfconfigjson()
            return self.removeAdmin(admin)
        """--end"""


class HighAdminComms:
    """
    Commands for admins with default admin permissions
    """
    JSONBlocked = WorkWithBlockedJSON()

    def blockCommand(self, command):
        """
        Method blocks a command
        :param command: command we want to be blocked
        :return: there is no return(Except if the file with blocked commands is missing)
        """
        assert isinstance(command, str)
        """If config file does not exists it will create him and try method once again."""
        if os.path.isfile("../json/blocked.json"):
            loaded = self.JSONBlocked.loadjson()
            with open("../json/blocked.json", "w", encoding='UTF8') as file:
                loaded[command] = "blocked"
                json.dump(loaded, file, ensure_ascii=False, indent=4)
        else:
            """if file does not exists"""
            self.JSONBlocked.dfconfigjson()
            return self.blockCommand(command)
        """--end"""

    def unblockCommand(self, command):
        """
        Method unblocks an command
        :param command: command we want to be unblocked
        :return: there is no return(Except if the file with blocked commands is missing)
        """
        assert isinstance(command, str)

        """If config file does not exists it will create him and try method once again."""
        if os.path.isfile("../json/blocked.json"):
            loaded = self.JSONBlocked.loadjson()
            with open("../json/blocked.json", "w", encoding='UTF8') as file:
                for key, value in dict(loaded).items():
                    if key == command:
                        del loaded[key]
                json.dump(loaded, file, ensure_ascii=False, indent=4)
        else:
            """if file does not exists"""
            self.JSONBlocked.loadjson()
            return self.unblockCommand(command)
        """--end"""


