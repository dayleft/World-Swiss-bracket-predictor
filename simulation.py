import random

class Team:
    def __init__(self,rating,name):
        self.rating = rating
        self.name = name
        self.wins = 0
        self.losses = 0
        self.defeated = []
        self.defeatedBy = []
        self.numQf = 0
        self.prob = 1

    def resetRecord(self):
        self.wins = 0
        self.losses = 0
        self.defeated = []
        self.defeatedBy = []

    def __str__(self):
        return self.name


class TeamGroup:
    def __init__(self,name,teams):
        self.name = name
        self.teams = teams
        self.prob = 1
        self.probsNot = 1


class Series:
    def __init__(self,team1,team2,winsReq):
        self.team1 = team1
        self.team1Wins = 0
        self.team2 = team2
        self.team2Wins = 0
        self.winsReq = winsReq

    def runGame(self):
        chance = random.randint(1,100)
        if chance <= self.winpercentage():
            self.team1Wins = self.team1Wins + 1
        else:
            self.team2Wins = self.team2Wins + 1


    def runSeries(self):
        while self.team1Wins < self.winsReq and self.team2Wins < self.winsReq:
            self.runGame()
        if self.team1Wins > self.team2Wins:
            self.team1.defeated.append(self.team2)
            self.team2.defeatedBy.append(self.team1)
            return (self.team1,self.team2)
        else:
            self.team2.defeated.append(self.team1)
            self.team1.defeatedBy.append(self.team2)
            return (self.team2,self.team1)

    def winpercentage(self):
        ratingdiff = self.team1.rating - self.team2.rating
        percentperdiff = 3
        winpercent = (ratingdiff * percentperdiff) + 50
        if winpercent > 95:
            return 95
        elif winpercent <5:
            return 5
        else:
            return winpercent
        

        

class Bracket:
    def __init__(self,T1,TL,C9,MAD,GenG,GAM,JDG,BDS,G2,DK,NRG,WBG,FNC,LNG,BLG,KT):
        self.groups = {(0,0):[],
                        (1,0):[],
                        (0,1):[],
                        (1,1):[],
                        (0,2):[],
                        (2,1):[],
                        (1,2):[],
                        (2,0):[],
                        (2,2):[]
                       }
        self.matchupHistory = {(0,0):[(T1,TL),(C9,MAD),(GenG,GAM),(JDG,BDS),(G2,DK),(NRG,WBG),(FNC,LNG),(BLG,KT)],
                        (1,0):[],
                        (0,1):[],
                        (1,1):[],
                        (2,0):[],
                        (0,2):[],
                        (1,2):[],
                        (2,1):[],
                        (2,2):[]
                       }
        self.round = 0
        self.matchups = [(T1,TL),(C9,MAD),(GenG,GAM),(JDG,BDS),(G2,DK),(NRG,WBG),(FNC,LNG),(BLG,KT)]
        self.seriesWinsReq = 2

    
    def runMatchups(self):
        for match in self.matchups:
            team1 = match[0]
            team2 = match[1]
            winsRequired = 0
            if team1.wins == 2 or team1.losses == 2:
                winsRequired = self.seriesWinsReq;
            else:
                winsRequired = 1
            series = Series(team1,team2,winsRequired)
            (winner,loser) = series.runSeries()
            
            winner.wins = winner.wins + 1
            loser.losses = loser.losses + 1

            if winner.wins != 3:
                self.groups[(winner.wins,winner.losses)].append(winner)
            else:
                winner.numQf = winner.numQf + 1
                winner.resetRecord()
                
            if loser.losses != 3:
                self.groups[(loser.wins,loser.losses)].append(loser)
            else:
                loser.resetRecord()
        self.matchups = []
        self.round = self.round + 1
        
    
    def nextRound(self):
        for record in self.groups.keys():
            if self.round == (record[0]+record[1]):
                teams = self.groups[record]
                numTeams = len(teams)
                randTeams = random.sample(teams,numTeams)
                for i in range(0,numTeams,2):
                    self.matchups.append((randTeams[i],randTeams[i+1]))
                    self.matchupHistory[record].append((randTeams[i],randTeams[i+1]))


    def __str__(self):
        string = ""
        for round in self.matchupHistory.keys():
            string = string + str(round) + ": " + "\n"
            for matchup in self.matchupHistory[round]:
                string = string + str(matchup[0]) + " vs " + str(matchup[1]) + "\n"
        return string
        

