import requests
from bs4 import BeautifulSoup
from commands.HLTVcommands3 import HLTVStats3
from other.Exceptions import MatchBoxListException, WebSiteNotFoundException
from other.WorkWithFiles import WorkWithCSV


class HLTVStats4:
    """
    Another class with commands which are parsing page for information
    """
    csvfile = WorkWithCSV()

    # TODO could be better

    def hltv_upcoming_matches(self, team):
        """
        Finds upcoming matches for the team
        :param team:
        :return: list of matches
        """
        matchsWinRate = {}
        eventList = []
        team = team.lower()
        # TODO this part of code repeats itself sometimes (could be a method)
        if " " in team:
            team = team.replace(" ", "-")
        try:
            code = self.csvfile.get_info_teams()[team]
        except FileNotFoundError:
            raise FileNotFoundError
        req = requests.get("https://www.hltv.org/team/" + code + "/" + team + "#tab-matchesBox")
        page = BeautifulSoup(req.content, "lxml")

        try:
            hh = page.find("h1").text
            if str(hh) == "404":
                return "Oops, it looks like we cant find this team... Try it later"
        except Exception:
            pass

        teamProfile = page.find("div", {"class", "teamProfile"})
        matchesBox = teamProfile.find("div", {"class", "highlighted-stats-box"}).find_all("div", {"class": "stat"})

        tableCon = teamProfile.find_all("table", {"class": "match-table"})
        tbodys = ["none string ;)"]

        if len(tableCon) == 1:
            # Why
            if " " in team:
                team = team.replace(" ", "-")
            code = self.csvfile.get_info_teams()[team]
            return "No upcoming matches for " + team.title() + ", check back later.\n\n"
        else:
            theads = tableCon[0].find_all("thead")
            tbodytemp = tableCon[0].find_all("tbody")

        for i in tbodytemp:
            tbodys.append(i)

        # TODO COULD BE A METHOD
        for i in range(len(theads)):
            if (i != 0) and (i < 3):
                eventName = theads[i].text
                event = {}
                matches = []
                teamrow = tbodys[i].find_all("tr", {"class": "team-row"})
                for x in teamrow:
                    match = {"date": x.find("td", {"class": "date-cell"}).text}
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

    def hltv_team_achievements(self, team):
        assert isinstance(team, str)
        team = team.lower()
        eventList = []
        if " " in team:
            team = team.replace(" ", "-")
        try:
            code = self.csvfile.get_info_teams()[team]
        except FileNotFoundError:
            # return "Oops, it looks like our file is damaged. Try it later."
            raise FileNotFoundError
        req = requests.get("https://www.hltv.org/team/" + code + "/" + team + "#tab-achievementsBox")
        page = BeautifulSoup(req.content, "lxml")

        try:
            hh = page.find("h1").text
            if str(hh) == "404":
                raise WebSiteNotFoundException
        except Exception:
            pass

        achievementBox = page.find("div", {"id": "achievementsBox"})
        lanAchievements = achievementBox.find("div", {"id": "lanAchievement"}).find("tbody").find_all("tr")

        for i in range(len(lanAchievements)):
            if i < 10:
                event = {
                    lanAchievements[i].find("a").text: lanAchievements[i].find("div", {"class": "achievement"}).text
                }
                eventList.append(event)

        return eventList


    def hltv_lastmatch_team(self, team):
        assert isinstance(team, str)

        HLTV = HLTVStats3()
        """
        Getting a link with 'hltv_lastmatch_linkfinder' method, which is in other class
        """
        try:
            link, img = HLTV.hltv_lastmatch_linkfinder(team)
        except FileNotFoundError:
            raise FileNotFoundError
        except MatchBoxListException:
            raise MatchBoxListException

        req = requests.get(
            str(link)
        )

        page = BeautifulSoup(req.content, "lxml")

        divConCol = page.find("div", {"class": "contentCol"})  # finds div with class "contentCol"
        divTeamsBox = divConCol.find("div", {"class": "teamsBox"})  # finds div with class "teamsBox"

        match = {}
        maps = []

        """Finds teams and their score in the match"""
        divTeams = divTeamsBox.find_all("div", {"class": "team"})  # finds all divs with class "team"

        team1 = divTeams[0].find("div", {"class": "team1-gradient"}).find_all("div")[0].text.strip().rstrip()
        team1 = team1 + " " + divTeams[0].find("div", {"class": "team1-gradient"}).find_all("div")[1].text.strip(). \
            rstrip()
        team2 = divTeams[1].find("div", {"class": "team2-gradient"}).find_all("div")[0].text.strip().rstrip()
        team2 = divTeams[1].find("div", {"class": "team2-gradient"}).find_all("div")[1].text.strip().rstrip() \
                + " " + team2

        match["score"] = team1 + " : " + team2
        """--end"""

        """Finds event name, time and day of the match"""
        divTimeAndEvent = divTeamsBox.find("div", {"class": "timeAndEvent"})
        match["time"] = divTimeAndEvent.find("div", {"class": "time"}).text
        match["day"] = divTimeAndEvent.find("div", {"class": "date"}).text
        match["event"] = divTimeAndEvent.find("div", {"class": "event"}).text
        """--end"""

        """Finds played maps and their score"""
        divMaps = divConCol.find("div", {"class": "maps"})
        divPlayedMaps = divMaps.find("div", {"class": "flexbox-column"})
        divMapsHolder = divPlayedMaps.find_all("div", {"class": "mapholder"})
        for i in divMapsHolder:
            mapInfo = {}
            temp = i.find("div", {"class": "played"})
            if temp is not None:
                lost = i.find("div", {"class": "lost"})
                if lost is None:
                    lost = i.find("span", {"class": "lost"})
                mapInfo["NAME"] = temp.text.rstrip("\n").strip("\n")
                mapInfo["LOST"] = lost.find("div", {"class": "results-teamname"}).text.rstrip("\n").strip("\n")
                mapInfo["LOST_SCORE"] = lost.find("div", {"class": "results-team-score"}).text.rstrip("\n").strip("\n")
                won = i.find("span", {"class": "won"})
                if won is None:
                    won = i.find("div", {"class": "won"})
                mapInfo["WON"] = "**" + str(won.find("div", {"class": "results-teamname"}).text) + "**".rstrip("\n")\
                    .strip("\n")
                mapInfo["WON_SCORE"] = "**" + str(won.find("div", {"class": "results-team-score"}).text) + "**"\
                    .rstrip("\n").strip("\n")
                maps.append(mapInfo)

        match["MAPS"] = maps

        return match

    def hltv_teams_ranking3(self):
        """
        Method shows top 30 (21-30) teams at the moment
        :return: list of these teams
        """
        teamlist = []
        req = requests.get(
            "https://www.hltv.org/ranking/teams")
        page = BeautifulSoup(req.content, "lxml")
        divteams = page.find_all("div", {"class": "ranked-team standard-box"})
        count = 1
        for i in divteams:
            if count < 22:
                count += 1
            if 22 <= count < 32:
                team = {}
                count += 1
                team["position"] = i.find("span", {"class": "position"}).text
                team["name"] = i.find("span", {"class": "name"}).text
                team["points"] = i.find("span", {"class": "points"}).text
                teamlist.append(team)
        return teamlist
