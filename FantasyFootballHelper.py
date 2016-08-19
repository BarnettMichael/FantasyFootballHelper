import utils


class DraftGame(object):
    def __init__(self):
        """
        initialises current_team
        Connects to the database
        Creates a temp table for each position
        """
        
        self.current_team = {}
        self.connection, self.cursor = utils.connect_to_database()
        
        self.clone_table_column_creators = "id integer primary key, name varchar(100), player_url varchar(100), position varchar(100), age integer, current_team varchar(20), team_one_year_ago varchar(20), team_two_year_ago varchar(20), team_three_year_ago varchar(20), points_one_year_ago float, points_two_year_ago float, points_three_year_ago float"
        self.clone_table_columns = "id, name, player_url, position, age, current_team, team_one_year_ago, team_two_year_ago, team_three_year_ago, points_one_year_ago, points_two_year_ago, points_three_year_ago"
        self.temp_table_column_creators = "id integer primary key, name varchar(100), position varchar(100), current_team varchar(20), weighted_score float"
        self.temp_table_columns = "id, name, position, current_team, weighted_score"
        
        utils.create_temp_clone_table("players", "cloneplayers", self.clone_table_column_creators,
                                      self.clone_table_columns, self.connection, self.cursor)
        utils.add_column_to_table("cloneplayers", "weighted_score", "float", self.connection, self.cursor)
        utils.update_weighted_scores(self.connection, self.cursor)
        for position in utils.get_positions_list(self.cursor):
            filter_position = position.rstrip('0123456789 ').upper() + '%'
            utils.create_temporary_table(position, self.temp_table_column_creators, self.connection, self.cursor)
            utils.populate_temp_table_from_other_table(position, self.temp_table_columns, "cloneplayers", "position", filter_position, self.connection, self.cursor)
            
    def add_player_to_team(self, player):

        position = utils.get_player_position(player, self.cursor).rstrip('0123456789 ').upper()

        if utils.get_player_from_table(player, position, self.cursor) is not None:
            self.current_team[player] = position

        else:
            raise Exception("Couldn't add player to team")
            
    def check_current_team_positions(self):
        current_positions = {"QB": 0, "TE": 0,
                             "RB": 0, "K": 0,
                             "WR": 0, "DEFENSE": 0
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
        
    def get_needed_positions(self):

        positions = utils.get_positions_list(self.cursor)

        for position in positions:
            if position not in self.check_current_team_needs():
                positions.remove(position)

        return positions

    def get_possible_players_tuples(self, limit):
        """
        returns a list of tuples of player_name, weighted score and position,
        number of elements set by limit
        ordered by top weighted score from each position.
        """
        assert type(limit) == str
        possible_players = []
        for position in self.get_needed_positions():
            for player in utils.get_top_values(
                    position, "name, weighted_score, position",
                    "weighted_score", limit, self.cursor):

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
        best_score = max(scores)
        for player in possible_players:
            if player[1] == best_score:
                return str(player[0])
        return None

    def get_list_of_best_players(self, limit):
        """
        returns a list of tuples of player_name, weighted score and position,
        number of elements returned determined by top (limit) across all positions
        """
        assert type(limit) == str
        possible_players = self.get_possible_players_tuples(limit)
        
        possible_players.sort(key=lambda t: t[1], reverse=True)
        
        return possible_players[:int(limit)]
        
    def check_current_team_needs(self):
        """need 1QB, 2RB, 2WR, 1 TE, 1 K, 1 Def, 1 Flex, 7 Bench"""
        needs = {}
        required_team = {"QB": 1, "TE": 1,
                         "RB": 2, "K": 1,
                         "WR": 2, "DEFENSE": 1,
                         "Flex": 1, "Bench": 7
                         }

        current_positions = self.check_current_team_positions()

        for position in required_team.keys():
            try:
                if current_positions[position] < required_team[position]:
                    needs[position] = required_team[position] - current_positions[position]
            except:
                pass

        return needs
                
    def try_mean(self, integer_list):

        try:
            mean = sum(integer_list) / len(integer_list)
        except:
            mean = None

        return mean

    def try_variance(self, integer_list, mean):

        try:
            variance = sum((mean - item) ** 2 for item in integer_list) / len(integer_list)
        except:
            variance = 0

        return variance ** 0.5
        
    def make_variance_dictionary(self, player_list):

        qb, rb, wr, te, k, defense = [], [], [], [], [], []

        for player in player_list:
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

        qb_mean = self.try_mean(qb)
        rb_mean = self.try_mean(rb)
        wr_mean = self.try_mean(wr)
        te_mean = self.try_mean(te)
        k_mean = self.try_mean(k)
        def_mean = self.try_mean(defense)

        qb_var = self.try_variance(qb, qb_mean)
        rb_var = self.try_variance(rb, rb_mean)
        wr_var = self.try_variance(wr, wr_mean)
        te_var = self.try_variance(te, te_mean)
        k_var = self.try_variance(k, k_mean)
        def_var = self.try_variance(defense, def_mean)

        variance_dict = {"QB": qb_var, "RB": rb_var, "WR": wr_var,
                         "TE": te_var, "K": k_var, "DEFENSE": def_var}

        return variance_dict
        
    def most_recommended_player_remaining(self):
            
        return self.get_list_recommended_players("5")[0][0]
        
    def get_list_recommended_players(self, limit):
        """
        returns a list of players ordered by weighted score,
        with the current variance of that position added to the weighted score
        """
        assert type(limit) == str

        possible_players = self.get_possible_players_tuples(limit)
       
        variance_dict = self.make_variance_dictionary(possible_players)
        recommended_players = []
       
        for player in possible_players:
            position = utils.defense_fixer(player[2]).rstrip('0123456789 ').upper()
            
            player_tuple = (player[0],
                            player[1] + variance_dict[position],
                            player[2])
                        
            recommended_players.append(player_tuple)
            
        recommended_players.sort(key=lambda t: t[1], reverse=True)
        
        return recommended_players[:int(limit)]
