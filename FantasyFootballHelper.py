from Tkinter import *

import utils

#connection = None

## write a function that gets player past scores and weightedly averages them.

## Current PLAN:
## create temp clone of players table, work on that.
## get list of discrete positions, for each position create a temporary table.
## for every player in each position, populate appropriate temptable
## with name, weighted_score(primary key order by desc), current_team, position
## check current_team against restrictions on player composition
## then search a join of all temp tables. return player with highest weighted_score
## that fits the current restrictions.
## give option to pick or lost. If picked add to list/dictionary of current team
## whether lost or pick, remove from temp tables.
## repeat until current_team is full

    
class draftgame(object):
    def __init__(self):  #add database, username, password arguments
        """
        initialises current_team
        Connects to the database
        Creates a temp table for each position
        """
        
        self.current_team = {}
        self.connection, self.cursor = utils.connect_to_database() # use database, username, password arguments 
        
        self.clone_table_column_creators = "id integer primary key, name varchar(100), player_url varchar(100), position varchar(100), age integer, current_team varchar(20), team_one_year_ago varchar(20), team_two_year_ago varchar(20), team_three_year_ago varchar(20), points_one_year_ago float, points_two_year_ago float, points_three_year_ago float"
        self.clone_table_columns = "id, name, player_url, position, age, current_team, team_one_year_ago, team_two_year_ago, team_three_year_ago, points_one_year_ago, points_two_year_ago, points_three_year_ago"
        self.temp_table_column_creators = "id integer primary key, name varchar(100), position varchar(100), current_team varchar(20), weighted_score float"
        self.temp_table_columns = "id, name, position, current_team, weighted_score"
        
        utils.create_temp_clone_table("players", "cloneplayers", self.clone_table_column_creators,
                            self.clone_table_columns, self.connection, self.cursor)
        utils.add_column_to_table("cloneplayers", "weighted_score", "float", self.connection, self.cursor)
        utils.update_weighted_scores(self.connection, self.cursor)
        for position in utils.get_positions_list(self.cursor):
            filterposition = position.rstrip('0123456789 ').upper() + '%'
            utils.create_temporary_table(position, self.temp_table_column_creators, self.connection, self.cursor)
            utils.populate_temp_table_from_other_table(position, self.temp_table_columns, "cloneplayers", "position", filterposition, self.connection, self.cursor)
    
    def print_table(self, table):
        utils.print_table(table)
        
    def print_current_team(self):
        print self.current_team
            
    def add_player_to_team(self, player):
        self.current_team[player] = utils.get_player_position(player, self.cursor)
          
    def user_pick_player(self):
        pickmade = False
        while pickmade == False:
            player = raw_input("""Choose Your Player:
        1 for Best Player Available: %s
        2 for Most Recommended Player: %s
        Enter another player:\n-->""" % (self.get_best_player_remaining(), self.most_recommended_player_remaining()))
            if player.startswith("1"):
                print "%s picked\n" % self.get_best_player_remaining()
                self.add_player_to_team(self.get_best_player_remaining())
                utils.remove_player_from_possible_players(self.get_best_player_remaining(), self.connection, self.cursor)
                pickmade = True
            elif player.startswith("2"):
                print "%s picked\n" % self.most_recommended_player_remaining()
                self.add_player_to_team(self.most_recommended_player_remaining())
                utils.remove_player_from_possible_players(self.most_recommended_player_remaining(), self.connection, self.cursor)
                pickmade = True
            elif utils.get_player_position(player, self.cursor) != None:
                print "%s picked as user pick\n" % player
                self.add_player_to_team(player)
                utils.remove_player_from_possible_players(player, self.connection, self.cursor)
                pickmade = True
            else:
                print "%s not found in database\n" % player
        return pickmade
        
    def opponent_pick_player(self):
        pickmade = False
        print "Opponent Picking"
        print "If opponents picks defense, must type whole name e.g. Philadelphia Eagles"
        while pickmade == False:
            player = raw_input("Who did opponent pick?\n--> ")
            if utils.get_player_position(player, self.cursor) != None:
                utils.remove_player_from_possible_players(player, self.connection, self.cursor)
                print "%s removed from available players\n" % player
                pickmade = True
            else:
                print "%s not found in database\n" % player
            
    def check_current_team_positions(self):
        current_positions = {"QB" : 0, "TE" : 0,
                            "RB" : 0, "K" : 0,
                            "WR" : 0, "DEFENSE": 0
                            }
        current_position_list = self.current_team.values()
        for position in current_position_list:
            if position.startswith('QB'):
                current_positions["QB"] += 1
            elif position.startswith('RB'):
                current_positions["RB"] += 1
            elif position.startswith('WR'):
                current_positions["WR"] += 1
            elif position.startswith('TE'):
                current_positions["TE"] += 1
            elif position.startswith('K'):
                current_positions["K"] += 1
            elif position.startswith('DEF'):
                current_positions["DEFENSE"] += 1
    
        return current_positions
        
    def get_possible_players_tuples(self, limit):
        """
        returns a list of tuples of playername, weighted score and position,
        number of elements is top (limit) from each position.
        """
        assert type(limit) == str
        possible_players = []
        for position in utils.get_positions_list(self.cursor):
            for player in utils.get_top_values(position, "name, weighted_score, position", "weighted_score", limit, self.cursor):
                possible_players.append(player)
        return possible_players
          
    def get_best_player_remaining(self):
        """ 
        Finds the current highest rated player remaining
        returns as string of player name 
        """
        possible_players = self.get_possible_players_tuples("1")
        scores = []
        for player in possible_players:
            scores.append(player[1])
        bestscore = max(scores)
        for player in possible_players:
            if player[1] == bestscore:
                return str(player[0])
        return None

    def get_list_of_best_players(self, limit):
        """
        returns a list of tuples of playername, weighted score and position,
        number of elements returned determined by top (limit) across all positions
        """
        assert type(limit) == str
        possibleplayers = self.get_possible_players_tuples(limit)
        
        possibleplayers.sort(key=lambda t: t[1], reverse=True)
        
        return possibleplayers[:int(limit) + 1]
        
    def check_current_team_needs(self):
        """need 1QB, 2RB, 2WR, 1 TE, 1 K, 1 Def, 1 Flex, 7 Bench"""
        needs = {}
        required_team = {"QB" : 1, "TE" : 1,
                         "RB" : 2, "K" : 1,
                         "WR" : 2, "DEFENSE": 1,
                         "Flex" : 1, "Bench" : 7
                         }
        current_positions = self.check_current_team_positions()
        for position in required_team.keys():
            try:
                if current_positions[position] < required_team[position]:
                    needs[position] = required_team[position] - current_positions[position]
            except:
                pass
        return needs
        
    def clear_finished_tables(self):
        for position in utils.get_positions_list(self.cursor):
            if position not in self.check_current_team_needs():
                utils.clear_table(position, self.connection, self.cursor)
                
    def try_mean(self, list):
        try:
            mean = sum(list) / len(list)
        except:
            mean = None
        return mean

    def try_variance(self, list, mean):
        try:
            variance = sum((mean - item) ** 2 for item in list) / len(list)
        except:
            variance = 0
        return variance ** (0.5)
        
    def make_variance_dictionary(self, playerlist):
        
        qb, rb, wr, te, k, defense = [], [], [], [], [], []
        
        for player in playerlist:
            if player[2].rstrip('0123456789 ').upper() == "QB":
                qb.append(player[1])
            elif player[2].rstrip('0123456789 ').upper() == "RB":
                rb.append(player[1])
            elif player[2].rstrip('0123456789 ').upper() == "WR":
                wr.append(player[1])
            elif player[2].rstrip('0123456789 ').upper() == "TE":
                te.append(player[1])
            elif player[2].rstrip('0123456789 ').upper() == "K":
                k.append(player[1])
            elif utils.defense_fixer(player[2]) == "DEFENSE":
                defense.append(player[1])
        
        qbmean = self.try_mean(qb)
        rbmean = self.try_mean(rb)
        wrmean = self.try_mean(wr)
        temean = self.try_mean(te)
        kmean = self.try_mean(k)
        defmean = self.try_mean(defense)
                
        qbvar = self.try_variance(qb, qbmean)
        rbvar = self.try_variance(rb, rbmean)
        wrvar = self.try_variance(wr, wrmean)
        tevar = self.try_variance(te, temean)
        kvar = self.try_variance(k, kmean)
        defvar = self.try_variance(defense, defmean)
        
        vardict = {"QB": qbvar, "RB": rbvar, "WR": wrvar,
                   "TE": tevar, "K": kvar, "DEFENSE": defvar}
                   
        return vardict
        
    def most_recommended_player_remaining(self):
        
        possible_players = self.get_possible_players_tuples("1")
        
        vardict = self.make_variance_dictionary(self.get_possible_players_tuples("5"))
        maxvar = max(vardict.values())
        
        for position in vardict:
            if vardict[position] == maxvar:
                bestposition = position
                
        for player in possible_players:
            if utils.defense_fixer(player[2].rstrip('0123456789 ').upper()) == bestposition:
                return str(player[0])
            
        return None
        
    def get_list_recommended_players(self, limit):
        
        assert type(limit) == str
        possibleplayers = self.get_possible_players_tuples(limit)
       
        vardict = self.make_variance_dictionary(possibleplayers)
        recommendedplayers = []
       
        for player in possibleplayers:
            position = utils.defense_fixer(player[2]).rstrip('0123456789 ').upper()
            
            newtuple = (player[0],
                        player[1] + vardict[position],
                        player[2])
                        
            recommendedplayers.append(newtuple)
            
        recommendedplayers.sort(key=lambda t: t[1], reverse=True)
        
        return recommendedplayers[:int(limit) + 1]

