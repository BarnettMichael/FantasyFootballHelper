from Tkinter import *
import tkSimpleDialog
import tkMessageBox

import FantasyFootballHelper
import utils
import Opponent

class StartUpUI(Frame):
    """
    UI object for new draft window
    """
    
    def __init__(self, parent, draftgame):
        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()        
        self.__initUI()
        
    def __initUI(self):
        self.__draw_new_draft_window(self.parent)
        
    def __draw_new_draft_window(self, parent):

        self.parent.title("New Draft")

        style = StringVar()
        style.set("Snake")

        opponentlabel = Label(parent, text="Opponents")
        opponententry = Entry(parent, width=5)
        
        positionlabel = Label(parent, text="Draft Position")
        positionentry = Entry(parent, width=5)
        
        roundslabel = Label(parent, text="Number of Rounds")
        roundsentry = Entry(parent, width=5)
        
        stylelable = Label(parent, text="Draft Style")
        stylemenu = OptionMenu(parent, style, "Snake", "Linear")
        
        def begin_draft():
            """
            initializes variables to control the flow of the draft
            calls the first window of the draft.
            """
            self.game.numberofopponents = int(opponententry.get())
            self.game.draftposition = int(positionentry.get())
            self.game.numberofrounds = int(roundsentry.get())
            self.game.draftstyle = style.get()
            
            self.game.opponents = []
            self.game.currentposition = 1
            self.game.currentround = 1
            
            for x in xrange(self.game.numberofopponents):
                self.game.opponents.append(Opponent.Opponent(x))

            MainUI(self.parent, self.game)
            
        okbutton = Button(parent, text="OK", command=begin_draft)
        
        opponentlabel.grid(row=0)
        opponententry.grid(row=0, column=1)
        positionlabel.grid(row=1)
        positionentry.grid(row=1, column=1)
        roundslabel.grid(row=2)
        roundsentry.grid(row=2, column=1)
        stylelable.grid(row=3)
        stylemenu.grid(row=3, column=1)
        okbutton.grid(row=4, column=1, sticky=E)
        
