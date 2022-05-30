import requests
from bs4 import BeautifulSoup
import datetime
from other.Exceptions import WebSiteNotFoundException, NoMapsException
from other.WorkWithFiles import WorkWithCSV
import pandas as pd


class HLTVStats2:
    """
    Another class with commands which are parsing page for information
    """
    csvfile = WorkWithCSV()

    def hltv_player_stats(self, player):
        """
        Method gets pro player stats from 'hltv.org'
        :param player: nickname of player
        :return: return is stats(dict) and image source link
        """
        stats = {}
        assert isinstance(player, str)
        try:
            code = self.csvfile.get_info_player()[player]
        except FileNotFoundError:
            raise FileNotFoundError
        date_today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        date_tm_ago = str((datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d'))
        req = requests.get(
            "https://www.hltv.org/stats/players/" + code + "/" + player + "?startDate=" + date_tm_ago +
            "&endDate=" + date_today)
        page = BeautifulSoup(req.content, "lxml")

        divsum = page.find("div", {"class": "playerSummaryStatBox"})
        divph = divsum.find("div", {"class": "summaryBodyshotContainer"})
        img = divph.find("img", {"class": "summaryBodyshot"})
        divcon = divsum.find("div", {"class": "summaryBreakdownContainer"})
        divstats = divcon.find_all("div", {"class": "summaryStatBreakdown"})
        kast = divstats[2].find("div", {"class": "summaryStatBreakdownDataValue"}).text
        kast_split = kast.split("%")

        """Setting values into dictionary"""
        stats["2.0"] = round(float(divstats[0].find("div", {"class": "summaryStatBreakdownDataValue"}).text), 2)
        stats["DPR"] = divstats[1].find("div", {"class": "summaryStatBreakdownDataValue"}).text
        stats["KAST"] = round(float(kast_split[0]) * 0.01, 3)
        stats["IMPACT"] = round(float(divstats[3].find("div", {"class": "summaryStatBreakdownDataValue"}).text), 2)
        stats["ADR"] = round(float(divstats[4].find("div", {"class": "summaryStatBreakdownDataValue"}).text), 2)
        stats["KPR"] = round(float(divstats[5].find("div", {"class": "summaryStatBreakdownDataValue"}).text), 2)

        divfeatrat = page.find("div", {"class": "featured-ratings-container"})
        divcol = divfeatrat.find_all("div", {"class": "col-custom"})
        vstop5, vstop10, vstop20, vstop30, vstop50 = 0, 0, 0, 0, 0
        count = 0

        """Counting values (some of them could be None that's why there are many try catches)"""
        """Value: vstop5 - V.S. Top 5 HLTV"""
        try:
            vstop5 = float(divcol[0].find("div", {"class": "rating-value"}).text)
            if isinstance(vstop5, float):
                vstop5 = vstop5 * 1.04
                count += 1
        except ValueError:
            pass

        """Value: vstop10 - V.S. Top 10 HLTV"""
        try:
            vstop10 = float(divcol[1].find("div", {"class": "rating-value"}).text)
            if isinstance(vstop10, float):
                vstop10 = vstop10 * 1.03
                count += 1
        except ValueError:
            pass

        """Value: vstop20 - V.S. Top 20 HLTV"""
        try:
            vstop20 = float(divcol[2].find("div", {"class": "rating-value"}).text)
            if isinstance(vstop20, float):
                vstop20 = vstop20 * 1.02
                count += 1
        except ValueError:
            pass

        """Value: vstop30 - V.S. Top 30 HLTV"""
        try:
            vstop30 = float(divcol[3].find("div", {"class": "rating-value"}).text)
            if isinstance(vstop30, float):
                vstop30 = vstop30 * 1.01
                count += 1
        except ValueError:
            pass

        """Value: vstop50 - V.S. Top 50 HLTV"""
        try:
            vstop50 = float(divcol[4].find("div", {"class": "rating-value"}).text)
            if isinstance(vstop50, float):
                vstop10 = vstop50 * 0.97
                count += 1
        except ValueError:
            pass

        """--end"""

        vsTopOverall = (vstop5 + vstop10 + vstop20 + vstop30 + vstop50 + 0.98) / (count + 1)

        try:
            """Counting all of the values to a rating(My own)"""
            psd_kd = round(float(stats["2.0"]) * 1.0, 2)
            psd_dpr = round(float(stats["DPR"]) * 0.97, 2)
            psd_kast = round(float(stats["KAST"]) * 0.99, 2)
            psd_impact = round(float(stats["IMPACT"]) * 1.02, 2)
            psd_adr = round(float(stats["ADR"]) * 0.0098, 2)
            psd_kprc = round(float(stats["KPR"]) * 0.97, 2)
            psd_rating = psd_kd + psd_dpr + psd_kast + psd_impact + psd_adr + psd_kprc + vsTopOverall
            ratingCount = int(round(psd_rating / 7, 2) * 100)
            if ratingCount > 99:
                ratingCount = 99
            stats["FFRATING"] = ratingCount
        except ValueError:
            raise ValueError
        return stats, img["src"]

    def hltv_team_info(self, team):
        """
        Gets info about team
        Info: Name/Region/Rank in TOP/ Weeks in TOP/Average age of players/Coach
        :param team: Team whose information we want
        :return: Team info(teamInfo - dict) and player roster(players - list)
        """

        assert isinstance(team, str)
        players = []
        teamInfo = {}
        team = team.lower()

        """if input(team) has a space it will replace it with '-' for searching in files"""
        if " " in team:
            team = team.replace(" ", "-")
        try:
            code = self.csvfile.get_info_teams()[team]
        except FileNotFoundError:
            raise FileNotFoundError

        req = requests.get("https://www.hltv.org/team/" + code + "/" + team)
        page = BeautifulSoup(req.content, "lxml")

        try:
            hh = page.find("h1")
            if str(hh) == "404":
                raise WebSiteNotFoundException
        except Exception:
            pass

        teamProfile = page.find("div", {"class", "contentCol"})
        divpls = teamProfile.find("div", {"class", "bodyshot-team"})
        plrnickname = divpls.find_all("span", {"class": "text-ellipsis"})

        """Getting nickname of all players"""
        for i in plrnickname:
            players.append(i.text)

        profileTopBox = teamProfile.find("div", {"class": "profileTopBox"}).find("div", {"class": "flex"})
        profileInfo = profileTopBox.find("div", {"class": "profile-team-info"})
        region = profileInfo.find("div", {"class": "team-country"}).text
        teamName = profileInfo.find("h1", {"class": "profile-team-name"}).text

        teamInfoCon = teamProfile.find("div", {"class": "profile-team-stats-container"}).find_all("span")
        """
            list teamInfoCon - [0] Ranking; [1] Weeks in top 30; [2] Average players age; [3] Coach nickname
        """

        teamInfo["name"] = teamName
        teamInfo["region"] = region
        teamInfo["rank"] = teamInfoCon[0].text
        teamInfo["weeks"] = teamInfoCon[1].text
        teamInfo["age"] = teamInfoCon[2].text
        teamInfo["coach"] = teamInfoCon[3].text

        return teamInfo, players

    def hltv_recent_matches(self, team):
        """
        Gets recent matches of the team
        Recent match: EVENT/MATCH SCORE/DATE
        :param team: Team whose information about recent matches we want
        :return: eventList (List of events(dict).
                            Event is dictionary with match as value.
                            Match is dictionary with other values.)
        """
        matchsWinRate = {}
        eventList = []
        team = team.lower()

        """if input(team) has a space it will replace it with '-' for searching in files"""
        if " " in team:
            team = team.replace(" ", "-")
        try:
            code = self.csvfile.get_info_teams()[team]
        except FileNotFoundError:
            raise FileNotFoundError

        req = requests.get("https://www.hltv.org/team/" + code + "/" + team + "#tab-matchesBox")
        page = BeautifulSoup(req.content, "lxml")

        """if page is empty(or with error 404) it will return WebSiteNotFoundException"""
        try:
            hh = page.find("h1").text
            if str(hh) == "404":
                raise WebSiteNotFoundException
        except Exception:
            pass

        teamProfile = page.find("div", {"class", "teamProfile"})
        matchesBox = teamProfile.find("div", {"class", "highlighted-stats-box"}).find_all("div", {"class": "stat"})

        matchsWinRate["streak"] = matchesBox[0].text
        matchsWinRate["winrate"] = matchesBox[1].text

        tableCon = teamProfile.find_all("table", {"class": "match-table"})
        tbodys = ["none string ;)"]

        """Checks if there is only one 'match-table' class element.
           If there are two elements, one is recent matches and second is upcoming matches - we need recent"""
        if len(tableCon) == 1:
            theads = tableCon[0].find_all("thead")
            tbodytemp = tableCon[0].find_all("tbody")
        else:
            theads = tableCon[1].find_all("thead")
            tbodytemp = tableCon[1].find_all("tbody")
        """--end"""

        """Finds all events"""
        for i in tbodytemp:
            tbodys.append(i)

        for i in range(len(theads)):
            """Max 2 events in list. Reason - list would be too long."""
            if (i != 0) and (i < 3):
                eventName = theads[i].text
                event = {}
                matches = []
                teamrow = tbodys[i].find_all("tr", {"class": "team-row"})
                for x in teamrow:
                    """x - one match, teamrow - list of all matches"""
                    match = {
                        "date": x.find("td", {"class": "date-cell"}).text}

                    teamCell = x.find("td", {"class": "team-center-cell"})
                    teamName = teamCell.find_all("div", {"class": {"team-flex"}})[0].text
                    score = teamCell.find("div", {"class": "score-cell"}).text
                    teamName2 = teamCell.find_all("div", {"class": {"team-flex"}})[1].text
                    matchResult = teamName + " " + score + " " + teamName2
                    match["match"] = matchResult
                    matches.append(match)
                event[eventName] = matches
                eventList.append(event)
            else:
                pass

        return eventList

    def hltv_team_maps(self, team):
        """
        Shows team maps and their win rate
        Map: { Map Name : Win percentage }
        :param team: Team whose information about recent matches we want
        :return: mapList(List of maps. Map is a dictionary)
        """
        team = team.lower()
        mapList = []

        """if input(team) has a space it will replace it with '-' for searching in files"""
        if " " in team:
            team = team.replace(" ", "-")
        try:
            code = self.csvfile.get_info_teams()[team]
        except FileNotFoundError:
            raise FileNotFoundError
        req = requests.get("https://www.hltv.org/team/" + code + "/" + team + "#tab-statsBox")
        page = BeautifulSoup(req.content, "lxml")

        """if page is empty(or with error 404) it will return WebSiteNotFoundException"""
        try:
            hh = page.find("h1").text
            if str(hh) == "404":
                raise WebSiteNotFoundException
        except Exception:
            pass

        """If map box is None raises an exception"""
        statsBox = page.find("div", {"id": "statsBox"}).find("div", {"class": "map-statistics"})
        if statsBox is None:
            raise NoMapsException
        mapsStatistics = statsBox.find_all("div", {"class": "map-statistics-container"})

        """Searching maps"""
        for i in mapsStatistics:
            mapS = {i.find("div", {"class": "map-statistics-row-map-mapname"}).text: i.find("div", {
                "class": "map-statistics-row-win-percentage"}).text}
            mapList.append(mapS)
        return mapList

    def hltv_player_career(self, player):
        """
        Method should show a table with stats, but it is broken sometimes
        :param player:
        :return:
        """
        assert isinstance(player, str)
        try:
            code = self.csvfile.get_info_player()[player]
        except FileNotFoundError:
            raise FileNotFoundError
        req = requests.get(
            "https://www.hltv.org/stats/players/career/" + code + "/" + player
        )
        page = BeautifulSoup(req.content, "lxml")
        divcon = page.find("div", {"class": "contentCol"})
        tableStats = divcon.find("table", {"class": "stats-table"})
        df_list = pd.read_html(req.text, index_col=False)
        return df_list[0]