#numberofopponents = int(raw_input("How many other people are drafting?"))
#draft_position = int(raw_input("What position in the First Round are you drafting?"))
#numberofrounds = int(raw_input("How many rounds are you drafting?"))
#draft_type = "snake"
#round = 1
        
# while round <= numberofrounds:
    # if draft_type == "linear":
        # print "\nStart of round: %d\n\n" % round
        # for x in xrange(1, draft_position):
            # print "Opponent %d picking:" % x
            # ffhelper.opponent_pick_player()
        # ffhelper.user_pick_player()
        # for x in xrange(draft_position, numberofopponents + 1):
            # print "Opponent %d picking:" % x
            # ffhelper.opponent_pick_player()
        # print "Team Check", ffhelper.check_current_team_positions()
        # print "Current Team", ffhelper.current_team
        # print "Current Team Needs:", ffhelper.check_current_team_needs()
        # ffhelper.clear_finished_tables()
        # round += 1
        
    # if draft_type == "snake":
        # print "\nStart of round: %d\n\n" % round
        # for x in xrange(1, draft_position):
            # print "Opponent %d picking:" % x
            # ffhelper.opponent_pick_player()
        # ffhelper.user_pick_player()
        # for x in xrange(draft_position, numberofopponents + 1):
            # print "Opponent %d picking:" % x
            # ffhelper.opponent_pick_player()
        # print "Team Check", ffhelper.check_current_team_positions()
        # print "Current Team", ffhelper.current_team
        # print "Current Team Needs:", ffhelper.check_current_team_needs()
        # ffhelper.clear_finished_tables()
        # round += 1
        
        # print "\nStart of round: %d\n\n" % round
        # for x in xrange(1, ffhelper.numberofopponents + 1 - draft_position):
            # print "Opponent %d picking:" % (numberofopponents + 1 - x)
            # ffhelper.opponent_pick_player()
        # ffhelper.user_pick_player()
        # for x in xrange(numberofopponents - draft_position + 1, numberofopponents + 1):
            # print "Opponent %d picking:" % (draft_position + 1 - x)
            # ffhelper.opponent_pick_player()
        # print "Team Check", ffhelper.check_current_team_positions()
        # print "Current Team", ffhelper.current_team
        # print "Current Team Needs:", ffhelper.check_current_team_needs()
        # ffhelper.clear_finished_tables()
        # round += 1
        
#print "\n\nWHILE LOOP FINISHED"
#print "FINAL TEAM:"
#for player in ffhelper.current_team:
#    print player
    

#if connection:
#   connection.close()