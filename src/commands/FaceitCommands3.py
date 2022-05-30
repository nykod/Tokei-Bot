import requests
from bs4 import BeautifulSoup
from other.Exceptions import WebSiteNotFoundException


class FACEITStats3:
    """
    Class which contains many methods for FaceIT stats.
    """
    faceitCommands = {
        "!faceit stats 'player nickname'": "Shows faceit stats of the player",
        "!faceit compare 'player nickname' 'player2 nickname'": "Compare 2 players between each other and shows their"
                                                                " stats (highlights better one)",
        "!faceit teammates 'player nickname'": "Shows the teammates with whom the player has played the most",
        "!faceit enemies 'player nickname'": "Shows the enemies with whom the player has played the most",
        "!faceit highlights 'player nickname'": "Shows players best games on faceit"

    }

    def faceit_highlights(self, nickname):
        """
        Method finds highlights of the player.
        Most kills, Best KDR, Best +/- (Every category has few matches with those stats)
        :param nickname: nickname of player, which will be used in method for link
        :return: highlights (dict with key: stats)
        """
        req = requests.get(
            "https://faceitanalyser.com/highlights/" + nickname
        )
        page = BeautifulSoup(req.content, "lxml")

        """
        Trycatch finds 'empty' webs and raises Exception.
        Second except needed for an 'extra' situations.
        """
        try:
            hh = page.find("h1").text
            if str(hh) == "Player Not Found":
                raise WebSiteNotFoundException
        except WebSiteNotFoundException:
            raise WebSiteNotFoundException
        except Exception:
            pass
        """--end"""

        divView = page.find("div", {"id": "view1_stats"})
        divStatsCon = divView.find_all("div", {"class": "stats_container"})

        highlights = {}
        highlist = []

        for i in divStatsCon:
            matchList = []
            trKill = i.find_all("tr", {"class": "maps_tr"})
            for j in trKill:

                matchi = {}
                tdks = j.find_all("td", {"class": "stats_td"})
                matchi["MATCH"] = tdks[0].text
                matchi["DATE"] = tdks[1].text
                matchi["MAP"] = tdks[3].text.rstrip().strip("\n")
                chPov = j.find("td", {"class": "positive"})
                tempSc = tdks[4].text
                if chPov is not None:
                    a = str(chPov.text)
                    b = str(tempSc)
                    if a == b:
                        matchi["SCORE"] = "**" + tempSc + "**"
                    else:
                        matchi["SCORE"] = tempSc
                matchi["KILLS"] = tdks[5].text
                matchi["ASSISTS"] = tdks[6].text
                matchi["DEATHS"] = tdks[7].text
                matchi["PLMI"] = tdks[8].text
                matchi["KDR"] = tdks[9].text
                matchList.append(matchi)
            highlist.append(matchList)

        highlights["MKILLS"] = highlist[0]
        highlights["BKDR"] = highlist[1]
        highlights["BPLUSM"] = highlist[2]

        return highlights

    def faceit_names(self, nickname):
        req = requests.get(
            "https://faceitanalyser.com/names/" + nickname
        )
        page = BeautifulSoup(req.content, "lxml")

        """
        Trycatch finds 'empty' webs and raises Exception.
        Second except needed for an 'extra' situations.
        """
        try:
            hh = page.find("h1").text
            if str(hh) == "Player Not Found":
                raise WebSiteNotFoundException
        except WebSiteNotFoundException:
            raise WebSiteNotFoundException
        except Exception:
            pass
        """--end"""

        divCon = page.find("div", {"class": "stats_container"})
        divId = divCon.find("div", {"id": "view1_stats"})
        divCon2 = divId.find("div", {"class": "stats_container"})
        divStats = divCon2.find_all("div", {"class": "stats_totals_block_wrapper"})

        nameBlock = []

        for i in divStats:
            nameSt = {}
            lstfst = i.find_all("div", {"class": "stats_totals_block_item"})
            nameSt["NICKNAME"] = i.find("div", {"class": "stats_totals_block_main_value"}).text.rstrip("\n").strip("\n")
            nameSt["LAST_MATCH"] = lstfst[1].find_all("div")[0].text.rstrip("\n").strip("\n") \
                                   + " " + lstfst[1].find_all("div")[1].text.rstrip("\n").strip("\n").replace("-", "/")
            nameSt["FIRST_MATCH"] = lstfst[2].find_all("div")[0].text.rstrip("\n").strip("\n") \
                                    + " " + lstfst[2].find_all("div")[1].text.rstrip("\n").strip("\n").replace("-", "/")
            nameBlock.append(nameSt)

        return nameBlock


