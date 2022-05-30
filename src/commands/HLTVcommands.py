import requests
from bs4 import BeautifulSoup
import datetime
from other.Exceptions import NoOngoingMatchesException


class HLTVStats:
    """
    Class with commands which are parsing page for information
    """
    # TODO command names could be better
    hltvcomhelp = {"!hltv players 12": "Top 10 players for last 12 months",
                   "!hltv players 6": "Top 10 players for last 6 months",
                   "!hltv team ranking 10": "Teams ranking 1-10",
                   "!hltv team ranking 20": "Teams ranking 11-20",
                   "!hltv team ranking 30": "Teams ranking 21-30",
                   "!hltv ongoing events": "Events that are currently ongoing",
                   "!hltv upcoming events": "Events that are yet to come",
                   "!hltv results": "Match results",
                   "!hltv ongoing matches": "Matches that are currently ongoing",
                   "!hltv upcoming matches": "Matches that are yet to come",
                   "!hltv unknown matches": "Matches that are unknown",
                   "!hltv news": "Last news articles",
                   "!hltv player 'player nickname'": "Shows player stats",
                   "!hltv team information 'team name'": "Shows basic information about the team",
                   "!hltv matches 'team name'": "Shows information about recent and future matches",
                   "!hltv achievements 'team name'": "Shows information about last LAN events (max are 10 events)",
                   "!hltv leaderboard": "Shows current leaderboard",
                   "!hltv last match 'player name'(or you can use 'team name')": "Shows information about last"
                                                                                 " player's/team's match",
                   "!hltv team history 'player name'": "Shows information about player's teams in past",
                   "!hltv maps 'team name'": "Shows information about team's map pool"
                   }

    def page_parsing(self, url):
        assert type(url) is str
        req = requests.get(
            str(url))
        page = BeautifulSoup(req.content, "lxml")
        return page

    def hltv_top_players12(self):
        """
        Method finds top 10 players for last 12 months
        :return: list of these players
        """
        playerlist = []
        date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        date_year_ago = str((datetime.datetime.now() - datetime.timedelta(days=1 * 365)).strftime('%Y-%m-%d'))
        req = requests.get(
            "https://www.hltv.org/stats/players?startDate=" + date_year_ago + "&endDate="
            + date + "&rankingFilter=Top20")
        page = BeautifulSoup(req.content, "lxml")
        divclass = page.find_all("tbody")[0]
        divtop = divclass.find_all("tr")
        count = 1
        for i in divtop:
            if count < 11:
                count += 1
                player = {"nickname": i.find("a").text, "rating": i.find_all("td", {"class": "statsDetail"})[2].text,
                          "hltv_rating": i.find("td", {"class": "ratingCol"}).text}
                playerlist.append(player)
        return playerlist

    def hltv_top_players6(self):
        """
        Method finds top 10 players for last 6 months
        :return: list of these players
        """
        playerlist = []
        date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        date_hfyr_ago = str((datetime.datetime.now() - datetime.timedelta(days=0.5 * 365)).strftime('%Y-%m-%d'))
        req = requests.get(
            "https://www.hltv.org/stats/players?startDate=" + date_hfyr_ago + "&endDate="
            + date + "&rankingFilter=Top20")
        page = BeautifulSoup(req.content, "lxml")
        divclass = page.find_all("tbody")[0]
        divtop = divclass.find_all("tr")
        count = 1
        for i in divtop:
            if count < 11:
                count += 1
                player = {"nickname": i.find("a").text, "rating": i.find_all("td", {"class": "statsDetail"})[2].text,
                          "hltv_rating": i.find("td", {"class": "ratingCol"}).text}
                playerlist.append(player)
        return playerlist

    def hltv_teams_ranking(self):
        """
        Method shows top 10 (1-10) teams at the moment
        :return: list of these teams
        """
        teamlist = []
        req = requests.get(
            "https://www.hltv.org/ranking/teams")
        page = BeautifulSoup(req.content, "lxml")
        divteams = page.find_all("div", {"class": "ranked-team standard-box"})
        count = 1
        for i in divteams:
            # print(i)
            if count < 11:
                team = {}
                count += 1
                team["position"] = i.find("span", {"class": "position"}).text
                team["name"] = i.find("span", {"class": "name"}).text
                team["points"] = i.find("span", {"class": "points"}).text
                teamlist.append(team)
        return teamlist

    # TODO SPLIT BY "-" | CHOOSE RANKING (ex. !hltv ranking 10-20, !hltv ranking 1-10,...)

    def hltv_teams_ranking2(self):
        """
        Method shows top 20 (11-20) teams at the moment
        :return: list of these teams
        """
        teamlist = []
        req = requests.get(
            "https://www.hltv.org/ranking/teams")
        page = BeautifulSoup(req.content, "lxml")
        divteams = page.find_all("div", {"class": "ranked-team standard-box"})
        count = 1
        for i in divteams:
            if count < 12:
                count += 1
            if 12 <= count < 22:
                team = {}
                count += 1
                team["position"] = i.find("span", {"class": "position"}).text
                team["name"] = i.find("span", {"class": "name"}).text
                team["points"] = i.find("span", {"class": "points"}).text
                teamlist.append(team)
        return teamlist

    def hltv_ongoing_events(self):
        """
        Method shows ongoing events on csgo pro scene
        :return: list of these events
        """
        eventlist = []
        page = self.page_parsing("https://www.hltv.org/events#tab-TODAY")
        div_ev_live = page.find_all("div", {"class": "ongoing-events-holder"})
        templist = []
        try:
            for i in div_ev_live:
                a_ev_live = i.find_all("a", {"class": "a-reset ongoing-event"})
                for j in a_ev_live:
                    event = {}
                    if j.find("div", {"class": "text-ellipsis"}).text not in templist:
                        event["name"] = j.find("div", {"class": "text-ellipsis"}).text
                        templist.append(j.find("div", {"class": "text-ellipsis"}).text)
                        if len(j.find_all("span", {"data-time-format": "MMM do"})) > 1:
                            event["from_date"] = j.find_all("span", {"data-time-format": "MMM do"})[0].text
                            event["to_date"] = j.find_all("span", {"data-time-format": "MMM do"})[1].text
                        else:
                            event["from_date"] = j.find_all("span", {"data-time-format": "MMM do"})[0].text
                            event["to_date"] = "Unknown"
                        eventlist.append(event)
        except AttributeError:
            raise AttributeError

        return eventlist

    def hltv_upcoming_events(self):
        """
        Method shows upcoming events on csgo pro scene
        :return: list of these events
        """
        eventlist = []
        page = self.page_parsing("https://www.hltv.org/events")
        div_ev = page.find("div", {"class": "events-month"})
        div_date = div_ev.find("div", {"class": "standard-headline"}).text
        div_ev_a = div_ev.find_all("a", {"class": "a-reset small-event standard-box"})
        for i in div_ev_a:
            event = {}
            event["name"] = i.find("div", {"class": "text-ellipsis"}).text
            event["prize"] = i.find("td", {"class": "prizePoolEllipsis"}).text
            event["type"] = i.find("td", {"class": "gtSmartphone-only"}).text
            eventlist.append(event)
        return eventlist, div_date

    def hltv_match_results(self):
        """
        Method shows result of recent featured matches
        :return: list of these matches, name of the event, title
        """
        resultlist = []
        eventname = ""
        page = self.page_parsing("https://www.hltv.org/results")
        divres = page.find_all("div", {"class": "big-results"})
        featured = page.find("h1", {"class": "standard-headline"}).text

        for i in divres:
            divname = i.find("div", {"class": "text-ellipsis"})
            divteamstemp = i.find("div", {"class": "results-sublist"})
            divteams = divteamstemp.find_all("div", {"class": "result-con"})
            for j in divteams:
                result = {}
                result["team_1"] = j.find_all("div", {"class": "team"})[0].text
                result["score"] = j.find("td", {"class": "result-score"}).text
                result["team_2"] = j.find_all("div", {"class": "team"})[1].text
                result["event_name"] = divname.find("span").text
                resultlist.append(result)
        return resultlist, eventname, featured

    def hltv_match_results2(self):
        """
        Method shows result of recent matches
        :return: list of these matches, day of the match
        """
        resultlist = []
        page = self.page_parsing("https://www.hltv.org/results")
        divtemp = page.find("div", {"class": "allres"})
        divteamstemp = divtemp.find("div", {"class": "results-sublist"})
        divteams = divteamstemp.find_all("div", {"class": "result-con"})
        day = divteamstemp.find("span", {"class": "standard-headline"}).text
        for j in divteams:
            result = {}
            result["team_1"] = j.find_all("div", {"class": "team"})[0].text
            result["score"] = j.find("td", {"class": "result-score"}).text
            result["team_2"] = j.find_all("div", {"class": "team"})[1].text
            result["event_name"] = j.find("span", {"class": "event-name"}).text
            resultlist.append(result)
        return resultlist, day

    # TODO send link on streams
    def hltv_match_ongoing(self):
        """
        Method shows ongoing csgo matches
        :return: list of these matches
        """
        livematchlist = []
        page = self.page_parsing("https://www.hltv.org/matches")
        divlive = page.find("div", {"class": "liveMatchesSection"})
        if divlive is None:
            raise NoOngoingMatchesException
        divlive_matches = divlive.find_all("div", {"class": "liveMatch"})

        for i in divlive_matches:
            livematches = {}
            fadedstars = i.find_all("i", {"class": "faded"})
            livematches["stars"] = 5 - len(fadedstars)
            livematches["format"] = i.find("div", {"class": "matchMeta"}).text
            divmatch_teams = i.find_all("div", {"class": "matchTeam"})
            temp = divmatch_teams[0]
            temp2 = divmatch_teams[1]
            livematches["team_1"] = temp.find("div", {"class": "matchTeamName"}).text
            ahref = i.find(href=True)

            site = ahref['href']
            page2 = self.page_parsing("https://www.hltv.org" + site)
            livematches["team_1_score"] = "unknown"  # temp.find("span", {"class": "currentMapScore"}).text
            livematches["team_1_map"] = "unknown"  # temp.find("span", {"class": "mapScore"}).text
            livematches["team_2"] = temp2.find("div", {"class": "matchTeamName"}).text
            livematches["team_2_score"] = "unknown"  # temp.find("span", {"class": "currentMapScore"}).text
            livematches["team_2_map"] = "unknown"  # temp.find("span", {"class": "mapScore"}).text

            livematchlist.append(livematches)
        return livematchlist


