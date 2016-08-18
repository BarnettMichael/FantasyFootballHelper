import psycopg2
import sys

from FFHelper import security


def connect_to_database():
    """
    Connects to a database specified using attributes the security.py file
    returns a tuple of a database connection and a cursor within the database.
    """

    connection = None
    
    try:
        connection = psycopg2.connect(database=security.database, user=security.username, password=security.password)
        cursor = connection.cursor()
            
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
        
    return connection, cursor
        

def add_column_to_table(table_name, column_name, datatype, connection, cursor):
    command = "ALTER TABLE %s ADD COLUMN %s %s" % (table_name, column_name, datatype)
    cursor.execute(command)
    try:
        connection.commit()
    except:
        connection.rollback()
        raise
            

def name_fixer(player):
    player = player.replace("'", "''")
    return player


def defense_fixer(position):
    if position.upper().startswith("DEFENSE"):
        position = "DEFENSE"
    return position
    

def get_player_from_table(player, table, cursor):
    """
    Selects entire row from table that matches player.
    Not sure need the \ escape characters
    """
    command = "SELECT * from %s where name = \'%s\'" % (defense_fixer(table), name_fixer(player))
    cursor.execute(command)
    try:
        playerdata = cursor.fetchall()[0]
        return playerdata
    except IndexError:
        return None
    

def remove_player_from_table(player, table_name, connection, cursor):
    assert (type(table_name) == type(player) == str)
    command = "delete from %s where name = \'%s\'" % (table_name, player)
    cursor.execute(command)
    try:
        connection.commit()
    except:
        connection.rollback()
        raise

# Functions used on Cloneplayer table specifically so as not to damage permanent database
# Planned to be removed and functionality done by instantiating player objects in client
# to reduce stress on database


def get_player_position(player, cursor):
    command = "select position from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    if data == []:
        position = None
    else:
        position = data[0][0]
    return position
    

def get_player_age(player, cursor):
    command = "select age from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    age = data[0][0]
    return age
    

def get_current_team(player, cursor):
    command = "select current_team from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    current_team = data[0][0]
    return current_team
    

def get_team_one_year_ago(player, cursor):
    command = "select team_one_year_ago from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    current_team = data[0][0]
    return current_team
    

def get_team_two_year_ago(player, cursor):
    command = "select team_two_year_ago from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    previous_team = data[0][0]
    return previous_team
    

def get_team_three_year_ago(player, cursor):
    command = "select team_three_year_ago from cloneplayers where name = \'%s\'" % name_fixer(player)
    cursor.execute(command)
    data = cursor.fetchall()
    previous_team = data[0][0]
    return previous_team
    

def get_player_points(player, cursor):
    command = "select points_one_year_ago, points_two_year_ago, points_three_year_ago from cloneplayers where name = \'%s\'" % name_fixer(player) 
    cursor.execute(command)
    player_points = list(cursor.fetchall()[0])
    while None in player_points:
        Noneindex = player_points.index(None)
        player_points[Noneindex] = 0
    return player_points
    

def get_player_weighted_score(player, cursor):
    pointslist = get_player_points(player, cursor)
    weighted_score = (pointslist[0] + pointslist[1] * 0.75 + pointslist[2] * 0.5) / 3
    return weighted_score
    

def get_positions_list(cursor):
    command = "select distinct position from cloneplayers"
    cursor.execute(command)
    data = cursor.fetchall()
    position_list = []
    full_positions_list = [position for tuple in data for position in tuple]
    for position in full_positions_list:
        positionindex = full_positions_list.index(position)
        if defense_fixer(position).rstrip('0123456789 ').upper() not in position_list:
            position_list.append(defense_fixer(position).rstrip('0123456789 ').upper())
        else:
            pass
        
    return position_list
    

def get_players_from_position(position, cursor):
    position = position.rstrip('0123456789 ').upper() + '%'
    command = "select name from cloneplayers where position like \'%s\'" % position
    cursor.execute(command)
    data = cursor.fetchall()
    playerslist = [player for tuple in data for player in tuple]
    return playerslist

###################################################################################################
    
def get_top_values(table, select_columns, order_by, limit, cursor):
        """
        Gets the top value(s) of the order_by column, up to limit.
        Pushes Null values to bottom of list.
        returns a list of tuples
        """
        command = "select %s from %s order by %s is null asc, %s desc limit %s" % (select_columns,
                                                                                   table, order_by,
                                                                                   order_by,
                                                                                   limit)
        cursor.execute(command)
        data = cursor.fetchall()
        return data
        
def update_column_data(table_name, column, data, filter_column, filter_value, connection, cursor):
    command = "UPDATE %s SET %s = %s WHERE %s = '%s'" % (table_name, column, data, filter_column, filter_value)
    cursor.execute(command)
    try:
        connection.commit()
    except:
        connection.rollback()
        raise
    
def update_weighted_scores(connection, cursor):
    for position in get_positions_list(cursor):
        playerlist = get_players_from_position(position, cursor)
        for player in playerlist:
            update_column_data("cloneplayers", "weighted_score", str(get_player_weighted_score(player, cursor)), "name", name_fixer(player), connection, cursor)
    
def create_temporary_table(table_name, column_values, connection, cursor):
    assert type(table_name) == type(column_values) == str
    command = "create temporary table %s(%s)" % (table_name, column_values)
    cursor.execute(command)
    try:
        connection.commit()
    except:
        connection.rollback()
        raise

def populate_temp_table_from_other_table(target_table, target_table_columns,
                                        other_table, filter_column,
                                        filter_value, connection, cursor):
    assert (type(target_table) == type(target_table_columns) ==
            type(other_table) == type(filter_column) ==
            type(filter_value) == str)
    command = ("insert into %s (select %s from %s where %s like \'%s\')" % 
                  (target_table, target_table_columns, other_table,
                   filter_column, filter_value))
    cursor.execute(command)
    
    try:
        connection.commit()
    except:
        connection.rollback()
        raise
     
def create_temp_clone_table(old_table, new_table, column_creators, columns, connection, cursor):
    
    create_temporary_table(new_table, column_creators, connection, cursor)
    populate_temp_table_from_other_table(new_table, columns, old_table,
                                         "'%'", "%", connection, cursor)
                                         
def remove_player_from_possible_players(player, connection, cursor):
        
        position = get_player_position(player, cursor).rstrip('0123456789 ').upper()
        command = "delete from %s where name like \'%s\'" % (defense_fixer(position), name_fixer(player))
        cursor.execute(command)
                    
        try:
            connection.commit()
        except:
            connection.rollback()
            raise
            
def clear_table(table, connection, cursor):
    command = "truncate table %s" % table
    cursor.execute(command)
    try:
        connection.commit()
    except:
        connection.rollback()
        raise