from dataclasses import dataclass
import valo_api
from enum import Enum
class Team:
    """class for a team, team can have up to 10 players with a minimum of 5,
    team should hold everyones name, region, and tag, should be able to calculate
    average rank as well as store (atleast temporarily) the information about the team
    (because if i get their ranks at 5:30 they wont change by 5:31)"""

    def __init__(self, namea):
        self.name = namea
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)
    
    def calculateAvgRank(self):
        sum = 0
        for obj in self.players:
            if (obj.rankInt != None):
                sum += obj.rankInt
        return sum / len(self.players)

class Queue:
    """class for a Queue, a Queue is a Max 5 minimum 1 team that will have a Time that,
    when reached, will notify all members, (must store their discord tag?). Players in
    a queue must all be in the same region and in the same rank area so they can actually
    play together (i.e. a gold player cannot queue with a diamond, unless in a 5 stack)
    maxplayers will default to 5 but can be set lower, to allow for searching for a duo
    or trio. A queue object will be stored in a dictionary with the owner's name as its key
    Time is an integer, unix time of the time the queue scheduled. Queue will be deleted by
    creator or can expire automatically."""

    def __init__(self, owner, time = 1676242800,  maxplayers = 5):
        self.owner = owner
        self.players = []
        self.maxplayers = maxplayers
        self.time = time # queue time

    def addPlayer(self, player):
        if (len(self.players) < self.maxplayers):
            self.players.append(player)
    
    def calculateAvgRank(self):
        sum = 0
        for obj in self.players:
            if (obj.rankInt != None):
                sum += obj.rankInt
        return sum / len(self.players)



class Player:
    """Player is an object represting the 3 core pieces of storing player data
    their region, their name, their tag (na, cosine, 3893) aswell as potential
    extra data (last checked rank, rr, last played game? etc.)"""
    def __init__(self, region: str, name: str, tag: int):
        self.region = region
        self.name = name
        self.tag = tag
        self.playerData = valo_api.get_mmr_details_by_name(region=self.region,name=self.name,tag=self.tag,version="v2")
        self.rank = self.playerData.current_data.currenttier
        self.rankString = self.playerData.current_data.currenttierpatched
        self.discordName = "cosine"
        self.discordTag = "0616"

def pickColor(rankInt: int):
    colorDict = {3: 0x5D5D5D, 4: 0x5D5D5D, 5: 0x5D5D5D, 6: 0x966B18, 7: 0x966B18, 8: 0x966B18, 9: 0xE1E8E7,  10: 0xE1E8E7,  
                11: 0xE1E8E7, 12: 0xE9C54C, 13: 0xE9C54C, 14: 0xE9C54C, 15: 0x52D5DE, 16: 0x52D5DE, 17: 0x52D5DE, 18: 0xF197F4,
                19: 0xF197F4, 20: 0xF197F4, 21: 0x3CB57B, 22: 0x3CB57B, 23: 0x3CB57B, 24: 0xB02639, 25: 0xB02639, 26: 0xB02639,
                27: 0xFFFFB, None: 0x1B1B1B}
    return colorDict[rankInt]