def simulation():
    numSimulated = 10000
    JDG = Team(98,"JDG")
    BLG = Team(92,"BLG")
    LNG = Team(96,"LNG")
    WBG = Team(87,"WBG")
    GenG = Team(95,"GenG")
    T1 = Team(92,"T1")
    KT = Team(89,"KT")
    DK = Team(89,"DK")
    G2 = Team(88,"G2")
    FNC = Team(80,"FNC")
    MAD = Team(78,"MAD")
    BDS = Team(75,"BDS")
    NRG = Team(80,"NRG")
    C9 = Team(78,"C9")
    TL = Team(76,"TL")
    GAM = Team(75,"GAM")

    teams = [T1,TL,C9,MAD,GenG,GAM,JDG,BDS,G2,DK,NRG,WBG,FNC,LNG,BLG,KT]
    k_teams = TeamGroup("Korean Teams",[T1,GenG,KT,DK])
    c_teams = TeamGroup("Chinese Teams",[JDG,LNG,BLG,WBG])
    asia_teams = TeamGroup("Asia Teams",k_teams.teams + c_teams.teams)
    na_teams = TeamGroup("Trash Teams",[TL,C9,NRG,GAM])
    eu_teams = TeamGroup("EU Garbo Combustable Teams",[G2,FNC,MAD,BDS])
    west_teams = TeamGroup("Western Teams",na_teams.teams + eu_teams.teams)
    teamGroups = [k_teams,c_teams,asia_teams,na_teams,eu_teams,west_teams]
    
    for i in range(numSimulated):
        bracket = Bracket(T1,TL,C9,MAD,GenG,GAM,JDG,BDS,G2,DK,NRG,WBG,FNC,LNG,BLG,KT)
        while len(bracket.matchups) > 0:
            bracket.runMatchups()
            bracket.nextRound()
        #if NRG.numQf == 1:
            #print(bracket)
            #print("\n")
    for team in teams:
        team.prob = team.numQf/numSimulated
        print(team.name + ": " + str(round(team.numQf/numSimulated * 100,2)) + "%")
    for teamGroup in teamGroups:
        for team in teamGroup.teams:
            teamGroup.prob = teamGroup.prob * (team.numQf/numSimulated)
            teamGroup.probsNot = teamGroup.probsNot * (1-(team.numQf/numSimulated))

        teamOneGetsOut = teamGroup.teams[0].prob * (1-teamGroup.teams[1].prob) * (1-teamGroup.teams[2].prob) * (1-teamGroup.teams[3].prob)
        teamTwoGetsOut = teamGroup.teams[1].prob * (1-teamGroup.teams[0].prob) * (1-teamGroup.teams[2].prob) * (1-teamGroup.teams[3].prob)
        teamThreeGetsOut = teamGroup.teams[2].prob * (1-teamGroup.teams[1].prob) * (1-teamGroup.teams[0].prob) * (1-teamGroup.teams[3].prob)
        teamFourGetsOut = teamGroup.teams[3].prob * (1-teamGroup.teams[1].prob) * (1-teamGroup.teams[0].prob) * (1-teamGroup.teams[2].prob)
        oneTeamGetsOut = teamOneGetsOut + teamTwoGetsOut + teamThreeGetsOut + teamFourGetsOut
        twoOrMoreGetsOut = 1 - (oneTeamGetsOut + teamGroup.probsNot)
        print(teamGroup.name + " all get out: " + str(round(teamGroup.prob*100,2)) + "%")
        print(teamGroup.name + " at least 1 gets out: " + str(round((1-teamGroup.probsNot)*100,2)) + "%")
        print(teamGroup.name + " at least 2 gets out: " + str(round((twoOrMoreGetsOut)*100,2)) + "%")
        

simulation()