class MainUI(Frame):
    """
    Main UI window for draft
    """
    
    def __init__(self, parent, draftgame):

        self.current_opponent_id = 0
        self.userpickmade = BooleanVar()
        self.userpickmade.set(False)

        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()        
        self.__MainUI()

        self.draft_logic()

    def draft_logic(self):

        if self.game.draftstyle == "Linear":
            self.LinearDraft()

        elif self.game.draftstyle == "Snake":
            self.SnakeDraft()

        FinalUI(self.parent, self.game)

    def LinearDraft(self):
        print "Linear Draft Started"
        while self.game.currentround <= self.game.numberofrounds:
            if self.game.draftposition != self.game.currentposition:
                self.opponent_pick_logic(self.current_opponent_id)
                self.current_opponent_id += 1
                self.increment_position()
            else:
                self.user_pick_logic()
                self.increment_position()

    def SnakeDraft(self):
        print "Snake Draft Started"
        while self.game.currentround <= self.game.numberofrounds:
            if self.game.currentround % 2 != 0:
                if self.game.draftposition != self.game.currentposition:
                    print "Opponent {0} Pick, odd round".format(self.current_opponent_id)
                    self.opponent_pick_logic(self.current_opponent_id)
                    self.current_opponent_id += 1
                    self.increment_position()
                else:
                    print "User Pick"
                    self.user_pick_logic()
                    self.increment_position()
            else:
                if self.game.draftposition != \
                                        self.game.numberofopponents \
                                        - self.game.currentposition + 2:
                    print "Opponent {0} Pick, Even round".format(
                        self.game.numberofopponents - self.current_opponent_id - 1
                    )
                    self.opponent_pick_logic(
                        self.game.numberofopponents - self.current_opponent_id - 1
                    )
                    self.current_opponent_id += 1
                    self.increment_position()
                else:
                    self.user_pick_logic()
                    self.increment_position()

    def increment_position(self):

        self.game.currentposition += 1

        if self.game.currentposition > self.game.numberofopponents + 1:
            self.game.currentround += 1
            self.game.currentposition = 1
            self.current_opponent_id = 0

    def user_pick_logic(self):

        self.userpickmade.set(False)

        while not self.userpickmade.get():
            self.wait_variable(name=self.userpickmade)
            self.__MainUI()

    def opponent_pick_logic(self, opponent_id):
        pickmade = False

        pick = tkSimpleDialog.askstring(
            "Opponent's pick",
            "Who did your opponent pick?\nCurrent Pick: Round {0}: Pick {1}" \
                .format(self.game.currentround, self.game.currentposition))

        while not pickmade:
            try:
                if utils.get_player_position(pick, self.game.cursor) != None:
                    position = utils.get_player_position(pick, self.game.cursor).rstrip('0123456789 ').upper()
                    if utils.get_player_from_table(pick, position, self.game.cursor) != None:
                        utils.remove_player_from_possible_players(pick, self.game.connection, self.game.cursor)
                        opponent = [opponent for opponent in self.game.opponents if opponent_id == opponent.id][0]
                        opponent.team.append(pick)
                        self.__MainUI()
                        pickmade = True
                    else:
                        pick = tkSimpleDialog.askstring(
                            "Opponent's pick",
                            "Not a valid pick, please select again\nCurrent Pick: Round {0}: Pick {1}" \
                                .format(self.game.currentround, self.game.currentposition))

                else:
                    pick = tkSimpleDialog.askstring(
                        "Opponent's pick",
                        "Not a valid pick, please select again\nCurrent Pick: Round {0}: Pick {1}" \
                            .format(self.game.currentround, self.game.currentposition))
            except AttributeError:
                tkMessageBox.showinfo("Error","Opponent must pick a valid player")
                pick = tkSimpleDialog.askstring(
                    "Opponent's pick",
                    "Not a valid pick, please select again\nCurrent Pick: Round {0}: Pick {1}" \
                        .format(self.game.currentround, self.game.currentposition))

    def __MainUI(self):
    
        self.parent.title("Fantasy Football Helper")
               
        for widget in self.parent.winfo_children():
            widget.destroy()
                
        #self.__draw_menu()
        self.__draw_round_label(self.parent)
        self.__draw_recommended_list(self.parent)
        self.__draw_valuable_list(self.parent)
        self.__draw_current_team(self.parent)
        self.__draw_team_requirements(self.parent)
        self.__draw_current_choice(self.parent)
        self.__draw_opponent_teams(self.parent)

    def __draw_round_label(self, parent):

        Label(parent, text="Round{0}: Pick{1}".format(self.game.currentround,
                                                      self.game.currentposition)). \
            grid(row=0)

        
    def __draw_current_choice(self, parent):
        
        choice = IntVar()
        otherplayer = StringVar()
        recommended = self.game.most_recommended_player_remaining()
        valuable = self.game.get_best_player_remaining()
        
        recommendedbutton = Radiobutton(parent, text=recommended, variable=choice, value=1)
        valuablebutton = Radiobutton(parent, text=valuable, variable=choice, value=2)
        otherbutton = Radiobutton(parent, text="", variable=choice, takefocus=0, value=3)
        othertext = Entry(parent, textvariable=otherplayer)
        
        def textfocus(event):
            otherbutton.select()
        
        othertext.bind("<Button-1>", textfocus)
        
        
        def pickplayer():

            decision = choice.get()

            if decision == 1:
                self.game.add_player_to_team(self.game.most_recommended_player_remaining())
                utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)

            elif decision == 2:
                self.game.add_player_to_team(self.game.get_best_player_remaining())
                utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)

            elif decision == 3:
                player = otherplayer.get()
                try:
                    self.game.add_player_to_team(player)
                    utils.remove_player_from_possible_players(player, self.game.connection, self.game.cursor)
                except:
                    tkMessageBox.showinfo("Error", "Can't add that player to team, try again.")
                    self.user_pick_logic()


            #self.game.clear_finished_tables()
            self.userpickmade.set(True)



        Label(parent, text="Recommended Player").grid(sticky=W, row=1)
        recommendedbutton.grid(sticky=W, row=1, column=1, columnspan=2)
        
        Label(parent, text="Most Valuable Player").grid(sticky=W, row=2)
        valuablebutton.grid(sticky=W, row=2, column=1, columnspan=2)
        
        Label(parent, text="Choose other Player").grid(sticky=W, row=3)
        otherbutton.grid(sticky=W, row=3, column=1)
        othertext.grid(row=3, column=2, sticky=W)
        
        pickbutton = Button(parent, text="Pick", command=pickplayer).grid(
            row=4, columnspan=3, sticky=NE)
        
    def __draw_recommended_list(self, parent):
        
        recommendedlist = self.game.get_list_recommended_players("10")
        recommendedlistbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Recommended Players").grid(row=1, column=3)
        recommendedlistbox.grid(row=2, column=3, rowspan=4, sticky=N)
        for player in recommendedlist:
            index = str(recommendedlist.index(player) + 1)
            recommendedlistbox.insert(END, index + ":"
                                           + player[0] + " "
                                           + player[2] + " " 
                                           + format(player[1], '.2f') + "\n"
                                   )
           
        recommendedlistbox.config(state=DISABLED)
        
    def __draw_valuable_list(self, parent):
        
        valuablelist = self.game.get_list_of_best_players("10")
        valuablelistbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Most Valuable Players").grid(row=1, column=4)
        valuablelistbox.grid(row=2, column=4, rowspan=4, sticky=N)
        for player in valuablelist:
            index = str(valuablelist.index(player) + 1)
            valuablelistbox.insert(END, index + ":" 
                                        + player[0] + " "
                                        + player[2] + " " 
                                        + format(player[1], '.2f') + "\n"
                                   )
                
        valuablelistbox.config(state=DISABLED)
            
    def __draw_team_requirements(self, parent):
        
        requirements = self.game.check_current_team_needs()
        requirementlist = []
        
        for key in requirements.keys():
            keystring = "%d%s" % (requirements[key], key)
            requirementlist.append(keystring)
        
        Label(parent, text = "Still Need: " + ", ".join(requirementlist)).grid(
            row = 5, columnspan = 3, sticky=W)
            
    def __draw_current_team(self, parent):
        
        currentteam = self.game.current_team
        teamlist = []
        
        for key in currentteam.keys():
            playerstring = "%s %s" % (key, currentteam[key])
            teamlist.append(playerstring)
        
        currentteamstring = (", ".join(teamlist[0:len(teamlist) / 2 + 1])
                             + "\n" + ", ".join(teamlist[len(teamlist) / 2 + 1:]))
        
        Label(parent, text = "Current Team: ").grid(
            row=6)
        Label(parent, text = currentteamstring).grid(
            row=6, column=1, columnspan=4)

    def __draw_opponent_teams(self, parent):

        opponents = self.game.opponents

        for opponent in opponents:
            Label(parent, text = "Opponent{0}'s Team: ".format(opponent.id + 1)).grid(
                row = 7 + opponent.id)
            Label(parent, text = str(opponent.team)).grid(
                row=7 + opponent.id,
                column=1, columnspan=4)

