import requests
from bs4 import BeautifulSoup
import datetime
from other.WorkWithFiles import WorkWithCSV
from commands.HLTVcommands import HLTVStats
from other.Exceptions import MatchBoxListException
from other.Exceptions import PlayerNotFoundException


class HLTVStats3:
    """
    Another class with commands which are parsing page for information
    """
    hltvpp = HLTVStats()
    csvfile = WorkWithCSV()

    def hltv_match_upcoming(self):
        """
        Method shows upcoming matches from hltv.org
        :return: list of these matches, list of unknown matches(matches which don't have opponents, date, etc.),
         day of the match
        """
        upcomingmatches = []
        unknownmatches = []
        page = self.hltvpp.page_parsing("https://www.hltv.org/matches")
        divmatch_con = page.find("div", {"class": "upcomingMatchesContainer"})
        divdaymatch = divmatch_con.find("div", {"class": "upcomingMatchesSection"})
        divupcoming = divdaymatch.find_all("div", {"class": "upcomingMatch"})
        day = divdaymatch.find("span", {"class": "matchDayHeadline"}).text
        for i in divupcoming:
            if i.find("div", {"class": "matchInfoEmpty"}) is None:
                matchinfo = {}
                fadedstars = i.find_all("i", {"class": "faded"})
                matchinfo["time"] = i.find("div", {"class": "matchTime"}).text
                matchinfo["stars"] = 5 - len(fadedstars)
                matchinfo["format"] = i.find("div", {"class": "matchMeta"}).text
                team1 = i.find("div", {"class": "team1"})
                matchinfo["team_1"] = team1.find("div", {"class": "text-ellipsis"}).text
                team2 = i.find("div", {"class": "team2"})
                matchinfo["team_2"] = team2.find("div", {"class": "text-ellipsis"}).text
                matchinfo["event"] = i.find("div", {"class": "matchEventName"}).text
                upcomingmatches.append(matchinfo)
            else:
                tempempty = i.find("div", {"class": "matchInfoEmpty"})
                unknownmatches.append(tempempty.find("span").text)
        return upcomingmatches, unknownmatches, day

    def hltv_news(self):
        """
        Method shows today's csgo pro scene news
        :return: list of these news
        """
        newslist = []
        page = self.hltvpp.page_parsing("https://www.hltv.org")
        divindex = page.find("div", {"class": "index"})
        h2text = divindex.find_all("h2", {"class": "newsheader"})
        divnews_box = divindex.find_all("div", {"standard-box"})
        tempcount = 0
        # count = 1
        tempcount2 = 0
        for i in divnews_box:
            if tempcount2 < 2:
                h2temp = h2text[tempcount2].text
                a_news = i.find_all("a", {"class", "article"})
                ahref = i.find_all("a", href=True)
                for j in a_news:
                    newstemp = {}
                    news = {}
                    news["article"] = j.find("div", {"class", "newstext"}).text
                    news["time"] = j.find("div", {"class", "newsrecent"}).text
                    news["site"] = "https://www.hltv.org" + str(ahref[tempcount]["href"])
                    newstemp[h2temp] = news
                    newslist.append(newstemp)
                    tempcount += 1
                tempcount2 += 1
                tempcount = 0
        return newslist

    def hltv_player_team_history(self, player):
        """
        Shows information about history of player's past teams.
        Also some additional information about player.
        :param player: nickname of player, which will be used in method
        :return: teamStatsList(list of dictionaries), teamBreakdownList(list of dictionaries - past teams information),
         img['src'](image source link)
        """
        assert isinstance(player, str)
        try:
            code = self.csvfile.get_info_player()[player]
        except FileNotFoundError:
            raise FileNotFoundError
        req = requests.get(
            "https://www.hltv.org/player/" + code + "/" + player + "#tab-teamsBox"
        )

        teamStatsList = []
        teamBreakdownList = []

        page = BeautifulSoup(req.content, "lxml")

        teamsBox = page.find("div", {"id": "teamsBox"})
        img = page.find("img", {"class", "bodyshot-img"})
        divteamsStats = teamsBox.find("div", {"class": "highlighted-stats-box"})
        teamsStats = divteamsStats.find_all("div", {"class": "highlighted-stat"})

        for i in teamsStats:
            tempdict = {i.find("div", {"class": "description"}).text: i.find("div", {"class": "stat"}).text}
            teamStatsList.append(tempdict)

        tableteamBreakdown = teamsBox.find("table", {"class": "team-breakdown"})

        teamBreakdown = tableteamBreakdown.find("tbody").find_all("tr", {"class": "team"})

        for i in teamBreakdown:
            tempdict = {"period": i.find("td", {"class": "time-period-cell"}).text,
                        "team": i.find("td", {"class": "team-name-cell"}).text}
            teamBreakdownList.append(tempdict)

        return teamStatsList, teamBreakdownList, img['src']

    def hltv_leaderboard(self):
        """
        Method gets all leaderboard's information.
        :return: tableList(List of all tables that are on web page.)
        """
        date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        dateSvnDs = str((datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))
        req = requests.get(
            "https://www.hltv.org/stats/leaderboards?startDate=" + dateSvnDs + "&endDate="
            + date + "&rankingFilter=Top30"
        )
        page = BeautifulSoup(req.content, "lxml")

        divCol = page.find("div", {"class": "columns"})
        divLeftCol = divCol.find("div", {"class": "col"})

        sa = divLeftCol.find_all("div", {"class": "standard-box"})
        count = "-"
        count2 = 0
        count3 = 1

        tableList = []

        for i in sa:
            playerDict = {}
            player = {}
            colmName = {}
            playerList = []
            divLeader = i.find("div", {"class": "leader"})
            leadName = divLeader.find("span", {"class": "leader-player"}).text
            leadTeam = divLeader.find("span", {"class": "leader-team"}).text
            count = count + "-"
            player[leadName + " (" + leadTeam + ")" + count] = str(
                divLeader.find_all("span", {"class": "leader-rating"})[0]
                    .text).rstrip("\xa0")
            playerDict["leader"] = player
            playerList.append(playerDict)
            divPlayers = i.find_all("div", {"class": "stats-row"})

            for j in divPlayers:
                playerDictTemp = {}
                playerTemp = {}
                ahrefs = j.find_all("a")
                playerTemp[ahrefs[0].text + " (" + ahrefs[1].text + ")"] = j.find_all("span")[2].text
                playerDictTemp["player" + str(count3)] = playerTemp
                count3 += 1
                playerList.append(playerDictTemp)

            count3 = 1
            colmName[divCol.find_all("span", {"class": {"standard-headline"}})[count2].text] = playerList
            count2 += 1
            tableList.append(colmName)

        return tableList

    def hltv_lastmatch_linkfinder(self, value):
        """
        Method will find a link that we need for another method. Parameter player is needed to find it from players
        profile.
        :param value: nickname of a player/ name of a team, which will be used in method
        :return: return is a link that we were searching for. Link of the last match(at the moment) of this player/team
        """
        teamBool = False
        try:
            code = self.csvfile.get_info_player()[value]
        except KeyError:
            team = value.lower()
            if " " in team:
                team = team.replace(" ", "-")
            teamBool = True
            try:
                code = self.csvfile.get_info_teams()[team]
            except FileNotFoundError:
                raise FileNotFoundError
            # return "Oops, it looks like our file is damaged. Try it later."

        """Checks if we want team stats or player stats"""
        req = None
        if teamBool is False:
            req = requests.get(
                "https://www.hltv.org/player/" + code + "/" + value + "#tab-matchesBox"
            )
        elif teamBool is True:
            req = requests.get(
                "https://www.hltv.org/team/" + code + "/" + value + "#tab-matchesBox"
            )
        """--end"""

        page = BeautifulSoup(req.content, "lxml")
        try:
            img = page.find("img", {"class", "bodyshot-img"})
            if img is None:
                raise Exception
        except Exception:
            img = page.find("img", {"class", "teamlogo"})

        divMatchOv = page.find("div", {"id": "matchesBox"})  # finds div with id "matchesBox"
        divMatchesTemp = divMatchOv.find_all("table", {"class": "match-table"})  # finds all divs with class
        # "match-table"

        try:
            if len(divMatchesTemp) == 2:
                divMatches = divMatchesTemp[1]
            elif len(divMatchesTemp) == 1:
                divMatches = divMatchesTemp[0]
            else:
                raise MatchBoxListException
        except MatchBoxListException:
            raise MatchBoxListException

        TeamRow = divMatches.find("tbody").find("tr", {"class": "team-row"})
        buttonCell = TeamRow.find("td", {"class": "stats-button-cell"}).find("a").get("href")

        link = "https://www.hltv.org/" + str(buttonCell)
        return link, img["src"]

    def hltv_lastmatch_player(self, player):
        """
        Method finds information about player's last match
        :param player: nickname of player, which will be used in method
        :return: list of 2 elements - dictPlayerStats(player stats which are in dictionary)
                                    - img(image source)
        """
        assert isinstance(player, str)
        """
        Getting a link with 'hltv_lastmatch_linkfinder' method
        """
        try:
            link, img = self.hltv_lastmatch_linkfinder(player)
        except FileNotFoundError:
            raise FileNotFoundError
        except MatchBoxListException:
            raise MatchBoxListException

        req = requests.get(
            str(link)
        )

        page = BeautifulSoup(req.content, "lxml")

        divConCol = page.find("div", {"class": "contentCol"})
        divStatsMatch = divConCol.find("div", {"class": "stats-match"})  # finds div with class "stats-match"

        # finds all tables with class "stats-table"
        tableWithStats = divStatsMatch.find_all("table", {"class": "stats-table"})

        """
        tableWithStats is a list and now we need to find there stats of our player.
        First 'for' will find all players.
        Second 'for' will search the player that we need in a list of players.
        """
        dictPlayerStats = {}
        for i in tableWithStats:
            playersStats = i.find("tbody").find_all("tr")
            for j in playersStats:
                foundNick = j.find("td", {"class": "st-player"}).text
                foundNick = foundNick.rstrip().strip().lower()
                if str(foundNick) == str(player):
                    dictPlayerStats["NICKNAME"] = foundNick
                    dictPlayerStats["KILLS"] = j.find("td", {"class": "st-kills"}).text
                    dictPlayerStats["ASSISTS"] = j.find("td", {"class": "st-assists"}).text
                    dictPlayerStats["DEATHS"] = j.find("td", {"class": "st-deaths"}).text
                    dictPlayerStats["KAST"] = j.find("td", {"class": "st-kdratio"}).text
                    dictPlayerStats["ADR"] = j.find("td", {"class": "st-adr"}).text
                    dictPlayerStats["FIRSTKILLS"] = j.find("td", {"class": "st-fkdiff"}).text
                    dictPlayerStats["KD20"] = j.find("td", {"class": "st-rating"}).text
                    return [dictPlayerStats, img]
        raise PlayerNotFoundException


