import requests
from bs4 import BeautifulSoup
from other.Exceptions import WebSiteNotFoundException


class FACEITStats2:
    """
    Another class which contains many methods for FaceIT stats.
    """
    def faceit_teammates_link(self, nickname):
        """
        Method finds the teammates with whom the player has played the most
        :param nickname: nickname of player, which will be used in method for link
        :return:
        """
        req = requests.get(
            "https://faceitanalyser.com/teammates/" + nickname
        )

        page = BeautifulSoup(req.content, "lxml")

        """
            Trycatch finds 'empty' webs and raises Exception.
            Second except needed for an 'extra' situations.
        """
        try:
            hh = page.find("h2").text
            if str(hh) == "Player not found!":
                raise WebSiteNotFoundException
        except WebSiteNotFoundException:
            raise WebSiteNotFoundException
        except Exception:
            pass
        """--end"""

        tmtsList = []

        stCon = page.find("div", {"class": "stats_container"})
        divTemp = stCon.find("div", {"class": "mobile_adjust_additional_align"})
        ahrefs = divTemp.find("a")
        """Finding last updated stats. Through links that are on web page"""
        while ahrefs is not None:
            req = requests.get(
                "https://faceitanalyser.com" + ahrefs["href"]
            )

            page = BeautifulSoup(req.content, "lxml")

            stCon = page.find("div", {"class": "stats_container"})
            divTemp = stCon.find("div", {"class": "mobile_adjust_additional_align"})
            ahrefs = divTemp.find("a")
        """--end"""

        divView = page.find("div", {"id": "view1_stats"})

        tbody = divView.find("tbody")
        trks = tbody.find_all("tr", {"class": "maps_tr"})

        count = 0
        for i in trks:
            if count < 3:
                count += 1
                teammate = {}
                tdks = i.find_all("td", {"class": "stats_td"})
                teammate["NICKNAME"] = tdks[1].text.rstrip().strip()
                teammate["MATCHES"] = tdks[2].text.rstrip().strip()
                img = tdks[1].find_all("img")
                teammate["IMGSRC"] = img[0]["src"]
                wins = int(tdks[3].text.rstrip().strip())
                loses = int(tdks[4].text.rstrip().strip())
                winrate = float(tdks[5].text.rstrip("%").strip())

                if wins > loses:
                    teammate["WINS"] = "**" + str(wins) + "**"
                    teammate["LOSES"] = str(loses)
                elif wins < loses:
                    teammate["WINS"] = str(wins)
                    teammate["LOSES"] = "**" + str(loses) + "**"
                else:
                    teammate["WINS"] = "**" + str(wins) + "**"
                    teammate["LOSES"] = "**" + str(loses) + "**"

                if winrate >= 50:
                    teammate["WINRATE"] = "**" + str(winrate) + "%**"
                else:
                    teammate["WINRATE"] = str(winrate)

                tmtsList.append(teammate)

        return tmtsList

    def faceit_enemies_link(self, nickname):
        """
        Method finds the enemies with whom the player has played the most
        :param nickname: nickname of player, which will be used in method for link
        :return:
        """
        req = requests.get(
            "https://faceitanalyser.com/teammates/" + nickname
        )

        page = BeautifulSoup(req.content, "lxml")

        """
            Trycatch finds 'empty' webs and raises Exception.
            Second except needed for an 'extra' situations.
        """
        try:
            hh = page.find("h2").text
            if str(hh) == "Player not found!":
                raise WebSiteNotFoundException
        except WebSiteNotFoundException:
            raise WebSiteNotFoundException
        except Exception:
            pass
        """--end"""

        tmtsList = []

        stCon = page.find("div", {"class": "stats_container"})
        divTemp = stCon.find("div", {"class": "mobile_adjust_additional_align"})
        ahrefs = divTemp.find("a")
        """Finding last updated stats. Through links that are on web page"""
        while ahrefs is not None:
            req = requests.get(
                "https://faceitanalyser.com" + ahrefs["href"]
            )

            page = BeautifulSoup(req.content, "lxml")

            stCon = page.find("div", {"class": "stats_container"})
            divTemp = stCon.find("div", {"class": "mobile_adjust_additional_align"})
            ahrefs = divTemp.find("a")
        """--end"""

        divView = page.find("div", {"id": "view2_stats"})

        tbody = divView.find("tbody")
        trks = tbody.find_all("tr", {"class": "maps_tr"})

        count = 0
        for i in trks:
            if count < 3:
                count += 1
                teammate = {}
                tdks = i.find_all("td", {"class": "stats_td"})
                teammate["NICKNAME"] = tdks[1].text.rstrip().strip()
                teammate["MATCHES"] = tdks[2].text.rstrip().strip()
                img = tdks[1].find_all("img")
                teammate["IMGSRC"] = img[0]["src"]
                wins = int(tdks[3].text.rstrip().strip())
                loses = int(tdks[4].text.rstrip().strip())
                winrate = float(tdks[5].text.rstrip("%").strip())

                if wins < loses:
                    teammate["WINS"] = "**" + str(wins) + "**"
                    teammate["LOSES"] = str(loses)
                elif wins > loses:
                    teammate["WINS"] = str(wins)
                    teammate["LOSES"] = "**" + str(loses) + "**"
                else:
                    teammate["WINS"] = "**" + str(wins) + "**"
                    teammate["LOSES"] = "**" + str(loses) + "**"

                if winrate >= 50:
                    teammate["WINRATE"] = "**" + str(winrate) + "%**"
                else:
                    teammate["WINRATE"] = str(winrate)

                tmtsList.append(teammate)

        return tmtsList