class FinalUI(Frame):
    """
    After draft results Screen
    """

    def __init__(self, parent, draftgame):
        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()
        self.__FinalUI()

    def __FinalUI(self):
        self.parent.title("Results")

        for widget in self.parent.winfo_children():
            widget.destroy()

        # self.__draw_menu()
        self.__draw_final_team(self.parent)
        self.__draw_opponent_teams(self.parent)

    def __draw_final_team(self, parent):
        finalteam = self.game.current_team
        teamlist = []

        for key in finalteam.keys():
            playerstring = "{0} {1}".format(key, finalteam[key])
            teamlist.append(playerstring)

        finalteamstring = (", ".join(teamlist[0:len(teamlist) / 2 + 1])
                             + "\n" + ", ".join(teamlist[len(teamlist) / 2 + 1:]))

        Label(parent, text="Final Team: ").grid(
            row=1)
        Label(parent, text=finalteamstring).grid(
            row=1, column=1, columnspan=4)

    def __draw_opponent_teams(self, parent):

        opponents = self.game.opponents

        for opponent in opponents:
            Label(parent, text = "Opponent{0}'s Team: ".format(opponent.id + 1)).grid(
                row = 2 + opponent.id)
            Label(parent, text = str(opponent.team)).grid(
                row=2 + opponent.id,
                column=1, columnspan=4)

        
ffhelper = FantasyFootballHelper.draftgame()       
        
root = Tk()
StartUpUI(root, ffhelper)
root.mainloop()