import csv
import json
import lxml.etree
import lxml.builder
from datetime import datetime
import os


class WorkWithCSV:
    """
    Class that works with CSV files
    """

    def get_info_player(self):
        """
        Gets players from csv file
        :return: playerdict(dictionary - {nickname: idcode})
        """
        playerdict = {}
        with open("../csv/HLTV_players.csv", newline="") as file:
            output = csv.DictReader(file, delimiter="/")
            for i in output:
                playerdict[i["nickname"]] = i["idcode"]
        return playerdict

    def get_info_teams(self):
        """
        Gets teams from csv file
        :return: teamsdict(dictionary - {nickname: idcode})
        """
        teamsdict = {}
        with open("../csv/HLTV_teams.csv", newline="") as file:
            output = csv.DictReader(file, delimiter="/")
            for i in output:
                teamsdict[i["team"]] = i["idcode"]
        return teamsdict


class WorkWithErrorLog:
    """
    Class that works with Error log
    """
    def errorlog(self, err, erreas, inp):
        """
        Error log
        :param inp: Input(message that was sent)
        :param err: Error
        :param erreas: Error description
        :return:
        """
        if os.path.exists('../log/error.log'):
            pass
        else:
            with open("../log/error.log", "w") as file:
                file.write("")

        dtime = datetime.now()

        EM = lxml.builder.ElementMaker()
        ExceptionR = EM.Exception
        Error = EM.Error
        errx = EM.Type
        time = EM.Time
        errDesc = EM.Error_description
        inpmsg = EM.Input_message
        resxml = ExceptionR(
            Error(
                errx(str(err)),
                time(str(dtime.strftime("%Y/%m/%d %H:%M:%S"))),
                errDesc(erreas),
                inpmsg(inp)
            )
        )

        with open("../log/error.log", "ab") as file:
            file.write(lxml.etree.tostring(resxml, pretty_print=True))


class WorkWithJSON:
    def dfconfigjson(self):
        """
        Default config of json file
        """
        adminList = {
            "ADMIN": "Kiyotaka#9299"
        }

        with open("../json/admins.json", "w", encoding='UTF8') as file:
            json.dump(adminList, file, ensure_ascii=False, indent=4)

    def loadjson(self):
        """
        Load json file
        :return: return the data from json file
        """
        if os.path.isfile("../json/admins.json"):
            with open("../json/admins.json", "r", encoding='UTF8') as file:
                datajson = json.load(file)
                return datajson
        else:
            self.dfconfigjson()
            return self.loadjson()


class WorkWithBlockedJSON:
    def dfconfigjson(self):
        """
        Default config of json file
        """
        blockedList = {
            "nameCon": "blocked"
        }

        with open("../json/blocked.json", "w", encoding='UTF8') as file:
            json.dump(blockedList, file, ensure_ascii=False, indent=4)

    def loadjson(self):
        """
        Load json file
        :param self:
        :return: return the data from json file
        """
        if os.path.isfile("../json/blocked.json"):
            with open("../json/blocked.json", "r", encoding='UTF8') as file:
                datajson = json.load(file)
                return datajson
        else:
            self.dfconfigjson()
            return self.loadjson()
