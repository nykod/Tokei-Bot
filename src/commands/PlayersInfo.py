import requests
from bs4 import BeautifulSoup


class Players:

    help = {
        "!hltv help": "Shows !hltv commands",
        "!faceit help": "Shows !faceit commands",
        "!player help": "Shows !hltv commands"
    }

    playercomhelp = {
        "!player settings 'player name'": "Shows player settings",
        "!player info 'player name'": "Shows player information"
    }

    def player_settings(self, playerWeb):
        """
        Method shows player mouse settings and monitor settings
        :param playerWeb: value that helps find player profile on web
        :return is dictionary with mouse settings and monitor settings:
        """
        assert isinstance(playerWeb, str)
        mousesettings = {}
        monitorsettings = {}
        req = requests.get("https://csgopedia.com/players/" + str(playerWeb))
        page = BeautifulSoup(req.content, 'html.parser')
        ulss = page.find("ul", {"class": "list-details-2"})
        tempdiv = ulss.find_all("div", {"class": "pull-right"})
        mousesettings["DPI"] = tempdiv[0].text
        mousesettings["eDPI"] = tempdiv[1].text
        ulss2 = page.find_all("ul", {"class": "list-details-2"})[1]
        tempdiv = ulss2.find_all("div", {"class": "pull-right"})
        mousesettings["sensitivity"] = tempdiv[0].text
        mousesettings["zoom-sens"] = tempdiv[1].text
        mousesettings["mouse_ac"] = tempdiv[2].text
        mousesettings["rawinp"] = tempdiv[3].text
        ulss3 = page.find_all("ul", {"class": "list-details-2"})[2]
        tempdiv = ulss3.find_all("div", {"class": "pull-right"})
        monitorsettings["resolution"] = tempdiv[0].text
        monitorsettings["AR"] = tempdiv[1].text
        monitorsettings["scaling"] = tempdiv[2].text
        monitorsettings["frames"] = tempdiv[3].text
        return mousesettings, monitorsettings

    # TODO COULD BE DELETED IN FUTURE BECAUSE OF HLTV STATS
    def player_stats(self, playerWeb):
        """
        Method shows player stats
        :param playerWeb: value that helps find player profile on web
        :return: dictionary with various stats
        """
        assert isinstance(playerWeb, str)
        playerstats = {}
        req = requests.get("https://csgopedia.com/players/" + str(playerWeb))
        page = BeautifulSoup(req.content, 'html.parser')
        divbox = page.find("div", {"class": "user-box"})
        divrow10 = divbox.find("div", {"class": "row_10"})
        divrowcol = divrow10.find("div", {"class": "col-md-5"})
        divstrong = divrowcol.find_all("strong")
        playerstats["K/D"] = divstrong[1].text
        playerstats["diff"] = divstrong[2].text
        playerstats["rating"] = divstrong[3].text
        playerstats["maps"] = divstrong[4].text
        playerstats["kpr"] = divstrong[5].text
        playerstats["dpr"] = divstrong[6].text
        playerstats["hs"] = divstrong[7].text
        playerstats["rndscon"] = divstrong[8].text
        return playerstats

    def player_info(self, playerWeb):
        """
        Method shows basic information about player
        :param playerWeb: value that helps find player profile on web
        :return: dictionary with information
        """
        assert isinstance(playerWeb, str)
        playerinfo = {}
        req = requests.get("https://csgopedia.com/players/" + str(playerWeb))
        page = BeautifulSoup(req.content, 'html.parser')
        divbox = page.find("div", {"class": "user-box"})
        divcol = divbox.find("div", {"class": "col-md-7"})
        h1all = divcol.find("h1")
        strong = h1all.find_all("strong")
        playerinfo["name"] = strong[0].text
        playerinfo["nickname"] = strong[1].text
        playerinfo["surname"] = strong[2].text
        ulls = divcol.find_all("ul", {"class": "list-inline"})
        playerinfo["country"] = ulls[0].find_all("div", {"class", "icon"})[0].text
        playerinfo["age"] = ulls[0].find_all("div", {"class", "icon"})[1].text
        divspan = divcol.find("div", {"class": "m-b-1"})
        playerinfo["team"] = divspan.find("span").text
        return playerinfo
