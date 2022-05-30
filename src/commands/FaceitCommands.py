import requests
from bs4 import BeautifulSoup
from other.Exceptions import PlayerEloException, WebSiteNotFoundException


class FACEITStats:
    """
    Class which contains many methods for FaceIT stats.
    """
    def faceit_stats(self, nickname):
        """
        Method find all needed statistic for a player.
        Also there are values which are not in statistic.
        Example: Rank(the letter one) - I think original faceit ranking system is not as good as it could be.
        Player who has lvl 10 - 2300 elo is not as good as someone who has 3300 elo.
        That is the main reason of my own rating system.
        (D- <650; D 651-1000; C 1001-1400; C+ 1401-1550; B- 1551-1650; B 1651-1800; A 1801-2100; S 2101-2900; S+ >2901)
        :param nickname: nickname of player that we are searching statistic for
        :return: player (dict with keys: stats) and image source
        """
        req = requests.get(
            "https://faceitanalyser.com/stats/" + nickname
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

        divProfileInfo = page.find("div", {"class": "stats_profile_inner"})
        img = divProfileInfo.find("img", {"class": "stats_profile_avatar"})

        player = {}
        """KILLS/DEATHS RATING - AVERAGE"""
        KDRavg = {}
        """--end"""
        matches = {}
        eloSplit = divProfileInfo.find("div", {"id": "lvl"}).text.rstrip().strip().split()
        elo = int(eloSplit[0])
        player["ELO"] = elo

        divStatsCon = page.find("div", {"id": "view1_stats"})
        divStatsWrapper = divStatsCon.find_all("div", {"class": "stats_totals_block_wrapper"})

        """Finds rating data"""
        divRating = divStatsWrapper[0].find_all("div", {"class": "stats_totals_block_item"})

        KDRavg["KDR"] = divStatsWrapper[0].find("div", {"class": "stats_totals_block_main_value"}).text. \
            rstrip("\n").strip("\n")
        KDRavg["KPR"] = divRating[0].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")
        KDRavg["KILLS"] = divRating[1].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")
        KDRavg["DEATHS"] = divRating[2].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")

        player["KDAVG"] = KDRavg
        """--end"""

        player["HLTV"] = float(divStatsWrapper[1].find("div", {"class": "stats_totals_block_main_value"}).text. \
                               rstrip("\n").strip("\n")) * 0.8

        """Finds matches data"""
        divMatches = divStatsWrapper[2].find_all("div", {"class": "stats_totals_block_item"})

        matches["WINRATE"] = divStatsWrapper[2].find("div", {"class": "stats_totals_block_main_value"}).text. \
            rstrip("\n").strip("\n")
        matches["MATCHES"] = divMatches[0].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")
        matches["WINS"] = divMatches[1].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")
        matches["LOSES"] = divMatches[2].find("span", {"class": "stats_totals_block_item_value"}).text. \
            rstrip("\n").strip("\n")

        player["MATCHES"] = matches
        """--end"""

        """Finds faceit lvl (this thing will be important in other method)"""
        if elo <= 800:
            player["LVL"] = 1
        elif 800 < elo <= 950:
            player["LVL"] = 2
        elif 950 < elo <= 1100:
            player["LVL"] = 3
        elif 1100 < elo <= 1250:
            player["LVL"] = 4
        elif 1250 < elo <= 1400:
            player["LVL"] = 5
        elif 1400 < elo <= 1550:
            player["LVL"] = 6
        elif 1550 < elo <= 1700:
            player["LVL"] = 7
        elif 1700 < elo <= 1850:
            player["LVL"] = 8
        elif 1850 < elo <= 2000:
            player["LVL"] = 9
        elif 2000 < elo:
            player["LVL"] = 10
        else:
            return PlayerEloException
        """--end"""

        """Finds rank (My own ranking. Why? I think faceit lvl is not enough to show your skill - someone's skill)"""
        if elo <= 650:
            player["RANK"] = "D-"
        elif 650 < elo <= 1000:
            player["RANK"] = "D"
        elif 1000 < elo <= 1400:
            player["RANK"] = "C"
        elif 1400 < elo <= 1550:
            player["RANK"] = "C+"
        elif 1550 < elo <= 1650:
            player["RANK"] = "B-"
        elif 1650 < elo <= 1800:
            player["RANK"] = "B"
        elif 1800 < elo <= 2100:
            player["RANK"] = "A"
        elif 2100 < elo <= 2900:
            player["RANK"] = "S"
        elif 2900 < elo:
            player["RANK"] = "S+"
        else:
            return PlayerEloException
        """--end"""

        return player, img["src"]

    def faceit_stats_count(self, nickname):
        """
        Method will count stats to another unique rating. The rating is similar to FIFA rating.
        But here, in my stats, is only overall rating made by FIFA method
        :param nickname: nickname of player, which can be used in method
        :return: player (dict with keys: stats) and image source
        """
        assert isinstance(nickname, str)
        try:
            player, img = self.faceit_stats(nickname)
        except WebSiteNotFoundException:
            raise WebSiteNotFoundException
        except PlayerEloException:
            raise PlayerEloException

        playerret = {}

        try:
            playerret["ELO"] = player["ELO"]

            kdr = float(player["KDAVG"]["KDR"])
            kpr = float(player["KDAVG"]["KPR"])
            kills = float(player["KDAVG"]["KILLS"])
            deaths = float(player["KDAVG"]["DEATHS"])

            hltv = float(player["HLTV"])

            winrate = round(float(player["MATCHES"]["WINRATE"]) * 0.01, 2)
            playerret["MATCHES"] = player["MATCHES"]["MATCHES"]
            playerret["WINS"] = player["MATCHES"]["WINS"]
            playerret["LOSES"] = player["MATCHES"]["LOSES"]

            lvl = player["LVL"]
            lvlvalue = lvl * 0.1
            playerret["LVL"] = lvl
            playerret["RANK"] = player["RANK"]
        except ValueError as e:
            raise ValueError

        playerret["RATING"] = int(round(((((kdr + kpr + (kills / deaths) + hltv + winrate) / 5) * lvlvalue) * 100), 0))
        playerret["KDR"] = kdr
        playerret["WINRATE"] = str(winrate * 100) + "%"
        playerret["KPR"] = kpr
        playerret["KILLS"] = kills
        playerret["DEATHS"] = deaths

        return playerret, img

    def faceit_comparision(self, nickname1, nickname2):
        """
        Method that compares two players statistic between each other and highlights better one.
        :param nickname1: nickname of player that will be compared
        :param nickname2: nickname of player that will be compared
        :return: player1ret (dict with keys: stats), player2ret (dict with keys: stats)
        """
        assert isinstance(nickname1, str)
        assert isinstance(nickname2, str)

        player1, img = self.faceit_stats_count(nickname1)
        player2, img = self.faceit_stats_count(nickname2)

        player1ret = {}
        player2ret = {}

        """Because we cannot compare ranks between each other, we must do a unique 'for' for them"""
        rank = {"D-": 1, "D": 2, "C": 3, "C+": 4, "B-": 5, "B": 6, "A": 7, "S": 8, "S+": 9}
        ranktemp = 0
        ranktemp2 = 0
        for a, b in rank.items():
            if player1["RANK"] == a:
                ranktemp = b
            if player2["RANK"] == a:
                ranktemp2 = b
            if ranktemp > ranktemp2:
                player1ret["RANK"] = "**" + str(player1["RANK"]) + "**"
                player2ret["RANK"] = str(player2["RANK"])
            elif ranktemp < ranktemp2:
                player1ret["RANK"] = str(player1["RANK"])
                player2ret["RANK"] = "**" + str(player2["RANK"]) + "**"
            else:
                player1ret["RANK"] = "**" + str(player1["RANK"]) + "**"
                player2ret["RANK"] = "**" + str(player2["RANK"]) + "**"
        """--end"""

        """Because winrate has '%' in value, we need to .rstrip() it"""
        winrate1 = float(player1["WINRATE"].rstrip("%"))
        winrate2 = float(player2["WINRATE"].rstrip("%"))

        if winrate1 > winrate2:
            player1ret["WINRATE"] = "**" + str(winrate1) + "%**"
            player2ret["WINRATE"] = str(winrate2) + "%"
        elif winrate1 < winrate2:
            player1ret["WINRATE"] = str(winrate1) + "%"
            player2ret["WINRATE"] = "**" + str(winrate2) + "%**"
        else:
            player1ret["WINRATE"] = "**" + str(winrate1) + "%**"
            player2ret["WINRATE"] = "**" + str(winrate2) + "%**"
        """--end"""

        """We need to highlight better result. In 'for' cycles we are comparing them between each other."""
        for i, j in player1.items():
            for x, y in player2.items():
                if i == x:
                    if (i == "RANK") and (x == "RANK"):
                        pass
                    elif(i == "WINRATE") and (x == "WINRATE"):
                        pass
                    elif float(j) > float(y):
                        player1ret[i] = "**" + str(j) + "**"
                        player2ret[x] = str(y)
                    elif float(j) < float(y):
                        player1ret[i] = str(j)
                        player2ret[x] = "**" + str(y) + "**"
                    else:
                        player1ret[i] = "**" + str(j) + "**"
                        player2ret[x] = "**" + str(y) + "**"
        """--end"""

        return player1ret, player2ret

